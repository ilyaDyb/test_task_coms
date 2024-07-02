import email
import sys
import imaplib
import os

from email.header import decode_header

from dotenv import load_dotenv

from main.utils import functions

load_dotenv()

#help func
def list_mailboxes():
    username = "ilyachannel1.0@gmail.com"
    password = os.environ.get("IMAP_PASSWORD_GMAIL")
    if "gmail.com" in username:
        imap_server = "imap.gmail.com"
    elif "mail.ru" in username:
        imap_server = "imap.mail.ru"
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)
    status, mailboxes = imap.list()
    if status == "OK":
        for mailbox in mailboxes:
            print(mailbox.decode("utf-8"))
    imap.logout()

async def start_reading(mail_pass, username):
    ENCODING = "utf-8"
    try:
        imap = functions.connection(mail_pass=mail_pass, username=username)
        if not imap:
            sys.exit()

        imap.select("INBOX") #/Newsletters")
        res, unseen_msg = imap.uid("search", "UNSEEN", "ALL")

        if not unseen_msg or unseen_msg[0].decode(ENCODING) == '':
            raise ValueError("Empty")
        
        unseen_msg = unseen_msg[0].decode(ENCODING).split(" ")
        if unseen_msg[0]:
            for letter in unseen_msg:
                try:
                    attachments = []
                    res, msg = imap.uid("fetch", letter, "(RFC822)")
                    if res == "OK":
                        msg = email.message_from_bytes(msg[0][1])
                        msg_date = functions.date_parse(email.utils.parsedate_tz(msg["Date"]))
                        msg_from = functions.from_subj_decode(msg["From"])
                        msg_subj = functions.from_subj_decode(msg["Subject"])
                        if msg["Return-path"]:
                            msg_email = msg["Return-path"].lstrip("<").rstrip(">")
                        else:
                            msg_email = msg_from

                        if not msg_email:
                            try:
                                encoding = decode_header(msg["From"])[0][1]
                                msg_email = (
                                    decode_header(msg["From"])[1][0]
                                    .decode(encoding)
                                    .replace("<", "")
                                    .replace(">", "")
                                    .replace(" ", "")
                                )
                            except Exception:
                                msg_email = "unknown"

                        letter_text = functions.get_letter_text(msg)
                        attachments = functions.get_attachments(msg)

                        msg_json_data = functions.post_construct(
                            msg_subj, msg_from, msg_email, letter_text, attachments, msg_date
                        )
                        yield msg_json_data
                except Exception:
                    continue
            imap.logout()
        else:
            imap.logout()
            sys.exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        yield "Emprty box"
        
