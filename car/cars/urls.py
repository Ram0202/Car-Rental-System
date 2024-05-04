from django.urls import path
from . import views
from .views import logouts


urlpatterns = [
    path("", views.admin_login, name="admin_login"),
    path("user_login/", views.user_login, name="user_login"),
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("available_cars/", views.available_cars, name="available_cars"),
    path("car_details/<int:car_id>/", views.car_details, name="car_details"),
    path('bookings/<int:car_id>/<int:user_id>/', views.bookings, name='bookings'),
    path('feedback/<int:user_id>/', views.feedback, name='feedback'),
    path("add_cars/", views.add_cars, name="add_cars"),
    path("car_list/", views.car_list, name="car_list"),
    path("view_bookings/", views.view_bookings, name="view_bookings"),
    path("view_feedback/", views.view_feedback, name="view_feedback"),
    path("logout/", logouts, name="logout"),
]