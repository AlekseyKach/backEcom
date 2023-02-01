from django.urls import path
from base.views import order_views as views


urlpatterns = [
    path('add/' , views.AddOrderItem , name='orders-add'),
     path('<str:pk>/' , views.GetOrderById, name='user-order')

    

]