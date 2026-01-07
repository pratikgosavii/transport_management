from django.db import models
from django.utils import timezone as dj_timezone
from users.models import User
from datetime import datetime
from store.models import *

ex_for = (
    ('for', 'for'),
    ('ex', 'ex'),
)

mode = (
    ('cash', 'cash'),
    ('online', 'online'),
)

mode1 = (
    ('cash', 'cash'),
    ('online', 'online'),
)


class builty(models.Model):
    company = models.ForeignKey(company, on_delete=models.CASCADE, related_name='sdwe', db_index=True)
    builty_no = models.CharField(max_length=50, db_index=True)
    DC_date = models.DateField(default=datetime.now, db_index=True)
    truck_details = models.ForeignKey(truck_details, on_delete=models.CASCADE, related_name='sdsdsc', db_index=True)
    truck_owner = models.ForeignKey(truck_owner, on_delete=models.CASCADE, related_name='cxcdfdfvd', db_index=True)
    consignor = models.ForeignKey(consignor, on_delete=models.CASCADE, related_name='wdsfgv', db_index=True)
    petrol_pump = models.ForeignKey(petrol_pump, null=True, blank=True, on_delete=models.CASCADE, related_name='wdsfgv', db_index=True)
    station_from = models.ForeignKey(from_station, on_delete=models.CASCADE, related_name='sdsdsdssdsdsdcs', db_index=True)
    station_to = models.ForeignKey(station, on_delete=models.CASCADE, related_name='dvccxcred', db_index=True)
    consignee = models.CharField(max_length=50, db_index=True)
    taluka = models.ForeignKey(taluka, on_delete=models.CASCADE, related_name='sdscsc', db_index=True)
    district = models.ForeignKey(district, on_delete=models.CASCADE, related_name='sddcxfw', db_index=True)
    onaccount = models.ForeignKey(onaccount, on_delete=models.CASCADE, related_name='wfdfgfdgv', db_index=True)
    article = models.ForeignKey(article, on_delete=models.CASCADE, related_name='dffdcxvc', db_index=True)
    bags = models.IntegerField()
    delivery_no = models.IntegerField(null=True, blank=True, db_index=True)
    mobile_no = models.FloatField(null=True, blank=True)
    ex_for = models.CharField(max_length=50, choices=ex_for, default="for", db_index=True)
    mode = models.CharField(max_length=50, choices=mode, default="cash", db_index=True)
    note = models.CharField(null=True, blank=True, max_length=50)
    rate = models.FloatField(default=0.0)
    mt = models.FloatField(default=0.0)
    freight = models.FloatField(default=0.0)
    less_advance = models.FloatField(default=0.0)
    less_tds = models.FloatField(null=True, blank=True, default=0.0)
    balance = models.FloatField(default=0)
    diesel = models.FloatField(default=0.0)
    editable = models.BooleanField(default=False, db_index=True)
    deleted = models.BooleanField(default=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['builty_no']),
            models.Index(fields=['DC_date']),
            models.Index(fields=['mode']),
            models.Index(fields=['deleted']),
            models.Index(fields=['company', 'DC_date']),
        ]
        ordering = ['-DC_date']
        verbose_name_plural = "Builty Records"

    def __str__(self):
        return self.builty_no


class ack(models.Model):
    builty = models.ForeignKey(builty, on_delete=models.CASCADE, related_name='have_ack', db_index=True)
    challan_number = models.CharField(max_length=50, db_index=True)
    challan_date = models.DateField(blank=True, null=True, db_index=True)
    voucher_payment_status = models.BooleanField(default=False, db_index=True)
    voucher_payment_mode = models.CharField(max_length=50, choices=mode1, default="cash", null=True, blank=True)
    voucher_payment_bank_ac_no = models.CharField(max_length=50, null=True, blank=True)
    voucher_payment_bank_ac_ifsc = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['challan_number']),
            models.Index(fields=['voucher_payment_status']),
        ]
        ordering = ['-challan_date']

    def __str__(self):
        return self.builty.builty_no


class ack_history(models.Model):
    builty = models.ForeignKey(builty, on_delete=models.CASCADE, related_name='have_ack3434', db_index=True)
    challan_number_before = models.CharField(max_length=50, db_index=True)
    challan_date_before = models.DateField(blank=True, null=True, db_index=True)
    update_date = models.DateField(default=dj_timezone.now, blank=True, null=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['update_date']),
        ]
        ordering = ['-update_date']

    def __str__(self):
        return self.builty.builty_no


class request_edit(models.Model):
    builty = models.ForeignKey(builty, on_delete=models.CASCADE, related_name="has_request", db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    status = models.BooleanField(default=False, db_index=True)
    history = models.BooleanField(default=False, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['history']),
        ]
        ordering = ['-id']

    def __str__(self):
        return self.user.username
