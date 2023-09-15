from django.shortcuts import render

# Create your views here.
import cv2
import json
from django.http import JsonResponse
from .models import UrineStrip

def analyze_urinestrip(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        colors = analyze_colors(image)
        colors_json = json.dumps(colors)

        urinestrip = UrineStrip(image=image, colors_json=colors_json)
        urinestrip.save()
        return JsonResponse(colors)
    else:
        return JsonResponse({'error': 'Invalid request'})

def analyze_colors(image):
    # TODO Use OpenCV to analyze the colors in the image and return them as a list of RGB values
    # For now, just returning a list of three random colors
    detected_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    return [{'R': r, 'G': g, 'B': b} for r, g, b in detected_colors]


def index(request):
    return render(request, 'upload.html')