from django.http import JsonResponse
from .pagination import MenuItemsPagination, CategoryPagination
from .permissions import IsDeliveryCrew, IsManager
from rest_framework import generics
from .models import MenuItem, Category, OrderItem, Cart
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer, CartSerializer
#from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
#from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttles import TenCallsPerMinute
from django.contrib.auth.models import Group, User
from rest_framework import viewsets

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
    permission_classes= [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderSerializer
    
class SingleOrderView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle] 
    permission_classes= [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderSerializer
    
class CartView(generics.ListCreateAPIView,generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes= [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    

class DeliveryCrewView(generics.RetrieveUpdateAPIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    permission_classes = [IsDeliveryCrew]
    

class ManagerView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    
    
class UserGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    


# @api_view()
# @permission_classes([IsAuthenticated])
# def secret(request):
#     return Response({"message":"Some Secret Message"})

    

# @api_view()
# @permission_classes([IsAuthenticated])
# def manager_view(request):
#     if request.user.groups.filter(name='Manager').exists():
#         return Response({"message":"Only Manager should see this message"})
#     else:   
#         return Response({"message":"You are not authorised"}, 403)
    

# @api_view()
# @throttle_classes([AnonRateThrottle])
# def throttle_check(request):
#     return Response({"message": "sucessful"})

# @api_view()
# @permission_classes([IsAuthenticated])
# @throttle_classes([UserRateThrottle])
# def throttle_check_auth(request):
#     return Response({"message":"Message for logged in user"})

# @api_view()
# @permission_classes([IsAuthenticated])
# @throttle_classes([TenCallsPerMinute])
# def throttle_check_custom(request):
#     return Response({"message":"Message for logged in user 10 call per minute"})

# @permission_classes([IsAuthenticated])
# class MenuItemsViewSet(viewsets.ModelViewSet):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
    
#     def get_throttles(self):
#         if self.action == 'list':
#             throttle_classes = [UserRateThrottle]
#         else:
#             throttle_classes = []
#         return [throttle() for throttle in throttle_classes]
