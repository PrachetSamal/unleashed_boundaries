from datetime import date
from django.db.models import Sum
from django.shortcuts import render, redirect
from myapp.models import *
from django.contrib import messages


import requests

# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    uid = request.session["loginid"]
    name = request.POST.get("name")
    subject = request.POST.get("subject")
    message = request.POST.get("message")

    insertdata = complaintable(userid=usertable(id=uid),subject=subject,message=message)
    insertdata.save()

    return render(request, 'contact.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def fetchsignupdata(request):

    username=request.POST.get("uname")
    useremail=request.POST.get("uemail")
    userphone=request.POST.get("uphone")
    userpassword=request.POST.get("upassword")
    usergender=request.POST.get("ugender")

    insertdata= usertable(name=username,email=useremail,phonenumber=userphone,password=userpassword,gender=usergender)
    insertdata.save()

    return render(request, 'login.html')

def checklogindata(request):

    useremail= request.POST.get("uemail")
    userpassword = request.POST.get("upassword")

    try:
        checkuser=usertable.objects.get(email=useremail,password=userpassword)
        request.session["loginid"]=checkuser.id
        request.session["loginname"]=checkuser.name
        request.session.save()

    except:
        checkuser= None

    if checkuser is not None:
        return redirect("/")


    else:
        print("Incorrect Password")
        messages.error(request,"Incorrect email or password")
        print(useremail)
        print(userpassword)

    return render(request, 'login.html')

def turf(request):
    getalldata = pitchtable.objects.all()
    context = {
        "pitchtable": getalldata
    }
    return render(request, 'turf.html',context)


def logout(request):
    try:
        del request.session["loginid"]
        del request.session["loginname"]

    except:
        pass

    return render(request,template_name="login.html")

def booking(request , id):
    context = {
        "pitchid":id
    }
    return render(request,"booking.html",context)


def product(request):
    getalldata = itemtable.objects.all()
    context = {
        "itemtable": getalldata
    }
    return render(request,"product.html", context)

def singleturf(request, tid):
    getsingledata = pitchtable.objects.get(id=tid)
    getseconddata= turfimages.objects.filter(turfid=tid)
    context = {
        "singledata": getsingledata,
        "seconddata": getseconddata,

    }
    return render(request, 'singleturf.html', context)

def singleproduct(request, pid):
    getsingledata = itemtable.objects.get(id=pid)
    getseconddata= productimages.objects.filter(itemid=pid)
    context = {
        "singledata": getsingledata,
        "seconddata": getseconddata,
    }

    return render(request, 'singleproduct.html', context)

def addtocart(request):
    uid= request.session["loginid"]
    proid=request.POST.get("pid")
    quantity=request.POST.get("quantity")
    price= request.POST.get("price")
    total = float(price) * int(quantity)
    print(total)


    try:
        checkitemincart = carttable.objects.get(userid=uid,itemid=proid,cartstatus=0)
    except:
        checkitemincart = None

    if checkitemincart is None:
         storedata= carttable(userid=usertable(id=uid),itemid=itemtable(id=proid),quantity=quantity,cartstatus=0,total=total
                              ,orderid=0)
         storedata.save()
    else:
        checkitemincart.quantity += int(quantity)
        checkitemincart.total += float(total)
        checkitemincart.save()

    return redirect("/cart")

def cart(request):
    uid = request.session["loginid"]
    getalldata = carttable.objects.filter(userid=uid,cartstatus=0,orderid=0)
    total_amount = getalldata.aggregate(total=Sum('total'))['total']
    print(total_amount)
    context = {
        "carttable": getalldata,
        "totalamount": total_amount
    }
    print(getalldata)
    return render(request, 'cart.html', context)

def increaseitem(request , id):
    getdata = carttable.objects.get(id=id)
    getdata.quantity += 1
    getdata.total += getdata.itemid.price
    getdata.save()
    return redirect("/cart")

def decreaseitem(request , id):
    getdata = carttable.objects.get(id=id)
    getdata.quantity -= 1
    getdata.total -= getdata.itemid.price
    getdata.save()
    return redirect("/cart")

def deleteitem(request, id):

    getturf= carttable.objects.get(id=id)
    getturf.delete()

    return redirect("/cart")

def fetchturfdata(request):
    pid = request.POST.get("pitchid")
    uid = request.session["loginid"]
    name=request.POST.get("uname")
    phone=request.POST.get("uphone")
    bdate=request.POST.get("udate")
    btime=request.POST.get("utime")
    payment = request.POST.get("payment")

    insertdata = bookingtable(userid=usertable(id=uid),pitchid=pitchtable(id=pid),name=name,phonenumber=phone,bookingdate=bdate,bookingtime=btime,paymentmode=payment)
    insertdata.save()

    return redirect("/booked")

def booked(request):
    getalldata = bookingtable.objects.all()
    context ={
        "bookedtable": getalldata
    }
    return render(request,'booked.html',context)


def deleteturf(request, id):

    getturf= bookingtable.objects.get(id=id)
    getturf.delete()

    return redirect("/booked")


def placeorderpage(request):
    uid = request.session["loginid"]
    cartdata = carttable.objects.filter(userid=usertable(id=uid),orderid=0,cartstatus=0).aggregate(Sum('total'))
    data = cartdata.get('total__sum')
    context = {
        'data':data
    }
    return render(request,"placeorderproduct.html",context)

def placeorderproduct(request):
    uid = request.session["loginid"]
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    finaltotal = request.POST.get("totalbill")
    payment = request.POST.get("payment")

    # print(uid)
    # print(phone)
    # print(address)
    # print(finaltotal)
    # print(payment)


    storedata = ordertable(userid=usertable(id=uid), phonenumber=phone, address=address, totalbill=finaltotal,
                           paymentmode=payment, orderstatus="confirmed")
    storedata.save()

    lastid = storedata.id  # fetch last inserted id in order
    getdata = carttable.objects.filter(userid=uid, cartstatus=0)
    print(getdata)

    for i in getdata:
        i.cartstatus = 1
        i.orderid = lastid
        i.save()

    # messages.success(request, "order placed successfully")
    return redirect(showorders)

def showorders(request):
    uid = request.session["loginid"]
    getdata = ordertable.objects.filter(userid=uid)
    context = {
        "orderdata":getdata
    }

    return render(request,'showorders.html', context)



def cancelorder(request,id):
    getorderdata = ordertable.objects.get(id=id)
    getorderdata.orderstatus = "cancelled"
    getorderdata.save()
    messages.success(request,"order cancelled succesfully")
    return redirect("/showorders")

def singleorder(request , id):
    getitemdata = carttable.objects.filter(orderid=id)
    context = {
        "cartdata":getitemdata
    }
    return render(request,"singleorder.html",context)

def findproduct(request):
    itemname = request.POST.get("itemname")
    finddata = itemtable.objects.filter(name__contains=itemname)
    context = {
        "alldata": finddata
    }
    return render(request,"product.html", context)


def feedback(request):
    name = request.POST.get("name")
    rating = request.POST.get("rating")
    comment = request.POST.get("review")

    insertdata = feedbacktable(name=name,rating=rating,comment=comment)
    insertdata.save()


    return render(request, "feedback.html")
