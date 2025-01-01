from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('careers/', include('careers.urls', namespace='careers')),
    path('', lambda request: redirect('careers:career_list'), name='home'),
]