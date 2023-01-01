from django.shortcuts import render
from django.http import HttpResponse

from playground.models import Playground

# Create your views here.
def say_hello(request):
    query_set = Playground.objects.all()
    for product in query_set:
      print(product.title)
    
    # return query_set
    return HttpResponse('heelo')