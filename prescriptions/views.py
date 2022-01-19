from prescriptions.models import Prescription
from prescriptions.serializer import PrescriptionSerializer
import json
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from prescriptions.requests import Request
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
# @transaction.atomic
def prescription_get_set(request):
    if request.method == "POST":
        req = Request()
        data_in = json.loads(request.body)

        ids_in = {
            "phy_id": data_in['physician']['id'],
            "clinic_id": data_in['clinic']['id'],
            "patient_id": data_in['patient']['id']
        }
        pres_id = 655

        phy = req.request_physicians(ids_in['phy_id'])
        clinic = req.request_physicians(ids_in['clinic_id'])
        patient = req.request_patients(ids_in['patient_id'])

        metric = prepare_metrics(phy, clinic, patient, pres_id)
        metrics = req.request_metrics(metric)

        return HttpResponse(metrics, content_type='application/json')

    # queryset = Prescription.objects.all()
    # serializer_class = PrescriptionSerializer


def prepare_metrics(phy, clinic, patient, pres_id):
    data = {
        "clinic_id": clinic['id'],
        "clinic_name": clinic['name'],
        "physician_id": phy['id'],
        "physician_name": phy['name'],
        "physician_crm": phy['crm'],
        "patient_id": patient['id'],
        "patient_name": patient['name'],
        "patient_email": patient['email'],
        "patient_phone": patient['phone'],
        "prescription_id": pres_id
    }
    return data
