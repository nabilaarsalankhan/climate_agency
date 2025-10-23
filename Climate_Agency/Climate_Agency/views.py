from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import requests

# ✅ Your registered API key (keep it as you said)
API_KEY = 'bedfaf1716027c9c280859ad56670795'
BASE_URL = 'https://api.openweathermap.org/data/2.5/'


def index(request):
    weather_data = None
    if request.method == 'POST':
        city = request.POST.get('city')
        url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
        else:
            weather_data = {'error': 'City not found.'}

    return render(request, 'index.html', {'weather': weather_data})


def home(request):
    city = request.GET.get("city", "Karachi")  # default city
    weather, hourly, daily = None, [], []
    error = None

    try:
        # ✅ Current weather API call
        res = requests.get(f"{BASE_URL}weather?q={city}&units=metric&appid={API_KEY}").json()

        if res.get("cod") != 200:
            error = res.get("message", "City not found")
        else:
            weather = {
                "city": res["name"],
                "country": res["sys"]["country"],
                "temperature": round(res["main"]["temp"]),
                "description": res["weather"][0]["description"],
                "icon": res["weather"][0]["icon"],
                "humidity": res["main"]["humidity"],
                "wind": round(res["wind"]["speed"]),
                "sunrise": datetime.fromtimestamp(res["sys"]["sunrise"]).strftime("%H:%M"),
                "sunset": datetime.fromtimestamp(res["sys"]["sunset"]).strftime("%H:%M"),
                "condition": res["weather"][0]["main"],
            }

        # ✅ Forecast API call
        f_res = requests.get(f"{BASE_URL}forecast?q={city}&units=metric&appid={API_KEY}").json()
        if f_res.get("cod") == "200":
            # Hourly next 12 slots
            for item in f_res["list"][:12]:
                hourly.append({
                    "time": datetime.fromtimestamp(item["dt"]).strftime("%H:%M"),
                    "temp": round(item["main"]["temp"]),
                    "icon": item["weather"][0]["icon"],
                })

            # Daily forecast (1 per day, max 15)
            seen_days = set()
            for item in f_res["list"]:
                day = datetime.fromtimestamp(item["dt"]).strftime("%a %d")
                if day not in seen_days and len(daily) < 15:
                    seen_days.add(day)
                    daily.append({
                        "day": day,
                        "temp": round(item["main"]["temp"]),
                        "icon": item["weather"][0]["icon"],
                    })

    except Exception as e:
        error = str(e)

    return render(request, "index.html", {
        "weather": weather,
        "hourly": hourly,
        "daily": daily,
        "error": error,
    })
