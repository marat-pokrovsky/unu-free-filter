from datetime import datetime
from config import save_config

def add_room(rooms, name, room_type):
    """Add a room to the system"""
    room = {
        "id": len(rooms) + 1,
        "name": name,
        "type": room_type,  # living, bedroom, kitchen, bathroom, outdoor
        "devices": []
    }
    rooms.append(room)
    return room

def add_device(devices, rooms, name, device_type, room_id, status="off", power=0, **kwargs):
    """Add a device to the system"""
    device = {
        "id": len(devices) + 1,
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
    
    devices.append(device)
    
    # Add device to room
    for room in rooms:
        if room["id"] == room_id:
            room["devices"].append(device["id"])
            break
    
    return device

def update_device_status(devices, device_id, status, value=None):
    """Update device status"""
    for device in devices:
        if device["id"] == device_id:
            device["status"] = status
            device["last_update"] = datetime.now().isoformat()
            
            # For thermostats, update temperature value
            if device["type"] == "thermostat" and value is not None:
                device["value"] = value
            
            return device
    return None

def get_room_devices(devices, room_id):
    """Get devices in a room"""
    return [device for device in devices if device["room_id"] == room_id]
