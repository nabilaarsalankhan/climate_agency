from django.shortcuts import render
from .models import WeatherReport
from django.shortcuts import render
import requests
import os

# 🌤 Home Page (Fetch from API)
def home(request):
    city = request.GET.get('city', 'Karachi')
    api_key = 'bedfaf1716027c9c280859ad56670795'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    data = requests.get(url).json()

# save to MongoDB
WeatherReport.objects.create(
    city=city,
    temperature=data['main']['temp'],
    humidity=data['main']['humidity'],
    wind_speed=data['wind']['speed'],
    description=data['weather'][0]['description']
)

context = {
        'city': city,
        'temp': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'wind': data['wind']['speed'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'] 
    }
def home(request):
    city = request.GET.get('city', 'Karachi')
    api_key = 'bedfaf1716027c9c280859ad56670795'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    data = requests.get(url).json()

    # save to MongoDB
    WeatherReport.objects.create(
        city=city,
        temperature=data['main']['temp'],
        humidity=data['main']['humidity'],
        wind_speed=data['wind']['speed'],
        description=data['weather'][0]['description']
    )

    context = {
        'city': city,
        'temp': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'wind': data['wind']['speed'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'] 
    }
    return render(request, 'weather/home.html', context)
