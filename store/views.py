from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from users.models import User
from .models import *
from .forms import *
from .models import *

from datetime import date

from datetime import datetime
from django.urls import reverse
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages

from transactions.decorators import *


import pytz
ist = pytz.timezone('Asia/Kolkata')




def get_consignor_ajax(request):



    data = []

    if request.method == "POST":
        company_id = request.POST['company_id']
        try:
            company_instance = company.objects.get(id= company_id)
            dropdown1 = consignor.objects.filter(company = company_instance, office_location = request.user.office_location)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(dropdown1.values('id', 'name')), safe = False) 




@user_is_active
def numOfDays(date1):

    dt1 = date1.split('T')

    time = dt1[1]
    time1 = time.split(':')

    dt1 = dt1[0]
    
    dt1 = dt1.split('-')
    

    year = int(dt1[0])
    month = int(dt1[1])
    day = int(dt1[2])

    date1 = datetime(year,month, day , int(time1[0]), int(time1[1]), tzinfo=ist)

    return date1



@login_required(login_url='login')
@user_is_active
def add_company(request):

    if request.method == 'POST':

        forms = company_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_company')
        else:
            context = {
                'form': forms
            }
            return render(request, 'store/add_company.html', context)
    
    else:

        forms = company_Form()

        context = {
            'form': forms
        }
        return render(request, 'store/add_company.html', context)

        

@login_required(login_url='login')
@user_is_active
def update_company(request, company_id):

    if request.method == 'POST':

        instance = company.objects.get(id=company_id)

        forms = company_Form(request.POST, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_company')
        else:

            context = {
                'form': forms
            }
            return render(request, 'store/add_company.html', context)
    
    else:

        instance = company.objects.get(id=company_id)
        forms = company_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'store/add_company.html', context)

        

@login_required(login_url='login')
@user_is_active
def delete_company(request, company_id):

    company.objects.get(id=company_id).delete()

    return HttpResponseRedirect(reverse('list_company_delete'))


        

@login_required(login_url='login')
@user_is_active
def list_company(request):

    data = company.objects.all().order_by('-id')

    context = {
        'data': data
    }

    return render(request, 'store/list_company.html', context)

@login_required(login_url='login')
@user_is_active
def add_office_location(request):

    if request.method == 'POST':

        forms = office_location_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_office_location')
        else:

            context = {
                    'form': forms
                }
            return render(request, 'store/add_office_location.html', context)
    else:

        forms = office_location_Form()

        context = {
            'form': forms
        }
        return render(request, 'store/add_office_location.html', context)

        

@login_required(login_url='login')
@user_is_active
def update_office_location(request, office_location_id):

    if request.method == 'POST':

        instance = office_location.objects.get(id=office_location_id)

        forms = office_location_Form(request.POST, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_office_location')
        else:

            context = {
                    'form': forms
                }
            return render(request, 'store/add_office_location.html', context)

    else:

        instance = office_location.objects.get(id=office_location_id)
        forms = office_location_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'store/add_office_location.html', context)

        

@login_required(login_url='login')
@user_is_active
def delete_office_location(request, office_location_id):

    office_location.objects.get(id=office_location_id).delete()

    return HttpResponseRedirect(reverse('list_office_location_delete'))


        

@login_required(login_url='login')
@user_is_active
def list_office_location(request):

    data = office_location.objects.all().order_by('-id')

    context = {
        'data': data
    }

    return render(request, 'store/list_office_location.html', context)



@login_required(login_url='login')
@user_is_active
def add_consignor(request):
    
    if request.method == 'POST':
  
        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})
       
        forms = consignor_Form(updated_request)

        if forms.is_valid():
            forms.save()
            return redirect('list_consignor')
        else:

            context = {
                'form': forms
            }

            return render(request, 'store/add_consignor.html', context)
    
    else:

        forms = consignor_Form()

        context = {
            'form': forms
        }

        return render(request, 'store/add_consignor.html', context)



from django.views.decorators.csrf import csrf_exempt
import json


@login_required(login_url='login')
@user_is_active
@csrf_exempt
def add_consignor_ajax(request):
    
    if request.method == 'POST':


        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})
        if request.user.is_superuser:
            
            forms = consignor_Form(updated_request)
            
        else:

            updated_request.update({'company': request.user.company})
            forms = consignor_Form(updated_request)

        if forms.is_valid():
            a = forms.save()

            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.name}), safe=False, content_type="application/json") 

        else:
            error = forms.errors.as_json()

            return JsonResponse(json.dumps(json.dumps({'error' : error})), safe=False)
  

@user_is_active
def update_consignor(request, consignor_id):

    if request.method == 'POST':

        instance = consignor.objects.get(id=consignor_id)
        
        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})
        
        forms = consignor_Form(updated_request, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_consignor')

        else:

            comapnyID = instance.company.id
            comapny_consignor_ID = instance.id

            context = {
                'form': forms,
                'comapnyID' : comapnyID,
                'comapny_consignor_ID' : comapny_consignor_ID
                
            }

            return render(request, 'store/add_consignor.html', context)
    else:

        instance = consignor.objects.get(id=consignor_id)

        forms = consignor_Form(instance = instance)

        comapnyID = instance.company.id
        comapny_consignor_ID = instance.id

        context = {
            'form': forms,
            'comapnyID' : comapnyID,
            'comapny_consignor_ID' : comapny_consignor_ID
            
        }

        return render(request, 'store/add_consignor.html', context)


@login_required(login_url='login')
@user_is_active
def delete_consignor(request, consignor_id):
    
    consignor.objects.get(id=consignor_id).delete()

    return HttpResponseRedirect(reverse('list_consignor_delete'))


@login_required(login_url='login')
@user_is_active
def list_consignor(request):

    if request.user.is_superuser:

        data =  consignor.objects.all().order_by('-id')

    else:
    
        data = consignor.objects.filter(office_location = request.user.office_location).order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_consignor.html', context)



@login_required(login_url='login')
@user_is_active
def add_article(request):
    
    if request.method == 'POST':

        updated_request = request.POST.copy()
        updated_request.update({'company_name': request.user.company, 'office_location': request.user.office_location})
        
        forms = article_Form(request.user, updated_request)

        if forms.is_valid():
            forms.save()
            return redirect('list_article')
        else:

            data = company.objects.all()

            context = {
                'form': forms,
                'data' : data,
            }

            return render(request, 'store/add_article.html', context)
    
    else:

        forms = article_Form(request.user)
        data = company.objects.all()

        context = {
            'form': forms,
            'data' : data,
        }

        return render(request, 'store/add_article.html', context)


@login_required(login_url='login')
@user_is_active
@csrf_exempt
def add_article_ajax(request):
    
    if request.method == 'POST':

        updated_request = request.POST.copy()
        updated_request.update({'company_name': request.user.company, 'office_location': request.user.office_location})

        
        if request.user.is_superuser:
            
            forms = article_Form(request.user, updated_request)

                
        else:

            forms = article_Form( request.user, updated_request)




        if forms.is_valid():
            a = forms.save()

            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.name}), safe=False, content_type="application/json") 

        else:
            
            error = forms.errors.as_json()
            return JsonResponse(json.dumps({'error' : error}), safe=False)
    
    else:

        forms = article_Form(request.user)
        data = company.objects.all()

        context = {
            'form': forms,
            'data' : data,
        }

        return render(request, 'store/add_article.html', context)


from transactions.models import *


@login_required(login_url='login')
@user_is_active
@csrf_exempt
def get_buily_code(request):
        
    consignor_id = request.POST.get('consignor_id')

    consignor_instance = consignor.objects.get(id = consignor_id)
    
    builty_code = consignor_instance.builty_code

    financial_year = request.session['financial_year']
    financial_year = financial_year.split('-')
    print(financial_year)
    year_1 = financial_year[0]
    year_2 = financial_year[1]

        
    # Assuming 'financial_year' is in the format 'YYYY-YYYY'
    start_date = datetime(int(year_1), 4, 1)  # April 1st of year_1
    end_date = datetime(int(year_2), 3, 31)     # March 31st of year_2

    consignor_builty_count = builty.objects.filter(
        consignor=consignor_instance, 
        DC_date__gte=start_date, 
        DC_date__lte=end_date,
        deleted=False
    ).count()

    builty_code = builty_code + '-' + str(consignor_builty_count + 1)

    return JsonResponse(json.dumps({'builty_code' : builty_code}), safe=False, content_type="application/json") 




@login_required(login_url='login')
@user_is_active
def update_article(request, article_id):

    if request.method == 'POST':

        instance = article.objects.get(id=article_id)

        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})

        forms = article_Form(request.user, updated_request, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_article')
    
    else:

        instance = article.objects.get(id=article_id)

        

        forms = article_Form(request.user, instance = instance)
        consignor_ID = instance.consignor.id

        context = {
            'form': forms,
            'comapnyID' : instance.company_name.id,
            'consignor_ID' : consignor_ID,
        }

        return render(request, 'store/update_article.html', context)


@login_required(login_url='login')
@user_is_active
def delete_article(request, company_goods_id):
    
    article.objects.get(id=company_goods_id).delete()

    return HttpResponseRedirect(reverse('list_article_delete'))


@login_required(login_url='login')
@user_is_active
def list_article(request):

    if request.user.is_superuser:

        data = article.objects.all().order_by('-id')

    else:

        data = article.objects.filter(office_location = request.user.office_location).order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_article.html', context)




@login_required(login_url='login')
@user_is_active
def add_truck_details(request):
    
    if request.method == 'POST':

        forms = truck_details_Form(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('list_truck_details')
        else:
           
            company_data = company.objects.all()

            context = {
                'form': forms,
                'company' : company_data
            }

            return render(request, 'store/add_truck_details.html', context)
    
    else:

        forms = truck_details_Form()
      
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_truck_details.html', context)





@login_required(login_url='login')
@user_is_active
@csrf_exempt
def add_truck_details_ajax(request):
    
    if request.method == 'POST':

        forms = truck_details_Form(request.POST)
        
        if forms.is_valid():
          
            a = forms.save()
            
            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.truck_number, 'owner_name' : a.truck_owner.owner_name, 'owner_id' : a.truck_owner.id}), safe=False, content_type="application/json") 

        else:
           
            error = forms.errors.as_json()

            return JsonResponse(json.dumps({'error' : error}), safe=False)

    
    else:

        forms = truck_details_Form()

        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_truck_details.html', context)


@login_required(login_url='login')
@user_is_active
def update_truck_details(request, truck_details_id):

    if request.method == 'POST':

        instance = truck_details.objects.get(id=truck_details_id)

        forms = truck_details_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_truck_details')
    
    else:

        instance = truck_details.objects.get(id=truck_details_id)

        forms = truck_details_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_truck_details.html', context)


@login_required(login_url='login')
@user_is_active
def delete_truck_details(request, truck_details_id):
    
    truck_details.objects.get(id=truck_details_id).delete()

    return HttpResponseRedirect(reverse('list_truck_details_delete'))


@login_required(login_url='login')
@user_is_active
def list_truck_details(request):
    
    data = truck_details.objects.all().order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_truck_details.html', context)

@login_required(login_url='login')
@user_is_active
def add_truck_owner(request):
    
    if request.method == 'POST':

        forms = truck_owner_Form(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('list_truck_owner')
        else:

            company_data = company.objects.all()

            context = {
                'form': forms,
                'company' : company_data
            }

            return render(request, 'store/add_truck_owner.html', context)
    
    else:

        forms = truck_owner_Form()
        
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_truck_owner.html', context)

@login_required(login_url='login')
@user_is_active
@csrf_exempt
def add_truck_owner_ajax(request):
    
    if request.method == 'POST':

        forms = truck_owner_Form(request.POST)
        if forms.is_valid():
            a = forms.save()
            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.owner_name}), safe=False, content_type="application/json") 

        else:
            
            error = forms.errors.as_json()

            return JsonResponse(json.dumps({'error' : error}), safe=False)
    
    
    else:

        forms = truck_owner_Form()

        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_truck_owner.html', context)


@login_required(login_url='login')
@user_is_active
def update_truck_owner(request, truck_owner_id):

    if request.method == 'POST':

        instance = truck_owner.objects.get(id=truck_owner_id)

        forms = truck_owner_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_truck_owner')
    
    else:

        instance = truck_owner.objects.get(id=truck_owner_id)

        forms = truck_owner_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_truck_owner.html', context)


@login_required(login_url='login')
@user_is_active
def delete_truck_owner(request, truck_owner_id):
    
    truck_owner.objects.get(id=truck_owner_id).delete()

    return HttpResponseRedirect(reverse('list_truck_owner_delete'))

@login_required(login_url='login')
@user_is_active
def list_truck_owner(request):
    
    data = truck_owner.objects.all().order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_truck_owner.html', context)


@login_required(login_url='login')
@user_is_active
def add_rate(request):
    
    if request.method == 'POST':

        forms = rate_Form(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('list_rate')
        else:

            company_data = company.objects.all()

            context = {
                'form': forms,
                'company' : company_data
            }

            return render(request, 'store/add_rate.html', context)
    
    else:

        forms = rate_Form()

        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_rate.html', context)

@login_required(login_url='login')
@user_is_active
@csrf_exempt
def add_rate_ajax(request):
    
    if request.method == 'POST':

        forms = rate_Form(request.POST)
        if forms.is_valid():
            a = forms.save()
            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.owner_name}), safe=False, content_type="application/json") 

        else:
            
            error = forms.errors.as_json()

            return JsonResponse(json.dumps({'error' : error}), safe=False)
    
    
    else:

        forms = rate_Form()
    
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_rate.html', context)


@login_required(login_url='login')
@user_is_active
def update_rate(request, rate_id):

    if request.method == 'POST':

        instance = rate.objects.get(id=rate_id)

        forms = rate_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_rate')
    
    else:

        instance = rate.objects.get(id=rate_id)

        forms = rate_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_rate.html', context)


@login_required(login_url='login')
@user_is_active
def delete_rate(request, rate_id):
    
    rate.objects.get(id=rate_id).delete()

    return HttpResponseRedirect(reverse('list_rate_delete'))


@login_required(login_url='login')
@user_is_active
def list_rate(request):
    
    data = rate.objects.all().order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_rate.html', context)


@login_required(login_url='login')
@user_is_active
def add_station(request):
    
    if request.method == 'POST':
            

        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})

        forms = station_Form(request.user, updated_request)

        if forms.is_valid():
            forms.save()
            return redirect('list_station')
        else:

            company_data = company.objects.all()

            context = {
                'form': forms,
                'company' : company_data
            }

            return render(request, 'store/add_station.html', context)
        
    else:

        forms = station_Form(user = request.user)
        
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_station.html', context)





@login_required(login_url='login')
@user_is_active
@csrf_exempt
def add_station_ajax(request):
    
    if request.method == 'POST':

        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})


        forms = station_Form(request.user, updated_request)
        if forms.is_valid():
            a = forms.save()
            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.name, 'taluka' : a.taluka.id, 'district' : a.taluka.district.id}), safe=False, content_type="application/json") 

        else:

            error = forms.errors.as_json()

            return JsonResponse(json.dumps({'error' : error}), safe=False)
    
    
    else:

        forms = station_Form(user = request.user)
        
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_station.html', context)


@login_required(login_url='login')
@user_is_active
def update_station(request, station_id):

    if request.method == 'POST':

        instance = station.objects.get(id=station_id)
        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})

        forms = station_Form(request.user, updated_request, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_station')
    
    else:

        instance = station.objects.get(id=station_id)

        forms = station_Form(request.user, instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_station.html', context)


@login_required(login_url='login')
@user_is_active
def delete_station(request, station_id):
    
    station.objects.get(id=station_id).delete()

    return HttpResponseRedirect(reverse('list_station_delete'))


@login_required(login_url='login')
@user_is_active
def list_station(request):

    if request.user.is_superuser:

        data = station.objects.all().order_by('-id')
    
    else:
    
        data = station.objects.all().order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_station.html', context)

@login_required(login_url='login')
@user_is_active
def add_from_station(request):
    
    if request.method == 'POST':
            

        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})

        forms = from_station_Form(request.user, updated_request)

        if forms.is_valid():
            forms.save()
            return redirect('list_from_station')
        else:

            company_data = company.objects.all()

            context = {
                'form': forms,
                'company' : company_data
            }

            return render(request, 'store/add_from_station.html', context)
        
    else:

        forms = from_station_Form(user = request.user)
        
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_from_station.html', context)





@login_required(login_url='login')
@user_is_active
@csrf_exempt
def add_from_station_ajax(request):
    
    if request.method == 'POST':

        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})


        forms = from_station_Form(request.user, updated_request)
        if forms.is_valid():
            a = forms.save()
            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.name, 'taluka' : a.taluka.id, 'district' : a.taluka.district.id}), safe=False, content_type="application/json") 

        else:

            error = forms.errors.as_json()

            return JsonResponse(json.dumps({'error' : error}), safe=False)
    
    
    else:

        forms = from_station_Form(user = request.user)
        
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_from_station.html', context)


@login_required(login_url='login')
@user_is_active
def update_from_station(request, from_station_id):

    if request.method == 'POST':

        instance = from_station.objects.get(id=from_station_id)
        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})

        forms = from_station_Form(request.user, updated_request, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_from_station')
    
    else:

        instance = from_station.objects.get(id=from_station_id)

        forms = from_station_Form(request.user, instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_from_station.html', context)


@login_required(login_url='login')
@user_is_active
def delete_from_station(request, from_station_id):
    
    from_station.objects.get(id=from_station_id).delete()

    return HttpResponseRedirect(reverse('list_from_station_delete'))


@login_required(login_url='login')
@user_is_active
def list_from_station(request):

    if request.user.is_superuser:

        data = from_station.objects.all().order_by('-id')
    
    else:
    
        data = from_station.objects.all().order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_from_station.html', context)



@login_required(login_url='login')
@user_is_active
def add_district(request):
    
    if request.method == 'POST':

        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})
        forms = district_Form(updated_request)

        if forms.is_valid():
            forms.save()
            return redirect('list_district')
        else:

            company_data = company.objects.all()

            context = {
                'form': forms,
                'company' : company_data
            }

            return render(request, 'store/add_district.html', context)
        
    else:

        forms = district_Form()
        
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_district.html', context)


@login_required(login_url='login')
@user_is_active
@csrf_exempt
def add_district_ajax(request):

    updated_request = request.POST.copy()
    updated_request.update({'office_location': request.user.office_location})

    if request.method == 'POST':

        if request.user.is_superuser:
            
            forms = district_Form(updated_request)

                
        else:

            updated_request.update({'company_name': request.user.company})
            forms = district_Form(updated_request)




        if forms.is_valid():
            a = forms.save()

            return JsonResponse(json.dumps({'status' : 'True'}), safe=False, content_type="application/json") 

        else:
            
            error = forms.errors.as_json()

            return JsonResponse(json.dumps({'error' : error}), safe=False)
    
    

@login_required(login_url='login')
@user_is_active
def update_district(request, district_id):

    if request.method == 'POST':

        instance = district.objects.get(id=district_id)

        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})

        forms = district_Form(updated_request, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_district')
    
    else:

        instance = district.objects.get(id=district_id)

        forms = district_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_district.html', context)


@login_required(login_url='login')
@user_is_active
def delete_district(request, district_id):
    
    district.objects.get(id=district_id).delete()

    return HttpResponseRedirect(reverse('list_district_delete'))


@login_required(login_url='login')
@user_is_active
def list_district(request):
    
    data = district.objects.all().order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_district.html', context)

@login_required(login_url='login')
@user_is_active
def add_taluka(request):
    
    if request.method == 'POST':

        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})
        forms = taluka_Form(request.user, updated_request)


        if forms.is_valid():
            forms.save()
            return redirect('list_taluka')
        else:

            company_data = company.objects.all()



            context = {
                        'form': forms,
                        'company' : company_data
                    }

            return render(request, 'store/add_taluka.html', context)
    
    else:

        forms = taluka_Form(request.user)
    
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_taluka.html', context)



@login_required(login_url='login')
@user_is_active
@csrf_exempt
def add_taluka_ajax(request):
    
    if request.method == 'POST':

        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})

        forms = taluka_Form(request.user, updated_request)
        if forms.is_valid():
            a = forms.save()
           
            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.name, 'district_id' : a.district.id, 'district_name' : a.district.name}), safe=False, content_type="application/json") 



        else:
            
            
            error = forms.errors.as_json()
            return JsonResponse(json.dumps({'error' : error}), safe=False)
    
    

@login_required(login_url='login')
@user_is_active
def update_taluka(request, taluka_id):

    if request.method == 'POST':

        instance = taluka.objects.get(id=taluka_id)
        updated_request = request.POST.copy()
        updated_request.update({'office_location': request.user.office_location})
        forms = taluka_Form(request.user, updated_request, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_taluka')
        else:
            
            context = {
                'form': forms
            }

            return render(request, 'store/add_taluka.html', context)
    else:

        instance = taluka.objects.get(id=taluka_id)

        forms = taluka_Form(request.user, instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_taluka.html', context)


@login_required(login_url='login')
@user_is_active
def delete_taluka(request, taluka_id):
    
    taluka.objects.get(id=taluka_id).delete()

    return HttpResponseRedirect(reverse('list_taluka_delete'))


@login_required(login_url='login')
@user_is_active
def list_taluka(request):

    if request.user.is_superuser:

        data = taluka.objects.all().order_by('-id')
    
    else:

        data = taluka.objects.all().order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_taluka.html', context)


@login_required(login_url='login')
@user_is_active
def add_onaccount(request):
    
    if request.method == 'POST':
        
        updated_request = request.POST.copy()
        updated_request.update({'company': request.user.company, 'office_location': request.user.office_location})
        forms = onaccount_Form(updated_request)
        if forms.is_valid():
            forms.save()
            return redirect('list_onaccount')
        else:

            company_data = company.objects.all()

            context = {
                'form': forms,
                'company' : company_data
            }

            return render(request, 'store/add_onaccount.html', context)
    
    else:

        forms = onaccount_Form()
       
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_onaccount.html', context)


@login_required(login_url='login')
@user_is_active
@csrf_exempt
def add_onaccount_ajax(request):
    
    if request.method == 'POST':

            
        updated_request = request.POST.copy()
        updated_request.update({'company': request.user.company, 'office_location': request.user.office_location})
        forms = onaccount_Form(updated_request)

        if request.user.is_superuser:
            
            forms = onaccount_Form(updated_request)

                
        else:

            updated_request.update({'company': request.user.company})
            forms = onaccount_Form(updated_request)


        
        if forms.is_valid():
            a = forms.save()
            
            
            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.name}), safe=False, content_type="application/json") 

        else:


            error = forms.errors.as_json()

            return JsonResponse(json.dumps({'error' : error}), safe=False)
    
    
    else:

        forms = onaccount_Form()

        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_onaccount.html', context)


@login_required(login_url='login')
@user_is_active
def update_onaccount(request, onaccount_id):

    if request.method == 'POST':

        instance = onaccount.objects.get(id=onaccount_id)
        
        updated_request = request.POST.copy()
        updated_request.update({'company': request.user.company, 'office_location': request.user.office_location})
        
        forms = onaccount_Form(updated_request, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_onaccount')
        else:
            context = {
                
                'form': forms
            }

            return render(request, 'store/add_onaccount.html', context)

    else:

        instance = onaccount.objects.get(id=onaccount_id)

        forms = onaccount_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_onaccount.html', context)


@login_required(login_url='login')
@user_is_active
def delete_onaccount(request, onaccount_id):
    
    onaccount.objects.get(id=onaccount_id).delete()

    return HttpResponseRedirect(reverse('list_onaccount_delete'))


@login_required(login_url='login')
@user_is_active
def list_onaccount(request):

    if request.user.is_superuser:

        data = onaccount.objects.all().order_by('-id')

    else:
    
        data = onaccount.objects.filter(office_location = request.user.office_location).order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_onaccount.html', context)

@login_required(login_url='login')
@user_is_active
def add_driver(request):
    
    if request.method == 'POST':

        forms = driver_Form(request.POST)
        
        if forms.is_valid():
            forms.save()
            return redirect('list_driver')
        else:

            company_data = company.objects.all()

            context = {
                'form': forms,
                'company' : company_data
            }

            return render(request, 'store/add_driver.html', context)
        
    else:

        forms = driver_Form()

        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_driver.html', context)

@login_required(login_url='login')
@user_is_active
def update_driver(request, driver_id):

    if request.method == 'POST':

        instance = driver.objects.get(id=driver_id)

        forms = driver_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_driver')
    
    else:

        instance = driver.objects.get(id=driver_id)

        forms = driver_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_driver.html', context)


@login_required(login_url='login')
@user_is_active
def delete_driver(request, driver_id):
    
    driver.objects.get(id=driver_id).delete()

    return HttpResponseRedirect(reverse('list_driver_delete'))


@login_required(login_url='login')
@user_is_active
def list_driver(request):
    
    data = driver.objects.all().order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_driver.html', context)


@login_required(login_url='login')
@user_is_active
def add_petrol_pump(request):
    
    if request.method == 'POST':

        forms = petrol_pump_Form(request.POST)
        
        if forms.is_valid():
            forms.save()
            return redirect('list_petrol_pump')
        else:
           
            company_data = company.objects.all()

            context = {
                'form': forms,
                'company' : company_data
            }

            return render(request, 'store/add_petrol_pump.html', context)
        
    else:

        forms = petrol_pump_Form()

        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_petrol_pump.html', context)


@login_required(login_url='login')
@user_is_active
@csrf_exempt
def add_petrol_pump_ajax(request):
    
    if request.method == 'POST':
    
        forms = petrol_pump_Form(request.POST)


        
        if forms.is_valid():
            a = forms.save()
            
            
            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.name}), safe=False, content_type="application/json") 

        else:


            error = forms.errors.as_json()

            return JsonResponse(json.dumps({'error' : error}), safe=False)
    
    
    else:

        forms = petrol_pump_Form()

        context = {
            'form': forms,
        }

        return render(request, 'store/add_petrol_pump.html', context)


@login_required(login_url='login')
@user_is_active
def update_petrol_pump(request, petrol_pump_id):

    if request.method == 'POST':

        instance = petrol_pump.objects.get(id=petrol_pump_id)

        forms = petrol_pump_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_petrol_pump')
    
    else:

        instance = petrol_pump.objects.get(id=petrol_pump_id)

        forms = petrol_pump_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_petrol_pump.html', context)


@login_required(login_url='login')
@user_is_active
def delete_petrol_pump(request, petrol_pump_id):
    
    petrol_pump.objects.get(id=petrol_pump_id).delete()

    return HttpResponseRedirect(reverse('list_petrol_pump_delete'))


@login_required(login_url='login')
@user_is_active
def list_petrol_pump(request):
    
    data = petrol_pump.objects.all().order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'store/list_petrol_pump.html', context)



# delete view

     

@login_required(login_url='login')
@user_is_active
def list_company_delete(request):

    data = company.objects.all().order_by('-id')

    context = {
        'data': data
    }

    return render(request, 'delete/list_company_delete.html', context)



@login_required(login_url='login')
@user_is_active
def list_company_goods_delete(request):
    
    data = company_goods.objects.all().order_by('company__company_name')

    context = {
            'data': data
        }


    return render(request, 'delete/list_company_goods_delete.html', context)



@login_required(login_url='login')
@user_is_active
def list_goods_company_delete(request):
    
    data = goods_company.objects.all().order_by('company_name__company_name')

    context = {
            'data': data
        }


    return render(request, 'delete/list_goods_company_delete.html', context)




@login_required(login_url='login')
@user_is_active
def list_agent_delete(request):
    
    data = agent.objects.all().order_by('-id')

    context = {
            'data': data
        }


    return render(request, 'delete/list_agent_delete.html', context)

