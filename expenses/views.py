from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib import messages


from transactions.models import *
from transactions.filters import *



from django.core.paginator import Paginator, EmptyPage



from django.db.models.functions import Substr

from django.core.paginator import Paginator, EmptyPage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.shortcuts import render, redirect
from django.urls import reverse


from django.db.models import Sum

from .forms import *


import copy




@login_required(login_url='login')
def main_dashboard(request):

    if request.user.is_superuser:

        builty_count = builty.objects.all().count()
    
    else:
        builty_count = builty.objects.filter(user = request.user).count()
    
    truck_count = truck_details.objects.all().count()
    user_count = User.objects.all().count()

    queryset_data = builty.objects.filter(user = request.user, deleted = False).order_by('-id')

    builty_filters = builty_filter(request.user, request.GET, queryset=queryset_data, request=request)
    
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

        data = builty_expense.objects.all().order_by('-id')

    else:

        data = builty_expense.objects.filter(user = request.user).order_by('-id')

    builty_expense_filters = builty_expense_filter(request.GET, queryset=data)

    filter_data = builty_expense_filters.qs

    total_amount = filter_data.aggregate(total_amount=Sum('amount'))['total_amount']

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
        'total_amount': total_amount,
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

        

def update_expense_category(request, expense_category_id):

    instance = expense_category.objects.get(id = expense_category_id)

    if request.method == 'POST':

        forms = expense_category_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_expense_category')
        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_expense_category.html', context)

    else:

        forms = expense_category_Form(instance = instance)

        context = {
            'form': forms
        }
        return render(request, 'expense/add_expense_category.html', context)

        

def list_expense_category(request):
    
    data = expense_category.objects.all().order_by('-id')

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

    return render(request, 'expense/list_expense_category.html', context)




def add_truck_expense(request):
    
    
    if request.method == 'POST':
        # Bulk submit: one truck, multiple expense rows
        from django.db import transaction

        forms = truck_expense_Form(request.POST, request=request)  # used only to re-render selects consistently on error

        truck_id = request.POST.get('truck')
        if not truck_id:
            messages.error(request, 'Truck is required')
            return render(request, 'expense/add_truck_expense.html', {'form': forms})

        # Row fields come as lists
        expense_types = request.POST.getlist('expense_type[]')
        tyre_nos = request.POST.getlist('tyre_no[]')
        patterns = request.POST.getlist('pattern[]')
        types = request.POST.getlist('type[]')
        companies = request.POST.getlist('company[]')
        driver_ids = request.POST.getlist('driver[]')
        mechanic_ids = request.POST.getlist('mechanic[]')
        mechanic_names = request.POST.getlist('mechanic_name[]')
        spare_part_names = request.POST.getlist('spare_part_name[]')
        labour_costs = request.POST.getlist('labour_cost[]')
        costs = request.POST.getlist('cost[]')
        work_descriptions = request.POST.getlist('work_description[]')
        vendor_ids = request.POST.getlist('vendor[]')
        amounts = request.POST.getlist('amount[]')
        notes = request.POST.getlist('note[]')
        entry_dates = request.POST.getlist('entry_date[]')

        row_count = max(
            len(expense_types),
            len(amounts),
            len(notes),
            len(vendor_ids),
            0
        )

        created = 0
        total_amount = 0.0

        def _get(lst, idx, default=''):
            try:
                return lst[idx]
            except Exception:
                return default

        with transaction.atomic():
            truck_obj = truck_details.objects.get(id=truck_id)

            for i in range(row_count):
                exp_type = (_get(expense_types, i) or 'other').strip()
                amount_raw = (_get(amounts, i) or '').strip()

                # Skip empty rows
                if not exp_type and not amount_raw:
                    continue
                if not amount_raw:
                    # allow mechanic auto-calc to fill, but if still empty -> skip row
                    continue

                try:
                    amount_val = float(amount_raw)
                except Exception:
                    continue

                vendor_id = (_get(vendor_ids, i) or '').strip()
                driver_id = (_get(driver_ids, i) or '').strip()
                mechanic_id = (_get(mechanic_ids, i) or '').strip()

                te = truck_expense(
                    truck=truck_obj,
                    expense_type=exp_type,
                    tyre_no=(_get(tyre_nos, i) or '').strip() or None,
                    pattern=(_get(patterns, i) or '').strip() or None,
                    type=(_get(types, i) or '').strip() or None,
                    company=(_get(companies, i) or '').strip() or None,
                    spare_part_name=(_get(spare_part_names, i) or '').strip() or None,
                    work_description=(_get(work_descriptions, i) or '').strip() or None,
                    note=(_get(notes, i) or '').strip() or None,
                    user=request.user,
                    amount=amount_val,
                )

                # Optional numeric fields
                labour_raw = (_get(labour_costs, i) or '').strip()
                cost_raw = (_get(costs, i) or '').strip()
                try:
                    te.labour_cost = float(labour_raw) if labour_raw else None
                except Exception:
                    te.labour_cost = None
                try:
                    te.cost = float(cost_raw) if cost_raw else None
                except Exception:
                    te.cost = None

                # Optional FKs
                if vendor_id:
                    try:
                        te.vendor_id = int(vendor_id)
                    except Exception:
                        pass
                if driver_id:
                    try:
                        te.driver_id = int(driver_id)
                    except Exception:
                        pass
                if mechanic_id:
                    try:
                        te.mechanic_id = int(mechanic_id)
                    except Exception:
                        pass

                # Optional entry_date (date input in template)
                ed = (_get(entry_dates, i) or '').strip()
                if ed:
                    try:
                        te.entry_date = ed  # Django will parse ISO yyyy-mm-dd for DateField
                    except Exception:
                        pass

                te.save()
                created += 1
                total_amount += amount_val

            if created == 0:
                messages.error(request, 'Please add at least one expense row with amount.')
                forms = truck_expense_Form(request.POST, request=request)
                return render(request, 'expense/add_truck_expense.html', {'form': forms})

            # Update balance once for total
            user_instance = request.user
            user_instance.balance = user_instance.balance - float(total_amount)
            user_instance.save()

        return redirect('list_truck_expense')

    else:

        forms = truck_expense_Form(request=request)

        context = {
            'form': forms
        }
        return render(request, 'expense/add_truck_expense.html', context)

    
    
def update_truck_expense(request, truck_expense_id):

    instance = truck_expense.objects.get(id = truck_expense_id)

    if request.method == 'POST':

        print('here')

        amount = request.POST.get("amount")
        
        instance_old = copy.copy(instance) 

      

        
        forms = truck_expense_Form(request.POST, instance=instance, request=request)

        if forms.is_valid():

            print('here1')

            print(instance_old.amount)
            print(instance.amount)



            instance = forms.save(commit=False)
            instance.user = instance_old.user  # Assign the logged-in user
            instance.save()

            user_instance = instance.user
            user_instance.balance = user_instance.balance + float(instance_old.amount)
            user_instance.save()


            user_instance1 = instance_old.user
            user_instance1.balance = user_instance1.balance - float(amount)
            user_instance1.save()


            return redirect('list_truck_expense')
        

        else:
            context = {
                'form': forms
            }
            return render(request, 'expense/add_truck_expense.html', context)

    else:

        forms = truck_expense_Form(instance=instance, request=request)


        context = {
            'form': forms,
        }
            
        return render(request, 'expense/add_truck_expense.html', context)




def delete_truck_expense(request, truck_expense_id):


    truck_expense_instance = truck_expense.objects.get(id = truck_expense_id)

    user_instance = truck_expense_instance.user
    user_instance.balance = user_instance.balance + truck_expense_instance.amount
    user_instance.save()
    
    truck_expense_instance.delete()

    return redirect('list_truck_expense')
    
    
def list_truck_expense(request):
    
    if request.user.is_superuser:

        data = truck_expense.objects.all().order_by('-id')

    else:

        data = truck_expense.objects.filter(user = request.user).order_by('-id')

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

    # builty_expense.objects.all().delete()
    # truck_expense.objects.all().delete()
    # transfer_fund.objects.all().delete()
    # diesel_expense.objects.all().delete()
    # truck_diesel_expense.objects.all().delete()
    # other_expense.objects.all().delete()
    # salary.objects.all().delete()
    # fund.objects.all().delete()

    # a = User.objects.all()

    # for i in a:

    #     i.balance = 0.0
    #     i.save()

    pass

    
def check_balance(request):

    data = User.objects.all().order_by('-id')

    total_amount = User.objects.aggregate(total_balance=Sum('balance'))['total_balance'] or 0

    context = {
        'data': data,
        'total_amount': total_amount,
    }
    
    return render(request, 'expense/list_balance.html', context)

    
def cross_check(request):

    data = builty_expense.objects.all()

    for i in data:

        if i.is_advance:


            if not i.amount == i.builty.less_advance:

                print(i.id)

        else:


            if not i.amount == i.builty.balance:

                print(i.id)




    
def add_diesel_rate(request):
    
    instance = diesel_rate.objects.get(id = 2)

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

    instance_main = transfer_fund.objects.get(id = transfer_fund_id)

    instance_old = copy.copy(instance_main) 

    if request.method == 'POST':
        
        amount = request.POST.get('amount')

        

        forms = transfer_fund_Form(request.POST, instance = instance_main)

        if forms.is_valid():


            instance = forms.save(commit=False)
            instance.user = instance_old.user  # Assign the logged-in user
            instance.save()

            transfer_to_user = request.POST.get('transfer_to_user')

            user_instance = instance_old.user
            user_instance.balance = user_instance.balance + float(instance_old.amount)
            user_instance.save()

            user_instance1 = instance_old.transfer_to_user
            user_instance1.balance = user_instance1.balance - float(instance_old.amount)
            user_instance1.save()

            
            user_instance = instance_old.user
            user_instance.balance = user_instance.balance - float(amount)
            user_instance.save()

            user_instance = User.objects.get(id = transfer_to_user)
            user_instance.balance = user_instance.balance + float(amount)
            user_instance.save()

            return redirect('list_transfer_fund')
        

        else:

            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'expense/add_transfer_fund.html', context)

    else:

        forms = transfer_fund_Form(instance = instance_main)


        context = {
            'form': forms,
        }
            
        return render(request, 'expense/add_transfer_fund.html', context)




def delete_transfer_fund(request, transfer_fund_id):


    transfer_fund_instance = transfer_fund.objects.get(id = transfer_fund_id)


    user_instance = transfer_fund_instance.user
    user_instance.balance = user_instance.balance + float(transfer_fund_instance.amount)
    user_instance.save()

    user_instance1 = transfer_fund_instance.transfer_to_user
    user_instance1.balance = user_instance1.balance - float(transfer_fund_instance.amount)
    user_instance1.save()
    

    transfer_fund_instance.delete()
    

    return redirect('list_transfer_fund')




    
    
def list_transfer_fund(request):
    
    if request.user.is_superuser:

            data = transfer_fund.objects.all().order_by('-id')

    else:

        data = transfer_fund.objects.filter(user = request.user).order_by('-id')

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

    instance_old = copy.copy(instance.user.id)

    if request.method == 'POST':

        forms = diesel_expense_Form(request.POST, instance = instance)

        if forms.is_valid():

            instance_old = User.objects.get(id = instance_old)

            instance = forms.save(commit=False)
            instance.user = instance_old  # Assign the logged-in user
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
    diesel_expense_instance.delete()

    return redirect('list_diesel_expense')



def list_diesel_expense(request):
    
    if request.user.is_superuser:

        data = diesel_expense.objects.all().order_by('-id')

    else:

        data = diesel_expense.objects.filter(user = request.user).order_by('-id')

    rate = diesel_rate.objects.get(id=2)
    
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

    instance_old = copy.copy(instance.user.id)

    if request.method == 'POST':

        forms = truck_diesel_expense_Form(request.POST, instance = instance)

        if forms.is_valid():

            instance_old = User.objects.get(id = instance_old)

            instance = forms.save(commit=False)
            instance.user = instance_old  # Assign the logged-in user
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
    truck_diesel_expense_instance.delete()

    return redirect('list_truck_diesel_expense')




def list_truck_diesel_expense(request):
    
    rate = diesel_rate.objects.get(id=2)

    if request.user.is_superuser:

            data = truck_diesel_expense.objects.all().order_by('-id')

    else:

        data = truck_diesel_expense.objects.filter(user = request.user).order_by('-id')

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
    employee_instance.delete()

    return redirect('list_employee')

    
    
def list_employee(request):
    
    data = employee.objects.all().order_by('-id')



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

        instance_old = copy.copy(instance) 

       
       
        forms = salary_Form(request.POST, instance = instance)

        if forms.is_valid():


            instance = forms.save(commit=False)
            instance.user = instance_old.user  # Assign the logged-in user
            instance.save()

            user_instance = instance_old.user
            user_instance.balance = user_instance.balance + float(instance_old.salary)
            user_instance.save()

            user_instance1 = instance_old.user
            user_instance1.balance = user_instance1.balance - float(amount)
            user_instance1.save()


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

    user_instance = salary_instance.user
    user_instance.balance = user_instance.balance + salary_instance.salary
    user_instance.save()

    salary_instance.delete()

    return redirect('list_salary')
    
    
def list_salary(request):
    

    if request.user.is_superuser:

            data = salary.objects.all().order_by('-id')

    else:

        data = salary.objects.filter(user = request.user).order_by('-id')

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



def list_delete(request):

    
    expense_category.objects.all().delete()
    employee.objects.all().delete()
    truck_expense.objects.all().delete()
    transfer_fund.objects.all().delete()
    builty_expense.objects.all().delete()
    diesel_expense.objects.all().delete()
    truck_diesel_expense.objects.all().delete()
    salary.objects.all().delete()
    fund.objects.all().delete()
    other_expense.objects.all().delete()
    diesel_rate.objects.all().delete()

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



import json

def add_other_expense_json(request):
    
    
    if request.method == 'POST':

         # Create a list to store form data for multiple entries
        form_data_list = []
        
        
        # Extracting the fields from the request
        expense_categories = request.POST.getlist('expense_category')
        amounts = [request.POST.get(f'amount{i}') for i in range(10)]
        notes = [request.POST.get(f'note{i}') for i in range(10)]
        
        for i in range(10):
            if expense_categories[i] or amounts[i] or notes[i]:
                data = {
                    'expense_category': expense_categories[i],
                    'amount': amounts[i],
                    'note': notes[i]
                }
                form_data_list.append(data)

        # Process each set of form data
        for data in form_data_list:
            form = other_expense_Form(data)
            if form.is_valid():

                print(data)

                instance = form.save(commit=False)
                instance.user = request.user  # Assign the logged-in user
                instance.save()
                print('ssas')
                form.save()  # Save each form entry

                amount = data["amount"]
                
                user_instance = request.user
                user_instance.balance = user_instance.balance - float(amount)
                user_instance.save()

            else:

                print(form.errors)


        return JsonResponse(json.dumps({'status' : 'done'}), safe=False, content_type="application/json")
    
        
        


    else:

        forms = other_expense_Form()

        context = {
            'form': forms
        }
        return render(request, 'expense/add_other_expense_json.html', context)

        

def update_other_expense(request, other_expense_id):

    instance = other_expense.objects.get(id = other_expense_id)

    if request.method == 'POST':

        amount = request.POST.get("amount")

        instance_old = copy.copy(instance) 

       
        forms = other_expense_Form(request.POST, instance = instance)

        if forms.is_valid():


            instance = forms.save(commit=False)
            instance.user = instance_old.user  # Assign the logged-in user
            instance.save()

            user_instance = instance.user
            user_instance.balance = user_instance.balance + float(instance_old.amount)
            user_instance.save()

            user_instance1 = instance_old.user
            user_instance1.balance = user_instance1.balance - float(amount)
            user_instance1.save()

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

    user_instance = other_expense_instance.user
    user_instance.balance = user_instance.balance + other_expense_instance.amount
    user_instance.save()

    other_expense_instance.delete()

    return redirect('list_other_expense')
    
    
def list_other_expense(request):
    
    data = other_expense.objects.all().order_by('-id')


    if request.user.is_superuser:

        data = other_expense.objects.all().order_by('-id')

    else:

        data = other_expense.objects.filter(user = request.user).order_by('-id')

    
    
    other_expense_filters = other_expense_filter(request.GET, queryset=data)
    
    filter_data = other_expense_filters.qs

    print(filter_data.count())

    total = 0

    for i in filter_data:

        total = total + i.amount

    print(total)

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

        instance_old = copy.copy(instance) 

       

        forms = fund_Form(request.POST, instance = instance)

        if forms.is_valid():
            

            instance = forms.save(commit=False)
            instance.user = instance_old.user  # Assign the logged-in user
            instance.save()

            user_instance = instance_old.user
            user_instance.balance = user_instance.balance - float(instance_old.amount)
            user_instance.save()

            user_instance1 = instance_old.user
            user_instance1.balance = user_instance1.balance + float(amount)
            user_instance1.save()
        

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

    
    user_instance_fund_add = fund_instance.user
    
    user_instance_fund_add.balance = user_instance_fund_add.balance - fund_instance.amount
    user_instance_fund_add.save()

    fund_instance.delete()

    return redirect('list_fund')

    
    
def list_fund(request):
    

    data = fund.objects.all().order_by('-id')


    if request.user.is_superuser:

                data = fund.objects.all().order_by('-id')

    else:

        data = fund.objects.filter(user = request.user).order_by('-id')

    
    
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



import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import csv
import mimetypes
from django.http import FileResponse, HttpResponse, JsonResponse
import pandas as pd
from django.db.models import Q
from io import StringIO
import io
from datetime import date




def is_invalid_get_params(get_params):
    # Check if 'undefined' exists and has no value, or if the GET request is empty
    return not get_params or ('undefined' in get_params and len(get_params['undefined']) == 0)


    


def master_report(request):


    print(request.GET)

    print('------------')

    user_instance = request.GET.get('user')

    combined_data1 = []


    # Function to check if request.GET is either empty or contains 'undefined'
   
    # Check if request.GET is empty
    if is_invalid_get_params(request.GET):
        # Create a mutable copy of request.GET
        default_params = QueryDict(mutable=True)
        
        # Set default parameters
        default_params.update({
            'entry_date_start': date.today(),
            'entry_date_end': date.today()
        })


    else:

        default_params = request.GET
        




    if user_instance:

        print('------------------------')

        transfer_fund_expenses = transfer_fund.objects.filter(transfer_to_user = user_instance)
        transfer_fund_expenses = transfer_fund1_filter(default_params, queryset=transfer_fund_expenses)
        transfer_fund_expenses = transfer_fund_expenses.qs


        print(transfer_fund_expenses)

        for expense in transfer_fund_expenses:
            combined_data1.append(('transfer_fund_expense', expense.entry_date, expense.amount, expense.user, expense.note))

    funds = fund.objects.all()
    funds = truck_expense_filter(default_params, queryset=funds)
    funds = funds.qs

    for expense in funds:
        combined_data1.append(('fund', expense.entry_date, expense.amount, expense.user, expense.note))

    combined_data1.sort(key=lambda x: x[2])









    combined_data = []

        # Query and append data from each table
    builty_expenses = builty_expense.objects.all()
    builty_expenses = builty_expense_filter1(default_params, queryset=builty_expenses)
    builty_expenses = builty_expenses.qs

    builty_expenses_total = builty_expenses.aggregate(builty_expenses_total=Sum('amount'))['builty_expenses_total']


    builty_expense_filters1 = builty_expense_filter1(default_params, queryset=builty_expenses)
    builty_expenses1 = builty_expense_filters1.qs

    builty_expenses_total_owned = builty_expenses1.filter(builty__truck_owner__id='1')
    builty_expenses_total_owned = builty_expenses_total_owned.aggregate(builty_expenses_total_owned=Sum('amount'))['builty_expenses_total_owned'] or 0
    print('builty_expenses_total_owned')
    print(builty_expenses_total_owned)

    for expense in builty_expenses:
        combined_data.append(('builty_expense', expense.entry_date, expense.amount, expense.user, expense.is_advance, expense.is_porch))

    truck_expenses = truck_expense.objects.all()
    truck_expenses = truck_expense_filter(default_params, queryset=truck_expenses)
    truck_expenses = truck_expenses.qs

    truck_expenses_total = truck_expenses.aggregate(truck_expenses_total=Sum('amount'))['truck_expenses_total']

    for expense in truck_expenses:
        combined_data.append(('truck_expense', expense.entry_date, expense.amount, expense.user, expense.note))

    transfer_funds = transfer_fund.objects.all()
    transfer_funds = transfer_fund_filter(default_params, queryset=transfer_funds)
    transfer_funds = transfer_funds.qs

    transfer_funds_total = transfer_funds.aggregate(transfer_funds_total=Sum('amount'))['transfer_funds_total']

    for expense in transfer_funds:
        combined_data.append(('transfer_fund', expense.entry_date, expense.amount, expense.user, expense.note))

    other_expenses = other_expense.objects.all()
    other_expenses = other_expense_filter(default_params, queryset=other_expenses)
    other_expenses = other_expenses.qs

    other_expenses_total = other_expenses.aggregate(other_expenses_total=Sum('amount'))['other_expenses_total']

    for expense in other_expenses:
        combined_data.append(('other_expense', expense.entry_date, expense.amount, expense.user, expense.note, expense.expense_category))

    salaries = salary.objects.all()
    salaries = salary_filter(default_params, queryset=salaries)
    salaries = salaries.qs

    salaries_total = salaries.aggregate(salaries_total=Sum('salary'))['salaries_total']

    for expense in salaries:
        combined_data.append(('salary',  expense.entry_date, expense.salary, expense.user, expense.note, expense.salary_of_date, expense.employee))

   

    # Sort combined data by entry_date
    combined_data.sort(key=lambda x: x[2])


        # Calculate total amount for combined_data
    total_amount_combined_data = sum(row[2] for row in combined_data)

    # Calculate total amount for combined_data1
    total_amount_combined_data1 = sum(row[2] for row in combined_data1)

    # Generate CSV in memory
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(['Expense Type', 'Entry Date', 'Amount/Salary', 'User', 'Note', 'Additional Fields'])
    
    for row in combined_data:
        csv_writer.writerow(row)

            
    # Add empty row as a separator
    csv_writer.writerow([])

    # Write total amount for combined_data
    csv_writer.writerow(['Total Amount for combined_data:', '', total_amount_combined_data, '', '', ''])

   

    empty_row = [''] * 6  # Adjust the number of empty columns as needed
    csv_writer.writerow(empty_row * 2) 

    for row in combined_data1:
        csv_writer.writerow(row)

         # Add empty row as a separator
    csv_writer.writerow([])

    # Write headers for the right side
    csv_writer.writerow(['Total Amount for combined_data:', '', total_amount_combined_data1, '', '', ''])


    # Create HTTP response with CSV file
    response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="combined_expenses.csv"'
    return response


from django.http import QueryDict

def master_report_list(request):



    
    # Check if request.GET is empty
    if not request.GET:
        # Create a mutable copy of request.GET
        default_params = QueryDict(mutable=True)
        
        # Set default parameters
        default_params.update({
            'entry_date_start': date.today(),  # Replace 'date_field' with the actual field you're filtering by
            'entry_date_end': date.today()  # Replace 'date_field' with the actual field you're filtering by
        })

    else:

        default_params = request.GET
        

    combined_data = []


    
    user_instance = request.GET.get('user')


    if user_instance:

        transfer_fund_expenses = transfer_fund.objects.filter(transfer_to_user = user_instance)

        transfer_fund_data =  transfer_fund1_filter(default_params, queryset=transfer_fund_expenses)
        
        transfer_fund_total = transfer_fund_data.qs.aggregate(transfer_fund_total=Sum('amount'))['transfer_fund_total'] or 0


        
    else:

        transfer_fund_total = 0



    funds = fund.objects.all()
    funds = fund_filter(default_params, queryset=funds)
    funds = funds.qs
    
    fund_total = funds.aggregate(fund_total=Sum('amount'))['fund_total'] or 0

        # Query and append data from each table
    builty_expenses = builty_expense.objects.all()
    builty_expense_filters = builty_expense_filter1(default_params, queryset=builty_expenses)
    builty_expenses = builty_expense_filters.qs

    builty_expense_filters1 = builty_expense_filter1(default_params, queryset=builty_expenses)
    builty_expenses1 = builty_expense_filters1.qs

    builty_expenses_total = builty_expenses.aggregate(builty_expenses_total=Sum('amount'))['builty_expenses_total'] or 0
    

    builty_expenses_porch_total = builty_expenses.filter(is_porch = True).aggregate(builty_expenses_total=Sum('amount'))['builty_expenses_total'] or 0
    builty_expenses_advance_total = builty_expenses.filter(is_advance = True).aggregate(builty_expenses_total=Sum('amount'))['builty_expenses_total'] or 0
    
    builty_expenses_total_owned = builty_expenses1.filter(builty__truck_owner__id='1')
    builty_expenses_total_owned = builty_expenses_total_owned.aggregate(builty_expenses_total_owned=Sum('amount'))['builty_expenses_total_owned'] or 0
   
    for expense in builty_expenses:
        combined_data.append(('builty_expense', expense.entry_date, expense.amount, expense.user, expense.is_advance, expense.is_porch))

    truck_expenses = truck_expense.objects.all()
    truck_expenses = truck_expense_filter(default_params, queryset=truck_expenses)
    truck_expenses = truck_expenses.qs

    truck_expenses_total = truck_expenses.aggregate(truck_expenses_total=Sum('amount'))['truck_expenses_total'] or 0

    for expense in truck_expenses:
        combined_data.append(('truck_expense', expense.entry_date, expense.amount, expense.user, expense.note))

    transfer_funds = transfer_fund.objects.all()
    transfer_funds = transfer_fund_filter(default_params, queryset=transfer_funds)
    transfer_funds = transfer_funds.qs
    
    transfer_funds_total = transfer_funds.aggregate(transfer_funds_total=Sum('amount'))['transfer_funds_total'] or 0

    for expense in transfer_funds:
        combined_data.append(('transfer_fund', expense.entry_date, expense.amount, expense.user, expense.note))

    other_expenses = other_expense.objects.all()
    other_expenses = other_expense_filter(default_params, queryset=other_expenses)
    other_expenses = other_expenses.qs

    other_expenses_total = other_expenses.aggregate(other_expenses_total=Sum('amount'))['other_expenses_total'] or 0
    
    for expense in other_expenses:
        combined_data.append(('other_expense', expense.entry_date, expense.amount, expense.user, expense.note, expense.expense_category))

    salaries = salary.objects.all()
    salaries = salary_filter(default_params, queryset=salaries)
    salaries = salaries.qs

    salaries_total = salaries.aggregate(salaries_total=Sum('salary'))['salaries_total'] or 0
    
    for expense in salaries:
        combined_data.append(('salary',  expense.entry_date, expense.salary, expense.user, expense.note, expense.salary_of_date, expense.employee))

  
    # Sort combined data by entry_date
    combined_data.sort(key=lambda x: x[2])


  # Paginate the combined data
    paginator = Paginator(combined_data, 20)  # 10 items per page
    page = default_params.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        data = paginator.page(paginator.num_pages)

    print('-------------------1111')
    print(builty_expenses_total)
    print(truck_expenses_total)
    print(transfer_funds_total)
    print(other_expenses_total)
    print(salaries_total)

    total_incoming = fund_total + transfer_fund_total
    total_outgoing = builty_expenses_total + truck_expenses_total+ transfer_funds_total + other_expenses_total+ salaries_total 
    
    total_balance = total_incoming - total_outgoing

    context = {
        'data': data,
        'transfer_fund_total': transfer_fund_total,
        'fund_total': fund_total,
        'builty_expenses_total': builty_expenses_total,
        'truck_expenses_total': truck_expenses_total,
        'builty_expenses_total_other': int(builty_expenses_total - builty_expenses_total_owned),
        'builty_expenses_total_owned': builty_expenses_total_owned,
        'transfer_funds_total': transfer_funds_total,
        'other_expenses_total': other_expenses_total,
        'salaries_total': salaries_total,
        'builty_expense_filter' : builty_expense_filters,
        'total_incoming' : total_incoming,
        'total_outgoing' : total_outgoing,
        'total_balance' : total_balance,
        'builty_expenses_porch_total' : builty_expenses_porch_total,
        'builty_expenses_advance_total' : builty_expenses_advance_total,
    
    }

    return render(request, 'report/master_report.html', context)



def master_report_normal(request):


    print(request.GET)

    print('------------')

    user_instance = request.GET.get('user')

    combined_data1 = []


    
    # Check if request.GET is empty
    if not request.GET:
        # Create a mutable copy of request.GET
        default_params = QueryDict(mutable=True)
        
        # Set default parameters
        default_params.update({
            'entry_date_start': date.today(),  # Replace 'date_field' with the actual field you're filtering by
            'entry_date_end': date.today()  # Replace 'date_field' with the actual field you're filtering by
        })

    else:

        default_params = request.GET
        

    if user_instance:

        print('------------------------')

        transfer_fund_expenses = transfer_fund.objects.filter(transfer_to_user = user_instance)
        transfer_fund_expenses = transfer_fund1_filter(default_params, queryset=transfer_fund_expenses)
        transfer_fund_expenses = transfer_fund_expenses.qs


        print(transfer_fund_expenses)

        for expense in transfer_fund_expenses:
            combined_data1.append(('transfer_fund_expense', expense.entry_date, expense.amount, expense.user, expense.note))

    funds = fund.objects.all()
    funds = truck_expense_filter(default_params, queryset=funds)
    funds = funds.qs

    for expense in funds:
        combined_data1.append(('fund', expense.entry_date, expense.amount, expense.user, expense.note))

    combined_data1.sort(key=lambda x: x[2])









    combined_data = []

        # Query and append data from each table
    builty_expenses = builty_expense.objects.all()
    builty_expenses = builty_expense_filter1(default_params, queryset=builty_expenses)
    builty_expenses = builty_expenses.qs

    builty_expenses_total = builty_expenses.aggregate(builty_expenses_total=Sum('amount'))['builty_expenses_total'] or 0


    builty_expense_filters1 = builty_expense_filter1(default_params, queryset=builty_expenses)
    builty_expenses1 = builty_expense_filters1.qs

    builty_expenses_total_owned = builty_expenses1.filter(builty__truck_owner__id='1')
    builty_expenses_total_owned = builty_expenses_total_owned.aggregate(builty_expenses_total_owned=Sum('amount'))['builty_expenses_total_owned'] or 0
    print('builty_expenses_total_owned')
    print(builty_expenses_total_owned)

    for expense in builty_expenses:
        combined_data.append(('builty_expense', expense.entry_date, expense.amount, expense.user, expense.is_advance, expense.is_porch))

    truck_expenses = truck_expense.objects.all()
    truck_expenses = truck_expense_filter(default_params, queryset=truck_expenses)
    truck_expenses = truck_expenses.qs

    truck_expenses_total = truck_expenses.aggregate(truck_expenses_total=Sum('amount'))['truck_expenses_total'] or 0

    for expense in truck_expenses:
        combined_data.append(('truck_expense', expense.entry_date, expense.amount, expense.user, expense.note))

    transfer_funds = transfer_fund.objects.all()
    transfer_funds = transfer_fund_filter(default_params, queryset=transfer_funds)
    transfer_funds = transfer_funds.qs

    transfer_funds_total = transfer_funds.aggregate(transfer_funds_total=Sum('amount'))['transfer_funds_total'] or 0

    for expense in transfer_funds:
        combined_data.append(('transfer_fund', expense.entry_date, expense.amount, expense.user, expense.note))

    other_expenses = other_expense.objects.all()
    other_expenses = other_expense_filter(default_params, queryset=other_expenses)
    other_expenses = other_expenses.qs

    other_expenses_total = other_expenses.aggregate(other_expenses_total=Sum('amount'))['other_expenses_total'] or 0

    for expense in other_expenses:
        combined_data.append(('other_expense', expense.entry_date, expense.amount, expense.user, expense.note, expense.expense_category))

    salaries = salary.objects.all()
    salaries = salary_filter(default_params, queryset=salaries)
    salaries = salaries.qs

    salaries_total = salaries.aggregate(salaries_total=Sum('salary'))['salaries_total'] or 0

    for expense in salaries:
        combined_data.append(('salary',  expense.entry_date, expense.salary, expense.user, expense.note, expense.salary_of_date, expense.employee))

   

    # Sort combined data by entry_date
    combined_data.sort(key=lambda x: x[2])


        # Calculate total amount for combined_data
    total_amount_combined_data = sum(row[2] for row in combined_data)

    # Calculate total amount for combined_data1
    total_amount_combined_data1 = sum(row[2] for row in combined_data1)

    # Generate CSV in memory
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(['Expense Type', 'Entry Date', 'Amount/Salary', 'User', 'Note', 'Additional Fields'])
    
    for row in combined_data:
        csv_writer.writerow(row)

            
    # Add empty row as a separator
    csv_writer.writerow([])

    # Write total amount for combined_data
    csv_writer.writerow(['Total Amount for combined_data:', '', total_amount_combined_data, '', '', ''])

   

    empty_row = [''] * 6  # Adjust the number of empty columns as needed
    csv_writer.writerow(empty_row * 2) 

    for row in combined_data1:
        csv_writer.writerow(row)

         # Add empty row as a separator
    csv_writer.writerow([])

    # Write headers for the right side
    csv_writer.writerow(['Total Amount for combined_data:', '', total_amount_combined_data1, '', '', ''])

    print(combined_data)

    # Create HTTP response with CSV file
    response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="combined_expenses.csv"'
    return response



def master_report_normal_list(request):


    combined_data = []


    
    user_instance = request.user


    

    transfer_fund_expenses = transfer_fund.objects.filter(transfer_to_user = user_instance)

    transfer_fund_data =  transfer_fund1_filter(request.GET, queryset=transfer_fund_expenses)
    
    transfer_fund_total = transfer_fund_data.qs.aggregate(transfer_fund_total=Sum('amount'))['transfer_fund_total'] or 0


        
  



    funds = fund.objects.filter(user = request.user)
    funds = fund_filter(request.GET, queryset=funds)
    funds = funds.qs
    
    fund_total = funds.aggregate(fund_total=Sum('amount'))['fund_total'] or 0

        # Query and append data from each table
    builty_expenses = builty_expense.objects.filter(user = request.user)
    builty_expense_filters = builty_expense_filter1(request.GET, queryset=builty_expenses)
    builty_expenses = builty_expense_filters.qs

    builty_expense_filters1 = builty_expense_filter1(request.GET, queryset=builty_expenses)
    builty_expenses1 = builty_expense_filters1.qs

    builty_expenses_total = builty_expenses.aggregate(builty_expenses_total=Sum('amount'))['builty_expenses_total'] or 0

    builty_expenses_porch_total = builty_expenses.filter(is_porch = True).aggregate(builty_expenses_total=Sum('amount'))['builty_expenses_total'] or 0
    builty_expenses_advance_total = builty_expenses.filter(is_advance = True).aggregate(builty_expenses_total=Sum('amount'))['builty_expenses_total'] or 0
    

    builty_expenses_total_owned = builty_expenses1.filter(builty__truck_owner__id='1')
    builty_expenses_total_owned = builty_expenses_total_owned.aggregate(builty_expenses_total_owned=Sum('amount'))['builty_expenses_total_owned'] or 0
    print('builty_expenses_total_owned')
    print(builty_expenses_total_owned)

    for expense in builty_expenses:
        combined_data.append(('builty_expense', expense.entry_date, expense.amount, expense.user, expense.is_advance, expense.is_porch))

    truck_expenses = truck_expense.objects.filter(user = request.user)
    truck_expenses = truck_expense_filter(request.GET, queryset=truck_expenses)
    truck_expenses = truck_expenses.qs

    truck_expenses_total = truck_expenses.aggregate(truck_expenses_total=Sum('amount'))['truck_expenses_total'] or 0

    for expense in truck_expenses:
        combined_data.append(('truck_expense', expense.entry_date, expense.amount, expense.user, expense.note))

    transfer_funds = transfer_fund.objects.filter(user = request.user)
    transfer_funds = transfer_fund_filter(request.GET, queryset=transfer_funds)
    transfer_funds = transfer_funds.qs
    
    transfer_funds_total = transfer_funds.aggregate(transfer_funds_total=Sum('amount'))['transfer_funds_total'] or 0

    for expense in transfer_funds:
        combined_data.append(('transfer_fund', expense.entry_date, expense.amount, expense.user, expense.note))

    other_expenses = other_expense.objects.filter(user = request.user)
    other_expenses = other_expense_filter(request.GET, queryset=other_expenses)
    other_expenses = other_expenses.qs

    other_expenses_total = other_expenses.aggregate(other_expenses_total=Sum('amount'))['other_expenses_total'] or 0
    
    for expense in other_expenses:
        combined_data.append(('other_expense', expense.entry_date, expense.amount, expense.user, expense.note, expense.expense_category))

    salaries = salary.objects.filter(user = request.user)
    salaries = salary_filter(request.GET, queryset=salaries)
    salaries = salaries.qs

    salaries_total = salaries.aggregate(salaries_total=Sum('salary'))['salaries_total'] or 0
    
    for expense in salaries:
        combined_data.append(('salary',  expense.entry_date, expense.salary, expense.user, expense.note, expense.salary_of_date, expense.employee))

  
    # Sort combined data by entry_date
    combined_data.sort(key=lambda x: x[2])


  # Paginate the combined data
    paginator = Paginator(combined_data, 20)  # 10 items per page
    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        data = paginator.page(paginator.num_pages)


    print(builty_expenses_total),
    print(truck_expenses_total)
    print(transfer_funds_total)
    print(other_expenses_total)
    print(salaries_total)

    total_incoming = fund_total + transfer_fund_total
    total_outgoing = builty_expenses_total + truck_expenses_total+ transfer_funds_total + other_expenses_total+ salaries_total 
    
    total_balance = total_incoming - total_outgoing

    context = {
        'data': data,
        'transfer_fund_total': transfer_fund_total,
        'fund_total': fund_total,
        'builty_expenses_total': builty_expenses_total,
        'truck_expenses_total': truck_expenses_total,
        'builty_expenses_total_other': int(builty_expenses_total - builty_expenses_total_owned),
        'builty_expenses_total_owned': builty_expenses_total_owned,
        'transfer_funds_total': transfer_funds_total,
        'other_expenses_total': other_expenses_total,
        'salaries_total': salaries_total,
        'builty_expense_filter' : builty_expense_filters,
        'total_incoming' : total_incoming,
        'total_outgoing' : total_outgoing,
        'total_balance' : total_balance,
        'builty_expenses_porch_total' : builty_expenses_porch_total,
        'builty_expenses_advance_total' : builty_expenses_advance_total,
    
    }

    return render(request, 'report/master_report_normal.html', context)



def master_fund_report_list(request):


    user_instance = request.GET.get('user')

    combined_data1 = []

    if user_instance:

        print('inedfdfdef')


        transfer_fund_expenses = transfer_fund.objects.filter(transfer_to_user = user_instance)
        print(transfer_fund_expenses)
        transfer_fund_expenses = transfer_fund1_filter(request.GET, queryset=transfer_fund_expenses)
        transfer_fund_expenses = transfer_fund_expenses.qs
        print(transfer_fund_expenses)

        for expense in transfer_fund_expenses:
            combined_data1.append(('transfer_fund_expense', expense.entry_date, expense.amount, expense.user, expense.note))
    
        transfer_fund_total = transfer_fund_expenses.aggregate(transfer_fund_total=Sum('amount'))['transfer_fund_total']
    
    else:

        print('in else')

        print(user_instance)

        transfer_fund_total = 0

    funds = fund.objects.all()
    funds_filters = fund_filter(request.GET, queryset=funds)
    funds = funds_filters.qs
    
    fund_total = funds.aggregate(fund_total=Sum('amount'))['fund_total']

    for expense in funds:
        combined_data1.append(('fund', expense.entry_date, expense.amount, expense.user, expense.note))

    combined_data1.sort(key=lambda x: x[2])


    
  # Paginate the combined data
    paginator = Paginator(combined_data1, 20)  # 10 items per page
    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        data = paginator.page(paginator.num_pages)


    context = {
        'data': data,
        'transfer_fund_total': transfer_fund_total,
        'fund_total': fund_total,
        'builty_expense_filter': funds_filters,

    }

    return render(request, 'report/master_fund_report.html', context)




def master_fund_report(request):


    print(request.GET)

    print('------------')

    user_instance = request.GET.get('user')

    combined_data1 = []

    if user_instance:

        print('------------------------')

        transfer_fund_expenses = transfer_fund.objects.filter(transfer_to_user = user_instance)
    
        transfer_fund_expenses = transfer_fund1_filter(request.GET, queryset=transfer_fund_expenses)
        transfer_fund_expenses = transfer_fund_expenses.qs

        print(transfer_fund_expenses)

        for expense in transfer_fund_expenses:
            combined_data1.append(('transfer_fund_expense', expense.entry_date, expense.amount, expense.user, expense.note))

    funds = fund.objects.all()
    funds = fund_filter(request.GET, queryset=funds)
    funds = funds.qs

    for expense in funds:
        combined_data1.append(('fund', expense.entry_date, expense.amount, expense.user, expense.note))

    combined_data1.sort(key=lambda x: x[2])





    # Sort combined data by entry_date
    combined_data1.sort(key=lambda x: x[2])



    # Calculate total amount for combined_data1
    total_amount_combined_data1 = sum(row[2] for row in combined_data1)

    # Generate CSV in memory
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(['Expense Type', 'Entry Date', 'Amount/Salary', 'User', 'Note', 'Additional Fields'])
    
    for row in combined_data1:
        csv_writer.writerow(row)

            
    # Add empty row as a separator
    csv_writer.writerow([])

    # Write total amount for combined_data
    csv_writer.writerow(['Total Amount for combined_data:', '', total_amount_combined_data1, '', '', ''])

   
    # Create HTTP response with CSV file
    response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="combined_expenses.csv"'
    return response


@login_required(login_url='login')
def user_master_report_list(request):
    """User Master Report - from date to date, everything a user did: builty (count, list, total MT), all expenses."""
    user_id = request.GET.get('user')
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')

    # Resolve user: superuser can select, others get self
    if request.user.is_superuser:
        selected_user_id = user_id
        users_list = User.objects.all().order_by('username')
    else:
        selected_user_id = str(request.user.id)
        users_list = [request.user]

    # Default dates if not provided
    if not from_date_str:
        from_date_str = str(date.today())
    if not to_date_str:
        to_date_str = str(date.today())

    from_date = None
    to_date = None
    try:
        from datetime import datetime
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        from_date = date.today()
        to_date = date.today()

    context = {
        'users_list': users_list,
        'from_date': from_date_str,
        'to_date': to_date_str,
        'selected_user_id': selected_user_id,
        'is_superuser': request.user.is_superuser,
    }

    if not selected_user_id:
        context['builty_list'] = []
        context['builty_count'] = 0
        context['builty_total_mt'] = 0
        context['builty_expenses_total'] = 0
        context['builty_expenses_porch_total'] = 0
        context['porch_builty_list'] = []
        context['porch_builty_count'] = 0
        context['porch_total_mt'] = 0
        context['builty_expenses_advance_total'] = 0
        context['builty_expenses_advance_owned'] = 0
        context['builty_expenses_advance_other'] = 0
        context['truck_expenses_total'] = 0
        context['diesel_expenses_total'] = 0
        context['truck_diesel_expenses_total'] = 0
        context['truck_diesel_liters_total'] = 0
        context['builty_diesel_list'] = []
        context['other_expenses_total'] = 0
        context['salaries_total'] = 0
        context['transfer_funds_total'] = 0
        context['grand_total_expense'] = 0
        context['combined_data'] = []
        context['user_obj'] = None
        return render(request, 'report/user_master_report.html', context)

    user_obj = User.objects.get(id=selected_user_id)

    # Builty created by user in date range (DC_date)
    builty_list = builty.objects.filter(user=user_obj, deleted=False, DC_date__gte=from_date, DC_date__lte=to_date).order_by('-DC_date')
    builty_count = builty_list.count()
    builty_total_mt = builty_list.aggregate(mt_sum=Sum('mt'))['mt_sum'] or 0

    # Expenses by user in date range (entry_date)
    builty_expenses = builty_expense.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date).order_by('entry_date')
    truck_expenses = truck_expense.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date).order_by('entry_date')
    diesel_expenses = diesel_expense.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date).order_by('entry_date')
    truck_diesel_expenses = truck_diesel_expense.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date).order_by('entry_date')
    other_expenses = other_expense.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date).order_by('entry_date')
    salaries_list = salary.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date).order_by('entry_date')
    transfer_funds_list = transfer_fund.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date).order_by('entry_date')

    # Totals
    builty_expenses_total = builty_expenses.aggregate(s=Sum('amount'))['s'] or 0
    builty_expenses_porch_total = builty_expenses.filter(is_porch=True).aggregate(s=Sum('amount'))['s'] or 0
    porch_builty_list = builty_expenses.filter(is_porch=True).order_by('entry_date')
    porch_builty_count = porch_builty_list.count()
    porch_total_mt = builty_expenses.filter(is_porch=True).aggregate(s=Sum('builty__mt'))['s'] or 0
    builty_expenses_advance_total = builty_expenses.filter(is_advance=True).aggregate(s=Sum('amount'))['s'] or 0
    builty_expenses_advance_owned = builty_expenses.filter(is_advance=True, builty__truck_owner__id=1).aggregate(s=Sum('amount'))['s'] or 0
    builty_expenses_advance_other = builty_expenses.filter(is_advance=True).exclude(builty__truck_owner__id=1).aggregate(s=Sum('amount'))['s'] or 0
    truck_expenses_total = truck_expenses.aggregate(s=Sum('amount'))['s'] or 0
    diesel_expenses_total = diesel_expenses.aggregate(s=Sum('amount'))['s'] or 0
    truck_diesel_expenses_total = truck_diesel_expenses.aggregate(s=Sum('amount'))['s'] or 0
    # Diesel liters: use builty.diesel - same source as main Builty List, ensures total and popup match
    truck_diesel_liters_total = builty_list.aggregate(s=Sum('diesel'))['s'] or 0
    # Builties with diesel: from builty_list where diesel > 0
    builty_diesel_list = [(b, b.diesel) for b in builty_list if b.diesel and float(b.diesel) > 0]
    other_expenses_total = other_expenses.aggregate(s=Sum('amount'))['s'] or 0
    salaries_total = salaries_list.aggregate(s=Sum('salary'))['s'] or 0
    transfer_funds_total = transfer_funds_list.aggregate(s=Sum('amount'))['s'] or 0

    grand_total_expense = (builty_expenses_total + truck_expenses_total + diesel_expenses_total +
                          truck_diesel_expenses_total + other_expenses_total + salaries_total + transfer_funds_total)

    # Combined master view - each row: (type, date, amount, user, note, extra, view_url, display_label)
    combined_data = []
    for e in builty_expenses:
        builty_no = e.builty.builty_no if e.builty else '-'
        ext = 'Adv:%s Porch:%s' % (e.is_advance, e.is_porch)
        if e.is_porch:
            exp_type, display_label = 'builty_expense_porch', 'Builty (Porch)'
        elif e.is_advance:
            exp_type, display_label = 'builty_expense_advance', 'Builty (Less Advance)'
        else:
            exp_type, display_label = 'builty_expense', 'Builty Expense'
        view_url = reverse('update_builty', args=[e.builty.id]) if e.builty else ''
        combined_data.append((exp_type, e.entry_date, e.amount, e.user, builty_no, ext, view_url, display_label))
    for e in truck_expenses:
        note = (e.note or '')[:50]
        view_url = reverse('update_truck_expense', args=[e.id])
        combined_data.append(('truck_expense', e.entry_date, e.amount, e.user, note, e.truck.truck_number if e.truck else '-', view_url, 'Truck Expense'))
    for e in diesel_expenses:
        view_url = reverse('update_diesel_expense', args=[e.id])
        combined_data.append(('diesel_expense', e.entry_date, e.amount, e.user, e.note or '', e.builty.builty_no if e.builty else '-', view_url, 'Diesel Expense'))
    for e in truck_diesel_expenses:
        view_url = reverse('update_truck_diesel_expense', args=[e.id])
        combined_data.append(('truck_diesel_expense', e.entry_date, e.amount, e.user, e.note or '', e.truck.truck_number if e.truck else '-', view_url, 'Truck Diesel'))
    for e in other_expenses:
        view_url = reverse('update_other_expense', args=[e.id])
        combined_data.append(('other_expense', e.entry_date, e.amount, e.user, e.note or '', e.expense_category.name if e.expense_category else '-', view_url, 'Other Expense'))
    for e in salaries_list:
        view_url = reverse('update_salary', args=[e.id])
        combined_data.append(('salary', e.entry_date, e.salary, e.user, e.note or '', e.employee.name if e.employee else '-', view_url, 'Salary'))
    for e in transfer_funds_list:
        to_user = e.transfer_to_user.username if e.transfer_to_user else '-'
        view_url = reverse('update_transfer_fund', args=[e.id])
        combined_data.append(('transfer_fund', e.entry_date, e.amount, e.user, e.note or '', to_user, view_url, 'Transfer Fund'))

    combined_data.sort(key=lambda x: x[1])

    context.update({
        'user_obj': user_obj,
        'builty_list': builty_list,
        'builty_count': builty_count,
        'builty_total_mt': builty_total_mt,
        'builty_expenses_total': builty_expenses_total,
        'builty_expenses_porch_total': builty_expenses_porch_total,
        'porch_builty_list': porch_builty_list,
        'porch_builty_count': porch_builty_count,
        'porch_total_mt': porch_total_mt,
        'builty_expenses_advance_total': builty_expenses_advance_total,
        'builty_expenses_advance_owned': builty_expenses_advance_owned,
        'builty_expenses_advance_other': builty_expenses_advance_other,
        'truck_expenses_total': truck_expenses_total,
        'diesel_expenses_total': diesel_expenses_total,
        'truck_diesel_expenses_total': truck_diesel_expenses_total,
        'truck_diesel_liters_total': truck_diesel_liters_total,
        'other_expenses_total': other_expenses_total,
        'salaries_total': salaries_total,
        'transfer_funds_total': transfer_funds_total,
        'grand_total_expense': grand_total_expense,
        'combined_data': combined_data,
    })

    return render(request, 'report/user_master_report.html', context)


@login_required(login_url='login')
def user_master_report(request):
    """Download User Master Report as CSV."""
    user_id = request.GET.get('user')
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')

    if request.user.is_superuser:
        selected_user_id = user_id
    else:
        selected_user_id = str(request.user.id)

    if not selected_user_id:
        response = HttpResponse('Please select a user.', content_type='text/plain')
        return response

    from datetime import datetime
    from_date = date.today()
    to_date = date.today()
    try:
        if from_date_str:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        if to_date_str:
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        pass

    user_obj = User.objects.get(id=selected_user_id)

    builty_list = builty.objects.filter(user=user_obj, deleted=False, DC_date__gte=from_date, DC_date__lte=to_date).order_by('-DC_date')
    builty_count = builty_list.count()
    builty_total_mt = builty_list.aggregate(mt_sum=Sum('mt'))['mt_sum'] or 0

    builty_expenses = builty_expense.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date)
    truck_expenses = truck_expense.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date)
    diesel_expenses = diesel_expense.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date)
    truck_diesel_expenses = truck_diesel_expense.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date)
    other_expenses = other_expense.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date)
    salaries_list = salary.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date)
    transfer_funds_list = transfer_fund.objects.filter(user=user_obj, entry_date__gte=from_date, entry_date__lte=to_date)

    csv_buffer = StringIO()
    w = csv.writer(csv_buffer)

    w.writerow(['User Master Report', user_obj.username, from_date, to_date])
    w.writerow([])
    w.writerow(['BILITY SUMMARY'])
    w.writerow(['Builty Count', builty_count])
    w.writerow(['Total MT', builty_total_mt])
    w.writerow([])
    w.writerow(['BILITY LIST'])
    w.writerow(['Builty No', 'DC Date', 'Consignor', 'From', 'To', 'Article', 'Bags', 'MT', 'Rate', 'Freight', 'Less Advance', 'Balance'])
    for b in builty_list:
        w.writerow([
            b.builty_no, b.DC_date,
            b.consignor.name if b.consignor else '',
            b.station_from.name if b.station_from else '',
            b.station_to.name if b.station_to else '',
            b.article.name if b.article else '',
            b.bags, b.mt, b.rate, b.freight, b.less_advance, b.balance
        ])
    w.writerow([])
    w.writerow(['EXPENSE SUMMARY'])
    builty_exp_total = builty_expenses.aggregate(s=Sum('amount'))['s'] or 0
    truck_exp_total = truck_expenses.aggregate(s=Sum('amount'))['s'] or 0
    diesel_exp_total = diesel_expenses.aggregate(s=Sum('amount'))['s'] or 0
    truck_diesel_total = truck_diesel_expenses.aggregate(s=Sum('amount'))['s'] or 0
    other_exp_total = other_expenses.aggregate(s=Sum('amount'))['s'] or 0
    sal_total = salaries_list.aggregate(s=Sum('salary'))['s'] or 0
    tf_total = transfer_funds_list.aggregate(s=Sum('amount'))['s'] or 0
    w.writerow(['Builty Expense', builty_exp_total])
    w.writerow(['Truck Expense', truck_exp_total])
    w.writerow(['Diesel Expense', diesel_exp_total])
    w.writerow(['Truck Diesel Expense', truck_diesel_total])
    w.writerow(['Other Expense', other_exp_total])
    w.writerow(['Salary', sal_total])
    w.writerow(['Transfer Fund', tf_total])
    w.writerow(['GRAND TOTAL EXPENSE', builty_exp_total + truck_exp_total + diesel_exp_total + truck_diesel_total + other_exp_total + sal_total + tf_total])
    w.writerow([])
    w.writerow(['EXPENSE DETAIL (Master View)'])
    w.writerow(['Type', 'Entry Date', 'Amount', 'User', 'Note/Ref', 'Extra'])
    for e in builty_expenses:
        builty_no = e.builty.builty_no if e.builty else '-'
        w.writerow(['builty_expense', e.entry_date, e.amount, e.user, builty_no, str(e.is_advance) + '/' + str(e.is_porch)])
    for e in truck_expenses:
        w.writerow(['truck_expense', e.entry_date, e.amount, e.user, e.note or '', e.truck.truck_number if e.truck else '-'])
    for e in diesel_expenses:
        w.writerow(['diesel_expense', e.entry_date, e.amount, e.user, e.note or '', e.builty.builty_no if e.builty else '-'])
    for e in truck_diesel_expenses:
        w.writerow(['truck_diesel_expense', e.entry_date, e.amount, e.user, e.note or '', e.truck.truck_number if e.truck else '-'])
    for e in other_expenses:
        w.writerow(['other_expense', e.entry_date, e.amount, e.user, e.note or '', e.expense_category.name if e.expense_category else '-'])
    for e in salaries_list:
        w.writerow(['salary', e.entry_date, e.salary, e.user, e.note or '', e.employee.name if e.employee else '-'])
    for e in transfer_funds_list:
        w.writerow(['transfer_fund', e.entry_date, e.amount, e.user, e.note or '', e.transfer_to_user.username if e.transfer_to_user else '-'])

    response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_master_report_{}.csv"'.format(user_obj.username)
    return response


from django.db.models import Sum

def check_data(request):

    userss = User.objects.all()

    for i in userss:

        incoming = 0
        outgoing = 0
        total = 0

        fund_sum = fund.objects.filter(user=i).aggregate(fund_sum=Sum('amount'))['fund_sum'] or 0
        transfer_fund_sum = transfer_fund.objects.filter(transfer_to_user=i).aggregate(fund_sum=Sum('amount'))['fund_sum'] or 0

        incoming = fund_sum + transfer_fund_sum

        transfer_fund_sum = transfer_fund.objects.filter(user=i).aggregate(transfer_fund_sum=Sum('amount'))['transfer_fund_sum'] or 0
        builty_expense_sum = builty_expense.objects.filter(user=i).aggregate(builty_expense_sum=Sum('amount'))['builty_expense_sum'] or 0
        truck_expense_sum = truck_expense.objects.filter(user=i).aggregate(truck_expense_sum=Sum('amount'))['truck_expense_sum'] or 0
        other_expense_sum = other_expense.objects.filter(user=i).aggregate(other_expense_sum=Sum('amount'))['other_expense_sum'] or 0
        salary_expense_sum = salary.objects.filter(user=i).aggregate(total_amount=Sum('salary'))['total_amount'] or 0

        outgoing = transfer_fund_sum + builty_expense_sum + truck_expense_sum + other_expense_sum + salary_expense_sum

        total = incoming - outgoing


        print(i.username)
        print(total)





def add_close_balance(request):


    closing_balance.objects.create(user = request.user, closing_balance = request.user.balance)

    return redirect('list_close_balance')


def list_close_balance(request):

    if request.user.is_superuser:

        data = closing_balance.objects.all().order_by('-id')

    else:

        data = closing_balance.objects.filter(user = request.user).order_by('-id')


    filter_data = closing_balance_filter(request.GET, queryset=data)

    data = filter_data.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(data, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)


    context = {
        'data': data,
        'closing_filter' : filter_data
    }

    return render(request, 'expense/list_closing_balance.html', context)





