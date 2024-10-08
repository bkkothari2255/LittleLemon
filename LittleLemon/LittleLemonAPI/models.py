from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True,default=1)
    
    def __str__(self):
        return self.title
    
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,default=1)
    
    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2,null=True)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    class Meta:
        unique_together = ('menu_item','user')
    
    def __str__(self):
        return self.user.username + " | " + self.menu_item.title
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivry_crew", limit_choices_to={'groups__name':'Delivery Crew'},null=True)
    status = models.BooleanField(db_index=True,default=0)
    total = models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateField(db_index=True)
    time = models.TimeField(db_index=True,null=True)
    
    def __str__(self):
        return 'ODR#'+str(self.id)+"-D"+str(self.date).replace('-','')+"T"+str(self.time).replace(':','')
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    
    class Meta:
        unique_together = ('order', 'menu_item')
    
    def __str__(self):
        return self.order.user.username + " | " + self.menu_item.title