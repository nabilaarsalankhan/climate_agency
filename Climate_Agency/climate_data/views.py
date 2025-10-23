import requests
from django.shortcuts import render

API_KEY = "bedfaf1716027c9c280859ad56670795"  # 🔹 apna key yahan dalna

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
