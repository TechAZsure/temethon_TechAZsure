from django.db import models

class EnergyData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    heterojunction_solar_voltage = models.FloatField(null=True, blank=True)
    heat_generated = models.FloatField(null=True, blank=True)
    thermoelectric_voltage = models.FloatField(null=True, blank=True)
    output_voltage = models.FloatField(null=True, blank=True)
    max_power_generated = models.FloatField(null=True, blank=True)
    load_power_consumption = models.FloatField(null=True, blank=True)
    unused_power = models.FloatField(null=True, blank=True)
    x_axis_direction = models.FloatField(null=True, blank=True)
    z_axis_direction = models.FloatField(null=True, blank=True)
    co2_level = models.FloatField(null=True, blank=True)
    carbon_reduction = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"EnergyData @ {self.timestamp}"
