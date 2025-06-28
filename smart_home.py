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
        