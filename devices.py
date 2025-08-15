import random

class SmartDevice:
    """Base class for smart devices"""

    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type
        self.status = "off"

    def turn_on(self):
        self.status = "on"

    def turn_off(self):
        self.status = "off"

class Light(SmartDevice):
    """Represents a smart light"""

    def __init__(self, device_id):
        super().__init__(device_id, "light")
        self.brightness = 100

    def set_brightness(self, brightness):
        self.brightness = brightness

class Thermostat(SmartDevice):
    """Represents a smart thermostat"""

    def __init__(self, device_id):
        super().__init__(device_id, "thermostat")
        self.temperature = 20

    def set_temperature(self, temperature):
        self.temperature = temperature

class SecurityCamera(SmartDevice):
    """Represents a security camera"""

    def __init__(self, device_id):
        super().__init__(device_id, "security_camera")
        self.is_recording = False

    def start_recording(self):
        self.is_recording = True

    def stop_recording(self):
        self.is_recording = False
