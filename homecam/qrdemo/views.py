from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

# Create your views here.
def qrhome(request):
    return render(request, 'qrdemo/index.html')

def get_qr(request):
    qr_query = (request.GET['qr_query'])
    url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + qr_query
    response = requests.get(url)
    print(response.content)
    context = {
        'name': qr_query,
        'img': url
    }
    print(qr_query)
    return render(request, 'qrdemo/index.html', context=context)