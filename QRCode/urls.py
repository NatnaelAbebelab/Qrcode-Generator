from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('QRGenerator/', include('QR_Generator.urls')),
    path('Seller/', include('Seller.urls')),
    path('Product/', include('Product.urls'))
]
