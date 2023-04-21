"""postgresDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include #new

# this is where we import the url to represent the dbApp folder
# so the data/ path represents our whole endpoint
# so data/tel/pk is the specific telemetry endpoint and data/pos/pk is the position endpoint
# (pk represents packet number)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('data/', include('dbApp.urls')), #new
]
