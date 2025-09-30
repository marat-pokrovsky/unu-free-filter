from flask import Flask, render_template
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from smart_home import SmartHomeSystem

app = Flask(__name__)
smart_home = SmartHomeSystem()

@app.route('/')
def index():
    return render_template('index.html', rooms=smart_home.rooms)

@app.route('/devices')
def devices():
    return render_template('devices.html', devices=smart_home.devices)

@app.route('/automations')
def automations():
    return render_template('automations.html', automations=smart_home.automations)

@app.route('/security')
def security():
    return render_template('security.html', security_log=smart_home.security_log)

if __name__ == '__main__':
    app.run(debug=True)
