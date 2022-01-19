from rest_framework import serializers
from prescriptions.models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'clinic_id', 'physician_id', 'patient_id', 'prescription_name']
