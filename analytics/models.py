from django.db import models

class CustomerData(models.Model):

    customer_Id = models.IntegerField(default=1)
    EMI_paid_on_time = models.CharField(max_length=10,default=True)

    
