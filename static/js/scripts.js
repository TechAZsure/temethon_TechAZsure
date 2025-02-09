function updateSensorData() {
  fetch('/api/sensor-data/')
    .then(response => response.json())
    .then(data => {
      console.log("Data received:", data);
      // Update DOM elements:
      document.getElementById('solar_voltage').innerText =
        data.solar_voltage !== null ? data.solar_voltage : '--';
      document.getElementById('thermo_voltage').innerText =
        data.thermo_voltage !== null ? data.thermo_voltage : '--';
      document.getElementById('output_voltage').innerText =
        data.output_voltage !== null ? data.output_voltage : '--';
      document.getElementById('load_power').innerText =
        data.load_power !== null ? data.load_power : '--'; // Verify this line!
    })
    .catch(error => console.error('Error fetching sensor data:', error));
}

setInterval(updateSensorData, 5000);
updateSensorData();
