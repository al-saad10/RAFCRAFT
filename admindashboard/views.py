from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from products.models import *
from home_and_auth.models import *
from order.models import *
from user.models import *
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
# Create your views here.


#custom decorator function
def staff_required(function):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url='/admin_login/',  
    )
    return actual_decorator(function)

#Admin LogIn
class AdminLogIn(View):
    def get (self, request):
        return render (request, "admin/login.html")
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Only stuffs are allowed to use custom admin services!")
            return redirect("admin_login")


#Admin maindashboard
class AdminDashboard(View):
    @method_decorator(staff_required)
    def get(self, request):
        regular_users = User.objects.exclude(is_staff=True, is_superuser=True)
        orders_with_items = Order.objects.annotate(num_items=Count('orderitem')).filter(num_items__gte=1)
        return render(request, 'admin/dashboard.html', {
                                                        'regular_users_count':regular_users.count(),
                                                        'orders': orders_with_items,
                                                         'order_count': orders_with_items.count(),
                                                         'category_object_count':Category.objects.all().count(),
                                                         'slider_item_object_count': SliderItem.objects.all().count(),
                                                         'subcategory_object_count':SubCategory.objects.all().count(),
                                                         })
    @method_decorator(staff_required)
    def post(self, request):
        order_id = request.POST.get('order_id')
        order_object = Order.objects.get(id=order_id)
        order_object.delete()
        return redirect(reverse('admin_dashboard'))


#Admin category module management
class AdminCategoryManagement(View):
    @method_decorator(staff_required)
    def get(self, request):
        category_objects = Category.objects.all()
        return render(request, 'admin/category.html', {'category_objects': category_objects})

    @method_decorator(staff_required)   
    def post(self, request):
        if 'add_category_name' in request.POST and 'add_category_image' in request.FILES:
            new_category_name = request.POST.get('add_category_name')
            new_category_image = request.FILES.get('add_category_image')
            Category.objects.create(name=new_category_name, image=new_category_image)

        elif 'update_category_name' in request.POST:
            updated_category_name = request.POST.get('update_category_name')
            category_id = request.POST.get('category_id')
            category = Category.objects.get(pk=category_id)
            category.name = updated_category_name
            category.save()
        elif 'update_category_image' in request.FILES:
            updated_category_image = request.FILES.get('update_category_image')
            category_id = request.POST.get('category_id')
            category = Category.objects.get(pk=category_id)
            category.image = updated_category_image
            category.save()

        elif 'delete_category_object' in request.POST:
            category_id = request.POST.get('delete_category_object')
            category = Category.objects.get(pk=category_id)
            category.delete()
        return redirect('admin_category_management')
    
    
#Admin Subcategory Management
class AdminSubCategoryManagement(View):
    @method_decorator(staff_required)
    def get(self, request):
        available_category = Category.objects.all()
        subcategory_objects = SubCategory.objects.all()
        return render(request, 'admin/subcategory.html', {'available_category':available_category,'subcategory_objects': subcategory_objects})
    @method_decorator(staff_required)   
    def post(self, request):
        if 'available_category_status' in request.POST and 'add_subcategory_name' in request.POST and 'add_subcategory_image' in request.FILES :
            category_id = request.POST.get('available_category_status')  # Fetching the selected category ID
            category = Category.objects.get(id=category_id)
            new_subcategory_name = request.POST.get('add_subcategory_name')
            new_subcategory_image = request.FILES.get('add_subcategory_image')
            SubCategory.objects.create(category=category, name=new_subcategory_name, image=new_subcategory_image)

        elif 'update_subcategory_name' in request.POST:
            updated_subcategory_name = request.POST.get('update_subcategory_name')
            subcategory_id = request.POST.get('subcategory_id')
            subcategory = SubCategory.objects.get(id=subcategory_id)
            subcategory.name = updated_subcategory_name
            subcategory.save()
        elif 'update_subcategory_image' in request.FILES:
            updated_subcategory_image = request.FILES.get('update_subcategory_image')
            subcategory_id = request.POST.get('subcategory_id')
            subcategory = SubCategory.objects.get(id=subcategory_id)
            subcategory.image = updated_subcategory_image
            subcategory.save()

        elif 'delete_subcategory_object' in request.POST:
            subcategory_id = request.POST.get('delete_subcategory_object')
            subcategory = SubCategory.objects.get(id=subcategory_id)
            subcategory.delete()
        return redirect('admin_subcategory_management')



#Admin event module management
class AdminEventManagement(View):
    @method_decorator(staff_required)
    def get(self, request):
        event_objects = SliderItem.objects.all()
        return render(request, 'admin/event.html', {'event_objects': event_objects})
    @method_decorator(staff_required)   
    def post(self, request):
        if 'add_event_name' in request.POST and 'add_event_image' in request.FILES:
            new_event_name = request.POST.get('add_event_name')
            new_event_image = request.FILES.get('add_event_image')
            new_event_item = SliderItem.objects.create(event=new_event_name)
            SliderItemImage.objects.create(slider_item=new_event_item, image=new_event_image)

    
        elif 'update_event_name' in request.POST:
            updated_event_name = request.POST.get('update_event_name')
            event_id = request.POST.get('event_id')
            event_item = SliderItem.objects.get(pk=event_id)
            event_item.event = updated_event_name
            event_item.save()
        elif 'update_event_image' in request.FILES:
            updated_event_image = request.FILES.get('update_event_image')
            event_id = request.POST.get('event_id')
            event_item = SliderItem.objects.filter(id=event_id)
            event_image_update = SliderItemImage.objects.filter(slider_item=event_id).first()
            event_image_update.image = updated_event_image
            event_image_update.save()


        elif 'delete_event_object' in request.POST:
            event_id = request.POST.get('delete_event_object')
            event = SliderItem.objects.get(id=event_id)
            event.delete()
        return redirect('admin_event_management')

#Admin Product Management
class AdminProductManagement(View):
    @method_decorator(staff_required)
    def get(self, request):
        category_objects = Category.objects.all()
        subcategory_objects = SubCategory.objects.all()
        all_event_objects=SliderItem.objects.all()
        all_products_object = Product.objects.all()
        
        context = {
            'all_products_object': all_products_object,
            'category_objects': category_objects,
            'subcategory_objects': subcategory_objects,
            'all_event_objects':all_event_objects
        }
        
        return render(request, 'admin/product_management.html', context)
    @method_decorator(staff_required)
    def post(self, request):
        if 'delete_product' in request.POST:
            product_id = request.POST.get('delete_product')
            Product.objects.get(id=product_id).delete()
            messages.success(request, 'Product deleted successfully.')
        else:
            product_id = request.POST.get('product_id')
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            discounted_price = request.POST.get('discounted_price')
            category_id = request.POST.get('category_id')
            subcategory_id = request.POST.get('subcategory_id')
            quantity = request.POST.get('quantity')
            event_id = request.POST.get('event')
            event = SliderItem.objects.get(id=event_id)
            material = request.POST.get('material')
            weight = request.POST.get('weight')
            warranty_year = request.POST.get('warranty_year')
            warranty_policy = request.POST.get('warranty_policy')

            product = Product.objects.get(id=product_id)

            product.name = name
            product.description = description
            product.price = price
            product.discounted_price = discounted_price
            product.category_id = category_id
            product.subcategory_id = subcategory_id
            product.quantity = quantity
            product.event = event
            product.material = material
            product.weight = weight
            product.warranty_year = warranty_year
            product.warranty_policy = warranty_policy
            
            product.save()
            messages.success(request, 'Product updated successfully.')

        return redirect('admin_product_management')
    
class AdminAddProductManagement(View):
    @method_decorator(staff_required)
    def get(self,request):
        category_objects = Category.objects.all()
        subcategory_objects = SubCategory.objects.all()
        all_event_objects=SliderItem.objects.all()
        context = {
            'category_objects': category_objects,
            'subcategory_objects': subcategory_objects,
            'all_event_objects':all_event_objects
        }
        
        return render(request, 'admin/add_product_management.html', context)
    @method_decorator(staff_required)
    def post(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            discounted_price = request.POST.get('discounted_price')
            category_id = request.POST.get('category_id')
            subcategory_id = request.POST.get('subcategory_id')
            quantity = request.POST.get('quantity')
            event_id = request.POST.get('event')
            material = request.POST.get('material')
            weight = request.POST.get('weight')
            warranty_year = request.POST.get('warranty_year')
            warranty_policy = request.POST.get('warranty_policy')

            if event_id:
                try:
                    event = SliderItem.objects.get(id=event_id)
                except:
                    pass
            else:
                event = None

            new_product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                discounted_price=discounted_price,
                category_id=category_id,
                subcategory_id=subcategory_id,
                quantity=quantity,
                event=event,  
                material=material,
                weight=weight,
                warranty_year=warranty_year,
                warranty_policy=warranty_policy
            )
            messages.success(request, 'Product added successfully.')
        return redirect('admin_add_product_management')


        
class AdminProductImageManagement(View):
    @method_decorator(staff_required)
    def get(self,request):
        all_product_objects = Product.objects.all()
        products_with_images = ProductImage.objects.all()
        return render (request, 'admin/admin_product_image_management.html', {'products_with_images':products_with_images, 'all_product_objects':all_product_objects})
    @method_decorator(staff_required)
    def post(self, request):
        if 'available_product' in request.POST and 'add_product_image' in request.FILES :
            product_id = request.POST.get('available_product')  # Fetching the selected category ID
            product = Product.objects.get(id=product_id)
            new_product_image = request.FILES.get('add_product_image')
            ProductImage.objects.create(product=product, image=new_product_image)
            messages.success(request, 'Product Image added successfully.')

        elif 'update_product_image' in request.FILES:
            updated_product_image = request.FILES.get('update_product_image')
            product_image_id = request.POST.get('productimage_id')
            product_image = ProductImage.objects.get(id=product_image_id)
            product_image.image = updated_product_image
            product_image.save()
            messages.success(request, 'Product Image Updated successfully.')

        elif 'delete_product_image' in request.POST:
            product_image_id = request.POST.get('delete_product_image')
            image = ProductImage.objects.get(id=product_image_id)
            image.delete()
            messages.success(request, 'Product Image deleted successfully.')
        return redirect('admin_add_product_image_management')
    
class AdminProductInventoryManagement(View):
    @method_decorator(staff_required)
    def get(self,request):
        all_product_objects = Product.objects.all()
        products_with_invenotry_status = Inventory.objects.all()
        return render (request, 'admin/admin_product_inventory_management.html', {'products_with_invenotry_status':products_with_invenotry_status, 'all_product_objects':all_product_objects})
    @method_decorator(staff_required)
    def post(self, request):
        if 'available_product' in request.POST and 'add_product_inventory' in request.POST :
            
            product_id = request.POST.get('available_product')  # Fetching the selected category ID
            product = Product.objects.get(id=product_id)
            product_inventory_status = request.POST.get('add_product_inventory')
            Inventory.objects.create(product=product, quantity_available=product_inventory_status)
            messages.success(request, 'Product Inventory Status added successfully.')

        elif 'product_availability' in request.POST:
            updated_inventory_status = request.POST.get('product_availability')
            product_inventory_status_id = request.POST.get('product_inventory_status_id')
            inventory_details = Inventory.objects.get(id=product_inventory_status_id)
            inventory_details.quantity_available = updated_inventory_status
            inventory_details.save()
            messages.success(request, 'Product Inventory Status updated successfully.')
            
        return redirect('admin_product_inventory_management')
    
#Admin order module management 
class AdminOrderModuleManagement(View):
    @method_decorator(staff_required)
    def get(self, request, id):
        pending_order_items = OrderItem.objects.filter(order=id)
        pending_order_items_count = pending_order_items.count()
        return render(request, 'admin/order_item.html', {'pending_order_items': pending_order_items, 'pending_order_items_count': pending_order_items_count})
    
    @method_decorator(staff_required)
    def post(self, request, id):
        order_item = OrderItem.objects.get(id=id)
        order_id = order_item.order.id  # Rename id to order_id to avoid conflict
        print("Debug1")

        if 'order_item_status' in request.POST:
            order_item.status = request.POST.get('order_item_status')
            order_item.save()
            messages.success(request, 'Order item status updated successfully.')

        elif 'order_item_id' in request.POST:
            order_item.delete()
            messages.success(request, 'Order item deleted successfully.')
            
        return redirect(reverse('admin_order_item_management', kwargs={'id': order_id}))


#Admin User address management Module
class AdminCustomerProfileMangement(View):
    @method_decorator(staff_required)
    def get(self, request):
        regular_users = User.objects.exclude(is_staff=True, is_superuser=True)

        user_addresses=[]
        for user in regular_users:
            user_address = CustomUserProfile.objects.filter(user=user).first()
            if user_address:
                user_addresses.append((user, user_address))
            else:
                user_addresses.append((user, None))
        return render(request, 'admin/customer_details.html', {'regular_users': regular_users, 
                                                               'regular_users_count': regular_users.count(), 
                                                               'user_addresses':user_addresses})

    @method_decorator(staff_required)
    def post(self, request):
        if 'delete_user' in request.POST:
            user_id = request.POST.get('delete_user')
            user = get_object_or_404(User, id=user_id)
            user.delete()
            messages.success(request, 'User deleted successfully.')
        return redirect('admin_customer_datails_management')
    


        
        
    