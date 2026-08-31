from django.urls import path
from Tracker import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),
    path('home/', views.home, name='home'),
    path('expense_form/', views.expense_form, name='expense_form'),
    path('view_expense/<int:expense_id>/', views.view_expense, name='view_expense'), 
    path('view_form/', views.view_form, name='view_form'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('update_expense/<int:expense_id>/', views.update_expense, name='update_expense'),
]
