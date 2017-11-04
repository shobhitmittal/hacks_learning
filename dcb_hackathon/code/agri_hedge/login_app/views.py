from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin

# Create your views here.

def login_page(request):
    #add.delay(2,2)
    c = {}
    return render(request, 'login.html', c)

#@xframe_options_sameorigin
def login_user(request):
    if request.method=='POST':
        #print request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.lower(), password=password)
        data={}
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                redirect_path = request.POST.get('next')
                print redirect_path
                if redirect_path:
                    pass
                else:
                    redirect_path='/'
                return redirect(redirect_path)
                print("User is valid, active and authenticated")
            else:
                data['message']="The password is valid, but the account has been disabled!"
                return render(request,'message.html',data)
        else:
            # the authentication system was unable to verify the username and password
            data['message']="Username does not exist, Please use Username to login"
            return render(request,'message.html',data)

def logout_user(request):
    logout(request)
    print "User has been logged out."
    return redirect('/login_mod/login')



