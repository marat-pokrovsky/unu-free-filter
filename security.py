from datetime import datetime, timedelta
import random
from devices import update_device_status

security_log = []

def log_security_event(event, severity="info"):
    """Log security event"""
    security_log.append({
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "severity": severity
    })

def get_security_report():
    """Security report"""
    now = datetime.now()
    start_time = now - timedelta(hours=24)
    
    period_events = [e for e in security_log 
                    if datetime.fromisoformat(e["timestamp"]) >= start_time]
    
    critical_events = [e for e in period_events if e.get("severity") == "critical"]
    
    return {
        "total_events": len(period_events),
        "critical_events": len(critical_events),
        "last_events": period_events[-5:] if period_events else []
    }

def simulate_security_breach(devices):
    """Simulate security breach"""
    # Select a random door or window
    access_devices = [d for d in devices if d["type"] == "lock" and "door" in d["name"].lower()]
    if not access_devices:
        return
    
    device = random.choice(access_devices)
    log_security_event(f"Unauthorized access attempt: {device['name']}", severity="critical")
    
    # Activate alarm
    alarm = next((d for d in devices if "alarm" in d["name"].lower()), None)
    if alarm:
        update_device_status(devices, alarm["id"], "on")
