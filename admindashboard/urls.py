from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", AdminLogIn.as_view(), name="admin_login"),
    path("admin_dashboard/", AdminDashboard.as_view(), name="admin_dashboard"),
    path("admin_customer_management/", AdminCustomerProfileMangement.as_view(), name="admin_customer_datails_management"),
    path("admin_product_management/", AdminProductManagement.as_view(), name="admin_product_management"),
    path("admin_add_product_management/", AdminAddProductManagement.as_view(), name="admin_add_product_management"),
    path("admin_add_product_image_management/", AdminProductImageManagement.as_view(), name="admin_add_product_image_management"),
    path("admin_product_inventory_management/", AdminProductInventoryManagement.as_view(), name="admin_product_inventory_management"),
    path("order_item/<int:id>", AdminOrderModuleManagement.as_view(), name = 'admin_order_item_management'),
    path('admin_category/', AdminCategoryManagement.as_view(), name='admin_category_management'),
    path('admin_subcategory/', AdminSubCategoryManagement.as_view(), name='admin_subcategory_management'),
    path('admin_event/', AdminEventManagement.as_view(), name='admin_event_management'),
]