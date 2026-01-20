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
        serializer = PrescriptionInputSerializer(data=request.data)
        if not serializer.is_valid():
            # Check for custom errors from validation
            errors = serializer.errors
            
            # Helper to extract error dict
            if 'non_field_errors' in errors:
                 error_list = errors['non_field_errors']
                 if isinstance(error_list, list) and len(error_list) > 0:
                     first = error_list[0]
                     if isinstance(first, dict) and 'error' in first:
                         return Response(first, status=status.HTTP_400_BAD_REQUEST)
            
            if 'error' in errors:
                err_val = errors['error']
                if isinstance(err_val, list) and len(err_val) > 0:
                    return Response({'error': err_val[0]}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': err_val}, status=status.HTTP_400_BAD_REQUEST)

             # Fallback for standard DRF errors (missing fields, wrong types)
            return Response({
                 "error": {
                     "code": "01",
                     "message": "malformed request"
                 }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data

        ids_in = {
            "phy_id": data['physician']['id'],
            "clinic_id": data['clinic']['id'],
            "patient_id": data['patient']['id']
        }

        # Objects are now already fetched and validated in data
        phy = data['phy_obj']
        clinic = data['clinic_obj']
        patient = data['patient_obj']

        pres = get_or_create(ids_in, data['text'])

        response_serializer = PrescriptionResponseSerializer(
            pres, 
            context={
                "phy": phy,
                "clinic": clinic,
                "patient": patient,
            }
        )
        
        return Response({'data': response_serializer.data}, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.exception("Error in prescription_get_set: %s", e)
        return Response({
            "error": {
                "code": "10",
                "message": "prescription create error"
            }
        }, status=status.HTTP_400_BAD_REQUEST)

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