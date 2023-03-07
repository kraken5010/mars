from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', mainpage, name='mainpage'),
    path('devices/', get_devices, name='get_devices'),
    path('devpage/', devpage, name='devpage')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)