from datetime import datetime
from devices import update_device_status, get_room_devices
from security import log_security_event

def add_automation(automations, name, trigger, condition, actions):
    """Add automation rule"""
    automation = {
        "id": len(automations) + 1,
        "name": name,
        "trigger": trigger,  # {"type": "time", "value": "18:00"} or {"type": "sensor", "sensor_id": 123, "condition": ">", "value": 30}
        "condition": condition,  # {"type": "presence", "room_id": 1} or None
        "actions": actions  # [{"device_id": 1, "command": "on"}, ...]
    }
    automations.append(automation)
    return automation

def check_automations(devices, automations):
    """Check and execute automations"""
    now = datetime.now()
    for automation in automations:
        trigger = automation["trigger"]
        executed = False
        
        # Time trigger
        if trigger["type"] == "time":
            try:
                trigger_time = datetime.strptime(trigger["value"], "%H:%M").time()
                last_executed_str = automation.get("last_executed", "2000-01-01T00:00:00")
                last_executed = datetime.strptime(last_executed_str.split(".")[0], "%Y-%m-%dT%H:%M:%S")
                if now.time() >= trigger_time and (now - last_executed).days >= 1:
                    executed = execute_automation(devices, automation)
            except ValueError as e:
                print(f"Error parsing time for automation {automation['name']}: {e}")
        
        # Sensor trigger
        elif trigger["type"] == "sensor":
            sensor = next((d for d in devices if d["id"] == trigger["sensor_id"]), None)
            if sensor and check_sensor_condition(sensor, trigger["condition"], trigger["value"]):
                executed = execute_automation(devices, automation)
        
        if executed:
            automation["last_executed"] = now.isoformat()

def check_sensor_condition(sensor, condition, value):
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

def execute_automation(devices, automation):
    """Execute automation actions"""
    # Check conditions
    if automation["condition"]:
        cond = automation["condition"]
        if cond["type"] == "presence":
            # Check presence in room (simplified)
            room_devices = get_room_devices(devices, cond["room_id"])
            motion_sensors = [d for d in room_devices if d["type"] == "sensor" and d.get("subtype") == "motion"]
            if not any(s["status"] == "active" for s in motion_sensors):
                return False
    
    # Execute actions
    for action in automation["actions"]:
        update_device_status(devices, action["device_id"], action["command"])
    
    log_security_event(f"Automation executed: {automation['name']}")
    return True
