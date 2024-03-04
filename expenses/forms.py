from django import forms

from .models import *
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



class builty_expense_Form(forms.ModelForm):
    class Meta:
        model = builty_expense
        fields = '__all__'
        widgets = {

            'builty': forms.Select(attrs={
                'class': 'form-control', 'id': 'builty'
            }),
            'note': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'note'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount'
            }),
          
           
            

           
            'expense_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            'payment_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
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
            'note': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'note'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount'
            }),
            'truck': forms.Select(attrs={
                'class': 'form-control sele', 'id': 'truck'
            }),
            
            

            'expense_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            'payment_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(truck_expense_Form, self).__init__(*args, **kwargs)
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
            
            

            'expense_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            'payment_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(transfer_fund_Form, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['entry_date'].required = False

class bank_expense_Form(forms.ModelForm):
    class Meta:
        model = bank_expense
        fields = '__all__'
        widgets = {
            'bank_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'bank_name'
            }),
            'note': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'note'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'amount'
            }),
            
            'expense_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            'payment_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            'entry_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(bank_expense_Form, self).__init__(*args, **kwargs)
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
           
            
            
            'expense_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
            'payment_date': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
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
            'salary_paid_on': DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control date_css'}),
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



