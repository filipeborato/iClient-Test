from rest_framework import serializers
from .models import Prescription

class EntitySerializer(serializers.Serializer):
    id = serializers.IntegerField()

class PrescriptionInputSerializer(serializers.Serializer):
    clinic = EntitySerializer()
    physician = EntitySerializer()
    patient = EntitySerializer()
    text = serializers.CharField()

class PrescriptionResponseSerializer(serializers.ModelSerializer):
    clinic = serializers.SerializerMethodField()
    physician = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()
    metric = serializers.SerializerMethodField()
    text = serializers.CharField(source='prescription_name')

    class Meta:
        model = Prescription
        fields = ['id', 'clinic', 'physician', 'patient', 'text', 'metric']

    def get_clinic(self, obj):
        return {"id": obj.clinic_id}

    def get_physician(self, obj):
        return {"id": obj.physician_id}

    def get_patient(self, obj):
        return {"id": obj.patient_id}

    def get_metric(self, obj):
        # Recupera os objetos que foram passados via context na view.
        phy = self.context.get("phy")
        clinic = self.context.get("clinic")
        patient = self.context.get("patient")
        if phy and clinic and patient:
            return {
                "clinic_id": clinic['id'],
                "clinic_name": clinic['name'],
                "physician_id": phy['id'],
                "physician_name": phy['name'],
                "physician_crm": phy['crm'],
                "patient_id": patient['id'],
                "patient_name": patient['name'],
                "patient_email": patient['email'],
                "patient_phone": patient['phone'],
                "prescription_id": obj.id
            }
        return {}