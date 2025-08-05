
import json
import os
from datetime import datetime

def load_config(config_file="smart_home_config.json"):
    """Load configuration from file"""
    if os.path.exists(config_file):
        try:
            with open(config_file) as f:
                config = json.load(f)
                return config.get("devices", []), config.get("rooms", []), config.get("automations", [])
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
    return [], [], []

def save_config(devices, rooms, automations, config_file="smart_home_config.json"):
    """Save configuration to file"""
    try:
        config = {
            "devices": devices,
            "rooms": rooms,
            "automations": automations
        }
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"Error saving config: {e}")

def save_current_state(devices, energy_data, security_log):
    """Save current system state"""
    state = {
        "devices": devices,
        "energy_data": energy_data,
        "security_log": security_log,
        "timestamp": datetime.now().isoformat()
    }
    try:
        with open("smart_home_state.json", "w") as f:
            json.dump(state, f, indent=2)
    except IOError as e:
        print(f"Error saving state: {e}")
