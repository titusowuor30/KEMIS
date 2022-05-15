from .models import *
from django.db.models import Q

def get_reusable_waste(request):
    wastes=WasteProduct.objects.filter(Q(reusabe__icontains=True) and Q(reuse_plan__icontains="Sell"))[:5]
    return {'wastes':wastes}