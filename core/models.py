from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


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

class Item(models.Model):
    title = models.CharField(max_length=100, verbose_name='Titre')
    slug = models.SlugField()
    price =models.FloatField()
    discount_price =models.FloatField(blank=True, null=True)
    piture = models.ImageField(upload_to='item')
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
    

    
class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(ItemOrder)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)