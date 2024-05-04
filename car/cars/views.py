from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import CustomUser, Car, Book, Feedback
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        
        user = User.objects.create_user(username=username, password=password)

        custom_user = CustomUser.objects.create(user=user, email=email, phone=phone, age=age, gender=gender)
        
        messages.success(request, 'Signup successful. Please log in.')

        return redirect('user_login')
    return render(request, 'signup.html')
    

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'user_login.html')
    

def home(request):
    return render(request, "home.html")
    
    
def available_cars(request):
    cars = Car.objects.all()
    return render(request, "available_cars.html", {"cars": cars})
    
    
def car_details(request, car_id):
    car = Car.objects.get(id=car_id)
    return render(request, "car_details.html", {"car": car})
    
    
def bookings(request, car_id, user_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    try:
        car = Car.objects.get(id=car_id)
        custom_user = CustomUser.objects.get(user=request.user)
    except (Car.DoesNotExist, CustomUser.DoesNotExist):
        return render(request, "bookings.html")

    if request.method == 'POST':
        address = request.POST.get('address')
        messages.success(request, 'Car booked successfully.')
        Book.objects.create(car=car, user=custom_user, address=address)
        return redirect("/available_cars")

    return render(request, "bookings.html", {'car': car, 'user': custom_user})

    
def feedback(request, user_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    try:
        custom_user = CustomUser.objects.get(user=request.user)
    except CustomUser.DoesNotExist:
        return render(request, "feedback.html")

    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        messages.success(request, 'Thank you for your feedback.')
        Feedback.objects.create(user=custom_user, feedback=feedback)
        
        feedback = f"/feedback/{custom_user.id}/"
        return redirect(feedback)

    return render(request, "feedback.html", {'user': custom_user})


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('add_cars')
        else:
            messages.error(request, 'Invalid Credentials or You are not an admin.')
    return render(request, 'admin_login.html')
    
    
def add_cars(request):
    if request.method == 'POST':
        model = request.POST['model']
        year = request.POST['year']
        color = request.POST['color']
        price = request.POST['price']
        image = request.FILES['image']
        
        messages.success(request, 'Car added successfully.')
        
        Car(model=model, year=year, color=color, price=price, image=image).save()
        
    return render(request, 'add_cars.html')
    
    
def car_list(request):
    cars = Car.objects.all()
    return render(request, 'car_list.html', {"cars": cars})
    
    
def view_bookings(request):
    if not request.user.is_superuser:
        return redirect("/admin_login")

    bookings = Book.objects.select_related('user', 'car').all()

    return render(request, "view_bookings.html", {"bookings": bookings})
    
    
def view_feedback(request):
    if not request.user.is_superuser:
        return redirect("/admin_login")

    feedback = Feedback.objects.all()

    return render(request, "view_feedback.html", {"feedback": feedback})
    
    
def logouts(request):
    logout(request)
    return redirect("admin_login")