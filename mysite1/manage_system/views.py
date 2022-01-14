from django.db.models.fields import EmailField
from django.core.paginator import Paginator
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render,redirect
from django.contrib import auth
from manage_system.models import customer,storage,sys_users,product
import re
import django.db.utils
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordChangeView, PasswordChangeDoneView,PasswordResetCompleteView
import random
import string
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def login(request):
    '''if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')        
        return render(request,'index.html')
    return render(request, 'manage_system/login.html')'''
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user_obj=auth.authenticate(username=username,password=password)
        if user_obj:
            #uu=request.user
            auth.login(request, user_obj)#注册cookie
            context={'loginuser':user_obj}
            return render(request, 'manage_system/index.html',context)
            #return render(request, 'manage_system/login.html')  
    return render(request,'manage_system/login.html')      
    '''try:
        user = models.User.objects.get(name=username)
        if user.password == password:
            return redirect('/index/')
        else:
            message = "password is wrong"
    except:
        message = "user name does not exist"'''
def index(request):
    return HttpResponse("hello,this is index page")
def register(request):
    if request== 'GET':
        return render(request,'manage_system/register.html')
    if request.method== "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        u_type=request.POST.get('user_type')
        additional=request.POST.get('information')
        if not all([username, password, password2,u_type]):
            return HttpResponseBadRequest('please fill in all blanks')
        # 判断密码是否是?8-20个数字?
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseBadRequest('password length is wrong')
        # 判断两次密码是否一致?
        if password != password2:
            return HttpResponseBadRequest('different passwords are input')
        try:
            if u_type=="普通用户":
                u_type=1
                user=sys_users.objects.create_user(username=username,email=email, password=password,user_authority=u_type,user_infor=additional)
                user.is_superuser=0
            else :
                u_type=2
                user=sys_users.objects.create_user(username=username,email=email, password=password,user_authority=u_type,user_infor=additional)  
                user.is_superuser=1              
        except Exception as err:
            print(err)
            return HttpResponseBadRequest('register failed') 
        context={'loginuser':user}
        return render(request,'manage_system/index.html',context)     
    return render(request,'manage_system/register.html')    
    #return HttpResponse("this is register page")

def customer_show(request,pIndex=1):
    #return HttpResponse("客户信息")
    datas=customer.objects.all()

    mywhere=[]
    #获取并判断搜索条件?
    kw=request.GET.get("keyword",None)
    if kw:
        datas = datas.filter(Q(customer_id__contains=kw)|Q(customer_name__contains=kw))       
        mywhere.append('keyword='+kw)

    pIndex=int(pIndex)
    page = Paginator(datas,5)
    maxpages = page.num_pages

    if pIndex>maxpages :#分页查询
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex) #获取当前页数
    plist=page.page_range   #获取页码列表
    context={'list':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'manage_system/customer_index.html',context)
def customer_add(request):
    return render(request,"manage_system/customer_add.html")
def customer_insert(request):
    try:
        ob=customer()
        ob.customer_id=request.POST['ID']
        ob.customer_name=request.POST['name']
        ob.customer_type=request.POST['type']
        ob.contactor=request.POST['contactor']
        ob.tele=request.POST['tele']
        ob.address=request.POST['address']  
        ob.notes=request.POST['notes']  
        ob.save() 
        context={'info':"添加成功"} 
    except Exception as err:
        print(err)
        context={'info':"添加失败"}
    return render(request,"manage_system/info.html",context)
def customer_edit(request,uid):
    if request.user.user_authority==1 :
        context={'info':"非管理员，无权限修改"}
        return render(request,'manage_system/info.html',context)
    try:
        ob=customer.objects.get(customer_id=uid)
        context={'user':ob}
        return render(request,"manage_system/customer_edit.html",context)
    except Exception as err:
        print(err)
        context={'info':"没有要修改的信息"}
        return render(request,"manage_system/info.html",context)
def customer_update(request,uid):
    try:
        ob=customer.objects.get(customer_id=uid)
        if(request.POST['type']!=""):
            ob.customer_type=request.POST['type']
        if(request.POST['contactor']!=""):
            ob.contactor=request.POST['contactor']
        if(request.POST['tele']!=""):
            ob.tele=request.POST['tele']
        if(request.POST['address']!=""):
            ob.address=request.POST['address']
        if(request.POST['notes']!=""):
            ob.notes=request.POST['notes']
        ob.save()
        context={'info':"修改成功"}
    except Exception as err:
        print(err)
        context={'info':"修改失败"}
    return render(request,'manage_system/info.html',context)
def customer_delete(request,uid):
    if(request.user.user_authority==1):
        context={'info':"非管理员,无权限删除"}
        return render(request,'manage_system/info.html',context)
    try:
        ob=customer.objects.get(customer_id=uid)
        ob.delete()
        context={'info':"删除成功"}
    except:
        context={'info':"删除失败"}
    return render(request,'manage_system/info.html',context)

def storage_show(request,pIndex=1):
    datas=storage.objects.all()
    mywhere=[]
    kw=request.GET.get('keyword',None)
    if(kw):
        datas=datas.filter(Q(storage_id__contains=kw)|Q(storage_name__contains=kw))
        mywhere.append('keyword='+kw)
    pIndex=int(pIndex)
    page=Paginator(datas,5)
    maxpages=page.num_pages
    if pIndex>maxpages :
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)
    plist=page.page_range
    context={'list':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'manage_system/storage_index.html',context)
def storage_edit(request,sid):
    if request.user.user_authority==1 :
        context={'info':"非管理员，无权限修改"}
        return render(request,'manage_system/info.html',context)
    try:
        ob=storage.objects.get(storage_id=sid)
        context={'storage':ob,'storage_id':ob.storage_id}
        return render(request,"manage_system/storage_edit.html",context)
    except Exception as err:
        print(err)
        context={'info':"错误！"}
        return render(request,'manage_system/info.html',context)
def storage_update(request,sid):
    try:
        ob=storage.objects.get(storage_id=sid)
        if(request.POST['snotes']!=""):
            ob.storage_info=request.POST['snotes']
        ob.save()
        context={'info':"修改成功"}
    except Exception as err:
        print(err)
        context={'info':"修改失败"}
    return render(request,'manage_system/info.html',context)
def storage_delete(request,sid):
    if request.user.user_authority==1 :
        context={'info':"非管理员，无权限删除"}
        return render(request,'manage_system/info.html',context)
    try:
        ob=storage.objects.get(storage_id=sid)
        ob.delete()
        context={'info':"删除成功"}
    except Exception as err:
        print(err)
        context={'info':"删除失败"}
    return render(request,'manage_system/info.html',context)
def storage_add(request):
    return render(request,'manage_system/storage_add.html')
def storage_insert(request):
    try:
        ob=storage()
        ob.storage_id=request.POST['ID']
        ob.storage_name=request.POST['name']
        ob.storage_info=request.POST['infor'] 
        ob.save() 
        context={'info':"添加成功"} 
    except Exception as err:
        print(err)
        context={'info':"添加失败"}
    return render(request,"manage_system/info.html",context)  

def user_manage(request,pIndex=1):
    user=request.user
    if user.user_authority==2:
        mywhere=[]
        datas=sys_users.objects.all()
        pIndex=int(pIndex)
        page=Paginator(datas,5)
        maxpages=page.num_pages
        if pIndex>maxpages :
            pIndex=maxpages
        if pIndex<1:
            pIndex=1
        list2=page.page(pIndex)
        plist=page.page_range
        context={'list':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
        return render(request,'manage_system/user_manage.html',context)
    else:
        context={'info':"非管理员无权限访问"}
        return render(request,'manage_system/info.html',context)
def user_edit(request,uid):
    try:
        ob=sys_users.objects.get(id = uid)
        context={'user':ob}
        return render(request,'manage_system/user_edit.html',context)
    except Exception as err :
        print(err)
        context={'info':"错误！"}
        return render(request,"manage_system/info.html",context)
def user_update(request,uid):
    try:
        ob=sys_users.objects.get(id=uid)
        if request.POST['user_type'] == "普通用户" :
            ob.user_authority = 1
        else :
            ob.user_authority = 2
        ob.save()
        context={'info':"修改成功"}
    except Exception as err:
        print(err)
        context={'info':"修改失败"}
    return render(request,'manage_system/info.html',context)
def user_delete(request,uid):
    if request.user.id == uid :
        context={'info':"不能删除正在登录的用户，请重新选择"}
        return render(request,'manage_system/info.html',context)
    try:
        ob=sys_users.objects.get(id=uid)
        ob.delete()
        context={'info':"删除成功"}
    except:
        context={'info':"删除失败"}
    return render(request,'manage_system/info.html',context)   
def user_add(request):
    return render(request,'manage_system/user_add.html')
def user_insert(request,pIndex=1):
    try:
        ob=sys_users()
        ob.username=request.POST['name']
        ob.password=request.POST['password']
        ob.email=request.POST['email']
        if(request.POST['type'] == '普通用户'):
            ob.user_authority = 1
        else :
            ob.user_authority = 2

        ob.user_infor=request.POST['notes']
        ob.save()
        datas=sys_users.objects.all()
        mywhere=[]
        pIndex=int(pIndex)
        page=Paginator(datas,5)
        maxpages=page.num_pages
        if pIndex>maxpages :
            pIndex=maxpages
        if pIndex<1:
            pIndex=1
        list2=page.page(pIndex)
        plist=page.page_range
        context={'list':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
        return render(request,'manage_system/user_manage.html',context)
    except Exception as err:
        print(err)
        context={"info":"添加失败"}
        return render(request,'manage_system/info.html',context)

def product_show(request,pIndex = 1):
    datas=product.objects.all()
    mywhere=[]
    #获取并判断搜索条件
    kw=request.GET.get("keyword",None)
    if kw:
        datas = datas.filter(Q(product_id__contains=kw)|Q(product_name__contains=kw)|Q(product_storage__storage_id__contains=kw))       
        mywhere.append('keyword='+kw)

    pIndex=int(pIndex)
    page = Paginator(datas,5)
    maxpages = page.num_pages

    if pIndex>maxpages :#分页查询
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex) #获取当前页数
    plist=page.page_range   #获取页码列表
    context={'list':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'manage_system/product_index.html',context)
def product_add(request):
    storages=storage.objects.all()
    context={'storage':storages}
    return render(request,'manage_system/product_add.html',context)
def product_insert(request):
    try:
        ob=product() 
        ob.product_id=request.POST['ID']
        ob.product_name=request.POST['name']
        ob.product_size=request.POST['size']
        ob.product_value=request.POST['values']
        ob.product_leastcount=request.POST['leastcount']
        ob.product_maxcount=request.POST['maxcount']  
        str=request.POST['storageid']
        ob.product_storage=storage.objects.get(storage_id=str.split(" ")[0])
        ob.save() 
        context={'info':"添加成功"} 
    except Exception as err:
        print(err)
        context={'info':"添加失败"}
    return render(request,"manage_system/info.html",context)       
def product_edit(request,pid):
    if request.user.user_authority == 1:
        context={'info':"非管理员，无权限修改"}
        return render(request,'manage_system/info.html',context)
    try:
        ob=product.objects.get(product_id = pid)
        warehouse=storage.objects.all()
        context={'product':ob,'storage':warehouse}
        return render(request,'manage_system/product_edit.html',context)
    except Exception as err :
        print(err)
        context={'info':"跳转失败"}
        return render(request,"manage_system/info.html",context)
def product_update(request,pid):
    try:
        ob=product.objects.get(product_id=pid)
        if(request.POST['values']!=""):
            ob.product_value=request.POST['values']
        if(request.POST['lnum']!=""):
            ob.product_leastcount=request.POST['lnum']
        if(request.POST['mnum']!=""):
            ob.product_maxcount=request.POST['mnum']
        str=request.POST['storage']
        ob.product_storage=storage.objects.get(storage_id=str.split(" ")[0])
        ob.save()
        context={'info':"修改成功"}
    except Exception as err :
        print(err)
        context={'info':"修改失败"}
    return render(request,'manage_system/info.html',context)
def product_delete(request,pid):
    if (request.user.user_authority == 1) :
        context={'info':"非管理员无权限删除"}
        return render(request,'manage_system/info.html',context)
    try:        
        ob=product.objects.get(product_id = pid)
        ob.delete()
        context={'info':"删除成功"}
    except Exception as err :
        context={'info':"删除失败"}
    return render(request,'manage_system/info.html',context)

def forget_pwd(request):
    return render(request,'manage_system/forget_pwd.html')
def resetpassword(request):
    user=sys_users.objects.get(username=request.POST.get('username'))
    if(request.POST.get('password') != request.POST.get('password2')):
        context={'info':"两次密码输入不一致！"}
        return render(request,'manage_system/info.html',context)
    password=request.POST.get('password')
    password=str(password)
    #if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
     #   return HttpResponseBadRequest('密码长度8~20且包含字母和数字！')
    user.password=password
    print(user.password)
    context={'msg':"密码修改成功，请重新登录"}
    return render(request,'manage_system/login.html',context)

def forget_password(request):
    if request.method == "GET":
        return render(request, "manage_system/forget_pwd.html")
    else:
        username = request.POST.get("username")
        count = sys_users.objects.filter(username=username).count()
        if count == 1:
            email = sys_users.objects.get(username=username).email
            email_part = email[3:]

            # generate password,length = 8, letters and digits
            random_password = ''.join(random.sample(string.ascii_letters + string.digits, 8))

            # update password, hash password
            password = make_password(random_password)
            User.objects.filter(username=username).update(password=password)

            # send email
            subject = "Password reset notification"
            message = "Your username " + username + " 's password is changed into " + random_password
            sender = settings.EMAIL_HOST_USER
            recipient = [email]
            send_mail(
                subject,
                message,
                sender,
                recipient
            )
            return render(request, "manage_system/forget_pwd.html", {"forget_password_tips": "Password is sent to *****" + email_part + " , please check your inbox or junk box."})
        else:
            return render(request, "manage_system/forget_pwd.html", {"forget_password_tips": username + " is not exsit!"})