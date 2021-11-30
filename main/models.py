from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.validators import MinValueValidator, MaxValueValidator


class Customer(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    image = models.ImageField()

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 


class Category(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 


class Product(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12,
                                decimal_places=2)
    image = models.ImageField()
    
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 

    def get_absolute_url(self):
        return reverse_lazy('product-detail', args=(self.pk, ))


class Order(models.Model):
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=18)
                                        
    def __str__(self):
        return self.id

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0,
                                   null=True,
                                   blank=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity 
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE)
    address = models.CharField(max_length=200,
                            null=True)
    zipcode = models.CharField(max_length=200,
                            null=True)
    phone = models.SmallIntegerField()

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = 'Shipping Addresses'


class Review(models.Model):
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.DecimalField(max_digits=3,
                               decimal_places=2, 
                               validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.customer.name


class Blog(models.Model):
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField()
    date = models.DateTimeField(auto_now_add=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 

    def __str__(self):
        return self.title
