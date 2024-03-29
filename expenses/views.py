from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required


from transactions.models import *
from transactions.filters import *



from django.core.paginator import Paginator, EmptyPage



from django.db.models.functions import Substr

from django.core.paginator import Paginator, EmptyPage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.shortcuts import render, redirect


from django.db.models import Sum

from .forms import *





@login_required(login_url='login')
def main_dashboard(request):

    if request.user.is_superuser:

        builty_count = builty.objects.all().count()
    
    else:
        builty_count = builty.objects.filter(user = request.user).count()
    
    truck_count = truck_details.objects.all().count()
    user_count = User.objects.all().count()

    queryset_data = builty.objects.filter(user = request.user, deleted = False).order_by('-id')

    builty_filters = builty_filter(request.user, request.GET, queryset=queryset_data)
    
    context = {
        
        'truck_count': truck_count,
        'builty_count': builty_count,
        'user_count': user_count,
        'form' : builty_Form(request.user),
        'builty_filter' : builty_filters,


    }
    return render(request, 'expense/main_dashboard.html', context)



def add_builty_expense(request):


    if request.method == 'POST':

        forms = builty_expense_Form(request.POST)

        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            amount = request.POST.get('amount')

            user_instance = request.user
            user_instance.balance = user_instance.balance - float(amount)
            user_instance.save()

            return redirect('list_builty_expense')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_builty_expense.html', context)

    else:

        forms = builty_expense_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_builty_expense.html', context)
    
def add_builty_expense_ajax(request):


    pass

def add_builty_expense_json(request):


    if request.method == 'POST':

        forms = builty_expense_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_builty_expense')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_builty_expense.html', context)

    else:

        forms = builty_expense_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_builty_expense.html', context)



from .filters import *

def list_builty_expense(request):
    
    
    if request.user.is_superuser:

        data = builty_expense.objects.all()

    else:

        data = builty_expense.objects.filter(user = request.user)

    builty_expense_filters = builty_expense_filter(request.GET, queryset=data)


    page = request.GET.get('page', 1)
    paginator = Paginator(builty_expense_filters.qs, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)


    context = {
        'data': data,
        'expense_builty_filter' : builty_expense_filters,

    }

    return render(request, 'expense/list_builty_expense.html', context)


def add_expense_category(request):


    if request.method == 'POST':

        forms = expense_category_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_expense_category')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_expense_category.html', context)

    else:

        forms = expense_category_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_expense_category.html', context)

        

def list_expense_category(request):
    
    data = expense_category.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(data.qs, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)



    context = {
        'data': data
    }

    return render(request, 'expense/list_expense_category.html', context)




def add_truck_expense(request):
    
    
    if request.method == 'POST':

        forms = truck_expense_Form(request.POST)

        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            amount = request.POST.get('amount')
            
            user_instance = request.user
            user_instance.balance = user_instance.balance - float(amount)
            user_instance.save()

            return redirect('list_truck_expense')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_truck_expense.html', context)

    else:

        forms = truck_expense_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_truck_expense.html', context)

    
    
def update_truck_expense(request, truck_expense_id):

    instance = truck_expense.objects.get(id = truck_expense_id)

    if request.method == 'POST':

        amount = request.POST.get("amount")

        decide = instance.amount - float(amount)

        print(decide)

        if decide > 0:

            print(1)

            user_instance = request.user
            user_instance.balance = user_instance.balance + float(decide)
            user_instance.save()

        else:
            print(2)

            user_instance = request.user
            print(user_instance.balance - float(abs(decide)))
            user_instance.balance = user_instance.balance - float(abs(decide))
            user_instance.save()

        forms = truck_expense_Form(request.POST, instance = instance)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            return redirect('list_truck_expense')
        

        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_truck_expense.html', context)

    else:

        forms = truck_expense_Form(instance = instance)


        context = {
            'form': forms,
        }
            
        return render(request, 'expense/add_truck_expense.html', context)




def delete_truck_expense(request, truck_expense_id):


    truck_expense_instance = truck_expense.objects.get(id = truck_expense_id)

    user_instance = request.user
    user_instance.balance = user_instance.balance + truck_expense_instance.amount
    user_instance.save()
    
    truck_expense_instance.deleted = True
    truck_expense_instance.save()

    return redirect('list_truck_expense')
    
    
def list_truck_expense(request):
    
    if request.user.is_superuser:

        data = truck_expense.objects.all()

    else:

        data = truck_expense.objects.filter(user = request.user)

    truck_expense_filters = truck_expense_filter(request.GET, queryset=data)

    filter_data = truck_expense_filters.qs

    total_amount = filter_data.aggregate(total_amount=Sum('amount'))['total_amount']

    page = request.GET.get('page', 1)
    paginator = Paginator(truck_expense_filters.qs, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)


    context = {
        'data': data,
        'total_amount': total_amount,
        'truck_expense_filters' : truck_expense_filters
    }

    return render(request, 'expense/list_truck_expense.html', context)




def list_delete(request):

    builty_expense.objects.all().delete()
    truck_expense.objects.all().delete()
    transfer_fund.objects.all().delete()
    diesel_expense.objects.all().delete()
    truck_diesel_expense.objects.all().delete()
    other_expense.objects.all().delete()
    salary.objects.all().delete()
    fund.objects.all().delete()

    a = User.objects.all()

    for i in a:

        i.balance = 0.0
        i.save()

    
    

    
def add_diesel_rate(request):
    
    instance = diesel_rate.objects.get(id = 1)

    rate_data = request.POST.get('rate')

    instance.amount = rate_data
    instance.save()

    return redirect('list_diesel_expense')



def add_transfer_fund(request):
    
    
    if request.method == 'POST':

        forms = transfer_fund_Form(request.POST)

        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            amount = request.POST.get('amount')
            transfer_to_user = request.POST.get('transfer_to_user')
            user_instance = request.user
            user_instance.balance = user_instance.balance - float(amount)
            user_instance.save()

            user_instance1 = User.objects.get(id = transfer_to_user)
            user_instance1.balance = user_instance1.balance + float(amount)
            user_instance1.save()


            return redirect('list_transfer_fund')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_transfer_fund.html', context)

    else:

        forms = transfer_fund_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_transfer_fund.html', context)



def update_transfer_fund(request, transfer_fund_id):

    instance = transfer_fund.objects.get(id = transfer_fund_id)

    if request.method == 'POST':
        
        amount = request.POST.get('amount')

        decide = instance.amount - float(amount)

        print(decide)

        if decide > 0:

            print(1)

            user_instance = request.user
            user_instance.balance = user_instance.balance + float(decide)
            user_instance.save()

        else:
            print(2)

            user_instance = request.user
            print(user_instance.balance - float(abs(decide)))
            user_instance.balance = user_instance.balance - float(abs(decide))
            user_instance.save()

        forms = transfer_fund_Form(request.POST, instance = instance)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            transfer_to_user = request.POST.get('transfer_to_user')
            
            user_instance = request.user
            user_instance.balance = user_instance.balance - float(amount)
            user_instance.save()

            user_instance = request.user
            user_instance.balance = user_instance.balance + float(transfer_to_user)
            user_instance.save()

            return redirect('list_transfer_fund')
        

        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_transfer_fund.html', context)

    else:

        forms = transfer_fund_Form(instance = instance)


        context = {
            'form': forms,
        }
            
        return render(request, 'expense/add_transfer_fund.html', context)




def delete_transfer_fund(request, transfer_fund_id):


    transfer_fund_instance = transfer_fund.objects.get(id = transfer_fund_id)
    transfer_fund_instance.deleted = True
    transfer_fund_instance.save()

    return redirect('list_transfer_fund')




    
    
def list_transfer_fund(request):
    
    if request.user.is_superuser:

            data = transfer_fund.objects.all()

    else:

        data = transfer_fund.objects.filter(user = request.user)

    transfer_fund_filters = transfer_fund_filter(request.GET, queryset=data)

    filter_data = transfer_fund_filters.qs

    total_amount = filter_data.aggregate(total_amount=Sum('amount'))['total_amount']
     

    page = request.GET.get('page', 1)
    paginator = Paginator(transfer_fund_filters.qs, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)


    context = {
        'data': data,
        'total_amount': total_amount,
        'transfer_fund_filter' : transfer_fund_filters
    }

    return render(request, 'expense/list_transfer_fund.html', context)
    

def list_all_transfer_fund(request):
    
    data = transfer_fund.objects.all()

    context = {
        'data': data
    }

    return render(request, 'expense/list_all_transfer_fund.html', context)



def add_diesel_expense(request):
    
    
    if request.method == 'POST':

        forms = diesel_expense_Form(request.POST)

        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()
            return redirect('list_diesel_expense')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_diesel_expense.html', context)

    else:

        forms = diesel_expense_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_diesel_expense.html', context)

        

        
def update_diesel_expense(request, diesel_expense_id):

    instance = diesel_expense.objects.get(id = diesel_expense_id)

    if request.method == 'POST':

        forms = diesel_expense_Form(request.POST, instance = instance)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            return redirect('list_diesel_expense')
        

        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_diesel_expense.html', context)

    else:

        forms = diesel_expense_Form(instance = instance)


        context = {
            'form': forms,
        }
            
        return render(request, 'expense/add_diesel_expense.html', context)




def delete_diesel_expense(request, diesel_expense_id):


    diesel_expense_instance = diesel_expense.objects.get(id = diesel_expense_id)
    diesel_expense_instance.deleted = True
    diesel_expense_instance.save()

    return redirect('list_diesel_expense')



def list_diesel_expense(request):
    
    if request.user.is_superuser:

        data = diesel_expense.objects.all()

    else:

        data = diesel_expense.objects.filter(user = request.user)

    rate = diesel_rate.objects.get(id=1)
    
    diesel_expense_filters = diesel_expense_filter(request.GET, queryset=data)

    filter_data = diesel_expense_filters.qs

    total_amount = filter_data.aggregate(total_amount=Sum('amount'))['total_amount']
     
    page = request.GET.get('page', 1)
    paginator = Paginator(diesel_expense_filters.qs, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)



    context = {
        'data': data,  # Pass the filtered queryset
        'rate': rate.amount,
        'total_amount': total_amount,
        'diesel_expense_filter': diesel_expense_filters,  # If you need the filter form
    }

    return render(request, 'expense/list_diesel_expense.html', context)



def add_truck_diesel_expense(request):
    
    
    if request.method == 'POST':

        forms = truck_diesel_expense_Form(request.POST)

        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()
            return redirect('list_truck_diesel_expense')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_truck_diesel_expense.html', context)

    else:

        forms = truck_diesel_expense_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_truck_diesel_expense.html', context)

        

        
def update_truck_diesel_expense(request, truck_diesel_expense_id):

    instance = truck_diesel_expense.objects.get(id = truck_diesel_expense_id)

    if request.method == 'POST':

        forms = truck_diesel_expense_Form(request.POST, instance = instance)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            return redirect('list_truck_diesel_expense')
        

        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_truck_diesel_expense.html', context)

    else:

        forms = truck_diesel_expense_Form(instance = instance)


        context = {
            'form': forms,
        }
            
        return render(request, 'expense/add_truck_diesel_expense.html', context)




def delete_truck_diesel_expense(request, truck_diesel_expense_id):


    truck_diesel_expense_instance = truck_diesel_expense.objects.get(id = truck_diesel_expense_id)
    truck_diesel_expense_instance.deleted = True
    truck_diesel_expense_instance.save()

    return redirect('list_truck_diesel_expense')




def list_truck_diesel_expense(request):
    
    rate = diesel_rate.objects.get(id=1)

    if request.user.is_superuser:

            data = truck_diesel_expense.objects.all()

    else:

        data = truck_diesel_expense.objects.filter(user = request.user)

    truck_diesel_expense_filters = truck_diesel_expense_filter(request.GET, queryset=data)

    filter_data = truck_diesel_expense_filters.qs

    total_amount = filter_data.aggregate(total_amount=Sum('amount'))['total_amount']
    

    page = request.GET.get('page', 1)
    paginator = Paginator(truck_diesel_expense_filters.qs, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)




    context = {
        'data': truck_diesel_expense_filters.qs,  # Pass the filtered queryset
        'rate': rate.amount,
        'total_amount': total_amount,
        'truck_diesel_expense_filter': truck_diesel_expense_filters,  # If you need the filter form
    }

    return render(request, 'expense/list_truck_diesel_expense.html', context)



def add_employee(request):
    
    
    if request.method == 'POST':

        forms = employee_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_employee')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_employee.html', context)

    else:

        forms = employee_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_employee.html', context)

        

def update_employee(request, employee_id):
    
    instance = employee.objects.get(id = employee_id)
    
    if request.method == 'POST':

        forms = employee_Form(request.POST, instance = instance)

        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            amount = request.POST.get('amount')
            
            user_instance = request.user
            user_instance.balance = user_instance.balance - float(amount)
            user_instance.save()



            return redirect('list_employee')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_employee.html', context)

    else:

        forms = employee_Form(instance = instance)

        context = {
            'form': forms
        }
        return render(request, 'expense/add_employee.html', context)

        
def delete_employee(request, employee_id):


    employee_instance = employee.objects.get(id = employee_id)
    employee_instance.deleted = True
    employee_instance.save()

    return redirect('list_employee')

    
    
def list_employee(request):
    
    data = employee.objects.all()



    page = request.GET.get('page', 1)
    paginator = Paginator(data, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)



    context = {
        'data': data
    }

    return render(request, 'expense/list_employee.html', context)





def add_salary(request):
    
    
    if request.method == 'POST':

        forms = salary_Form(request.POST)

        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            amount = request.POST.get('salary')
            
            user_instance = request.user
            user_instance.balance = user_instance.balance - float(amount)
            user_instance.save()
            
            return redirect('list_salary')


        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_salary.html', context)

    else:

        forms = salary_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_salary.html', context)

        

        
def update_salary(request, salary_id):

    instance = salary.objects.get(id = salary_id)

    if request.method == 'POST':

        amount = request.POST.get("salary")

        decide = instance.salary - float(amount)

        print(decide)

        if decide > 0:

            print(1)

            user_instance = request.user
            user_instance.balance = user_instance.balance + float(decide)
            user_instance.save()

        else:
            print(2)

            user_instance = request.user
            print(user_instance.balance - float(abs(decide)))
            user_instance.balance = user_instance.balance - float(abs(decide))
            user_instance.save()

        forms = salary_Form(request.POST, instance = instance)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            return redirect('list_salary')
        

        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_salary.html', context)

    else:

        forms = salary_Form(instance = instance)


        context = {
            'form': forms,
        }
            
        return render(request, 'expense/add_salary.html', context)




def delete_salary(request, salary_id):


    salary_instance = salary.objects.get(id = salary_id)

    user_instance = request.user
    user_instance.balance = user_instance.balance + salary_instance.amount
    user_instance.save()

    salary_instance.deleted = True
    salary_instance.save()

    return redirect('list_salary')
    
    
def list_salary(request):
    

    if request.user.is_superuser:

            data = salary.objects.all()

    else:

        data = salary.objects.filter(user = request.user)

    salary_filters = salary_filter(request.GET, queryset=data)

    filter_data = salary_filters.qs

    total_amount = filter_data.aggregate(total_amount=Sum('salary'))['total_amount']

    page = request.GET.get('page', 1)
    paginator = Paginator(salary_filters.qs, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)



    context = {
        'data': data,
        'total_amount': total_amount,
        'salary_filter' : salary_filters
    }

    return render(request, 'expense/list_salary.html', context)


def add_other_expense(request):
    
    
    if request.method == 'POST':

        forms = other_expense_Form(request.POST)

        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            amount = request.POST.get('amount')
            
            user_instance = request.user
            user_instance.balance = user_instance.balance - float(amount)
            user_instance.save()



            return redirect('list_other_expense')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_other_expense.html', context)

    else:

        forms = other_expense_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_other_expense.html', context)

        

def update_other_expense(request, other_expense_id):

    instance = other_expense.objects.get(id = other_expense_id)

    if request.method == 'POST':

        amount = request.POST.get("amount")

        decide = instance.amount - float(amount)

        print(decide)

        if decide > 0:

            print(1)

            user_instance = request.user
            user_instance.balance = user_instance.balance + float(decide)
            user_instance.save()

        else:
            print(2)

            user_instance = request.user
            print(user_instance.balance - float(abs(decide)))
            user_instance.balance = user_instance.balance - float(abs(decide))
            user_instance.save()

        forms = other_expense_Form(request.POST, instance = instance)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            return redirect('list_other_expense')
        

        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_other_expense.html', context)

    else:

        forms = other_expense_Form(instance = instance)


        context = {
            'form': forms,
        }
            
        return render(request, 'expense/add_other_expense.html', context)




def delete_other_expense(request, other_expense_id):


    other_expense_instance = other_expense.objects.get(id = other_expense_id)

    user_instance = request.user
    user_instance.balance = user_instance.balance + other_expense_instance.amount
    user_instance.save()

    other_expense_instance.deleted = True
    other_expense_instance.save()

    return redirect('list_other_expense')
    
    
def list_other_expense(request):
    
    data = other_expense.objects.all()


    if request.user.is_superuser:

        data = other_expense.objects.all()

    else:

        data = other_expense.objects.filter(user = request.user)

    
    
    other_expense_filters = other_expense_filter(request.GET, queryset=data)
    
    filter_data = other_expense_filters.qs

    total_amount = filter_data.aggregate(total_amount=Sum('amount'))['total_amount']

    page = request.GET.get('page', 1)
    paginator = Paginator(other_expense_filters.qs, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)


    



    context = {
        'data': data,
        'total_amount': total_amount,
        'other_expense_filter' : other_expense_filters
    }

    return render(request, 'expense/list_other_expense.html', context)


def add_fund_admin(request):
    
    
    if request.method == 'POST':

        forms = fund_Form(request.POST)

        user_id = request.POST.get('user')
        amount = request.POST.get('amount')

        user_instance = request.user
        user_instance.balance = user_instance.balance - float(amount)
        user_instance.save()

        user_instance = User.objects.get(id = user_id)

        user_instance.balance = user_instance.balance + float(amount)

        user_instance.save()

        if forms.is_valid():
            forms.save()
            return redirect('list_fund')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_fund.html', context)

    else:

        forms = fund_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_fund_admin.html', context)

        

def update_fund_admin(request, fund_admin_id):

    instance = fund.objects.get(id = fund_admin_id)

    if request.method == 'POST':

        amount = request.POST.get("amount")

        decide = instance.amount - float(amount)

        print(decide)

        if decide > 0:

            print(1)

            user_instance = request.user
            user_instance.balance = user_instance.balance + float(decide)
            user_instance.save()

        else:
            print(2)

            user_instance = request.user
            print(user_instance.balance - float(abs(decide)))
            user_instance.balance = user_instance.balance - float(abs(decide))
            user_instance.save()

        forms = fund_Form(request.POST, instance = instance)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            return redirect('list_fund')
        

        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_fund_admin.html', context)

    else:

        forms = fund_Form(instance = instance)


        context = {
            'form': forms,
        }
            
        return render(request, 'expense/add_fund_admin.html', context)




def delete_fund_admin(request, fund_admin_id):


    fund_instance = fund.objects.get(id = fund_admin_id)

    user_instance_fund_add = User.objects.get(id = fund_instance.user)
    
    user_instance_fund_add = user_instance_fund_add.balance - fund_instance.amount
    user_instance_fund_add.save()

    fund_instance.deleted = True
    fund_instance.save()

    return redirect('list_fund_admin')
    
    
def list_fund_admin(request):
    
    data = fund.objects.all()

    fund_filters = fund_filter(request.GET, queryset=data)

    filter_data = fund_filters.qs

    total_amount = filter_data.aggregate(total_amount=Sum('amount'))['total_amount']

    page = request.GET.get('page', 1)
    paginator = Paginator(fund_filters.qs, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)




    context = {
        'data': data,
        'total_amount': total_amount,
        'fund_filter' : fund_filters
    }

    return render(request, 'expense/list_fund_admin.html', context)


def add_fund(request):
    
    
    if request.method == 'POST':


        amount = request.POST.get('amount')

        user_instance = request.user


        user_instance.balance = user_instance.balance + float(amount)

        user_instance.save()

        updated_request = request.POST.copy()
        updated_request.update({'user': user_instance})
        forms = fund_Form(updated_request)

        if forms.is_valid():

            


            forms.save()
            return redirect('list_fund')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_fund.html', context)

    else:

        forms = fund_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_fund.html', context)

        
def update_fund(request, fund_id):

    instance = fund.objects.get(id = fund_id)

    if request.method == 'POST':

        amount = request.POST.get("amount")

        decide = instance.amount - float(amount)

        print(decide)

        if decide > 0:

            print(1)

            user_instance = request.user
            user_instance.balance = user_instance.balance + float(decide)
            user_instance.save()

        else:
            print(2)

            user_instance = request.user
            print(user_instance.balance - float(abs(decide)))
            user_instance.balance = user_instance.balance - float(abs(decide))
            user_instance.save()

        forms = fund_Form(request.POST, instance = instance)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()

            return redirect('list_fund')
        

        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_fund.html', context)

    else:

        forms = fund_Form(instance = instance)


        context = {
            'form': forms,
        }
            
        return render(request, 'expense/add_fund.html', context)




def delete_fund(request, fund_id):


    fund_instance = fund.objects.get(id = fund_id)

    
    user_instance_fund_add = User.objects.get(id = fund_instance.user)
    
    user_instance_fund_add = user_instance_fund_add.balance - fund_instance.amount
    user_instance_fund_add.save()

    fund_instance.deleted = True
    fund_instance.save()

    return redirect('list_fund')

    
    
def list_fund(request):
    

    data = fund.objects.all()


    if request.user.is_superuser:

                data = fund.objects.all()

    else:

        data = fund.objects.filter(user = request.user)

    
    
    fund_filters = fund_filter(request.GET, queryset=data)

    filter_data = fund_filters.qs

    total_amount = filter_data.aggregate(total_amount=Sum('amount'))['total_amount']

    page = request.GET.get('page', 1)
    paginator = Paginator(fund_filters.qs, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)



    context = {
        'data': data,
        'total_amount': total_amount,
        'fund_filter' : fund_filters
    }

    return render(request, 'expense/list_fund.html', context)

