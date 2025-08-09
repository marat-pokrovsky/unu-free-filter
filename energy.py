from datetime import datetime, timedelta

energy_data = []

def log_energy_consumption(devices):
    """Log energy consumption"""
    total_power = 0
    for device in devices:
        if device["status"] == "on":
            # For thermostats, only count when actively heating/cooling
            if device["type"] == "thermostat" and device.get("heating_cooling") == "idle":
                continue
            total_power += device["power"]
    
    timestamp = datetime.now().isoformat()
    energy_data.append({
        "timestamp": timestamp,
        "power": total_power,
        "cost": calculate_energy_cost(total_power)
    })

def calculate_energy_cost(power):
    """Calculate energy cost with a more realistic tariff structure"""
    # Convert power (watts) to kWh for a 1-minute period
    kwh = power / 1000 * (1 / 60)  # consumption per minute
    
    # More realistic tariff structure with peak/off-peak rates
    current_hour = datetime.now().hour
    # Peak hours (7am-11pm) are more expensive
    if 7 <= current_hour < 23:
        rate = 0.15  # $0.15/kWh during peak hours
    else:
        rate = 0.10  # $0.10/kWh during off-peak hours
        
    return kwh * rate

def detect_anomalies():
    """Detect anomalies in energy consumption"""
    # Try to import required libraries
    try:
        from sklearn.ensemble import IsolationForest
        from sklearn.preprocessing import StandardScaler
        import numpy as np
    except ImportError:
        print("Anomaly detection disabled: Required libraries not available")
        return []
        
    if len(energy_data) < 24 * 60:  # less than 1 day of data
        return []
    
    # Prepare data
    power_values = [entry["power"] for entry in energy_data[-24*60:]]
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(np.array(power_values).reshape(-1, 1))
    
    # Train model
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(scaled_data)
    
    # Detect anomalies
    anomalies = model.predict(scaled_data)
    return [i for i, anomaly in enumerate(anomalies) if anomaly == -1]

def get_energy_report(devices, hours=24):
    """Energy consumption report"""
    now = datetime.now()
    start_time = now - timedelta(hours=hours)
    
    period_data = [e for e in energy_data 
                  if datetime.fromisoformat(e["timestamp"]) >= start_time]
    
    if not period_data:
        return {}
    
    total_energy = sum(e["power"] for e in period_data) / 60 / 1000  # kWh
    total_cost = sum(e["cost"] for e in period_data)
    
    # Consumption by devices - improved calculation
    device_consumption = {}
    # For each device, calculate how long it was on during the period
    for device in devices:
        if device["power"] > 0:  # Only devices that consume power
            # Count how many minutes this device was on
            minutes_on = 0
            for entry in period_data:
                # This is a simplified approach - in a real system we would track
                # device state changes more precisely
                minutes_on += 1 if device["status"] == "on" else 0
            
            # Calculate energy consumption for this device
            device_consumption[device["name"]] = device["power"] * minutes_on / 60 / 1000  # kWh
    
    return {
        "total_energy": total_energy,
        "total_cost": total_cost,
        "device_consumption": device_consumption
    }

def plot_energy_usage(hours=24):
    """Visualize energy consumption"""
    # Try to import required libraries
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Plotting disabled: matplotlib not available")
        return
        
    now = datetime.now()
    start_time = now - timedelta(hours=hours)
    
    period_data = [e for e in energy_data 
                  if datetime.fromisoformat(e["timestamp"]) >= start_time]
    
    if not period_data:
        print("No data to visualize")
        return
    
    timestamps = [datetime.fromisoformat(e["timestamp"]).strftime("%H:%M") for e in period_data]
    power_values = [e["power"] for e in period_data]
    
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, power_values, 'b-')
    plt.title("Smart Home Energy Consumption")
    plt.xlabel("Time")
    plt.ylabel("Power (Watts)")
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_device_consumption(devices):
    """Visualize consumption by devices"""
    # Try to import required libraries
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("Plotting disabled: Required libraries not available")
        return
        
    report = get_energy_report(devices, 24)
    if not report or not report.get("device_consumption"):
        print("No data to visualize")
        return
    
    devices_names = list(report["device_consumption"].keys())
    consumption = list(report["device_consumption"].values())
    
    # Sort by descending order
    sorted_idx = np.argsort(consumption)[::-1]
    devices_names = [devices_names[i] for i in sorted_idx]
    consumption = [consumption[i] for i in sorted_idx]
    
    plt.figure(figsize=(12, 6))
    plt.bar(devices_names, consumption, color='skyblue')
    plt.title("Energy Consumption by Devices")
    plt.xlabel("Devices")
    plt.ylabel("Energy (kWh)")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
