import time
import random
from datetime import datetime, timedelta

from config import save_config
from devices import (
    add_room, add_device, update_device_status, get_room_devices
)
from automations import add_automation, check_automations
from security import get_security_report, simulate_security_breach
from energy import (
    log_energy_consumption, get_energy_report, 
    plot_energy_usage, plot_device_consumption
)

# Initial data
rooms = []
devices = []
automations = []

def initialize_data():
    """Initialize the smart home with some rooms and devices"""
    # Rooms
    living_room = add_room(rooms, "Living Room", "living")
    bedroom = add_room(rooms, "Bedroom", "bedroom")
    kitchen = add_room(rooms, "Kitchen", "kitchen")

    # Devices
    add_device(devices, rooms, "Living Room Light", "light", living_room["id"])
    add_device(devices, rooms, "Bedroom Thermostat", "thermostat", bedroom["id"], value=22)
    add_device(devices, rooms, "Kitchen Camera", "camera", kitchen["id"])
    add_device(devices, rooms, "Main Door Lock", "lock", living_room["id"])
    add_device(devices, rooms, "Bedroom Motion Sensor", "sensor", bedroom['id'], subtype="motion")
    add_device(devices, rooms, "Kitchen Appliance", "appliance", kitchen["id"], power=1500)

    # Automations
    add_automation(
        automations,
        "Turn on living room light at 6 PM",
        trigger={"type": "time", "value": "18:00"},
        condition=None,
        actions=[{"device_id": 1, "command": "on"}]
    )
    add_automation(
        automations,
        "Turn off all lights at midnight",
        trigger={"type": "time", "value": "00:00"},
        condition=None,
        actions=[{"device_id": 1, "command": "off"}]
    )

def run_simulation(duration_days=7):
    """Run the smart home simulation"""
    print("Starting smart home simulation...")
    initialize_data()
    
    start_time = datetime.now()
    end_time = start_time + timedelta(days=duration_days)
    
    last_report_time = start_time
    
    while datetime.now() < end_time:
        # Log energy consumption every minute
        log_energy_consumption(devices)
        
        # Check automations
        check_automations(devices, automations)
        
        # Simulate random events
        if random.random() < 0.001:  # small chance of security breach
            simulate_security_breach(devices)
        
        # Print hourly report
        if (datetime.now() - last_report_time).seconds >= 3600:
            print_summary_report()
            last_report_time = datetime.now()
        
        time.sleep(60)  # Each minute in real time is a minute in simulation
        
    print("Simulation finished.")
    # Final reports and plots
    print_summary_report()
    plot_energy_usage(hours=duration_days*24)
    plot_device_consumption(devices)

def print_summary_report():
    """Print a summary report of the smart home status"""
    print(f"\n----- Report at {datetime.now().strftime('%Y-%m-%d %H:%M')}-----")
    
    # Energy report
    energy_report = get_energy_report(devices)
    if energy_report:
        print(f"  Total energy consumed in last 24h: {energy_report['total_energy']:.2f} kWh")
        print(f"  Total energy cost in last 24h: ${energy_report['total_cost']:.2f}")
    
    # Security report
    security_report = get_security_report()
    print(f"  Security events in last 24h: {security_report['total_events']}")
    print(f"  Critical security events in last 24h: {security_report['critical_events']}")
    
    # Device status
    print("  Device Status:")
    for device in devices:
        status_str = f"{device['name']}: {device['status']}"
        if device["type"] == "thermostat":
            status_str += f" ({device['value']}°C)"
        print(f"    - {status_str}")

if __name__ == "__main__":
    run_simulation(duration_days=1)  # Run for 1 day by default
