from django.db.models import Count
from django.http import HttpResponse,JsonResponse
from .models import CustomerData

def index(request):
    if request.method=='GET':
        result=list(CustomerData.objects.values('EMI_paid_on_time').annotate(total_customers=Count('customer_Id')).order_by())
        return JsonResponse(result,safe=False)
    return HttpResponse('post method')
