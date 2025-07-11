import json
import os
import random
import time
from datetime import datetime, timedelta
import threading
import matplotlib.pyplot as plt
import numpy as np
import pytz
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class SmartHomeSystem:
    def __init__(self, config_file="smart_home_config.json"):
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
        """Загрузка конфигурации из файла"""
        if os.path.exists(self.config_file):
            with open(self.config_file) as f:
                config = json.load(f)
                self.devices = config.get("devices", [])
                self.rooms = config.get("rooms", [])
                self.automations = config.get("automations", [])
        
    def save_config(self):
        """Сохранение конфигурации в файл"""
        config = {
            "devices": self.devices,
            "rooms": self.rooms,
            "automations": self.automations
        }
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=2)

    def add_room(self, name, room_type):
        """Добавление комнаты"""
        room = {
            "id": len(self.rooms) + 1,
            "name": name,
            "type": room_type,  # living, bedroom, kitchen, bathroom, outdoor
            "devices": []
        }
        self.rooms.append(room)
        self.save_config()
        return room

    def add_device(self, name, device_type, room_id, status="off", power=0):
        """Добавление устройства"""
        device = {
            "id": len(self.devices) + 1,
            "name": name,
            "type": device_type,  # light, thermostat, camera, lock, sensor, appliance
            "status": status,
            "power": power,  # Вт
            "room_id": room_id,
            "last_update": datetime.now().isoformat()
        }
        self.devices.append(device)
        
        # Добавляем устройство в комнату
        for room in self.rooms:
            if room["id"] == room_id:
                room["devices"].append(device["id"])
                break
        
        self.save_config()
        return device

    def update_device_status(self, device_id, status, value=None):
        """Обновление статуса устройства"""
        for device in self.devices:
            if device["id"] == device_id:
                device["status"] = status
                device["last_update"] = datetime.now().isoformat()
                
                # Для термостатов обновляем значение температуры
                if device["type"] == "thermostat" and value is not None:
                    device["value"] = value
                
                # Логируем изменения
                self.log_security_event(f"Устройство {device['name']} изменено: {status}")
                return device
        return None

    def get_room_devices(self, room_id):
        """Получение устройств в комнате"""
        return [device for device in self.devices if device["room_id"] == room_id]

    def add_automation(self, name, trigger, condition, actions):
        """Добавление автоматизации"""
        automation = {
            "id": len(self.automations) + 1,
            "name": name,
            "trigger": trigger,  # {"type": "time", "value": "18:00"} или {"type": "sensor", "sensor_id": 123, "condition": ">", "value": 30}
            "condition": condition,  # {"type": "presence", "room_id": 1} или None
            "actions": actions  # [{"device_id": 1, "command": "on"}, ...]
        }
        self.automations.append(automation)
        self.save_config()
        return automation

    def check_automations(self):
        """Проверка и выполнение автоматизаций"""
        now = datetime.now()
        for automation in self.automations:
            trigger = automation["trigger"]
            executed = False
            
            # Триггер по времени
            if trigger["type"] == "time":
                trigger_time = datetime.strptime(trigger["value"], "%H:%M").time()
                if now.time() >= trigger_time and (now - datetime.strptime(automation.get("last_executed", "2000-01-01T00:00:00"), "%Y-%m-%dT%H:%M:%S")).days >= 1:
                    executed = self.execute_automation(automation)
            
            # Триггер по датчику
            elif trigger["type"] == "sensor":
                sensor = next((d for d in self.devices if d["id"] == trigger["sensor_id"]), None)
                if sensor and self.check_sensor_condition(sensor, trigger["condition"], trigger["value"]):
                    executed = self.execute_automation(automation)
            
            if executed:
                automation["last_executed"] = now.isoformat()

    def check_sensor_condition(self, sensor, condition, value):
        """Проверка условия сенсора"""
        sensor_value = sensor.get("value", 0)
        try:
            value = float(value)
            if condition == ">": return sensor_value > value
            if condition == "<": return sensor_value < value
            if condition == "==": return sensor_value == value
            if condition == ">=": return sensor_value >= value
            if condition == "<=": return sensor_value <= value
        except:
            return False
        return False

    def execute_automation(self, automation):
        """Выполнение действий автоматизации"""
        # Проверка условий
        if automation["condition"]:
            cond = automation["condition"]
            if cond["type"] == "presence":
                # Проверка присутствия в комнате (упрощенная)
                room_devices = self.get_room_devices(cond["room_id"])
                motion_sensors = [d for d in room_devices if d["type"] == "sensor" and d.get("subtype") == "motion"]
                if not any(s["status"] == "active" for s in motion_sensors):
                    return False
        
        # Выполнение действий
        for action in automation["actions"]:
            self.update_device_status(action["device_id"], action["command"])
        
        self.log_security_event(f"Автоматизация выполнена: {automation['name']}")
        return True

    def log_energy_consumption(self):
        """Логирование энергопотребления"""
        total_power = 0
        for device in self.devices:
            if device["status"] == "on":
                # Для термостатов учитываем только когда они активно работают
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
        """Расчет стоимости энергии"""
        # Простая модель: стоимость за кВт*ч
        kwh = power / 1000 * (1 / 60)  # потребление за минуту
        return kwh * 5.0  # 5 руб/кВт*ч

    def log_security_event(self, event):
        """Логирование события безопасности"""
        self.security_log.append({
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "severity": "info"
        })