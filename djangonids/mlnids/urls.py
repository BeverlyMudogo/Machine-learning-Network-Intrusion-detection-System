"""
URL configuration for mlnids project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import start_capture, start_prediction_trigger, get_predictions, send_alert, get_packets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/start_capture/', start_capture, name='start_capture'),
    path('api/start_prediction_trigger/', start_prediction_trigger, name='start_prediction_trigger'),
    path('api/get_predictions/', get_predictions, name='get_predictions'),
    path('api/send_alert/', send_alert, name='send_alert'),
    path('api/get_packets', get_packets, name='get_packets'),
]
