from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import *


from store.models import *
from users.models import *

from transactions.filters import *


from django.db.models.functions import Substr

from django.core.paginator import Paginator, EmptyPage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




from django.db.models.functions import Substr

from django.db.models import Sum


@login_required(login_url='login')
def dashboard(request):

    financial_year = request.session.get('financial_year', '2025-2026')

    if request.user.is_superuser:

        builty_count = builty.objects.all().count()

    else:
        builty_count = builty.objects.filter(user = request.user).count()

    truck_count = truck_details.objects.all().count()
    user_count = User.objects.all().count()
    builty_data = None
    builty_filters = None
    total1_freight = None
    total1_advance = None
    total1_balance = None
    total1_mt = None
    total_freight = None
    total_advance = None
    total_balance = None
    total_mt = None
    data = None

    if request.user.is_superuser:
        builty_data = builty.objects.all().order_by('-id')

        # total1_freight = 0
        # total1_advance = 0
        # total1_balance = 0
        # total1_mt = 0

        # for i in builty_data:

        #     if not i.have_ack.filter():


        #         total1_balance = total1_balance + i.balance

        #     total1_freight = total1_freight + i.freight
        #     total1_advance = total1_advance + i.less_advance
        #     total1_mt = total1_mt + i.mt

        total1_freight = builty_data.aggregate(Sum('freight'))['freight__sum']
        total1_advance = builty_data.aggregate(Sum('less_advance'))['less_advance__sum']
        total1_mt = builty_data.aggregate(Sum('mt'))['mt__sum']
        total1_balance = builty_data.filter(have_ack__isnull = True).aggregate(Sum('balance'))['balance__sum']


        builty_filters = builty_filter(request.user, request.GET, queryset=builty_data, request=request)

        data = builty_filters.qs


        total_freight = 0
        total_advance = 0
        total_balance = 0
        total_mt = 0




        total_freight = data.aggregate(Sum('freight'))['freight__sum']
        total_advance = data.aggregate(Sum('less_advance'))['less_advance__sum']
        total_mt = data.aggregate(Sum('mt'))['mt__sum']
        total_balance = data.filter(have_ack__isnull = True).aggregate(Sum('balance'))['balance__sum']




        page = request.GET.get('page', 1)
        paginator = Paginator(data, 20)

        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)


        if total_balance:
            total_balance = round(total_balance, 2)
        if total_freight:
            total_freight = round(total_freight, 2)
        if total_advance:
            total_advance = round(total_advance, 2)
        if total_mt:
            total_mt = round(total_mt, 2)

        if total1_balance:
            total1_balance = round(total_balance, 2)
        if total1_freight:
            total1_freight = round(total_freight, 2)
        if total1_advance:
            total1_advance = round(total_advance, 2)
        if total_mt:
            total1_mt = round(total_mt, 2)


    context = {

        'data': data,
        'financial_year': financial_year,
        'builty_filter' : builty_filters,
        'truck_count': truck_count,
        'builty_count': builty_count,
        'user_count': user_count,
        'total_freight' : total_freight,
        'total_advance' : total_advance,
        'total_balance' : total_balance,
        'total1_freight' : total1_freight,
        'total1_advance' : total1_advance,
        'total1_balance' : total1_balance,
        'total_mt' : total_mt,
        'total1_mt' : total1_mt,
        'form' : builty_Form(request.user),

    }
    return render(request, 'dashboard.html', context)

