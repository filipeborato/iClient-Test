from rest_framework import viewsets
from prescriptions.models import Prescription
from prescriptions.serializer import PrescriptionSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
