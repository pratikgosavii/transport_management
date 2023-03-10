import django_filters
from django_filters import DateFilter, CharFilter
from django.forms.widgets import DateInput
from django import forms

from .models import *
from .forms import *




class builty_filter(django_filters.FilterSet):

    consignor = django_filters.ModelChoiceFilter(
        queryset=consignor.objects.all(),
        widget=forms.Select(
            attrs={
                'class' : 'form-control',
                'id' : 'company'
            })
    )

    article = django_filters.ModelChoiceFilter(
        queryset=article.objects.all(),
        widget=forms.Select(
            attrs={
                'class' : 'form-control',
                'id' : 'company'
            })
    )
   
    truck_details = django_filters.ModelChoiceFilter(
        queryset=truck_details.objects.all(),
        widget=forms.Select(
            attrs={
                'class' : 'form-control',
                'id' : 'company'
            })
    )
    truck_owner = django_filters.ModelChoiceFilter(
        queryset=truck_owner.objects.all(),
        widget=forms.Select(
            attrs={
                'class' : 'form-control',
                'id' : 'company'
            })
    )
    builty_no = django_filters.NumberFilter(
        widget=forms.NumberInput(
            attrs={
                'class' : 'form-control',
                'id' : 'company'
            })
    )

    

    DC_date_start__date = django_filters.NumberFilter( lookup_expr='year__gt')
    DC_date_end__date = django_filters.NumberFilter( lookup_expr='year__lt')


    class Meta:
        model = builty
        fields = ['company', 'consignor', 'builty_no']
       
   

class request_edit_filter(django_filters.FilterSet):

    
    builty_no = django_filters.NumberFilter(
        widget=forms.NumberInput(
            attrs={
                'class' : 'form-control',
                'id' : 'builty_no'
            })
    )

    
    class Meta:
        model = request_edit
        fields = ['builty_no', 'status']
       
   