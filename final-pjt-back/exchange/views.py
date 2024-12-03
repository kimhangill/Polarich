from django.shortcuts import render
from django.conf import settings
from .serializers import ExchangeSerializer
from .models import Exchange
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
import requests

# Create your views here.

API_KEY=settings.API_KEY_EXCHANGE

@api_view(['GET'])
def exchange(request):
    today = datetime.today().date()
    url=f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={API_KEY}&data=AP01'
    info = requests.get(url).json()
    
    for i in info:
        if not Exchange.objects.filter(date=datetime.today(),cur_unit=i.get('cur_unit')).exists():
            serializer = ExchangeSerializer(data=i)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

    result = Exchange.objects.all()
    serializer = ExchangeSerializer(result,many=True)
    return Response(serializer.data)
