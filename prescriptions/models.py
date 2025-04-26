from django.db import models


class Prescription(models.Model):
    clinic_id = models.IntegerField()
    physician_id = models.IntegerField()
    patient_id = models.IntegerField()
    prescription_name = models.TextField()
    
    class Meta:
        unique_together = ('clinic_id', 'physician_id', 'patient_id')

    @property
    def text(self):
        return self.prescription_name
