from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ClimateRecord
from .serializers import ClimateRecordSerializer

class ClimateDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = ClimateRecord.objects.all()
        serializer = ClimateRecordSerializer(data, many=True)
        return Response(serializer.data)
