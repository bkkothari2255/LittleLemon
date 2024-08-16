from django.db import models
from rest_framework.response import Response
from rest_framework import generics
from .models import MenuItem, Category, OrderItem, Cart
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer, CartSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttles import TenCallsPerMinute

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
    

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"Only Manager should see this message"})
    else:   
        return Response({"message":"You are not authorised"}, 403)
    

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "sucessful"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({"message":"Message for logged in user"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_custom(request):
    return Response({"message":"Message for logged in user 10 call per minute"})
