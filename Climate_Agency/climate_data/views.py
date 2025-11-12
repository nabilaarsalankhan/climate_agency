from django.http import HttpResponse
from .models import User  # Django model linked to database
import requests
from django.shortcuts import render
from .models import User  # Your model
from .views import index 
from climate_data.views import index

API_KEY = "bedfaf1716027c9c280859ad56670795"  # 🔹 apna key yahan dalna


def hello(request):
    return HttpResponse("Hello Nabela!")

def add_user(request):
    user = User(name="Nabela", age=23)
    user.save()  # Saves to the database configured in Django settings
    return HttpResponse("User added!")


def index(request):
    city = request.GET.get("city", "Karachi")  # default city
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            raise Exception(data.get("message", "City not found"))

        context = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "sunrise": data["sys"]["sunrise"],
            "sunset": data["sys"]["sunset"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
        }
    except Exception as e:
        context = {"error": str(e), "city": city}

    return render(request, "climate_data/index.html", context)


def index(request):
    users = User.objects.all()  # Get all users from database
    context = {
        'message': 'Hello from Django!',
        'users': users
    }
    return render(request, 'my-app/index.html', context)

from django.shortcuts import render
def index(request):
    return render(request, 'climate_data/index.html')  

