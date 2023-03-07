from .models import ContactInfo

def contact_info(request):
    return {'contact_info': ContactInfo.objects.first()}
