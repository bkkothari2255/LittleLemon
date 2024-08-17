from rest_framework import permissions
from django.contrib.auth.models import User

class IsDeliveryCrew(permissions.BasePermission):
    edit_methods = ('put','patch')
    
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Delivery Crew").exists():
            return True
        
class IsManager(permissions.BasePermission):
    edit_methods = ('put','patch','post')

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Manager").exists():
            return True