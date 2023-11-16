from django.db import models
from datetime import date, timedelta
import uuid,datetime,os
# Create your models here.

class QR (models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_id = models.CharField(max_length=200, null=True, blank=True, editable=False)
    product_id = models.CharField(max_length=200, null=True, blank=True, editable=False)
    generated_date = models.CharField(max_length=200, null=True, blank=True)
    amount = models.CharField(max_length=200, null=True, blank=True)
    tag = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.id 