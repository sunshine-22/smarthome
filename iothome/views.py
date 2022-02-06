from django.shortcuts import render,redirect
from . models import Registration
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from . tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.urls import reverse
from Adafruit_IO import *
aio=Client("sabarish_22_","aio_qnGk10XjBjYWBvwxqVxqbTQhmnbV")
#from django.contrib.auth.models import User
def dashboard(request):
    if(request.method=="POST") and "on" in request.POST:
        aio.send_data("green",1)
        msg="on"
        return render(request,"iothome/dashboard.html",{"msg":msg})
    if(request.method=="POST") and "off" in request.POST:
        aio.send_data("green",0)
        aio.send_data("blue",0)
        aio.send_data("white",0)
        aio.send_data("brown",0)
        aio.send_data("yellow",0)
        aio.send_data("red",0)
        aio.send_data("pink",0)
        msg="off"
        return render(request,"iothome/dashboard.html",{"msg":msg})
    if(request.method=="POST") and "blue" in request.POST:
        aio.send_data("blue",1)
        aio.send_data("green",0)
        aio.send_data("white",0)
        aio.send_data("brown",0)
        aio.send_data("yellow",0)
        aio.send_data("red",0)
        aio.send_data("pink",0)
        msg="blue"
        return render(request,"iothome/dashboard.html",{"msg":msg})
    if(request.method=="POST") and "white" in request.POST:
        aio.send_data("white",1)
        aio.send_data("green",0)
        aio.send_data("blue",0)
        aio.send_data("brown",0)
        aio.send_data("yellow",0)
        aio.send_data("red",0)
        aio.send_data("pink",0)
        msg="lightgreen"
        return render(request,"iothome/dashboard.html",{"msg":msg})
    if(request.method=="POST") and "brown" in request.POST:
        aio.send_data("brown",1)
        aio.send_data("green",0)
        aio.send_data("blue",0)
        aio.send_data("white",0)
        aio.send_data("yellow",0)
        aio.send_data("red",0)
        aio.send_data("pink",0)
        msg="aqua"
        return render(request,"iothome/dashboard.html",{"msg":msg})
    if(request.method=="POST") and "yellow" in request.POST:
        aio.send_data("yellow",1)
        aio.send_data("green",0)
        aio.send_data("blue",0)
        aio.send_data("white",0)
        aio.send_data("brown",0)
        aio.send_data("red",0)
        aio.send_data("pink",0)
        msg="yellow"
        return render(request,"iothome/dashboard.html",{"msg":msg})
    if(request.method=="POST") and "red" in request.POST:
        aio.send_data("red",1)
        aio.send_data("green",0)
        aio.send_data("blue",0)
        aio.send_data("white",0)
        aio.send_data("brown",0)
        aio.send_data("yellow",0)
        aio.send_data("pink",0)
        msg="red"
        return render(request,"iothome/dashboard.html",{"msg":msg})
    if(request.method=="POST") and "pink" in request.POST:
        aio.send_data("pink",1)
        aio.send_data("green",0)
        aio.send_data("blue",0)
        aio.send_data("white",0)
        aio.send_data("brown",0)
        aio.send_data("yellow",0)
        aio.send_data("pink",0)
        msg="pink"
        return render(request,"iothome/dashboard.html",{"msg":msg})
    return render(request,"iothome/dashboard.html")
def home(request):
    uname=request.session.get("uname","")
    paswd=request.session.get("paswd","")
    if(request.method=="POST"):
        try:
            username=request.POST.get("email")
            pswd=request.POST.get("password")
            request.session["uname"]=username
            request.session["paswd"]=pswd
            checker=Registration.objects.get(email=username)
            if(checker.is_active==True):
                if(checker.password==pswd):
                    return redirect("dashboard/")
                else:
                    msg="password not valid"
                    return render(request,"iothome/home.html",{"msg":msg})
            else:
                    msg="Account not activated"
                    return render(request,"iothome/home.html",{"msg":msg})
        except:
            msg="User Not Found"
            return render(request,"iothome/home.html",{"msg":msg})
             
            
    return render(request,"iothome/home.html",{"user":uname,"pswd":paswd})
def signup(request):
    if(request.method=="POST"):
        data1=request.POST.get("username")
        data2=request.POST.get("name")
        data3=request.POST.get("email")
        data4=request.POST.get("password")
        print(data1,data2,data3,data4)
        user=Registration(username=data1,name=data2,email=data3,password=data4)
        user.is_active=False
        user.save()
        uidb64=urlsafe_base64_encode(force_bytes(user.pk))
        currentsite=get_current_site(request).domain
        print(currentsite)
        link=reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(user)})
        activate_url="http://"+currentsite+link
        message="hi"+data1+"please use this link to verify\n"+activate_url
        mail_subject="Account Activation"
        email=EmailMessage(mail_subject,message,to=[data3])
        email.send()
        cnfrm="Email Has been Send to {}".format(data3)
        return render(request,"iothome/signup.html",{"msg":cnfrm})
                                                            
        
    return render(request,"iothome/signup.html")


def activate(request,uidb64,token):
    #User=get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        print("uid sucess",uid)
        user=Registration.objects.get(pk=uid)
        print(user)
    except(TypeError,ValueError,OverflowError,user.DoesNotExist):
        user=None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        msg="Verification Success"
        return render(request,"iothome/home.html",{"msg":msg})
    else:
        msg="Verification failed"
        return render(request,"iothome/home.html",{"msg":msg})
    #return redirect("/")
