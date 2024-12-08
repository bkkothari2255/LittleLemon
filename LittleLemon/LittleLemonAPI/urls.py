from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items',views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('message', views.msg),
    path('api-token-auth/', obtain_auth_token),
    path('category', views.CategoryView.as_view()),
    path('orders',views.OrdersView.as_view()),
    path('orders/<int:pk>',views.SingleOrderView.as_view()),
    path('cart/menu-items',views.CartView.as_view()),
    path('groups/manager/users',views.managers),
    path('groups/delivery-crew/users',views.DeliveryCrewGroupView.as_view()),
]