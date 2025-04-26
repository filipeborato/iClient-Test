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
        metrics = self.context.get('metrics', {})
        # Return a default id of 1 if none is provided
        return {"id": metrics.get('id', 1)}