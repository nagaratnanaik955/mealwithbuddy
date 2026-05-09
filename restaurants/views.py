from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Restaurant
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

@login_required
def user_home(request):
    return render(request, 'restaurants/user_home.html')

@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('view_restaurants')
    return render(request, 'restaurants/dashboard.html')

def is_admin(user):
    return user.is_superuser

@login_required
def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        cuisine_type = request.POST.get('cuisine_type')
        meal_name = request.POST.get('meal_name')
        cost = request.POST.get('cost')
        rating = request.POST.get('rating')
        logo_url = request.POST.get('logo_url')
        is_veg = request.POST.get('is_veg') == 'on'
        
        if name and location and cuisine_type and meal_name and cost and rating:
            Restaurant.objects.create(
                name=name,
                location=location,
                cuisine_type=cuisine_type,
                meal_name=meal_name,
                cost=cost,
                rating=rating,
                is_veg=is_veg,
                logo_url=logo_url if logo_url else "https://cdn-icons-png.flaticon.com/512/1996/1996055.png"
            )
            messages.success(request, "Restaurant added successfully!")
            return redirect('manage_restaurants')
        else:
            messages.error(request, "All fields are required.")
            
    return render(request, 'restaurants/add_restaurant.html')

from django.db.models import Avg, Max

@login_required
def view_restaurants(request):
    restaurants_data = Restaurant.objects.values('name').annotate(
        avg_rating=Avg('rating'),
        logo=Max('logo_url'), 
        cuisine=Max('cuisine_type')
    )
    restaurants = []
    for item in restaurants_data:
        restaurants.append({
            'name': item['name'],
            'avg_rating': item['avg_rating'],
            'logo_url': item['logo'],
            'cuisine_type': item['cuisine']
        })
    return render(request, 'restaurants/user_restaurants.html', {'restaurants': restaurants})

@login_required
@user_passes_test(is_admin, login_url='view_restaurants')
def manage_restaurants(request):
    restaurants_data = Restaurant.objects.values('name').annotate(
        avg_rating=Avg('rating'),
        logo=Max('logo_url'), 
        cuisine=Max('cuisine_type')
    )
    restaurants = []
    for item in restaurants_data:
        restaurants.append({
            'name': item['name'],
            'avg_rating': item['avg_rating'],
            'logo_url': item['logo'],
            'cuisine_type': item['cuisine']
        })
    return render(request, 'restaurants/admin_restaurants.html', {'restaurants': restaurants})

@login_required
def view_menu(request, restaurant_name):
    items = Restaurant.objects.filter(name=restaurant_name)
    return render(request, 'restaurants/user_menu.html', {'items': items, 'restaurant_name': restaurant_name})

@login_required
@user_passes_test(is_admin, login_url='view_menu')
def manage_menu(request, restaurant_name):
    items = Restaurant.objects.filter(name=restaurant_name)
    return render(request, 'restaurants/admin_menu.html', {'items': items, 'restaurant_name': restaurant_name})

@login_required
def add_to_cart(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    cart = request.session.get('cart', [])
    
    # Add item to cart
    cart.append({
        'id': restaurant.id,
        'name': restaurant.meal_name,
        'description': restaurant.description,
        'price': float(restaurant.cost),
        'image': restaurant.image_url
    })
    
    request.session['cart'] = cart
    messages.success(request, f"{restaurant.meal_name} added to cart!")
    return redirect('view_cart', username=request.user.username)

@login_required
def view_cart(request, username):
    cart = request.session.get('cart', [])
    total_price = sum(item['price'] for item in cart)
    return render(request, 'restaurants/cart.html', {
        'cart': cart,
        'total_price': total_price,
        'username': username
    })

@login_required
def delete_restaurant(request, restaurant_name):
    Restaurant.objects.filter(name=restaurant_name).delete()
    messages.success(request, f"Restaurant '{restaurant_name}' deleted successfully.")
    return redirect('manage_restaurants')

@login_required
def edit_restaurant(request, restaurant_name):
    restaurants = Restaurant.objects.filter(name=restaurant_name)
    first_item = restaurants.first()
    
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_cuisine = request.POST.get('cuisine_type')
        new_logo = request.POST.get('logo_url')
        
        # Update all items belonging to this restaurant name
        restaurants.update(
            name=new_name,
            cuisine_type=new_cuisine,
            logo_url=new_logo
        )
        messages.success(request, "Restaurant info updated successfully!")
        return redirect('manage_restaurants')
        
    return render(request, 'restaurants/edit_restaurant.html', {'restaurant': first_item})

@login_required
def delete_menu_item(request, item_id):
    item = Restaurant.objects.get(id=item_id)
    name = item.name
    item.delete()
    messages.success(request, "Item deleted successfully.")
    return redirect('view_menu', restaurant_name=name)

@login_required
def edit_menu_item(request, item_id):
    item = Restaurant.objects.get(id=item_id)
    if request.method == 'POST':
        item.meal_name = request.POST.get('meal_name')
        item.description = request.POST.get('description')
        item.cost = request.POST.get('cost')
        item.image_url = request.POST.get('image_url')
        item.is_veg = request.POST.get('is_veg') == 'on'
        item.save()
        messages.success(request, "Menu item updated successfully!")
        return redirect('view_menu', restaurant_name=item.name)
        
    return render(request, 'restaurants/edit_menu_item.html', {'item': item})

@login_required
def add_menu_item(request, restaurant_name):
    # Get the existing restaurant details to pre-fill info like location/cuisine if needed
    base_restaurant = Restaurant.objects.filter(name=restaurant_name).first()
    
    if request.method == 'POST':
        meal_name = request.POST.get('meal_name')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        image_url = request.POST.get('image_url')
        is_veg = request.POST.get('is_veg') == 'on'
        
        Restaurant.objects.create(
            name=restaurant_name,
            location=base_restaurant.location if base_restaurant else "Default",
            cuisine_type=base_restaurant.cuisine_type if base_restaurant else "Default",
            logo_url=base_restaurant.logo_url if base_restaurant else "",
            meal_name=meal_name,
            description=description,
            cost=cost,
            image_url=image_url,
            is_veg=is_veg,
            rating=5.0
        )
        messages.success(request, f"New item added to {restaurant_name}!")
        return redirect('view_menu', restaurant_name=restaurant_name)
        
    return render(request, 'restaurants/add_menu_item.html', {'restaurant_name': restaurant_name})

@login_required
def checkout(request, username):
    return render(request, 'restaurants/checkout.html', {'username': username})

