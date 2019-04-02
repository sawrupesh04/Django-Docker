from rest_framework import status
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer
from redis import Redis
from django.conf import settings
import pika
import threading
import time
import datetime
import sys
import paho.mqtt.client as paho
import socket

from .tasks import hello

# broker
# broker = '192.168.0.12'
# port = 1883
TOPIC = 'priya'

# Redis connection
r = Redis(host='redis', port=6379, db=3)


# Rabbit
def home(request):
    mqtthost = "192.168.0.104"
    mqttuser = "admin"
    mqttpass = "admin"
    mqtttopic = "deep"

    def on_connect(client, userdata, flags, rc):
        print("CONNACK received with code %d." % (rc))

    def on_publish(client, userdata, mid):
        print("mid: " + str(mid))

    client = paho.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.username_pw_set(mqttuser, mqttpass)
    client.connect(mqtthost, 1883, 60)

    client.loop_start()

    message = 'aya'
    (rc, mid) = client.publish(mqtttopic, str(message), qos=1)

    # time.sleep(10)

    return HttpResponse("Data has been sent")
    # return HttpResponse("Hello")


"""
    def onMqttConnectpub(client, userdata, flags, rc):
        if rc == 0:
            client1.connected_flag = True
            ret = client1.publish("shyam", "hello i am priya")
            print('published Status \n', ret)
        else:
            print("bad connection returned code=", rc)

    def onMqttConnectsub(client, userdata, flags, rc):
        if rc == 0:
            client2.connected_flag = True
            ret = client2.subscribe(TOPIC)
            print('subscribed Status \n', ret)
        else:
            print("bad connection returned code=", rc)

    def onGetMessage(client, userdata, message):
        print("received message =", str(message.payload.decode("utf-8")))

    client1 = paho.Client('client-001')
    client2 = paho.Client('client-002')

    client1.on_connect = onMqttConnectpub
    # client2.on_connect = onMqttConnectsub
    # client2.on_message = onGetMessage
    client1.connect('rabbit', 15672)
    # client2.connect(broker, port)

    client1.loop_start()
    client2.loop_start()


    connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs',
                             exchange_type='fanout')

    message = ' '.join(sys.argv[1:]) or "info: Hello World!"
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=message)
    print(" [x] Sent %r" % message)
    connection.close()

    
    # time_data = list()
    # file = open('time.txt', 'w')
    for i in range(10):
        a = datetime.datetime.now()
        time = "%s:%s.%s" % (a.hour, a.minute, a.microsecond)
        # file.write('TIME :  {} '.format(time+'\n'))
        # time_data.append(time)
        print(time)
    # file.close()

    mqtthost = "0.0.0.0"
    mqttuser = "admin"
    mqttpass = "mypass"
    mqtttopic = "hello"

    def on_connect(client, userdata, flags, rc):
        print("CONNACK received with code %d." % (rc))

    def on_publish(client, userdata, mid):
        print("mid: " + str(mid))

    client = paho.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.username_pw_set(mqttuser, mqttpass)
    client.connect(mqtthost, 1883, 60)
    client.loop_start()

   # print(socket.gethostname())

    return HttpResponse('END')
   
    """


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
            {'p_id': 'P3', 'name': 'Priya Pote', 'start': 'Yes', 'weight': 45.0, 'height': 159.0, 'time_stamp': '2019-03-02T05:28:45Z', 'location': 'Mumbai', 'city': 'Mumbai', 'email_id': 'priyan1@gmail.com', 'occupation': 'Engineer', 'mobile': '5678170687'}

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
