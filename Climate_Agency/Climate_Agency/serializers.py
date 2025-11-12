# climate_app/serializers.py
from rest_framework import serializers
from .models import ClimateDataset, ClimateDataSource
from rest_framework import serializers
from .models import ClimateRecord  # example model

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
        
class ClimateRecordSerializer(serializers.ModelSerializer):
    
   class Meta:
     model = ClimateRecord
     fields = '__all__'  # send all fields as JSON       