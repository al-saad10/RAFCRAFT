from django.shortcuts import render ,get_object_or_404
from django.http import JsonResponse
from django.views.generic import View
from .models import *


class ShopView(View):
    def get(self,request):
        categories = Category.objects.all()
        sub_categories = SubCategory.objects.all()
        products = Product.objects.all()
        return render(request , "products/shop.html" , {'sub_categories':sub_categories,'categories':categories,'products':products})
    
class DetailProductView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product_images = ProductImage.objects.filter(product=product)
        inventory = Inventory.objects.filter(product=product).first()
        colors = Color.objects.filter(product=product)
        
        # Fetch products within the specified price range
        min_price = product.discounted_price - 5000  # Example: Lower bound of the price range
        max_price = product.discounted_price + 5000  # Example: Upper bound of the price range
        similar_products = Product.objects.filter(discounted_price__range=(min_price, max_price))[:4]
        
        return render(request, "products/product.html", {
            "product": product,
            "product_images": product_images,
            "inventory": inventory,
            "colors": colors,
            "similar_products": similar_products  
        })


class CategoryView(View):
    def get(self, request):
        all_categories = Category.objects.all()
        all_category_product = []

        for category in all_categories:
            products_for_category = Product.objects.filter(category=category)
            subcategories_for_category = category.subcategories.all()
            product_images_for_category = []

            for product in products_for_category:
                first_image_for_product = ProductImage.objects.filter(product=product).first()
                product_images_for_category.append((product, first_image_for_product))

            all_category_product.append({
                'category': category,
                'products': products_for_category,
                'subcategories': subcategories_for_category,
                'product_images': product_images_for_category
            })

        return render(request, "products/shop.html", {"all_category_product": all_category_product})
    

class EachCategoryView(View):
    def get(self, request, category):
        categories = Category.objects.all()
        sub_categories = SubCategory.objects.all()
        category_instance = get_object_or_404(Category, name=category)
        products_with_images = []

        for product in Product.objects.filter(category=category_instance):
            first_image = ProductImage.objects.filter(product=product).first()
            products_with_images.append((product, first_image))

        return render(request, "products/extend_category.html", {"products_with_images": products_with_images,
                                                                  "category_instance": category_instance,
                                                                  'sub_categories':sub_categories,
                                                                  'categories':categories,})
    
    
class EachSubCategoryView(View):
    def get(self, request, subcategory):
        categories = Category.objects.all()
        sub_categories = SubCategory.objects.all()

        subcategory_instance = get_object_or_404(SubCategory, name=subcategory)
        products_with_images = []

        for product in Product.objects.filter(subcategory=subcategory_instance):
            first_image = ProductImage.objects.filter(product=product).first()
            products_with_images.append((product, first_image))

        return render(request, "products/extend_subcategory.html", {"products_with_images": products_with_images,
                                                                     "subcategory_instance": subcategory_instance,
                                                                     'sub_categories':sub_categories,'categories':categories,})


class EventView(View):
    def get(self, request, event):
        event_instance = get_object_or_404(SliderItem, event=event)
        products_with_images = []

        for product in Product.objects.filter(event=event_instance):
            first_image = ProductImage.objects.filter(product=product).first()
            products_with_images.append((product, first_image))

        return render(request, "products/event.html", {"products_with_images": products_with_images, "event_instance": event_instance})