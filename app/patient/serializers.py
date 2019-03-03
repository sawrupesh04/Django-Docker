from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('p_id', 'name', 'start', 'weight', 'height', 'time_stamp', 'location', 'city',
                  'email_id', 'occupation', 'mobile')
