from django.urls import path
from base.views import product_views as views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [


    path('',views.GetProducts ,name='products'),
    path('<str:pk>/',views.GetProductById ,name='product')

]
