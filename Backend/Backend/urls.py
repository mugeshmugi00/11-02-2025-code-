"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include,re_path

from django.conf import settings
from Masters.views import serve_react
urlpatterns = [
     path('chirayu/admin/', admin.site.urls),
    path('chirayu/Masters/',include('Masters.urls')),
    path('chirayu/Frontoffice/',include('Frontoffice.urls')),
    path('chirayu/IP/',include('IP.urls')),
    path('chirayu/OP/',include('OutPatient.urls')),
    path('chirayu/LeninManagement/',include('LeninManagement.urls')),
    path('chirayu/Workbench/',include('Workbench.urls')),
    path('chirayu/MisReports/',include('MisReports.urls')),
    path('chirayu/Ip_Workbench/',include('Ip_Workbench.urls')),
    path('chirayu/Inventory/',include('Inventory.urls')),
    path('chirayu/DrugAdminstrations/',include('DrugAdminstrations.urls')),
    path('chirayu/Insurance/',include('Insurance.urls')),
    path('chirayu/HR_Management/',include('HR_Management.urls')),   
    path('chirayu/finance/',include('Finance.urls')),    
    path('chirayu/AccetCategory/',include('AccetCategory.urls')),
    path('chirayu/WasteManagement/',include('WasteManagement.urls')),
    
    # re_path(r"^(?P<path>.*)$", serve_react, {"document_root": settings.REACT_APP_BUILD_PATH}),
    
]