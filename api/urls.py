from django.urls import path
from .views import UserView, UserDetailView, TransferView

urlpatterns = [
    path('users', UserView.as_view(), name='user'),
    path('users/<int:id>', UserDetailView.as_view(), name='user_detail'),
    path('users/<int:id>/transfer', TransferView.as_view(), name='transfer'),
]
