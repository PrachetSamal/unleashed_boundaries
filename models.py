from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
status_list = [
    ('active','active'),
    ('inactive','inactive'),
]

class usertable(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    phonenumber=models.BigIntegerField()
    password = models.CharField(max_length=20)
    gender=models.CharField(max_length=10)

    def __str__(self):
        return self.name

class categorytable(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name

class areatable(models.Model):
    name = models.CharField(max_length=30)
    address = models.TextField()

    def __str__(self):
        return self.name

class itemtable(models.Model):
    name = models.CharField(max_length=30)
    catid=models.ForeignKey(categorytable,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos')
    price=models.FloatField()
    brand=models.CharField(max_length=30, null= True)
    discription = models.TextField()

    def item_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))
    item_photo.allow_tags = True

    def __str__(self):
        return self.name

class carttable(models.Model):
    userid = models.ForeignKey(usertable, on_delete=models.CASCADE)
    itemid = models.ForeignKey(itemtable, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    cartstatus = models.IntegerField(null=True,default=0)
    total = models.FloatField()
    orderid =models.IntegerField(null=True,default=0)



class pitchtable(models.Model):
    name = models.CharField(max_length=30)
    price= models.IntegerField(null=True)
    areaid=models.ForeignKey(areatable,on_delete=models.CASCADE)
    phonenumber=models.BigIntegerField(null=True)
    image=models.ImageField(upload_to='photos',null=True)
    description=models.TextField(null= True)

    def pitch_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))
    pitch_photo.allow_tags = True

    def __str__(self):
        return self.name


class ordertable(models.Model):
    userid = models.ForeignKey(usertable, on_delete=models.CASCADE)
    orderstatus = models.CharField(max_length=40, null=True)
    phonenumber= models.BigIntegerField(null=True)
    address= models.TextField(null=True)
    totalbill= models.FloatField(null=True)
    paymentmode = models.CharField(max_length=20, null=True)
    datetime= models.DateTimeField(auto_now_add=True, null= True)

class bookingtable(models.Model):
    pitchid=models.ForeignKey(pitchtable,on_delete=models.CASCADE, null=True)
    userid=models.ForeignKey(usertable,on_delete=models.CASCADE)
    bookingdate = models.DateField()
    bookingtime = models.TimeField()
    name=models.CharField(max_length=30, null=True)
    phonenumber=models.BigIntegerField(null= True)
    datetime= models.DateTimeField(auto_now_add=True, null= True)
    paymentmode = models.CharField(max_length=20, null=True)


class feedbacktable(models.Model):
    name= models.CharField(max_length=30, null=True)
    rating=models.IntegerField(null= True)
    comment=models.TextField(null= True)

class complaintable(models.Model):
    userid = models.ForeignKey(usertable, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    subject = models.TextField(null=True)
    message = models.TextField(null=True)

class productimages(models.Model):
    itemid = models.ForeignKey(itemtable,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="photos")

    def pro_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))
    pro_photo.allow_tags = True

class turfimages(models.Model):
    turfid = models.ForeignKey(pitchtable,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="photos")

    def turf_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))
    turf_photo.allow_tags = True
