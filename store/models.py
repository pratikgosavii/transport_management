from django.db import models

from datetime import datetime, timezone

import pytz
ist = pytz.timezone('Asia/Kolkata')




class company(models.Model):

    company_name = models.CharField(max_length=120, unique=True)
    #address
    #mobile number

    
    def __str__(self):
        return self.company_name


class consignor(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='event_ticket')
    name = models.CharField(max_length=120, unique=False)
    
    
    def __str__(self):
        return self.name

class onaccount(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='scsdsds')
    name = models.CharField(max_length=120, unique=False)
    
    
    def __str__(self):
        return self.name


class article(models.Model):
    
    company_name = models.ForeignKey(company, on_delete=models.CASCADE, related_name='sfsf')
    consignor = models.ForeignKey(consignor , on_delete=models.CASCADE, related_name='sds')
    name = models.CharField(max_length=120, unique=False)

    def __str__(self):
        return self.name





class truck_owner(models.Model):

    owner_name = models.CharField(max_length=120, unique=True)
    bank_acc = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=120, unique=True)
    mobile_number =  models.IntegerField(unique=False)

       
    def __str__(self):
        return self.owner_name



        

class truck_details(models.Model):

    truck_owner = models.ForeignKey(truck_owner , on_delete=models.CASCADE, related_name='ddfdf')
    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='ddfdf')
    truck_number = models.CharField(max_length=120, unique=True)
    insurance_number = models.CharField(max_length=120, unique=True)
    permit_number = models.CharField(max_length=120, unique=True)
    puc_number = models.CharField(max_length=120, unique=True)
    fitness = models.CharField(max_length=120, unique=True)
   
    
    def __str__(self):
        return self.truck_number

   
 

class station(models.Model):

    name =  models.CharField(max_length=120, unique=True)

        
    def __str__(self):
        return self.name
 

class district(models.Model):

    name =  models.CharField(max_length=120, unique=True)

        
    def __str__(self):
        return self.name

class taluka(models.Model):

    district = models.ForeignKey(district, on_delete=models.CASCADE)

    name =  models.CharField(max_length=120, unique=True)

        
    def __str__(self):
        return self.name
 

 
