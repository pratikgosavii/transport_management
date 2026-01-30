from django import forms

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.forms.widgets import DateTimeInput


class company_Form(forms.ModelForm):
    class Meta:
        model = company
        fields = ['company_name']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            
        }


class office_location_Form(forms.ModelForm):
    class Meta:
        model = office_location
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            
        }



class consignor_Form(forms.ModelForm):
    class Meta:
        model = consignor
        fields = '__all__'
        widgets = {
            'company': forms.Select(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'builty_code': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'builty_code'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            
           
     
            
        }

   

class onaccount_Form(forms.ModelForm):
    class Meta:
        model = onaccount
        fields = '__all__'
        widgets = {
            'company': forms.Select(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            
            
        }

class district_Form(forms.ModelForm):
    class Meta:
        model = district
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            
            
        }

class taluka_Form(forms.ModelForm):
    class Meta:
        model = taluka
        fields = '__all__'
        widgets = {
            'district': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'district'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            
            
        }

         
    def __init__(self, user, *args, **kwargs):
        self.user = user  
        super(taluka_Form,self).__init__(*args, **kwargs)

        if not user.is_superuser:
            self.fields['district'].queryset = district.objects.filter(office_location = self.user.office_location)
        

class station_Form(forms.ModelForm):
    class Meta:
        model = station
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'taluka': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'sfgfsddsf'
            }),
            
            
        }



    def __init__(self, user, *args, **kwargs):
        self.user = user  
        super(station_Form,self).__init__(*args, **kwargs)

        if not self.user.is_superuser:
            self.fields['taluka'].queryset = taluka.objects.filter(office_location = self.user.office_location)
        

class from_station_Form(forms.ModelForm):
    class Meta:
        model = from_station
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'taluka': forms.Select(attrs={
                'id': 'sdsddsd',
                'class' : 'se sele',
            }),
            
            
        }



    def __init__(self, user, *args, **kwargs):
        self.user = user  
        super(from_station_Form,self).__init__(*args, **kwargs)

        if not self.user.is_superuser:
            self.fields['taluka'].queryset = taluka.objects.filter(office_location = self.user.office_location)
        

class article_Form(forms.ModelForm):
    class Meta:
        model = article
        fields = '__all__'
        widgets = {
            'company_name': forms.Select(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'consignor': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'consignor_id'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
           
            
        }

    
    def __init__(self, user, *args, **kwargs):
        self.user = user  
        super(article_Form,self).__init__(*args, **kwargs)

        if not self.user.is_superuser:
            self.fields['consignor'].queryset = consignor.objects.filter(office_location = self.user.office_location)
        

class truck_details_Form(forms.ModelForm):
    class Meta:
        model = truck_details
        fields = '__all__'
        widgets = {
            'truck_owner': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'gfghjkjhgc'
            }),
            'truck_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'insurance_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'permit_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'puc_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'fitness': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'company'
            }),
        }
           

class truck_owner_Form(forms.ModelForm):
    class Meta:
        model = truck_owner
        fields = '__all__'
        widgets = {
           
            'owner_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'bank_acc': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'pan_card': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'pan_card'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'mobile_number': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
            

        }
           

class rate_Form(forms.ModelForm):
    class Meta:
        model = rate
        fields = '__all__'
        widgets = {
           
            'from_station': forms.Select(attrs={
                'class': 'form-control', 'id': 'truck_owner'
            }),
            'to_station': forms.Select(attrs={
                'class': 'form-control', 'id': 'truck_owner'
            }),
            
            'company_rate': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
        }
           

class petrol_pump_Form(forms.ModelForm):
    class Meta:
        model = petrol_pump
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
            

        }
           

class driver_Form(forms.ModelForm):
    class Meta:
        model = driver
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
            'adhar_card': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
            'driving_licence': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'driving_licence'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
            'mobile_no': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
            
            'driving_licence_expiry_date': DateTimeInput(attrs={'type': 'date', 'class' : 'form-control date_css'}, format = '%Y-%m-%d'),

        }


class vendor_Form(forms.ModelForm):
    class Meta:
        model = vendor
        fields = ['name', 'address', 'mobile_number', 'gst_number']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'vendor_name',
                'placeholder': 'Vendor name'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'vendor_address',
                'placeholder': 'Address (optional)'
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'vendor_mobile',
                'placeholder': 'Mobile (optional)'
            }),
            'gst_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'vendor_gst',
                'placeholder': 'GST number (optional)'
            }),
        }


class mechanic_Form(forms.ModelForm):
    class Meta:
        model = mechanic
        fields = ['name', 'mobile_number']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'mechanic_name',
                'placeholder': 'Mechanic name'
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'mechanic_mobile',
                'placeholder': 'Mobile (optional)'
            }),
        }


class tyre_Form(forms.ModelForm):
    class Meta:
        model = tyre
        fields = '__all__'
        widgets = {
            'tyre_no': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'tyre_no'
            }),
            'pattern': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'tyre_pattern'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'tyre_type'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'tyre_company'
            }),
            'driver': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'tyre_driver'
            }),
            'vendor': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'tyre_vendor'
            }),
        }
            