import time
import random
from firebase_admin import db
from energy_app.firebase_config import *  # This file initializes your Firebase app

# Get a reference to the 'sensor_data' node in Firebase.
sensor_ref = db.reference('sensor_data')

def update_sensor_data():
    # Simulate dynamic sensor readings using random values.
    # Replace these with actual sensor readings from your hardware.
    sensor_data = {
        "heterojunction_solar_voltage": round(random.uniform(40, 50), 2),  # in volts
        "heat_generated": round(random.uniform(25, 35), 2),                # in degrees Celsius
        "thermoelectric_voltage": round(random.uniform(10, 15), 2),        # in volts
        "output_voltage": round(random.uniform(220, 240), 2),              # in volts
        "max_power_generated": round(random.uniform(950, 1050), 2),          # in watts
        "load_power_consumption": round(random.uniform(750, 850), 2),        # in watts
        "unused_power": round(random.uniform(100, 300), 2),                  # in watts
        "two_axis_direction": {
            "x_axis": round(random.uniform(0, 90), 2),                       # in degrees
            "z_axis": round(random.uniform(0, 90), 2)                        # in degrees
        },
        "co2_level": round(random.uniform(350, 450), 2),                     # in ppm
        "carbon_reduction": round(random.uniform(20, 30), 2)                 # in percentage
    }
    
    # The update() method ensures that the same keys are overwritten,
    # so the data structure remains consistent.
    sensor_ref.update(sensor_data)
    print("Updated sensor data:", sensor_data)

if __name__ == "__main__":
    # Loop continuously to simulate real-time data updates.
    while True:
        update_sensor_data()
        time.sleep(5)  # Adjust the delay as needed (e.g., update every 5 seconds)
