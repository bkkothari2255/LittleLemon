from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items',views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu-items-throttle',views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu-items-throttle/<int:pk>',views.MenuItemsViewSet.as_view({'get':'retrieve'})),
    path('category', views.CategoryView.as_view()),
    path('orders',views.OrdersView.as_view()),
    path('orders/<int:pk>',views.SingleOrderView.as_view()),
    path('cart/menu-items',views.CartView.as_view()),
    path('secret/',views.secret),
    path('api-auth-token/', obtain_auth_token), # only accepts http post call
    path('manager-view/',views.manager_view), # only manager should see this
    path('throttle-check/',views.throttle_check), # thorttle check 
    path('throttle-check-auth/',views.throttle_check_auth), # throttle check auth users
    path('throttle-check-custom/',views.throttle_check_custom), # throttle check custom
]