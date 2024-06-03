from django.shortcuts import render

# Create your views here.

from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

def registeration(request):
    ufo=Userform()
    pfo=Profileform()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=Userform(request.POST)
        pfd=Profileform(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            MUFDO=ufd.save(commit=False)  # It is not directly saved. If we have some operations and done after we can save down
            pw=ufd.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save() # these will save.

            MPFDO=pfd.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            send_mail('Registeration Process',
                      'Thank You Registration is Successfull!!!',
                      'vamsifun4@gmail.com',
                      [MUFDO.email],
                      fail_silently=False)


            return HttpResponse('Registration Succesfull')
        else:
            return HttpResponse('Invalid Data')
    return render(request,'registeration.html',d)


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Crenditals')

    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile_display(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)


@login_required
def change_password(request):
    # if request.method=='POST':
    #     pw=request.POST['pw']
    #     username=request.session.get('username')
    #     UO=User.objects.get(username = username)
    #     UO.set_password(pw)
    #     UO.save()
    if request.method=='POST':
        fm=PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            return HttpResponseRedirect(reverse('home'))
    else:
        fm=PasswordChangeForm(user=request.user)
    return render(request,'change_password.html',{'fm':fm})




def forgot_password(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponseRedirect(reverse('user_login'))
        else:
            return HttpResponse('Your name not matched in our database. So, Retype correctlyyy!!!!!')
    return render(request,'forgot_password.html')




















        







