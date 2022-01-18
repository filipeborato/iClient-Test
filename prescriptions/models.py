from django.db import models


class Prescription(models.Model):
    clinic_id = models.IntegerField()
    clinic_name = models.CharField(max_length=60)
    physician_id = models.IntegerField()
    physician_name = models.CharField(max_length=100)
    physician_crm = models.CharField(max_length=15)
    patient_id = models.IntegerField()
    patient_name = models.CharField(max_length=60)
    patient_email = models.CharField(max_length=40)
    patient_phone = models.CharField(max_length=40)
    prescription_id = models.IntegerField()
    prescription_name = models.CharField(max_length=60)
