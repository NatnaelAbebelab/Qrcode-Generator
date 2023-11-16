from django.urls import path
from django.views.generic.base import TemplateView
from .import views

urlpatterns = [
    path('generate', views.generate, name='generate'),
    path('generateqr', views.generate_qrcode, name='generateqr'),
    path('scan/<str:qr_id>', views.scan, name='scan'),
    path('verfiyproduct', views.verify_product, name='verfiyproduct'),
    path('verfiyfibertag', views.verfiy_fibertag, name='verfiyfibertag'),
    path('deleteqrs', views.delete_qrs, name='deleteqrs'),
    path(r'^verficationpage/', TemplateView.as_view(template_name="index.html"),
                name='page_verfication'),
    path(r'^fibertagpage/', TemplateView.as_view(template_name="fibertag.html"),
                name='page_fibertag'),
    path(r'^errorpage/', TemplateView.as_view(template_name="error.html"),
                name='page_error'),
]