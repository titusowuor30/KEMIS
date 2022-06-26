from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from django.shortcuts import render, redirect
from requests.auth import HTTPBasicAuth
import json
from .models import *
from time import sleep, perf_counter
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from KEMIS import settings
import time
from time import sleep
from sinchsms import SinchSMS
from django.core.mail import send_mail
import messagebird



global message
global msghead
message=""
msghead=""
def getAccessToken(request):
    consumer_key = 'pl1iuAP0UJTg7iHSGWsuTwKNBXcAbZCU'
    consumer_secret = 'BUzDTBeGOO0P8HMn'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


#@csrf_exempt
def lipa_na_mpesa_online(request):
    if request.method == 'POST':
        body_unicode = request.POST  # request.body.decode('utf-8')
        #body = json.loads(body_unicode)
        print(body_unicode)
        global payinfo
        payinfo = body_unicode
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(float(body_unicode['total'])),
            "PartyA": body_unicode['phone'],
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": body_unicode['phone'],
            "CallBackURL": "https://7090-105-161-91-67.in.ngrok.io/callback/",
            "AccountReference": "WMS for %s" % body_unicode['invoice_id'],
            "TransactionDesc": "WMS for %s" % body_unicode['invoice_id']
        }

        response = requests.post(api_url, json=request, headers=headers)
    #return HttpResponse({"CallBack Sent! ":response})
    global message
    global msghead
    message = ""
    msghead = ""
    sleep(15)
    return redirect("display")


@csrf_exempt
def MpesaCallBack(request):
    try:
        data = request.body.decode('utf-8')
        #print("callback sent:"+str(data))
        mpesa_payment = json.loads(data)
        #print(mpesa_payment)
        result = 0
        global message
        global msghead
        message = ""
        msghead = ""
        if result == mpesa_payment['Body']['stkCallback']['ResultCode']:
            msghead="Invoice Payment"
            print(msghead)
            message = "Payment Made Successfully!\nTranasction #ID {}!".format(payinfo['invoice_id'])
            print(message)
            SubmitToDB(request)
            if payinfo['email']:
                send_email(msghead,message)
            if payinfo['sms']:
                sendSMS(msghead,message)  
            message = ""
            msghead = ""          
        else:
            msghead = "Failed!"
            print(msghead)
            print("Payment cancelled by user")   
            message = "Request Failed!\nPayment cancelled by user!"
            displaymsg(request)
            message = ""
            msghead = ""
        return redirect('display')
    except Exception as e:
        print(e)


def SubmitToDB(request):
    try:
        print(payinfo)
        invoice=waste_invoice.objects.get(invoice_id=payinfo['invoice_id'])
        print(invoice)
        invoice.status="Paid"
        invoice.save()
        displaymsg(request)
    except Exception as e:
        print(e)
    
def displaymsg(request):
    try:
       return render(request, "pages/result/payinfo.html", {'message': message, 'msghead': msghead})
    except Exception as e:
        print(e)


def send_email(subject,message):
    print(settings.EMAIL_HOST_USER)
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            ['info@tdbsoft.co.ke'],
            fail_silently=False,
        )
        print('Mail Sent')
    except Exception as e:
        print(e)    
    
# function for sending SMS


def sendSMS(msghead,message):
    # 'test_gshuPaZoeEG6ovbc8M79w0QyM'  # xkMHWtkM2FBlxjYmbnc91u1la #307yPiT7RKFdqMLto2ObUn8A7
    ACCESS_KEY = settings.MESSAGE_BIRD_TEST_API_KEY
    print(ACCESS_KEY)
    try:
        # Create a MessageBird client with the specified ACCESS_KEY.
        client = messagebird.Client(ACCESS_KEY)
        # Send a new message.
        print(msghead)
        print(message)
        number=settings.TEL
        print(settings.TEL)
        msg = client.message_create(
          'WMS Center',
          '+254743793901',
          'New Invoice Generated please login to WMS and check',
          { 'reference' : 'Foobar' }
        )
        # Print the object information.
        print('\nThe following information was returned as a Message object:\n')
        print('  id                : %s' % msg.id)
        print('  href              : %s' % msg.href)
        print('  direction         : %s' % msg.direction)
        print('  type              : %s' % msg.type)
        print('  originator        : %s' % msg.originator)
        print('  body              : %s' % msg.body)
        print('  reference         : %s' % msg.reference)
        print('  validity          : %s' % msg.validity)
        print('  gateway           : %s' % msg.gateway)
        print('  typeDetails       : %s' % msg.typeDetails)
        print('  datacoding        : %s' % msg.datacoding)
        print('  mclass            : %s' % msg.mclass)
        print('  scheduledDatetime : %s' % msg.scheduledDatetime)
        print('  createdDatetime   : %s' % msg.createdDatetime)
        print('  recipients        : %s\n' % msg.recipients)
        print('Message Sent!')
        print()
    except messagebird.client.ErrorException as e:
        print('\nAn error occured while requesting a Message object:\n')

        for error in e.errors:
            print('  code        : %d' % error.code)
            print('  description : %s' % error.description)
            print('  parameter   : %s\n' % error.parameter)
