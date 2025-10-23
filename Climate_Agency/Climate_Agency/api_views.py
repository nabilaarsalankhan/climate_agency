# climate_app/api_views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from .models import ClimateDataset, ClimateDataSource
from .serializers import ClimateDatasetSerializer, ClimateDataSourceSerializer
import requests

class ClimateDataSourceViewSet(viewsets.ModelViewSet):
    queryset = ClimateDataSource.objects.all()
    serializer_class = ClimateDataSourceSerializer

class ClimateDatasetViewSet(viewsets.ModelViewSet):
    queryset = ClimateDataset.objects.all()
    serializer_class = ClimateDatasetSerializer

    @action(detail=False, methods=['post'])
    def fetch_open_meteo(self, request):
        """
        Fetch weather data from Open-Meteo API (no API key needed).
        Example body:
        {
            "lat": 24.9056,
            "lon": 67.0822,
            "city": "Karachi"
        }
        """
        # Get latitude/longitude from request (defaults to Karachi)
        lat = request.data.get("lat", 24.9056)
        lon = request.data.get("lon", 67.0822)
        city = request.data.get("city", "Karachi")

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m"
        }
        response = requests.get(url, params=params).json()

        # Create or get DataSource
        source, _ = ClimateDataSource.objects.get_or_create(
            name="Open-Meteo",
            source_type="weather_station",
            location=f"{city} ({lat},{lon})"
        )

        # Pick an admin as uploader
        User = get_user_model()
        admin_user = User.objects.filter(role="admin").first()

        # Save as ClimateDataset
        dataset = ClimateDataset.objects.create(
            name=f"Open-Meteo Weather - {city} - {now().strftime('%Y-%m-%d %H:%M')}",
            description="Weather data fetched from Open-Meteo API",
            data_type="temperature",
            format_type="json",
            source=source,
            file_size=len(str(response)),
            uploaded_by=admin_user,
            time_period_start=now(),
            time_period_end=now(),
            geographical_scope=city,
            is_public=True,
            requires_processing=False,
            file="dummy.json"  # placeholder
        )

        serializer = self.get_serializer(dataset)

        return Response({
            "dataset_saved": serializer.data,
            "api_response": response
        })