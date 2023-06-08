from django.http import JsonResponse
from django.db.models  import Sum,Count,Max
from .models import AllData, CustomerData

def table(request,start_date,end_date):
    unique_customers=CustomerData.objects.values('customer_Id').annotate(frequent_modes_of_transanction=Max('mode_of_payments'))
    # For TABLE
    customer = []
    values = []
    for item in unique_customers:
        customer.append(item['customer_Id'])
        values.append(item['frequent_modes_of_transanction'])

    response_data = {
            "customer" : customer,
            "values" :values
        }
    # Return the JSON response
 

# emi code
def index(request):
    # if request.method=='GET':
    result=list(CustomerData.objects.values('EMI_paid_on_time').annotate(total_customers=Count('customer_Id')).order_by('-total_customers'))
    return JsonResponse(result,safe=False)
    # return HttpResponse('post method')

# pie chart code 
def pichart(request):
    # if request.method=='GET':
        grouped_data = list(AllData.objects.values('category').annotate(sum_field=Sum('amount_spent')).order_by('-sum_field'))
        labels = []
        total = []
        sizes = []
        for entry in grouped_data:
            labels.append(entry['category']) 
            total.append(entry['sum_field'])

        sum_1 = sum(total)

        for i in range(len(total)):
            per = (total[i]/sum_1)*100
            sizes.append(per)

        response_data = {
            "labels" : labels,
            "sizes" : sizes,
        }
        return JsonResponse(response_data)

# code based on mode of payment 

def payment(request):
    # if request.method == 'GET':
        result = list(AllData.objects.values('mode_of_payments').annotate(total_customers=Count('customer_Id')).order_by('-total_customers'))
        return JsonResponse(result, safe=False)
    # return HttpResponse('post method')


# code for table

def table(request):
    # if request.method == 'GET':
        unique_customers=AllData.objects.values('customer_Id').annotate(frequent_modes_of_transanction=Max('mode_of_payments'))
    # For TABLE
        customer = []
        values = []
        for item in unique_customers:
            customer.append(item['customer_Id'])
            values.append(item['frequent_modes_of_transanction'])

        response_data = {
            "customer" : customer,
            "values" :values
        }
    # Return the JSON response
        return JsonResponse(response_data)


from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from django.conf import settings

class DataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split()[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']   
            data = {"WOW":"WOW"}
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=401)
