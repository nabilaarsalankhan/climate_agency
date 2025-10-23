import requests
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from Climate_Agency.models import ClimateDataSource, ClimateDataset

def fetch_open_meteo(city_coords):
    # city_coords = (lat, lon)
    lat, lon = city_coords
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }

    # Fetch weather data
    resp = requests.get(url, params=params).json()
    current = resp.get("current_weather", {})

    # ✅ Create or get the data source
    source, _ = ClimateDataSource.objects.get_or_create(
        name="OpenMeteo",
        source_type="weather_station",
        location=f"Lat {lat}, Lon {lon}"
    )

    # ✅ Get an admin user (first admin)
    User = get_user_model()
    admin = User.objects.filter(is_superuser=True).first()

    # ✅ Create dataset entry
    dataset = ClimateDataset.objects.create(
        name=f"OpenMeteo Weather - {lat},{lon} - {now()}",
        description="Weather data from OpenMeteo API",
        data_type="temperature",
        format_type="json",
        source=source,
        file_size=len(str(resp)),
        uploaded_by=admin,
        time_period_start=now(),
        time_period_end=now(),
        geographical_scope=f"{lat},{lon}",
        is_public=True,
        requires_processing=False,
        file="dummy.json"  # Placeholder
    )

    return dataset, resp
