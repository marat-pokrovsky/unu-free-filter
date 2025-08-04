import json
import os
import random
import time
from datetime import datetime, timedelta
import threading


class SmartHomeSystem:
    def __init__(self, config_file="smart_home_config.json"):
        """Initialize the smart home system"""
        self.config_file = config_file
        self.devices = []
        self.rooms = []
        self.automations = []
        self.energy_data = []
        self.security_log = []
        self.load_config()
        self.running = False
        self.simulation_thread = None

    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file) as f:
                    config = json.load(f)
                    self.devices = config.get("devices", [])
                    self.rooms = config.get("rooms", [])
                    self.automations = config.get("automations", [])
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
        
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                "devices": self.devices,
                "rooms": self.rooms,
                "automations": self.automations
            }
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")

    def add_room(self, name, room_type):
        """Add a room to the system"""
        room = {
            "id": len(self.rooms) + 1,
            "name": name,
            "type": room_type,  # living, bedroom, kitchen, bathroom, outdoor
            "devices": []
        }
        self.rooms.append(room)
        self.save_config()
        return room

    def add_device(self, name, device_type, room_id, status="off", power=0, **kwargs):
        """Add a device to the system"""
        device = {
            "id": len(self.devices) + 1,
            "name": name,
            "type": device_type,  # light, thermostat, camera, lock, sensor, appliance
            "status": status,
            "power": power,  # Watts
            "room_id": room_id,
            "last_update": datetime.now().isoformat()
        }
        
        # Add additional attributes if provided
        for key, value in kwargs.items():
            device[key] = value
        
        self.devices.append(device)
        
        # Add device to room
        for room in self.rooms:
            if room["id"] == room_id:
                room["devices"].append(device["id"])
                break
        
        self.save_config()
        return device

    def update_device_status(self, device_id, status, value=None):
        """Update device status"""
        for device in self.devices:
            if device["id"] == device_id:
                device["status"] = status
                device["last_update"] = datetime.now().isoformat()
                
                # For thermostats, update temperature value
                if device["type"] == "thermostat" and value is not None:
                    device["value"] = value
                
                # Log changes
                self.log_security_event(f"Device {device['name']} changed: {status}")
                return device
        return None

    def get_room_devices(self, room_id):
        """Get devices in a room"""
        return [device for device in self.devices if device["room_id"] == room_id]

    def add_automation(self, name, trigger, condition, actions):
        """Add automation rule"""
        automation = {
            "id": len(self.automations) + 1,
            "name": name,
            "trigger": trigger,  # {"type": "time", "value": "18:00"} or {"type": "sensor", "sensor_id": 123, "condition": ">", "value": 30}
            "condition": condition,  # {"type": "presence", "room_id": 1} or None
            "actions": actions  # [{"device_id": 1, "command": "on"}, ...]
        }
        self.automations.append(automation)
        self.save_config()
        return automation

    def check_automations(self):
        """Check and execute automations"""
        now = datetime.now()
        for automation in self.automations:
            trigger = automation["trigger"]
            executed = False
            
            # Time trigger
            if trigger["type"] == "time":
                try:
                    trigger_time = datetime.strptime(trigger["value"], "%H:%M").time()
                    last_executed_str = automation.get("last_executed", "2000-01-01T00:00:00")
                    last_executed = datetime.strptime(last_executed_str.split(".")[0], "%Y-%m-%dT%H:%M:%S")
                    if now.time() >= trigger_time and (now - last_executed).days >= 1:
                        executed = self.execute_automation(automation)
                except ValueError as e:
                    print(f"Error parsing time for automation {automation['name']}: {e}")
            
            # Sensor trigger
            elif trigger["type"] == "sensor":
                sensor = next((d for d in self.devices if d["id"] == trigger["sensor_id"]), None)
                if sensor and self.check_sensor_condition(sensor, trigger["condition"], trigger["value"]):
                    executed = self.execute_automation(automation)
            
            if executed:
                automation["last_executed"] = now.isoformat()

    def check_sensor_condition(self, sensor, condition, value):
        """Check sensor condition"""
        sensor_value = sensor.get("value", 0)
        try:
            value = float(value)
            if condition == ">": return sensor_value > value
            if condition == "<": return sensor_value < value
            if condition == "==": return sensor_value == value
            if condition == ">=": return sensor_value >= value
            if condition == "<=": return sensor_value <= value
        except (ValueError, TypeError):
            return False
        return False

    def execute_automation(self, automation):
        """Execute automation actions"""
        # Check conditions
        if automation["condition"]:
            cond = automation["condition"]
            if cond["type"] == "presence":
                # Check presence in room (simplified)
                room_devices = self.get_room_devices(cond["room_id"])
                motion_sensors = [d for d in room_devices if d["type"] == "sensor" and d.get("subtype") == "motion"]
                if not any(s["status"] == "active" for s in motion_sensors):
                    return False
        
        # Execute actions
        for action in automation["actions"]:
            self.update_device_status(action["device_id"], action["command"])
        
        self.log_security_event(f"Automation executed: {automation['name']}")
        return True

    def log_energy_consumption(self):
        """Log energy consumption"""
        total_power = 0
        for device in self.devices:
            if device["status"] == "on":
                # For thermostats, only count when actively heating/cooling
                if device["type"] == "thermostat" and device.get("heating_cooling") == "idle":
                    continue
                total_power += device["power"]
        
        timestamp = datetime.now().isoformat()
        self.energy_data.append({
            "timestamp": timestamp,
            "power": total_power,
            "cost": self.calculate_energy_cost(total_power)
        })

    def calculate_energy_cost(self, power):
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

    def log_security_event(self, event, severity="info"):
        """Log security event"""
        self.security_log.append({
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "severity": severity
        })

    def detect_anomalies(self):
        """Detect anomalies in energy consumption"""
        # Try to import required libraries
        try:
            from sklearn.ensemble import IsolationForest
            from sklearn.preprocessing import StandardScaler
            import numpy as np
        except ImportError:
            print("Anomaly detection disabled: Required libraries not available")
            return []
            
        if len(self.energy_data) < 24 * 60:  # less than 1 day of data
            return []
        
        # Prepare data
        power_values = [entry["power"] for entry in self.energy_data[-24*60:]]
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(np.array(power_values).reshape(-1, 1))
        
        # Train model
        model = IsolationForest(contamination=0.01, random_state=42)
        model.fit(scaled_data)
        
        # Detect anomalies
        anomalies = model.predict(scaled_data)
        return [i for i, anomaly in enumerate(anomalies) if anomaly == -1]

    def simulate_home(self):
        """Simulate smart home operation"""
        self.running = True
        print("Smart home simulation started...")
        
        while self.running:
            # Update sensor values
            for device in self.devices:
                if device["type"] == "sensor":
                    # Randomly change sensor values
                    if random.random() > 0.7:
                        if device.get("subtype") == "temperature":
                            device["value"] = round(random.uniform(18, 25), 1)
                        elif device.get("subtype") == "motion":
                            device["status"] = "active" if random.random() > 0.8 else "inactive"
            
            # Check automations
            self.check_automations()
            
            # Log energy
            self.log_energy_consumption()
            
            time.sleep(1)  # 1 second simulation = 1 minute real time

    def start_simulation(self):
        """Start simulation in separate thread"""
        if not self.simulation_thread or not self.simulation_thread.is_alive():
            self.simulation_thread = threading.Thread(target=self.simulate_home)
            self.simulation_thread.daemon = True
            self.simulation_thread.start()

    def stop_simulation(self):
        """Stop simulation"""
        self.running = False
        if self.simulation_thread:
            self.simulation_thread.join()

    def get_energy_report(self, hours=24):
        """Energy consumption report"""
        now = datetime.now()
        start_time = now - timedelta(hours=hours)
        
        period_data = [e for e in self.energy_data 
                      if datetime.fromisoformat(e["timestamp"]) >= start_time]
        
        if not period_data:
            return {}
        
        total_energy = sum(e["power"] for e in period_data) / 60 / 1000  # kWh
        total_cost = sum(e["cost"] for e in period_data)
        
        # Consumption by devices - improved calculation
        device_consumption = {}
        # For each device, calculate how long it was on during the period
        for device in self.devices:
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

    def plot_energy_usage(self, hours=24):
        """Visualize energy consumption"""
        # Try to import required libraries
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Plotting disabled: matplotlib not available")
            return
            
        now = datetime.now()
        start_time = now - timedelta(hours=hours)
        
        period_data = [e for e in self.energy_data 
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

    def plot_device_consumption(self):
        """Visualize consumption by devices"""
        # Try to import required libraries
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            print("Plotting disabled: Required libraries not available")
            return
            
        report = self.get_energy_report(24)
        if not report or not report.get("device_consumption"):
            print("No data to visualize")
            return
        
        devices = list(report["device_consumption"].keys())
        consumption = list(report["device_consumption"].values())
        
        # Sort by descending order
        sorted_idx = np.argsort(consumption)[::-1]
        devices = [devices[i] for i in sorted_idx]
        consumption = [consumption[i] for i in sorted_idx]
        
        plt.figure(figsize=(12, 6))
        plt.bar(devices, consumption, color='skyblue')
        plt.title("Energy Consumption by Devices")
        plt.xlabel("Devices")
        plt.ylabel("Energy (kWh)")
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
    
    def get_security_report(self):
        """Security report"""
        now = datetime.now()
        start_time = now - timedelta(hours=24)
        
        period_events = [e for e in self.security_log 
                        if datetime.fromisoformat(e["timestamp"]) >= start_time]
        
        critical_events = [e for e in period_events if e.get("severity") == "critical"]
        
        return {
            "total_events": len(period_events),
            "critical_events": len(critical_events),
            "last_events": period_events[-5:] if period_events else []
        }

    def simulate_security_breach(self):
        """Simulate security breach"""
        # Select a random door or window
        access_devices = [d for d in self.devices if d["type"] == "lock" and "door" in d["name"].lower()]
        if not access_devices:
            return
        
        device = random.choice(access_devices)
        self.log_security_event(f"Unauthorized access attempt: {device['name']}", severity="critical")
        
        # Activate alarm
        alarm = next((d for d in self.devices if "alarm" in d["name"].lower()), None)
        if alarm:
            self.update_device_status(alarm["id"], "on")

    def save_current_state(self):
        """Save current system state"""
        state = {
            "devices": self.devices,
            "energy_data": self.energy_data,
            "security_log": self.security_log,
            "timestamp": datetime.now().isoformat()
        }
        try:
            with open("smart_home_state.json", "w") as f:
                json.dump(state, f, indent=2)
        except IOError as e:
            print(f"Error saving state: {e}")

# Create demo configuration
def create_demo_config():
    """Create demo smart home configuration"""
    system = SmartHomeSystem()
    
    # Add rooms
    living_room = system.add_room("Living Room", "living")
    bedroom = system.add_room("Bedroom", "bedroom")
    kitchen = system.add_room("Kitchen", "kitchen")
    outside = system.add_room("Outside", "outdoor")
    
    # Add devices
    system.add_device("Main Light", "light", living_room["id"], power=60)
    system.add_device("Thermostat", "thermostat", living_room["id"], power=500, status="on")
    system.add_device("Television", "appliance", living_room["id"], power=120)
    system.add_device("Security Camera", "camera", outside["id"], power=15, status="on")
    system.add_device("Motion Sensor", "sensor", living_room["id"], power=5, status="inactive", subtype="motion")
    system.add_device("Temperature Sensor", "sensor", living_room["id"], power=5, status="on", subtype="temperature", value=22.0)
    system.add_device("Motion Sensor", "sensor", kitchen["id"], power=5, status="inactive", subtype="motion")
    system.add_device("Temperature Sensor", "sensor", kitchen["id"], power=5, status="on", subtype="temperature", value=21.0)
    system.add_device("Front Door", "lock", outside["id"], power=10, status="locked")
    system.add_device("Alarm System", "alarm", outside["id"], power=100, status="off")
    
    # Add automations
    system.add_automation(
        name="Evening Lights",
        trigger={"type": "time", "value": "18:00"},
        condition={"type": "presence", "room_id": living_room["id"]},
        actions=[{"device_id": 1, "command": "on"}]
    )
    
    system.add_automation(
        name="Night Energy Saving",
        trigger={"type": "time", "value": "23:00"},
        condition=None,
        actions=[
            {"device_id": 1, "command": "off"},
            {"device_id": 3, "command": "off"}
        ]
    )
    
    system.add_automation(
        name="Air Conditioning on Hot Days",
        trigger={"type": "sensor", "sensor_id": 6, "condition": ">", "value": "25"},
        condition={"type": "presence", "room_id": living_room["id"]},
        actions=[{"device_id": 2, "command": "cool"}]
    )
    
    return system


# Example usage
if __name__ == "__main__":
    # Create smart home system
    home_system = create_demo_config()
    
    # Start simulation
    home_system.start_simulation()
    
    # User interaction simulation
    print("\\nSmart Home Control:")
    print("1. Turn on living room lights")
    print("2. Unlock front door")
    print("3. Simulate security breach")
    print("4. Show reports")
    print("5. Stop simulation")
    
    try:
        while True:
            choice = input("\\nSelect action: ")
            
            if choice == "1":
                # Turn on lights
                light = next(d for d in home_system.devices if "light" in d["name"].lower())
                home_system.update_device_status(light["id"], "on")
                print("Living room lights turned on")
                
            elif choice == "2":
                # Unlock door
                door = next(d for d in home_system.devices if "door" in d["name"].lower())
                home_system.update_device_status(door["id"], "unlocked")
                print("Front door unlocked")
                
            elif choice == "3":
                # Simulate security breach
                home_system.simulate_security_breach()
                print("Security breach simulated")
                
            elif choice == "4":
                # Reports
                energy_report = home_system.get_energy_report()
                print("\\nEnergy Report:")
                print(f"Consumed: {energy_report['total_energy']:.2f} kWh")
                print(f"Cost: ${energy_report['total_cost']:.2f}")
                
                security_report = home_system.get_security_report()
                print("\\nSecurity Report:")
                print(f"Events in 24h: {security_report['total_events']}")
                print(f"Critical events: {security_report['critical_events']}")
                print("Recent events:")
                for event in security_report.get("last_events", [])[:3]:
                    print(f"- {event['event']} ({event['timestamp'][11:16]})")
                
                # Visualization
                home_system.plot_energy_usage()
                home_system.plot_device_consumption()
                
            elif choice == "5":
                home_system.stop_simulation()
                home_system.save_current_state()
                print("Simulation stopped")
                break
                
    except KeyboardInterrupt:
        home_system.stop_simulation()
        home_system.save_current_state()
        print("\\nSimulation stopped")