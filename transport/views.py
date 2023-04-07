from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import *


from store.models import *
from users.models import *

from transactions.filters import *


from django.db.models.functions import Substr

from django.core.paginator import Paginator, EmptyPage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='login')
def dashboard(request):

    
    builty_count = builty.objects.all().count()
    truck_count = truck_details.objects.all().count()
    user_count = User.objects.all().count()

    if request.user.is_superuser:
        builty_data = builty.objects.all().order_by('-id')
    else:
        builty_data = None

    total1_freight = 0
    total1_advance = 0
    total1_balance = 0
    total1_mt = 0

    for i in builty_data:

        if not i.have_ack.filter():


            total1_balance = total1_balance + i.balance

        total1_freight = total1_freight + i.freight
        total1_advance = total1_advance + i.less_advance
        total1_mt = total1_mt + i.mt

    builty_filters = builty_filter(request.GET, queryset=builty_data)
    
    data = builty_filters.qs


    total_freight = 0
    total_advance = 0
    total_balance = 0
    total_mt = 0

    for i in data:

        if not i.have_ack.filter():
       
            total_balance = total_balance + i.balance

        total_freight = total_freight + i.freight
        total_advance = total_advance + i.less_advance
        total_mt = total_mt + i.mt

    total_balance = round(total_balance, 2)
    total_advance = round(total_advance, 2)
    total_freight = round(total_freight, 2)
    total1_freight = round(total1_freight, 2)
    total_mt = round(total_mt, 2)
    total1_balance = round(total1_balance, 2)
    total1_advance = round(total1_advance, 2)
    total1_mt = round(total1_mt, 2)


    page = request.GET.get('page', 1)
    paginator = Paginator(data, 20)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
   
    context = {
        
        'data': builty_data,
        'data' : builty_filters.qs,
        'builty_filter' : builty_filters,
        'truck_count': truck_count,
        'builty_count': builty_count,
        'user_count': user_count,
        'user_count': user_count, 'total_freight' : total_freight,
        'total_advance' : total_advance,
        'total_balance' : total_balance,
        'total1_freight' : total1_freight,
        'total1_advance' : total1_advance,
        'total1_balance' : total1_balance,
        'total_mt' : total_mt,
        'total1_mt' : total1_mt,
    }
    return render(request, 'dashboard.html', context)
