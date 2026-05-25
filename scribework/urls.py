from django.urls import path
from . import views

urlpatterns=[
path('csp-commission-data', views.commission_data_ingestion, name="csp_data_ingestion"),
]