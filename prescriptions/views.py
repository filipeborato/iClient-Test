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
        phy_id = data_in['physician']['id']
        phy = req.request_physicians(phy_id)

        return HttpResponse(phy, content_type='application/json')

    # queryset = Prescription.objects.all()
    # serializer_class = PrescriptionSerializer
