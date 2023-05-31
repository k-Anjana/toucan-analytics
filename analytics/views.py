from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from .models import CustomerData,EMIData
import csv
from django.db import models
from django.db.models import Count,Sum,Max


# Create your views here.
def table(request,start_date,end_date):
    unique_customers=CustomerData.objects.filter(date__range=[start_date, end_date]).values('customer_Id').annotate(frequent_modes_of_transanction=Max('mode_of_payments'))
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
def bar(request,start_date,end_date):
    result=CustomerData.objects.filter(date__range=[start_date, end_date]).values('mode_of_payments').annotate(total_amount=Sum('amount_spent'))
    # For BAR GRAPH
    mode =[]
    amount=[]
    for item in result:
        mode.append(item['mode_of_payments'])
        amount.append(item['total_amount'])
    response_data = {
            "mode" : mode,
            "amount" : amount,
        }
    
    # Return the JSON response
    return JsonResponse(response_data)

def pie(request,start_date,end_date):
    grouped_data = CustomerData.objects.filter(date__range=[start_date, end_date]).values('category').annotate(sum_field=Sum('amount_spent'))
    print(start_date)
    print(end_date)
# For PIE CHART
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

def emi(request):
    EMI=EMIData.objects.values('EMI_paid_on_time').annotate(total_customers=Count('customer_Id')).order_by()
    inTime =[]
    total=[]
    for item in EMI:
        inTime.append(item['EMI_paid_on_time'])
        total.append(item['total_customers'])
    response_data = {
            "in_time" : inTime,
            "total" : total,
        }
    
    # Return the JSON response
    return JsonResponse(response_data)




@csrf_exempt
def analytics(request):
    if request.method == "GET":
        Type = request.GET.get('type')
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        
        if Type == "table":
            response = table(request,start_date,end_date)
            return response
        elif Type == "bar":
            response = bar(request,start_date,end_date)
            return response
        elif Type == "pie":
            response = pie(request,start_date,end_date)
            return response
        elif Type == "emi":
            response = emi(request)
            return response
        
    else:
        return HttpResponse("WOW")
    

def index(request):
    return redirect("http://192.168.56.159:8501")




