from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . forms import SignUpForm, SignInForm
from . models import Profile

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()

            # log user in
            login(request, user)

            # create user profile
            new_profile = Profile(user=user)
            new_profile.save()
            return redirect('/')

    else:
        form = SignUpForm()
    
    context = {'form': form}
        
    return render(request, 'authentication/signup.html', context)

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            Usermail = form.cleaned_data['Usermail']
            password = form.cleaned_data['Password']

            user = authenticate(username=Usermail, password=password)
            try:
                user_ = User.objects.get(email=Usermail)
            except:
                user_ = False
            if user is not None:
                login(request, user)              
                """redirect to homepage"""
                messages.success(request, 'Login Successful')
                return redirect('/')
            elif user_:
                if user_ != False:
                    if user_.check_password(password):
                        login(request, user_)
                        """redirect to homepage"""
                        messages.success(request, 'Login Successful')
                        return redirect('/')
            else:
                """flash message"""
                messages.error(request, 'Incorrect email or password')
                
    else:
        form = SignInForm()
    
    context = {'form': form}
    return render(request, 'authentication/signin.html', context)

@login_required(login_url='signin/')
def log_out(request):
    logout(request)
    return redirect(reverse(sign_in))


