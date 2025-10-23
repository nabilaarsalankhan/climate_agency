from djongo import models

class WeatherReport(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    description = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
def __str__(self):
    return f"{self.city} - {self.date.strftime('%Y-%m-%d %H:%M')}"
