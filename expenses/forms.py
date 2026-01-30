from django import forms

from .models import *
from store.models import mechanic, vendor
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.forms.widgets import DateTimeInput


class expense_category_Form(forms.ModelForm):
    class Meta:
        model = expense_category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            
        }



class employee_Form(forms.ModelForm):
    class Meta:
        model = employee
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'address'
            }),
             'mobile_no': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'mobile_no'
            }),
            
        }

class closing_balance_Form(forms.ModelForm):
    class Meta:
        model = closing_balance
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control', 'id': 'user'
            }),
            'closing_balance': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'closing_balance'
            }),
            
            'date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),

            
        }



class builty_expense_Form(forms.ModelForm):
    class Meta:
        model = builty_expense
        fields = '__all__'
        widgets = {

            'builty': forms.Select(attrs={
                'class': 'form-control', 'id': 'builty'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount'
            }),
          
            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

      

        def __init__(self, *args, **kwargs):
            super(builty_expense_Form, self).__init__(*args, **kwargs)
            self.fields['entry_date'].required = False
            self.fields['user'].required = False




class truck_expense_Form(forms.ModelForm):
    class Meta:
        model = truck_expense
        fields = '__all__'
        widgets = {
            'expense_type': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'expense_type'
            }),
            'note': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'note',
                'placeholder': 'Enter note (optional)...'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount',
                'step': '0.01', 'min': '0'
            }),
            'truck': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'truck'
            }),
            # Tyre expense fields
            'tyre_no': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'tyre_no',
                'placeholder': 'Enter tyre number...'
            }),
            'pattern': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'pattern'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'type'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'company',
                'placeholder': 'Enter company name...'
            }),
            'driver': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'driver'
            }),
            # Mechanic/Spare part expense fields
            'mechanic': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'mechanic',
                'placeholder': 'Select mechanic...'
            }),
            'mechanic_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'mechanic_name',
                'placeholder': 'Enter mechanic name...'
            }),
            'spare_part_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'spare_part_name',
                'placeholder': 'Enter spare part name...'
            }),
            'labour_cost': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'labour_cost',
                'step': '0.01', 'min': '0', 'placeholder': '0.00'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'cost',
                'step': '0.01', 'min': '0', 'placeholder': '0.00'
            }),
            'work_description': forms.Textarea(attrs={
                'class': 'form-control', 'id': 'work_description',
                'rows': 3, 'placeholder': 'Enter work description...'
            }),
            # Common fields
            'vendor': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'vendor'
            }),
            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(truck_expense_Form, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['entry_date'].required = False
        self.fields['expense_type'].required = True
        # Tyre fields
        self.fields['tyre_no'].required = False
        self.fields['pattern'].required = False
        self.fields['type'].required = False
        self.fields['company'].required = False
        self.fields['driver'].required = False
        # Mechanic: filter by current user's office_location
        if request and getattr(request.user, 'office_location', None):
            self.fields['mechanic'].queryset = mechanic.objects.filter(office_location=request.user.office_location).order_by('name')
            self.fields['vendor'].queryset = vendor.objects.filter(office_location=request.user.office_location).order_by('name')
        # Mechanic fields
        self.fields['mechanic'].required = False
        self.fields['spare_part_name'].required = False
        self.fields['labour_cost'].required = False
        self.fields['cost'].required = False
        self.fields['work_description'].required = False
        # Common fields
        self.fields['vendor'].required = False
        self.fields['note'].required = False

class diesel_expense_Form(forms.ModelForm):
    class Meta:
        model = diesel_expense
        fields = '__all__'
        widgets = {
            'builty': forms.Select(attrs={
                'class': 'form-control', 'id': 'builty'
            }),
            'note': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'note'
            }),
            'liter': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'liter'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount'
            }),
            'diesel': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'diesel'
            }),
            
            

            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(diesel_expense_Form, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['entry_date'].required = False

class truck_diesel_expense_Form(forms.ModelForm):
    class Meta:
        model = truck_diesel_expense
        fields = '__all__'
        widgets = {
            'truck': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'truck'
            }),
            'note': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'note'
            }),
            'liter': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'liter'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount'
            }),
            'diesel': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'diesel'
            }),
            
            

            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(truck_diesel_expense_Form, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['entry_date'].required = False

class diesel_expense_Form(forms.ModelForm):
    class Meta:
        model = diesel_expense
        fields = '__all__'
        widgets = {
            'builty': forms.Select(attrs={
                'class': 'form-control', 'id': 'builty'
            }),
            'note': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'note'
            }),
            'liter': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'liter'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount'
            }),
            'diesel': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'diesel'
            }),
            
            

            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(diesel_expense_Form, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['entry_date'].required = False

class transfer_fund_Form(forms.ModelForm):
    class Meta:
        model = transfer_fund
        fields = '__all__'
        widgets = {
            'note': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'note'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount'
            }),
            'transfer_to_user': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'transfer_to_user'
            }),
            
            

            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(transfer_fund_Form, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['entry_date'].required = False


class other_expense_Form(forms.ModelForm):
    class Meta:
        model = other_expense
        fields = '__all__'
        widgets = {
            
            'expense_category': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'expense_category'
            }),
            'note': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'note'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'salary'
            }),
            'user': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'user'
            }),
           
            
            
            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(other_expense_Form, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['entry_date'].required = False


class salary_Form(forms.ModelForm):
    class Meta:
        model = salary
        fields = '__all__'
        widgets = {
            'note': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'note'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'salary'
            }),
            'employee': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'employee'
            }),
           
            
            'salary_of_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(salary_Form, self).__init__(*args, **kwargs)
        self.fields['entry_date'].required = False
        self.fields['user'].required = False




class fund_Form(forms.ModelForm):
    class Meta:
        model = fund
        fields = '__all__'
        widgets = {

            'user': forms.Select(attrs={
                'class': 'form-control', 'id': 'user'
            }),
            'note': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'note'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount'
            }),
          
           
            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

      

        def __init__(self, *args, **kwargs):
            super(fund_Form, self).__init__(*args, **kwargs)
            self.fields['entry_date'].required = False



