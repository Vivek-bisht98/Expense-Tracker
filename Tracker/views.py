from itertools import count

from django.shortcuts import render,redirect
from .models import Expense 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 
from django.db.models import Sum,Count,Max,Avg
from django.core import paginator
from django.core.paginator import Paginator


# Create your views here.
@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    search = request.GET.get('search')
    if search:
        expenses = Expense.objects.filter(title__icontains=search, user=request.user).order_by('-date')
    dashboard = Expense.objects.filter(user=request.user).aggregate(total_amount=Sum('amount'), total_expenses=Count('id'), max_amount=Max('amount'), avg_amount=Avg('amount'))
    count = Expense.objects.filter(user=request.user).values('category').annotate(money=Sum('amount'))
    category_totals = { "food": 0,
        "transportation": 0,
        "entertainment": 0,
        "rent": 0,
        "other": 0,}

    for item in count:
        category_totals[item["category"]] = item["money"]
    pagination = Paginator(expenses, 5)
    page_number = request.GET.get("page")
    page_obj = pagination.get_page(page_number)
    return render(request, 'home.html', {'expenses': expenses, 'dashboard': dashboard, 'count': category_totals, 'page_obj': page_obj })

@login_required
def expense_form(request):
    if request.method == 'POST':
        title = request.POST.get('expense_name')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        category = request.POST.get('category')
        payment = request.POST.get('payment')
        description = request.POST.get('description')
        expense = Expense(user=request.user, title=title, amount=amount, date=date, category=category, payment=payment, description=description)
        expense.save()
        return redirect('home')
        
    return render(request, 'expense_form.html')

@login_required
def view_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)
    return render(request, 'view_expense.html', {'expense': expense})

@login_required
def view_form(request):

    category = request.GET.get("category")

    expenses = Expense.objects.filter(user=request.user, category=category).order_by("-date")
    pagination = Paginator(expenses, 5)
    page_number = request.GET.get("page")
    page_obj = pagination.get_page(page_number)


    return render(
        request,
        "view_form.html",
        {
            "expenses": expenses,
            "page_obj": page_obj
        }
    )

@login_required
def delete_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)
    expense.delete()
    return redirect('home')

@login_required
def update_expense(request, expense_id):
    expense = Expense.objects.get(user=request.user, id=expense_id)

    if request.method == 'POST':
        expense.title = request.POST.get('expense_name')
        expense.amount = request.POST.get('amount')
        expense.date = request.POST.get('date')
        expense.category = request.POST.get('category')
        expense.payment = request.POST.get('payment')
        expense.description = request.POST.get('description')
        expense.save()
        return redirect('home')

    return render(request, 'update_expense.html', {'expense': expense})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            return render(request, 'registration.html', {'error': 'Username already exists'})
        User.objects.create_user(username=username, password=password, email=email)
        return redirect('login_user')
    return render(request, 'registration.html')

def logout_user(request):
    logout(request)
    return redirect('login_user')