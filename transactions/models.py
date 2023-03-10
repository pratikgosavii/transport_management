from django.db import models

# Create your models here.



from users.models import User
from datetime import datetime, timezone
from store.models import *


ex_for = (
    ('for','for'),
    ('ex', 'ex'),
   
)

mode = (
    ('cash','cash'),
    ('online', 'online'),
   
)

class builty(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='sdwe')
    builty_no = models.FloatField()
    DC_date = models.DateField(auto_now_add=False)
    truck_details = models.ForeignKey(truck_details , on_delete=models.CASCADE, related_name='sdsdsc')
    truck_owner = models.ForeignKey(truck_owner , on_delete=models.CASCADE, related_name='cxcdfdfvd')
    consignor = models.ForeignKey(consignor , on_delete=models.CASCADE, related_name='wdsfgv')
    station_from = models.ForeignKey(station , on_delete=models.CASCADE, related_name='sdsdsdssdsdsdcs')
    station_to = models.ForeignKey(station , on_delete=models.CASCADE, related_name='dvccxcred')
    consignee = models.CharField(max_length=50)
    taluka = models.ForeignKey(taluka, on_delete=models.CASCADE, related_name='sdscsc')
    district = models.ForeignKey(district, on_delete=models.CASCADE, related_name='sddcxfw')
    onaccount = models.ForeignKey(onaccount , on_delete=models.CASCADE, related_name='wfdfgfdgv')
    article = models.ForeignKey(article , on_delete=models.CASCADE, related_name='dffdcxvc')
    bags = models.FloatField()
    delivery_no = models.FloatField()
    ex_for = models.CharField(max_length=50, choices=ex_for, default="for")
    mode = models.CharField(max_length=50, choices=mode)
    note = models.CharField(max_length=50)
    rate = models.FloatField()
    mt = models.FloatField()
    freight = models.FloatField()
    less_advance = models.FloatField()
    less_tds = models.FloatField()
    balance = models.FloatField()
    diesel = models.FloatField(default=0.0)
    editable = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company.company_name

   

class ack(models.Model):

    builty = models.ForeignKey(builty, on_delete=models.CASCADE, related_name='have_ack')
    challan_number = models.CharField(max_length=50)

    def __str__(self):
        return self.builty

class request_edit(models.Model):

    builty = models.ForeignKey(builty, on_delete=models.CASCADE, related_name="has_request")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
   

class sub_trip(models.Model):

    builty = models.ForeignKey(builty, on_delete=models.CASCADE, related_name = 'sub_trip_is')
    station_from = models.ForeignKey(station , on_delete=models.CASCADE, related_name='sdfdcxcde')
    station_to = models.ForeignKey(station , on_delete=models.CASCADE, related_name='dfdcxcfbgefwd')
    diesel = models.FloatField(default=0.0)
    note = models.CharField(max_length=50)

    def __str__(self):
        return self.builty.builty_no



   
