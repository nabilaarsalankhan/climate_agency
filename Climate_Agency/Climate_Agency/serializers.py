# climate_app/serializers.py
from rest_framework import serializers
from .models import ClimateDataset, ClimateDataSource

class ClimateDataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimateDataSource
        fields = '__all__'

class ClimateDatasetSerializer(serializers.ModelSerializer):
    source = ClimateDataSourceSerializer(read_only=True)
    uploaded_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ClimateDataset
        fields = '__all__'