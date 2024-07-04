from django.urls import path
from order import views
from .views import *

urlpatterns = [

    #cart module urls 
    path('add-to-cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='show_cart'),
    path('plus-cart', views.plus_cart),
    path('minus-cart', views.minus_cart),
    path('remove-cart', views.remove_cart),

    #order module urls
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('checkout/<int:id>', DirectCheckout.as_view(), name='direct_checkout'),
    # path('confirmation/', views.order, name='order'),
    path('order_history/', views.order_history, name='order_history'),
]
