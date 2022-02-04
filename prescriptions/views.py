from prescriptions.models import Prescription
import json
from django.http import HttpResponse
from django.db import transaction
from prescriptions.requests import Request
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@transaction.atomic
def prescription_get_set(request):
    try:
        if request.method == "POST":
            req = Request()
            data_in = json.loads(request.body)

            ids_in = {
                "phy_id": int(data_in['physician']['id']),
                "clinic_id": int(data_in['clinic']['id']),
                "patient_id": int(data_in['patient']['id'])
            }

            phy, err = req.request_physicians(ids_in['phy_id'])
            if err:
                return HttpResponse(json.dumps(phy), content_type='application/json', status=400)

            clinic, err = req.request_clinics(ids_in['clinic_id'])
            if err:
                return HttpResponse(json.dumps(clinic), content_type='application/json', status=400)

            patient, err = req.request_patients(ids_in['patient_id'])
            if err:
                return HttpResponse(json.dumps(patient), content_type='application/json', status=400)

            pres = get_or_create(ids_in, data_in['text'])

            metric = prepare_metrics(phy, clinic, patient, pres.id)
            metrics = req.request_metrics(metric)
            resp = json.dumps(prepare_response(pres, metrics))

            return HttpResponse(resp, content_type='application/json')
    except Exception as e:
        if e is dict:
            return HttpResponse(json.dumps(e), content_type='application/json', status=400)

        return HttpResponse(
            {
                "error": {
                    "code": "10",
                    "message": 'prescription create error'
                }
            },
            content_type='application/json',
            status=400)


def prepare_response(prescription, metrics):
    return \
        {
            "data": {
                "id": prescription.id,
                "clinic": {
                    "id": prescription.clinic_id
                },
                "physician": {
                    "id": prescription.physician_id
                },
                "patient": {
                    "id": prescription.patient_id
                },
                "text": prescription.prescription_name,
                "metric": {
                    "id": metrics['id']
                }
            }
        }


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


def get_or_create(ids_in, text):
    try:
        p = Prescription.objects.get(clinic_id=ids_in['clinic_id'],
                                     physician_id=ids_in['phy_id'],
                                     patient_id=ids_in['patient_id'])

    except Prescription.DoesNotExist:
        p = Prescription.objects.create(clinic_id=ids_in['clinic_id'],
                                        physician_id=ids_in['phy_id'],
                                        patient_id=ids_in['patient_id'],
                                        prescription_name=text)
    return p

@csrf_exempt
def laudo(request, ref):
    return HttpResponse(ref)
