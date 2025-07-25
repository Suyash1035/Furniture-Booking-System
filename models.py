from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
STATE_CHOICES = ( 
    ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'), 
    ('Andhra Pradesh','Andhra Pradesh'), 
    ('Arunachal Pradesh','Arunachal Pradesh'), 
    ('Assam','Assam'), 
    ('Bihar','Bihar'), 
    ('Chandigarh','Chandigarh'), 
    ('Chattisgarh','Chattisgarh'), 
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'), 
    ('Daman and Diu','Daman and Diu'), 
    ('Delhi','Delhi'), 
    ('Goa','Goa'), 
    ('Gujrat','Gujrat'), 
    ('Haryana','Haryana'), 
    ('Himachal Pradesh','Himachal Pradesh'), 
    ('Jammu & Kashmir','Jammu & Kashmir'), 
    ('Jharkhand','Jharkhand'), 
    ('Karnataka','Karnataka'), 
    ('Kerala','Kerala'), 
    ('Lakshadweep','Lakshadweep'), 
    ('Madhya Pradesh','Madhya Pradesh'), 
    ('Maharashtra','Maharashtra'), 
    ('Manipur','Manipur'), 
    ('Meghalaya','Meghalaya'), 
    ('Mizoram','Mizoram'), 
    ('Nagaland','Nagaland'), 
    ('Odisa','Odisa'), 
    ('Puducherry','Puducherry'), 
    ('Punjab','Punjab'), 
    ('Rajasthan','Rajasthan'), 
    ('Sikkim','Sikkim'), 
    ('Tamil Nadu','Tamil Nadu'), 
    ('Telangana','Telangana'), 
    ('Tripura','Tripura'), 
    ('Uttarakhand','Uttarakhand'), 
    ('Uttar Pradesh','Uttar Pradesh'), 
    ('West Bengal','West Bengal'), 
) 

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    locality = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES ,max_length=300)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('bs','bar_stools'),
    ('s','sofs'),
    ('bst','bed-side-table'),
    ('bsl','book_shelf'),
    ('ch','chaises'),
    ('cd','chestdrawer'),
    ('ct','coffeetable'),
    ('kb','kingbed'),
    ('lc','loungechair'),
    ('md','moderndining'),
    ('st','studytable'),
    ('wd','woodendining'),
    ('wc','wallcoverage'),
    ('wm','wallmount'),
    ('sw','swing'),
)

class Product(models.Model): 
    title = models.CharField(max_length=300)     
    selling_price = models.FloatField()     
    discounted_price = models.FloatField()     
    description = models.TextField()      
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)     
    product_image = models.ImageField(upload_to = 'productimg') 

    def __str__(self): 
        return str(self.id) 
     


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the Way','On the Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200,choices=STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

PAYMENT_CHOICES = (
    ('Successful','Successful'),
    ('Incomplete','Incomplete'),
    ('Failed','Failed')
)
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=200,choices=PAYMENT_CHOICES,default='Successful')