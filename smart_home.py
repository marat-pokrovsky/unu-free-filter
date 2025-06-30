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