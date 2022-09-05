from django.http import JsonResponse
from django.shortcuts import render
from calculator.models import Visualizer
from django.core import serializers

# Create your views here.
def index(request):
    return render(request, 'calculator/index.html')

def pivot_data(request):
    dataset = Visualizer.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

    