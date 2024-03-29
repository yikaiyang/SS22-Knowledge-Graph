"""
URL configuration for kg_webapp_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from .views import GetPOINodes, GetIncidentNodes, GetRoadNodes, GetPredictedRelatedNodes, GetSpeedRangeNodes, GetDateNodes, GetTimeNodes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('nodes', GetPredictedRelatedNodes.as_view(), name='get_related_nodes'),
    path('poi/', GetPOINodes.as_view(), name='get_poi'),
    path('incident/', GetIncidentNodes.as_view(), name='get_incidents'),
    path('road/', GetRoadNodes.as_view(), name='get_roads'),
    path('speed', GetSpeedRangeNodes.as_view(), name='get_speed'),
    path('date', GetDateNodes.as_view(), name='get_date'),
    path('time', GetTimeNodes.as_view(), name='get_time')
]
