from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
# import requests
import json
from django.views.decorators.csrf import csrf_exempt

import csv
from django.db.models import Sum
from analytics.models import CustomerData

# # Create your views here.
# @csrf_exempt
# def analytics(request):
    
#     if request.method == "GET":
#         file = open('/home/jahnavi/Toucan_analytics_P1/toucan_analytics/Data/data_for_database.csv',mode='r')
#         data = csv.reader(file)
#         dL = list(data)
#         dataList = dL[1:]
#         for row in dataList:
#             customerid = row[1]
#             category = row[2]
#             modeOfPayment = row[3]
#             amount = row[4]
#             date = row[5]
#             break

#         dictt = {
            
#             "customerid" : customerid,
#             "category" : category,
#             "mode" : modeOfPayment,
#             "amount" : amount,
#             "date" : date
#         }
#         file.close()
#         return JsonResponse(dictt)
    
#     return HttpResponse("wow")

def index(request):
    return HttpResponse("index")

def pie(request):
    grouped_data = CustomerData.objects.values('category').annotate(sum_field=Sum('amount_spent'))

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

@csrf_exempt
def analytics(request):
    if request.method == "GET":
        type = request.GET.get('type')
        if type == "pie":
            response = pie(request)
            return response
        else:
            return HttpResponse("NOT PIE")
    else:
        return HttpResponse("something")


