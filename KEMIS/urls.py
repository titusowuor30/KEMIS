"""KEMIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
# this is needed for file and image upload
from django.conf.urls.static import static
from django.conf import settings
from managemenet.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    # waste management
    path('', home_view.as_view(), name='home'),
    path('', include('managemenet.urls')),
    path('add-industry/', add_industry.as_view(), name='add-industry'),
    path('view-company/', company_view.as_view(), name='view-industry'),
    path('result/', result_view.as_view(), name='result'),
    path('auth', include('authentication.urls')),
    path('match-companies/<int:id>/', MatchListView, name="recycle"),
    path('recycle/<int:current_companyid>/<int:matching_companyid>/<int:waste_id>/',
         CreateInvoice, name='create_invoice'),
    path("invoices/", invoiceListView, name='invoices'),
    path('accounts/', include('django.contrib.auth.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# default: "Django Administration"
admin.site.site_header = 'KEMIS Administration'
# default: "Site administration"
admin.site.index_title = 'Admin Area'
admin.site.site_title = 'Administration'
