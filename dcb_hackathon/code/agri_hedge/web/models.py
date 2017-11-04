from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
# Create your models here.


class user_data(models.Model):

    user_data_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=500)
    user_addhar_verified = models.CharField(max_length=500, blank=True, null=True)
    user_phone = models.CharField(max_length=500)
    user_age = models.CharField(max_length=500, blank=True, null=True)
    user_state = models.CharField(max_length=500)
    user_pin_code = models.CharField(max_length=500, blank=True, null=True)
    user_area = models.CharField(max_length=500)
    user_district = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    User = models.ForeignKey(User, default=1)
    created_at= models.DateTimeField(default=timezone.now)
    updated_at= models.DateTimeField(default=timezone.now)

class transaction_table(models.Model):

    trans_id = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, default=1)
    quantity = models.CharField(max_length=500)
    crop_type = models.CharField(max_length=500)
    duration = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    premium_expected = models.CharField(max_length=500)
    amount_owned = models.CharField(max_length=500)
    payment_status = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class short_table(models.Model):

    short_id = models.AutoField(primary_key=True)
    trans_id = models.ForeignKey(transaction_table, default=1)
    short_price = models.CharField(max_length=500)
    quantity = models.CharField(max_length=200)
    contract_number = models.CharField(max_length=200)
    duration = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
