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
    print('i am here3')

    if request.method == "POST":
        company_id = request.POST['company_id']
        print(company_id)
        try:
            company_instance = company.objects.get(id= company_id)
            dropdown1 = consignor.objects.filter(company = company_instance)
            print('---------dropdown1')
            print(dropdown1)
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

    print('--------------')
    print(date1)
    return date1


@login_required(login_url='login')
@user_is_active
def get_company_goods_ajax(request):

    data = []
    

    if request.method == "POST":
        company_id = request.POST['company_id']
        print('----here----')
        print(company_id)
        try:
            instance = company.objects.filter(id = company_id).first()
            dropdown1 = company_goods.objects.filter(company = instance)
            print(dropdown1)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(dropdown1.values('id', 'name')), safe = False) 


@login_required(login_url='login')
@user_is_active
def get_goods_company_ajax(request):

    data = []
    print('i am here3')

    if request.method == "POST":
        company_id = request.POST['company_id']
        company_goods_id = request.POST['company_goods']
        print(company_id)
        try:
            company_instance = company.objects.get(id= company_id)
            instance = company_goods.objects.filter(id = company_goods_id).first()
            print(instance)
            dropdown1 = goods_company.objects.filter(company_goods = instance, company_name= company_instance)
            print(dropdown1)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(dropdown1.values('id', 'goods_company_name')), safe = False) 


@login_required(login_url='login')
@user_is_active
def get_agent_company_ajax(request):

    data = []
    print('i am here2')

    if request.method == "POST":
        company_id = request.POST['company_id']
        print(company_id)
        try:
            company_instance = company.objects.get(id= company_id)
            print(company_instance)
            
            agent_data = agent.objects.filter(company = company_instance)
            print(agent_data)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(agent_data.values('id', 'name')), safe = False) 



@login_required(login_url='login')
@user_is_active
def add_company(request):

    if request.method == 'POST':

        forms = company_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_company')
        else:
            print(forms.errors)
    
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
            print(forms.errors)
    
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

    data = company.objects.all()

    context = {
        'data': data
    }

    return render(request, 'store/list_company.html', context)



@login_required(login_url='login')
@user_is_active
def add_consignor(request):
    
    if request.method == 'POST':

        forms = consignor_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_consignor')
        else:
            print(forms.errors)
            return redirect('add_consignor')
    
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

        print('------------------------------------')

        forms = consignor_Form(request.POST)
        print(request.POST)


        if forms.is_valid():
            a = forms.save()

            print(a)

         
            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.name}), safe=False, content_type="application/json") 

        else:
            error = forms.errors.as_json()
            print(error)
            return JsonResponse({'error' : error}, safe=False)
    
    else:

        print('-------------------1-----------------')


        forms = consignor_Form()

        context = {
            'form': forms
        }

        return render(request, 'store/add_consignor.html', context)


@user_is_active
def update_consignor(request, consignor_id):

    if request.method == 'POST':

        instance = consignor.objects.get(id=consignor_id)

        forms = consignor_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_consignor')

        else:
            print(forms.errors)
    
    else:

        instance = consignor.objects.get(id=consignor_id)

        forms = consignor_Form(instance = instance)

        comapnyID = instance.company.id
        comapny_consignor_ID = instance.id

        print(comapnyID)
        print(comapny_consignor_ID)

        context = {
            'form': forms,
            'comapnyID' : comapnyID,
            'comapny_consignor_ID' : comapny_consignor_ID
            
        }

        return render(request, 'store/update_consignor.html', context)


@login_required(login_url='login')
@user_is_active
def delete_consignor(request, consignor_id):
    
    consignor.objects.get(id=consignor_id).delete()

    return HttpResponseRedirect(reverse('list_consignor_delete'))


@login_required(login_url='login')
@user_is_active
def list_consignor(request):
    
    data = consignor.objects.all().order_by('company__company_name')

    context = {
            'data': data
        }


    return render(request, 'store/list_consignor.html', context)



@login_required(login_url='login')
@user_is_active
def add_article(request):
    
    if request.method == 'POST':

        forms = article_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_article')
        else:
            print(forms.errors)
            return redirect('list_article')
    
    else:

        forms = article_Form()
        data = company.objects.all()
        print(data)

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

        print()

        forms = article_Form(request.POST)

        if forms.is_valid():
            a = forms.save()

            print(a)
            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.name}), safe=False, content_type="application/json") 

        else:
            
            error = forms.errors.as_json()
            print(error)
            return JsonResponse({'error' : error}, safe=False)
    
    else:

        forms = article_Form()
        data = company.objects.all()
        print(data)

        context = {
            'form': forms,
            'data' : data,
        }

        return render(request, 'store/add_article.html', context)

@login_required(login_url='login')
@user_is_active
def update_article(request, article_id):

    if request.method == 'POST':

        instance = article.objects.get(id=article_id)

        forms = article_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_article')
    
    else:

        instance = article.objects.get(id=article_id)

        

        forms = article_Form(instance = instance)
        consignor_ID = instance.consignor.id

        print('-----------------')
        print(instance.company_name.id)

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
    
    data = article.objects.all().order_by('company_name__company_name')

    context = {
            'data': data
        }


    return render(request, 'store/list_article.html', context)




@login_required(login_url='login')
@user_is_active
def add_truck_details(request):
    
    if request.method == 'POST':

        forms = truck_details_Form(request.POST)
        print('-----------------------------1---------------------')
        if forms.is_valid():
            forms.save()
            return redirect('list_truck_details')
        else:
            print('-----------------------------2---------------------')

            print(forms.errors)
            return redirect('list_truck_details')
    
    else:

        forms = truck_details_Form()
        print('--------------------------------------------------')

        
        print(forms)
        print('-----------------------------3---------------------')

        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_truck_details.html', context)





@login_required(login_url='login')
@user_is_active
def add_truck_details_ajax(request):
    
    if request.method == 'POST':

        forms = truck_details_Form(request.POST)
        print('-----------------------------1---------------------')
        if forms.is_valid():
            a = forms.save()
            return JsonResponse(json.dumps({'status' : 'True', 'id' : a.id,'value' : a.truck_number}), safe=False, content_type="application/json") 

        else:
            print('-----------------------------2---------------------')

            
            error = forms.errors.as_json()
            print(error)
            return JsonResponse({'error' : error}, safe=False)
    
    
    else:

        forms = truck_details_Form()
        print('--------------------------------------------------')

        
        print(forms)
        print('-----------------------------3---------------------')

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
    
    data = truck_details.objects.all()

    context = {
            'data': data
        }


    return render(request, 'store/list_truck_details.html', context)

@login_required(login_url='login')
@user_is_active
def add_truck_owner(request):
    
    if request.method == 'POST':

        forms = truck_owner_Form(request.POST)
        print('-----------------------------1---------------------')
        if forms.is_valid():
            forms.save()
            return redirect('list_truck_owner')
        else:
            print('-----------------------------2---------------------')

            print(forms.errors)
            return redirect('list_truck_owner')
    
    else:

        forms = truck_owner_Form()
        print('--------------------------------------------------')

        
        print(forms)
        print('-----------------------------3---------------------')

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
    
    data = truck_owner.objects.all()

    context = {
            'data': data
        }


    return render(request, 'store/list_truck_owner.html', context)


@login_required(login_url='login')
@user_is_active
def add_station(request):
    
    if request.method == 'POST':

        forms = station_Form(request.POST)
        print('-----------------------------1---------------------')
        if forms.is_valid():
            forms.save()
            return redirect('list_station')
        else:
            print('-----------------------------2---------------------')

            print(forms.errors)
            return redirect('list_station')
    
    else:

        forms = station_Form()
        print('--------------------------------------------------')

        
        print(forms)
        print('-----------------------------3---------------------')

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

        forms = station_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_station')
    
    else:

        instance = station.objects.get(id=station_id)

        forms = station_Form(instance = instance)

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
    
    data = station.objects.all()

    context = {
            'data': data
        }


    return render(request, 'store/list_station.html', context)



@login_required(login_url='login')
@user_is_active
def add_district(request):
    
    if request.method == 'POST':

        forms = district_Form(request.POST)
        print('-----------------------------1---------------------')
        if forms.is_valid():
            forms.save()
            return redirect('list_district')
        else:
            print('-----------------------------2---------------------')

            print(forms.errors)
            return redirect('list_district')
    
    else:

        forms = district_Form()
        print('--------------------------------------------------')

        
        print(forms)
        print('-----------------------------3---------------------')

        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_district.html', context)


@login_required(login_url='login')
@user_is_active
def update_district(request, district_id):

    if request.method == 'POST':

        instance = district.objects.get(id=district_id)

        forms = district_Form(request.POST, instance = instance)

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
    
    data = district.objects.all()

    context = {
            'data': data
        }


    return render(request, 'store/list_district.html', context)

@login_required(login_url='login')
@user_is_active
def add_taluka(request):
    
    if request.method == 'POST':

        forms = taluka_Form(request.POST)
        print('-----------------------------1---------------------')
        if forms.is_valid():
            forms.save()
            return redirect('list_taluka')
        else:
            print('-----------------------------2---------------------')

            print(forms.errors)
            return redirect('list_taluka')
    
    else:

        forms = taluka_Form()
        print('--------------------------------------------------')

        
        print(forms)
        print('-----------------------------3---------------------')

        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_taluka.html', context)


@login_required(login_url='login')
@user_is_active
def update_taluka(request, taluka_id):

    if request.method == 'POST':

        instance = taluka.objects.get(id=taluka_id)

        forms = taluka_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_taluka')
    
    else:

        instance = taluka.objects.get(id=taluka_id)

        forms = taluka_Form(instance = instance)

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
    
    data = taluka.objects.all()

    context = {
            'data': data
        }


    return render(request, 'store/list_taluka.html', context)


@login_required(login_url='login')
@user_is_active
def add_onaccount(request):
    
    if request.method == 'POST':

        forms = onaccount_Form(request.POST)
        print('-----------------------------1---------------------')
        if forms.is_valid():
            forms.save()
            return redirect('list_onaccount')
        else:
            print('-----------------------------2---------------------')

            print(forms.errors)
            return redirect('list_onaccount')
    
    else:

        forms = onaccount_Form()
        print('--------------------------------------------------')

        
        print(forms)
        print('-----------------------------3---------------------')

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

        forms = onaccount_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_onaccount')
    
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
    
    data = onaccount.objects.all()

    context = {
            'data': data
        }


    return render(request, 'store/list_onaccount.html', context)



# delete view

     

@login_required(login_url='login')
@user_is_active
def list_company_delete(request):

    data = company.objects.all()

    context = {
        'data': data
    }

    return render(request, 'delete/list_company_delete.html', context)


@login_required(login_url='login')
@user_is_active
def list_company_delete(request):

    data = company.objects.all()

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
    
    data = agent.objects.all()

    context = {
            'data': data
        }


    return render(request, 'delete/list_agent_delete.html', context)

