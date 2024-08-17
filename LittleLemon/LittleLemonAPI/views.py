from rest_framework.response import Response
from rest_framework import generics, viewsets
from .models import MenuItem, Category, OrderItem, Cart
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer, CartSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttles import TenCallsPerMinute

class CategoryView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes= [IsAuthenticated]
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    search_fields = ['title','category__title']
    ordering_fields = ['price','category']
    filterset_fields = ['category']
    
class SingleMenuItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes= [IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
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
    
class CartView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes= [IsAuthenticated]
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

@permission_classes([IsAuthenticated])
class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_throttles(self):
        if self.action == 'list':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]
