from django.db import models


# Create your models here.
class Booking(models.Model):
    name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)
    no_of_guests = models.IntegerField(default=1)

    def __str__(self): 
        return self.name


# Add code to create Menu model
class Menu(models.Model):
   title = models.CharField(max_length=200) 
   price = models.IntegerField(null=False) 
   menu_item_description = models.TextField(max_length=1000, default='')
   inventory = models.IntegerField(null=False,default=0) 

   def __str__(self):
      return self.name