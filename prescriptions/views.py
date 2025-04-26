from prescriptions.models import Prescription
import os
import logging
from django.http import FileResponse, JsonResponse
from django.db import transaction
from prescriptions.requests import Request
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PrescriptionInputSerializer, PrescriptionResponseSerializer

logger = logging.getLogger(__name__)

@api_view(['POST'])
@transaction.atomic
def prescription_get_set(request):
    try:
        # Validate input data
        serializer = PrescriptionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data_in = serializer.validated_data
        req = Request()

        ids_in = {
            "phy_id": data_in['physician']['id'],
            "clinic_id": data_in['clinic']['id'],
            "patient_id": data_in['patient']['id']
        }

        # Check physician
        phy, err = req.request_physicians(ids_in['phy_id'])
        if err:
            return Response(phy, status=status.HTTP_400_BAD_REQUEST)

        # Check clinic
        clinic, err = req.request_clinics(ids_in['clinic_id'])
        if err:
            return Response(clinic, status=status.HTTP_400_BAD_REQUEST)

        # Check patient
        patient, err = req.request_patients(ids_in['patient_id'])
        if err:
            return Response(patient, status=status.HTTP_400_BAD_REQUEST)

        # Create or get prescription
        pres = get_or_create(ids_in, data_in['text'])

        # Prepare metrics
        metric = prepare_metrics(phy, clinic, patient, pres.id)
        metrics = req.request_metrics(metric)

        # Serialize response
        response_serializer = PrescriptionResponseSerializer(
            pres, 
            context={'metrics': metrics}
        )
        
        return Response({'data': response_serializer.data})

    except Exception as e:
        if isinstance(e, dict):
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "error": {
                "code": "10",
                "message": 'prescription create error'
            }
        }, status=status.HTTP_400_BAD_REQUEST)


def prepare_response(prescription, metrics):
    # Convert Django model instance to dict
    prescription_dict = {
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
            "id": metrics.get('id')  # Using .get() to avoid KeyError
        }
    }
    
    return {"data": prescription_dict}


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
    # Calculate the base directory dynamically.
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logger.debug("Base directory resolved to: %s", base_dir)
    
    # Mapping from ref to filename.
    file_mapping = {
        "31d8c7ea-1aa4-4a3d-a5da-ca0595658a38": "Resultado_FilipeBoratoCastro.pdf",
        "f87a324d-608b-4b7e-bce7-106cbc3a306d": "Resultado_IsabelBiembengutVenturi.pdf"
    }
    
    filename = file_mapping.get(ref)
    if not filename:
        logger.error("No report found for ref: %s", ref)
        return JsonResponse({
            "error": {
                "code": "10",
                "message": "There is no report for this User"
            }
        }, status=400)
    
    # Construct the absolute filepath.
    filepath = os.path.join(base_dir, 'prescriptions', 'files', filename)
    logger.debug("Resolved filepath: %s", filepath)
    
    if not os.path.exists(filepath):
        logger.error("File not found at path: %s", filepath)
        return JsonResponse({
            "error": {
                "code": "11",
                "message": "File not found"
            }
        }, status=404)
    
    # Open the file without using a context manager.
    try:
        file_handle = open(filepath, 'rb')
        return FileResponse(
            file_handle,
            as_attachment=True,
            filename=filename
        )
    except Exception as e:
        logger.exception("Error serving file %s: %s", filename, e)
        return JsonResponse({
            "error": {
                "code": "12",
                "message": "Error serving file"
            }
        }, status=500)