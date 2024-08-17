import django.db
from rest_framework import serializers
from .models import Cart, Category, MenuItem, Order
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    #category = CategorySerializer()
    price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
    
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','price_after_tax','category']
        
    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user','delivery_crew','status','total','date']
        

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        field = ['id','user','menu_item','unit_price','quantity','price']
        
        
        