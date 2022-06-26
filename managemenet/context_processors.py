from .models import *
from django.db.models import Q

def get_reusable_waste(request):
    try:
        wastes=WasteProduct.objects.filter(Q(reusabe__icontains=True) and Q(reuse_plan__icontains="Sell"))[:5]
        return {'wastes':wastes}
    except Exception as e:
        print(e)
        return {'wastes': {}}
        
def get_notifiication_settings(request):
    try:
       nsettings = Notification.objects.all()[0]
       return {'nsettings': nsettings, 'nsettingsid': nsettings.id}
    except Exception as e:
        print(e)
        return {'nsettings': {}, 'nsettingsid':0}

    