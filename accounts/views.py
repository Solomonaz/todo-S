from django.shortcuts import render, redirect
from accounts.models import Account
from .forms import RegistrationForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
 

# Create your views here.
def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # email verification
            current_site = get_current_site(request)
            
            messages.success(request,"sucessfuly registered!")
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)

            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials!")
            return redirect('login')

    return render(request, 'accounts/login.html')
@login_required(login_url='login')
def logout(request):
    messages.success(request, 'you are logged out!')
    auth.logout(request)
    return redirect('login')