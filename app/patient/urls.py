from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patient', views.patient_list, name='patient_list'),
    # path('/patient/<int:p_id>', views.patient_detail, name='patient_detail'),
]
