from rest_framework import serializers
from .models import Prescription
from prescriptions.requests import Request

class EntitySerializer(serializers.Serializer):
    id = serializers.IntegerField()

class PrescriptionInputSerializer(serializers.Serializer):
    clinic = EntitySerializer()
    physician = EntitySerializer()
    patient = EntitySerializer()
    text = serializers.CharField()

    def validate(self, data):
        req = Request()
        
        # Physician validation
        phy_id = data.get('physician').get('id')
        phy, err = req.request_physicians(phy_id)
        if err:
            raise serializers.ValidationError(phy)
        
        # Clinic validation
        clinic_id = data.get('clinic').get('id')
        clinic, err = req.request_clinics(clinic_id)
        if err:
            raise serializers.ValidationError(clinic)
        
        # Patient validation
        patient_id = data.get('patient').get('id')
        patient, err = req.request_patients(patient_id)
        if err:
            raise serializers.ValidationError(patient)

        # Store validated objects in data
        data['phy_obj'] = phy
        data['clinic_obj'] = clinic
        data['patient_obj'] = patient
        
        return data

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