from django.db import models
from rest_framework.response import Response
from rest_framework import generics
from .models import MenuItem, Category, OrderItem, Cart
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer, CartSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    
class SingleMenuItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
class OrdersView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderSerializer
    
class SingleOrderView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderSerializer
    
class CartView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some Secret Message"})
    
    

