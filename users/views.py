from django.contrib import auth
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import PrivateOfficeForm, UserLoginForm

def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = auth.authenticate(request, username=username, password=password)

            if user is None:
                form.add_error(None, "Invalid login or password")
            else:
                auth.login(request, user)
                return redirect(reverse("main:index"))
    else:
        form = UserLoginForm()
    return render(request, "login.html", context={"form": form})



@login_required
def private_office_view(request):
    private_office = request.user.user_office
    
    if request.method == 'POST':
        form = PrivateOfficeForm(request.POST, instance=private_office)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:private_office'))
    else:
        form = PrivateOfficeForm(instance=private_office)
    
    return render(request, 'private_office.html', {'form': form})