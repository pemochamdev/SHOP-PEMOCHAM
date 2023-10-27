from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from django_countries.fields import CountryField


CATEGORY_CHOICES = (
    ('S','Shirt'),
    ('SW','Sport wear'),
    ('OW','Out wear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

PAYMENT_CHOICES = (
    ('p','Paypal'),
    ('s','Stripe'),
)


class Item(models.Model):
    title = models.CharField(max_length=100, verbose_name='Titre')
    slug = models.SlugField()
    price =models.FloatField()
    discount_price =models.FloatField(blank=True, null=True)
    picture = models.ImageField(upload_to='item')
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)


    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("add_to_cart", kwargs={"slug": self.slug})
    
    def get_remove_from_cart_url(self):
        return reverse("remove_from_cart", kwargs={"slug": self.slug})


    

class ItemOrder(models.Model):
    user = models.ForeignKey(User, related_name='user_oi', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_io')
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.title
    
    
    def get_total_item_price(self):
        return (self.quantity * self.item.price)
    
   
    def get_total_discount_item_price(self):
        return (self.quantity * self.item.discount_price)
    
    
    def get_amount_saved(self):
        return (self.get_total_item_price() - self.get_total_discount_item_price())

    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        
        return self.get_total_item_price()
    
class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(ItemOrder)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress',
        on_delete=models.SET_NULL,
        related_name='billing_address',
        blank=True,
        null=True
    )

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total



class BillingAddress(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_b_a', 
        on_delete=models.CASCADE
    )
    streep_address = models.CharField(
        max_length=100
    )
    appartment_address = models.CharField(
        max_length=100
    )
    country = CountryField(
        multiple = True
    )
    zip = models.CharField(
        max_length=100
    )
    # same_shipping_address = models.BooleanField(
    #     default=False
    # )
    # save_info = models.BooleanField(
    #     default=False
    # )
    payment_option = models.CharField(
        max_length=1,
        choices=PAYMENT_CHOICES
    )

    def __str__(self):
        return self.user.username
    