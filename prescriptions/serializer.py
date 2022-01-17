from rest_framework import serializers
from models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        Fields = ['id', 'clinic_id', 'clinic_name', 'physician_id', 'physician_name'
                  'physician_crm', 'patient_name', 'patient_email', 'patient_phone', 'prescription_id']
