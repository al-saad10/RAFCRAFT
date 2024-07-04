from django.urls import path
from .views import *



urlpatterns = [
    path('shop/', ShopView.as_view(), name='shop'),
    path('category/<str:category>/', EachCategoryView.as_view(), name='each_category_products'), 
    path('product/<int:pk>/', DetailProductView.as_view(), name='detail_product_view'),
    path('subcategory/<str:subcategory>/', EachSubCategoryView.as_view(), name='subcategory_detail'),
    path('Event/<str:event>/', EventView.as_view(), name='event_product'),
]