from django.http import HttpResponse,JsonResponse
from django.db.models  import Sum,Count,Max
from .models import AllData, CustomerData

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
