from django.db import models


class Prescription(models.Model):
    clinic_id = models.IntegerField()
    physician_id = models.IntegerField()
    patient_id = models.IntegerField()
    prescription_name = models.CharField(max_length=100)
