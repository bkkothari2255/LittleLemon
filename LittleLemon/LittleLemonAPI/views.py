from datetime import datetime,date
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .throttles import TenCallsPerMinute
from .pagination import MenuItemsPagination, CategoryPagination
from .permissions import IsManager
from .models import Cart, Category, MenuItem, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer, CartSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth.models import Group, User
from rest_framework import generics
import math

class CategoryView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsAuthenticated, IsAdminUser]
                   
        return [permission() for permission in permission_classes]
            

class MenuItemsView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    search_fields = ['title','category__title']
    ordering_fields = ['price','category']
    filterset_fields = ['category']
    pagination_class = MenuItemsPagination
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsAuthenticated, IsAdminUser]  
                     
        return [permission() for permission in permission_classes] 
    
class SingleMenuItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]  
        elif self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.request.method == "PATCH":
            permission_classes = [IsAuthenticated, IsManager]
        
        return [permission() for permission in permission_classes]
    
    def patch(self,request, *args, **kwargs):
        menu_item = MenuItem.objects.get(pk=self.kwargs['pk'])
        menu_item.featured = not menu_item.featured
        menu_item.save()
        return JsonResponse(status=200, data={'message':'Featured status of {} changed to {}'.format(str(menu_item.title) ,str(menu_item.featured))})

        
class OrdersView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        if self.request.user.groups.filter(name="Manager").exists():
            queryset = Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            queryset = Order.objects.filter(delivery_crew=self.request.user)
        else:
            queryset = Order.objects.filter(user=self.request.user)
        
        return queryset
    
    def get_permissions(self):
        if self.request.method == 'GET' or 'POST' : 
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        return[permission() for permission in permission_classes]
    
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user)
        x=cart.values_list()
        if len(x) == 0:
            return JsonResponse(status=400, data={'message':'Bad Request due to cart is empty.'})
        total = math.fsum([float(x[-1]) for x in x])       
        order = Order.objects.create(user=request.user, status=False, total=total, date=date.today(), time=datetime.now().time())
        for i in cart.values():
            try:
                menu_item = get_object_or_404(MenuItem, id=i['menu_item_id'])
                orderitem = OrderItem.objects.create(order=order,menu_item=menu_item,quantity=i['quantity'])
                orderitem.save()
            except:
                return JsonResponse(status="409",data={'message':'Order already placed..'})
        cart.delete()
        return JsonResponse(status=201, data={'message':'Your order has been placed! Your order number starting with ODR#{}'.format(str(order.id))})
    
class SingleOrderView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle] 
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]  
                 
        return [permission() for permission in permission_classes] 
    
    def get_queryset(self,*args,**kwargs):
        queryset = Order.objects.filter(id=self.kwargs['pk'])
        return queryset
    
    def patch(self,*args,**kwargs):
        if self.request.user.groups.filter(name='Delivery Crew').exists():
            order = Order.objects.get(pk=self.kwargs['pk'])
            order.status = not order.status
            order.save()
            return JsonResponse(status=200, data={'meassage':'Order Status changed to {}'.format( 'delivered' if order.status else 'not delivered.')})
        
        elif self.request.user.groups.filter(name='Manager').exists():
            order = Order.objects.get(pk=self.kwargs['pk'])
            id = self.request.data['delivery_crew']
            order.delivery_crew = User.objects.get(id=id)
            order.save()
            return JsonResponse(status=200,data={'message':'Assigned order {} to {}'.format(order, order.delivery_crew.username)})
        else:
            return JsonResponse(status=404, data={'message':"No order found."})
    
class CartView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes= [IsAuthenticated]
    serializer_class = CartSerializer
    
    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user)
        return queryset
    
    def post(self, request, *args, **kwargs):
        seriealized_item = CartSerializer(data=request.data, context={'request':request})
        seriealized_item.is_valid(raise_exception=True)
        menu_item_id = request.data['menu_item']
        quantity = request.data['quantity']
        item = get_object_or_404(MenuItem,id=menu_item_id)
        unit_price = item.price
        price = int(quantity) * unit_price
        try:
            Cart.objects.create(user=request.user,menu_item_id=menu_item_id,quantity=quantity,unit_price=unit_price,price=price)
        except:
            return JsonResponse(status=409, data={"message":"Items already in the cart."})
        return JsonResponse(status=201, data={"message":"Item added to the cart"})
    
    def delete(self, request, *args, **kwargs):
        if request.POST.get('menu_item'):
            menu_item_id = request.data['menu_item']
            cart = get_object_or_404(Cart,user=request.user,menu_item_id=menu_item_id)
            cart.delete()
            return JsonResponse(status=200, data={"message":"Menu Item deleted from the cart."})
        else:
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse(status=200, data={"message":"Cart is empty"})
    
class DeliveryCrewGroupView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    permission_classes = [IsAuthenticated,IsManager]
    queryset = User.objects.filter(groups__name='Delivery Crew')
    serializer_class = UserSerializer
    
    def post(self, *args, **kwargs):
        if self.request.POST.get('username'):
            delivery_crew = Group.objects.get(name='Delivery Crew')
            user = get_object_or_404(User, username= self.request.POST.get('username'))
            delivery_crew.user_set.add(user)
            return JsonResponse(status=201,data={'message':'{} is added to delivery crew'.format(user.username)})
        return JsonResponse(status=400, data={'message':'Bad request.'})
    
    def delete(self, *args, **kwargs):
        if self.request.POST.get('username'):
            delivery_crew = Group.objects.get(name='Delivery Crew')
            user = get_object_or_404(User, username= self.request.POST.get('username'))
            delivery_crew.user_set.remove(user)
            return JsonResponse(status=200,data={'message':'{} is removed from delivery crew'.format(user.username)})
        return JsonResponse(status=400, data={'message':'Bad request.'})
    
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAdminUser])
@throttle_classes([TenCallsPerMinute])
def managers(request):
    if request.method == "GET":
        users = User.objects.filter(groups__name='Manager')
        user_serializer = UserSerializer(users,many=True)
        return JsonResponse(status=200, data=user_serializer.data,safe=False)
    else:
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Manager')
            if request.method == "POST":
                managers.user_set.add(user)
                return JsonResponse(status=201,data={'message':'User {} is added to manager group'.format(str(username))})
            elif request.method == "DELETE":
                managers.user_set.remove(user)
                return JsonResponse(status=201,data={'message':'User {} is removed from manager group'.format(str(username))})   
    return JsonResponse(status=400,data ={'message':'Bad Request.'})
