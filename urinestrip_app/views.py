from django.shortcuts import render

# Create your views here.
import cv2
import os
from django.http import JsonResponse
from .models import UrineStrip
import numpy as np


def analyze_urinestrip(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        # colors = analyze_colors(image)
        # colors_json = json.dumps(colors)
        # urinestrip = UrineStrip(image=image, colors_json=colors_json)
        urinestrip = UrineStrip(image=image)
        urinestrip.save()
        colors = analyze_colors(urinestrip.image.url)
        return JsonResponse(colors, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request'})

def analyze_colors(imagepath): # /urinestrips/image3_oqLJQsX.jpg
    # detected_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    # return [{'R': r, 'G': g, 'B': b} for r, g, b in detected_colors]
    absolute_path = os.path.join(os.getcwd(), imagepath.split('/')[1] , imagepath.split('/')[2])
    image = cv2.imread(absolute_path)
    print(image, 'Image in ANALYZE_COLORS FUNCTION')
    print(image.shape)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper bounds for each color you want to detect
    color_ranges = [
        ((0, 50, 50), (20, 255, 255)),  # Red
        ((35, 50, 50), (85, 255, 255)),  # Yellow
        ((100, 50, 50), (140, 255, 255)),  # Green
        ((170, 50, 50), (180, 255, 255))  # Red (again, for the wrap-around in HSV)
    ]
    
    detected_colors = []
    
    # Iterate through each color range and find the corresponding pixels
    for (lower, upper) in color_ranges:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        
        mask = cv2.inRange(hsv_image, lower, upper)
        color_pixels = cv2.countNonZero(mask)
        
        # if color_pixels > 0:
        #     hsv_color = np.uint8([[[np.mean(lower[0], upper[0]), np.mean(lower[1], upper[1]), np.mean(lower[2], upper[2])]]])
        #     rgb_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
            
        #     detected_colors.append({'R': rgb_color[2], 'G': rgb_color[1], 'B': rgb_color[0]})
        if color_pixels > 0:
            # Calculate the HSV color corresponding to the detected color
            hsv_color = np.uint8([[[np.mean(lower[0], upper[0]), np.mean(lower[1], upper[1]), np.mean(lower[2], upper[2])]]])

            # Convert the HSV color to BGR
            bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]

            # Extract the individual B, G, and R components
            blue, green, red = bgr_color[0], bgr_color[1], bgr_color[2]

            detected_colors.append({'R': red, 'G': green, 'B': blue})



    return detected_colors


def index(request):
    return render(request, 'upload.html')