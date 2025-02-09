from django.http import HttpResponse
from .models import EnergyData
from firebase_admin import db
import firebase_config
from .models import EnergyData
from django.http import JsonResponse

def fetch_and_store_data():
    try:
        # Get reference to sensor_data in Firebase
        sensor_ref = db.reference('sensor_data')
        sensor_data = sensor_ref.get()  # Fetch the latest sensor readings

        if sensor_data is None:
            return HttpResponse("No sensor data found in Firebase.")

        # Create a new EnergyData record using the fetched data
        energy_instance = EnergyData(
            heterojunction_solar_voltage=sensor_data.get('heterojunction_solar_voltage'),
            heat_generated=sensor_data.get('heat_generated'),
            thermoelectric_voltage=sensor_data.get('thermoelectric_voltage'),
            output_voltage=sensor_data.get('output_voltage'),
            max_power_generated=sensor_data.get('max_power_generated'),
            load_power_consumption=sensor_data.get('load_power_consumption'),
            unused_power=sensor_data.get('unused_power'),
            x_axis_direction=sensor_data.get('two_axis_direction', {}).get('x_axis'),
            z_axis_direction=sensor_data.get('two_axis_direction', {}).get('z_axis'),
            co2_level=sensor_data.get('co2_level'),
            carbon_reduction=sensor_data.get('carbon_reduction')
        )
        energy_instance.save()  # Store data in MySQL

        return HttpResponse("Data stored successfully: " + str(energy_instance))
    except Exception as e:
        return HttpResponse("Error: " + str(e))

def sensor_data_api(request):
    latest_data = EnergyData.objects.order_by('-timestamp').first()
    if latest_data:
        data = {
            'solar_voltage': latest_data.heterojunction_solar_voltage,
            'thermo_voltage': latest_data.thermoelectric_voltage,
            'output_voltage': latest_data.output_voltage,
            'load_power': latest_data.load_power_consumption,  # Verify this field is present
            'heat_generated': latest_data.heat_generated,
            'max_power_generated': latest_data.max_power_generated,
            'unused_power': latest_data.unused_power,
            'x_axis_direction': latest_data.x_axis_direction,
            'z_axis_direction': latest_data.z_axis_direction,
            'co2_level': latest_data.co2_level,
            'carbon_reduction': latest_data.carbon_reduction,
        }
    else:
        data = {  # default values if no record exists
            'solar_voltage': None,
            'thermo_voltage': None,
            'output_voltage': None,
            'load_power': None,
            'heat_generated': None,
            'max_power_generated': None,
            'unused_power': None,
            'x_axis_direction': None,
            'z_axis_direction': None,
            'co2_level': None,
            'carbon_reduction': None,
        }
    return JsonResponse(data)
