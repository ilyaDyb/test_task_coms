from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import MessagesFromEmail
from main.utils.read_messages import list_mailboxes


def index(request):
    return render(request, "index.html")


@login_required
def messages(request):
    resource = request.GET.get("resource")
    allow = None
    if not resource:
        allow = False
    if resource == "mail" or resource == "gmail":
        allow = True

    messages = MessagesFromEmail.objects.all().order_by("-id")
    
    context = {
        "messages": messages,
        "allow": allow,
        "resource": resource,
    }
    print(allow, resource)
    return render(request, "messages.html", context=context)