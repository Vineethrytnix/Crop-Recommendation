from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import datetime as dt
from django.db import transaction
from .new_predict import predict_crop

# Create your views here.


def index(request):
    return render(request, "index.html")

@transaction.atomic
def User_reg(request):
    current_date = datetime.today().strftime("%Y-%m-%d")
    print(current_date)
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        address = request.POST["address"]
        image = request.FILES["image"]
        
        try:
            if Login.objects.filter(username=email).exists():
                messages.error(request, "Email is Already Exists")
                return redirect("/login")
            else:
                logUser = Login.objects.create_user(
                    username=email,
                    password=password,
                    userType="User",
                    viewPass=password,
                    is_active=0,
                )
                logUser.save()
                
                if image:

                    userReg = UserRegistration.objects.create(
                        name=name,
                        email=email,
                        phone=phone,
                        address=address,
                        loginid=logUser,
                        image=image,
                    )
                    userReg.save()
                else:
                    userReg = UserRegistration.objects.create(
                        name=name,
                        email=email,
                        phone=phone,
                        address=address,
                        loginid=logUser,
                    )
                    userReg.save()
        except Exception as e:
            transaction.set_rollback(True)
            return HttpResponse(f"<script>alert('{str(e)}');window.location='/user_reg'</script>")
            
    return render(request, "User_reg.html")


def log(request):
    if request.POST:
        email = request.POST["email"]
        passw = request.POST["password"]
        user = authenticate(username=email, password=passw)
        print(user)

        if user is not None:
            login(request, user)
            if user.userType == "Admin":
                return HttpResponse(
                    "<script>alert('Successfully logged in');window.location='/admin_home'</script>"
                )
            elif user.userType == "User":
                id = user.id
                email = user.username
                request.session["uid"] = id
                request.session["email"] = email

                return HttpResponse(
                    "<script>alert('Successfully logged in');window.location='/user_home'</script>"
                )
        else:
            print("Hiii")
            messages.error(request, "Invalid Username/Password")
    return render(request, "login.html")


def udp(request):
    up=Login.objects.filter(id=4).update(userType="User")
    return HttpResponse("deleted")

def admin_home(request):
    return render(request, "Admin/index.html")

def user_home(request):
    result=""
    alert_msg = "" 
    if request.POST:
        rain=request.POST.get('rain')
        area=request.POST.get('area')
        season=request.POST.get('season')
        state=request.POST.get('state')
        
        print("Prediction Datas : ",rain, area, season, state)
        
        result=predict_crop(area,season,state,rain)
        
        if result :
            alert_msg = f"Recommended Crop: {result}"
        
    return render(request, "User/index.html", {"result":result,"alert_msg": alert_msg})

def view_users(request):
    view=UserRegistration.objects.all()
        
    return render(request, "Admin/view_users.html",{"view":view})


def update_user_status(request):
    uid=request.GET.get('email')
    status=request.GET.get('status')
    
    if status=="success":
        up=Login.objects.filter(username=uid).update(is_active=1)
        return HttpResponse("<script>alert('User Approved');window.location='/view_users'</script>")
    else:
        up=Login.objects.filter(username=uid).delete()
        return HttpResponse("<script>alert('User Rejected');window.location='/view_users'</script>")
    
    
    
def add_feedback(request):
    uid=request.session['uid']
    Uid=UserRegistration.objects.get(loginid=uid)
    
    if request.method == 'POST':
        sub=request.POST.get('sub')
        feed=request.POST.get('feedback')
        
        ins=Feedback.objects.create(uid=Uid,feedback=feed,subject=sub)
        ins.save()
        return HttpResponse("<script>alert('Feedback Added');window.location='/add_feedback'</script>")
        
        
    return render(request,'User/add_feedback.html')

def view_feedback(request):
    view=Feedback.objects.all()
    return render(request,'Admin/view_feedback.html',{"view":view})