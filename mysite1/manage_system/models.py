from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class customer(models.Model):
    customer_id=models.CharField(max_length=100,primary_key=True)
    customer_name=models.CharField(max_length=100)
    customer_type=models.CharField(max_length=100)
    contactor=models.CharField(max_length=100)
    tele=models.CharField(max_length=20)
    address=models.CharField(max_length=100)
    notes=models.CharField(max_length=100)
    def __str__(self):
        return self.customer_id+self.customer_name+self.customer_type
class storage(models.Model):
    storage_id=models.CharField(max_length=100,primary_key=True)
    storage_name=models.CharField(max_length=100)
    storage_info=models.CharField(max_length=100)
    def __str__(self):
        return self.storage_id+" "+self.storage_name
class product(models.Model):
    product_id=models.CharField(max_length=100,primary_key=True)
    product_name=models.CharField(max_length=100)
    product_size=models.CharField(max_length=100)
    product_value=models.IntegerField(default=0)
    product_leastcount=models.IntegerField(default=0)
    product_maxcount=models.IntegerField(default=0)
    product_storage=models.ForeignKey('storage',on_delete=models.SET_DEFAULT,default='0')#默认是0
    def __str__(self):
        return self.product_id+self.product_name+self.product_size
class sys_users(AbstractUser):
    user_authority=models.IntegerField(default=0)#1是普通用户2是管理员
    user_infor=models.CharField(max_length=100)#备注
