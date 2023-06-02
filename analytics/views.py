from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
# import requests
import json
from django.views.decorators.csrf import csrf_exempt

import csv
from django.db.models import Sum,Count,Max
from analytics.models import CustomerData,EMIData

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


def index(request):
    return HttpResponse("index")

def pie(request):
    if request.method == "GET":
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        grouped_data = CustomerData.objects.filter(date__range=[start_date, end_date]).values('category').annotate(sum_field=Sum('amount_spent'))

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

#for EMI data bar chart
def emi(request):
    if request.method=='GET':
        result=list(EMIData.objects.values('EMI_paid_on_time').annotate(total_customers=Count('customer_Id')).order_by('-total_customers'))
        return JsonResponse(result,safe=False)
    return HttpResponse('post method')



#for mode of payments bar chart

def payments(request):

    if request.method == "GET":
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        result=list(CustomerData.objects.filter(date__range=[start_date, end_date]).values('mode_of_payments').annotate(total_customers=Count('customer_Id')).order_by('-total_customers'))
        return JsonResponse(result,safe=False)
    return HttpResponse('post method')


def table(request):
    if request.method == "GET":
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
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

# @csrf_exempt
# def analytics(request):
#     if request.method == "GET":
#         type = request.GET.get('type')
#         if type == "pie":
#             response = pie(request)
#             return response
#         elif type == "emi":
#             response = emi(request)
#             return response 
#         elif type == "payments":
#             response = payments(request)
#             return response 
#         elif type == "table":
#             response = table(request)
#             return response 
#     else:
#         return HttpResponse("something wrong ")
    

