from prescriptions.models import Prescription
import json, os, mimetypes
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
            json.dumps({
                "error": {
                    "code": "10",
                    "message": 'prescription create error'
                }
            }),
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
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if ref == "31d8c7ea-1aa4-4a3d-a5da-ca0595658a38":
        filename = 'Resultado_FilipeBoratoCastro.pdf'

    elif ref == "f87a324d-608b-4b7e-bce7-106cbc3a306d":
        filename = 'Resultado_IsabelBiembengutVenturi.pdf'
    else:
        return HttpResponse(
            json.dumps({
                "error": {
                    "code": "10",
                    "message": 'There is no report for this User'
                }
            }),
            content_type='application/json',
            status=400)
    filepath = BASE_DIR + '/prescriptions/files/' + filename
    path = open(filepath, 'rb')

    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response
