from rest_framework import status
from django.core.cache import cache
from django.http import HttpResponse
from .serializers import PatientSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient
from redis import Redis
import pika


# Redis connection
r = Redis(host='redis', port=6379, db=3)


# Rabbit connection01
connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0'))


channel = connection.channel()
while True:
    body = input('Enter body Section :')
    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=body)

    print('[*] sent message {}!'.format(body))

connection.close()

def home(request):
    cache.set('name', 'rupesh')
    # return render(request, 'home.html'2)
    return HttpResponse(cache.get('name'))


@api_view(['GET', 'POST'])
def patient_list(request):
    """
    List all code patients, or create a new patient.
    """
    if request.method == 'GET':
        patient = Patient.objects.all()
        serializer = PatientSerializer(patient, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            patient_data = serializer.data
            """
            {'p_id': 'P3', 'name': 'Priya ote', 'start': 'Yes', 'weight': 45.0, 'height': 159.0, 'time_stamp': '2019-03-02T05:28:45Z', 'location': 'Mumbai', 'city': 'Mumbai', 'email_id': 'priyan1@gmail.com', 'occupation': 'Engineer', 'mobile': '5678170687'}

            """
            r.set(patient_data['name'], '1234')
            print(r.get(patient_data['name']).decode('utf-8'))
            content = {"message": "success"}
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def patient_detail(request, patient_id):
    """
    Retrieve, update or delete a code patient.
    """
    try:
        patient = Patient.objects.get(patient_id=patient_id)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
