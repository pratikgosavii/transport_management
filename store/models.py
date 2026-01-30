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



class office_location(models.Model):

    name = models.CharField(max_length=120, unique=True)
    #address
    #mobile number

    
    def __str__(self):
        return self.name


class consignor(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='event_ticket')
    builty_code = models.CharField(max_length=120, unique = True)
    name = models.CharField(max_length=120, unique=False)
    office_location = models.ForeignKey(office_location, on_delete=models.CASCADE, blank = True, null = True,related_name='sdsfwfe')
    
    def __str__(self):
        return self.name

class onaccount(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='scsdsds')
    name = models.CharField(max_length=120, unique=False)
    office_location = models.ForeignKey(office_location, on_delete=models.CASCADE, blank = True, null = True,related_name='sefedsfwfe')
    
    
    def __str__(self):
        return self.name


class article(models.Model):
    
    company_name = models.ForeignKey(company, on_delete=models.CASCADE, related_name='sfsf')
    consignor = models.ForeignKey(consignor , on_delete=models.CASCADE, related_name='sds')
    name = models.CharField(max_length=120, unique=False)
    office_location = models.ForeignKey(office_location, on_delete=models.CASCADE, blank = True, null = True,related_name='fefefe4gefd')

    def __str__(self):
        return self.name





class truck_owner(models.Model):

    owner_name = models.CharField(max_length=120, unique = True, null=True, blank=True)
    pan_card = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    mobile_number =  models.IntegerField(unique=False, null=True, blank=True)
    bank_acc =  models.IntegerField(null=True, blank=True)

       
    def __str__(self):
        return self.owner_name


class petrol_pump(models.Model):

    name = models.CharField(max_length=120, unique=True)
   
       
    def __str__(self):
        return self.name


class driver(models.Model):

    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=120, unique=True)
    driving_licence = models.CharField(max_length=120, unique=True)
    adhar_card = models.CharField(max_length=120, unique=True)
    mobile_no = models.IntegerField()
    driving_licence_expiry_date = models.DateField(null=True, blank=True, auto_now_add=False)
   
       
    def __str__(self):
        return self.name



        

class truck_details(models.Model):

    truck_owner = models.ForeignKey(truck_owner , on_delete=models.CASCADE, related_name='ddfdf')
    truck_number = models.CharField(max_length=120, unique=True)
    insurance_number = models.CharField(max_length=120, unique=True, null=True, blank=True)
    permit_number = models.CharField(max_length=120, unique=True, null=True, blank=True)
    puc_number = models.CharField(max_length=120, unique=True, null=True, blank=True)
    fitness = models.CharField(max_length=120, null=True, blank=True)
   
    
    def __str__(self):
        return self.truck_number

   
 


class district(models.Model):

    name =  models.CharField(max_length=120)
    office_location = models.ForeignKey(office_location, on_delete=models.CASCADE)

        
    def __str__(self):
        return self.name
    

class taluka(models.Model):

    district = models.ForeignKey(district, on_delete=models.CASCADE)
    office_location = models.ForeignKey(office_location, on_delete=models.CASCADE, blank = True, null = True,related_name='ddfdf')

    name =  models.CharField(max_length=120)

        
    def __str__(self):
        return self.name
 

 
class from_station(models.Model):

    name =  models.CharField(max_length=120)
    office_location = models.ForeignKey(office_location, on_delete=models.CASCADE, blank = True, null = True,related_name='eereefedfeferefefdfed')
    taluka =  models.ForeignKey(taluka, related_name="xvds", on_delete=models.CASCADE)
        
    def __str__(self):
        return self.name
 
 
class station(models.Model):

    name =  models.CharField(max_length=120)
    office_location = models.ForeignKey(office_location, on_delete=models.CASCADE, blank = True, null = True,related_name='eeredfed')
    taluka =  models.ForeignKey(taluka, related_name="fefdws", on_delete=models.CASCADE)
        
    def __str__(self):
        return self.name
 

class rate(models.Model):

    from_station =  models.ForeignKey(station, related_name="dfgfdfdf", on_delete=models.CASCADE)
    to_station =  models.ForeignKey(station, related_name="dfgfddsdedfdf", on_delete=models.CASCADE)
    company_rate =  models.IntegerField()

        
    def __str__(self):
        return self.from_station.name
 

class vendor(models.Model):
    """Vendor master table for tyre purchases and truck expenses"""
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    gst_number = models.CharField(max_length=50, null=True, blank=True)
    office_location = models.ForeignKey(office_location, on_delete=models.CASCADE, blank=True, null=True, related_name='vendors')
    
    class Meta:
        unique_together = [['office_location', 'name']]
    
    def __str__(self):
        return self.name


class mechanic(models.Model):
    """Mechanic master table for truck mechanic/spare part expenses"""
    name = models.CharField(max_length=120)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    office_location = models.ForeignKey(office_location, on_delete=models.CASCADE, blank=True, null=True, related_name='mechanics')
    
    class Meta:
        unique_together = [['office_location', 'name']]
    
    def __str__(self):
        return self.name


# Tyre pattern choices
TYRE_PATTERN_CHOICES = (
    ('radial', 'Radial'),
    ('bias', 'Bias'),
    ('tubeless', 'Tubeless'),
    ('tube_type', 'Tube Type'),
)

# Tyre type choices
TYRE_TYPE_CHOICES = (
    ('front', 'Front'),
    ('rear', 'Rear'),
    ('spare', 'Spare'),
    ('all_position', 'All Position'),
)

class tyre(models.Model):
    """Tyre master table for truck expenses"""
    tyre_no = models.CharField(max_length=50, unique=True, db_index=True)
    pattern = models.CharField(max_length=50, choices=TYRE_PATTERN_CHOICES, db_index=True)
    type = models.CharField(max_length=50, choices=TYRE_TYPE_CHOICES, db_index=True)
    company = models.CharField(max_length=120, db_index=True)
    driver = models.ForeignKey(driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='tyres', db_index=True)
    vendor = models.ForeignKey(vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='tyres', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Tyres"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tyre_no']),
            models.Index(fields=['pattern']),
            models.Index(fields=['type']),
            models.Index(fields=['company']),
        ]
    
    def __str__(self):
        return f"{self.tyre_no} - {self.company}"
 

 