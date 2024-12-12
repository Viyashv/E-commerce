from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    first_name = models.CharField(max_length  = 50)
    last_name = models.CharField(max_length  = 50)
    e_mail = models.EmailField(max_length = 50)
    phone = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)

    def __str__(self):
        return self.first_name , self.last_name

class Com(models.Model):
    brand = models.CharField(max_length=20)
    ct = models.ForeignKey(Category , on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id)+" "+str(self.brand)+ " "+ str(self.ct)
    
class Product(models.Model):
    name = models.CharField(max_length = 20)
    price = models.DecimalField(default = 0 , max_digits = 10 , decimal_places = 2)
    image = models.ImageField(upload_to='upload/')
    brand = models.ForeignKey(Com , on_delete=models.CASCADE)
    description = models.CharField(max_length = 1000)
    category = models.ForeignKey(Category , on_delete = models.CASCADE)
    is_sale = models.BooleanField(default = False)
    sale_price = models.DecimalField(default = 0 , max_digits = 10 , decimal_places = 2)

    def __str__(self):
        return f"Id :- {self.id} - Name :- {self.name} - Category :- {self.category}"



class Order(models.Model):
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer , on_delete = models.CASCADE)
    address = models.CharField(max_length = 100 , null = False , blank = False)
    quantity = models.IntegerField(default = 1)
    phone = models.CharField(max_length = 20)
    date = models.DateField(default = datetime.datetime.today)
    status = models.BooleanField(default = False)
    

    def __str__(self):
        return self.product


class Cart(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    products =models.ForeignKey(Product, on_delete = models.CASCADE) 
    quantity = models.IntegerField(default = 1)
    ord_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user)+ " " +str(self.id)


