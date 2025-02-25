#!/usr/bin/env python3
"""
IoT Sensor Data Simulator

This script generates simulated sensor data for temperature, humidity, and motion sensors
and publishes it to an MQTT broker.
"""

import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import argparse

# Default configuration
DEFAULT_MQTT_HOST = "localhost"
DEFAULT_MQTT_PORT = 1883
DEFAULT_NUM_SENSORS = 5
DEFAULT_INTERVAL = 1.0  # seconds

# Sensor types and their characteristics
SENSOR_TYPES = {
    "temperature": {
        "unit": "°C",
        "min": 15.0,
        "max": 35.0,
        "precision": 1,
        "drift_max": 0.5,
    },
    "humidity": {
        "unit": "%",
        "min": 30.0,
        "max": 80.0,
        "precision": 1,
        "drift_max": 2.0,
    },
    "motion": {
        "unit": "boolean",
        "min": 0,
        "max": 1,
        "precision": 0,
        "drift_max": 0,
    }
}

class SensorSimulator:
    def __init__(self, mqtt_host, mqtt_port, num_sensors, interval):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.num_sensors = num_sensors
        self.interval = interval
        self.client = mqtt.Client()
        self.sensors = self._initialize_sensors()
        
    def _initialize_sensors(self):
        """Initialize sensor configurations"""
        sensors = []
        for i in range(self.num_sensors):
            sensor_type = random.choice(list(SENSOR_TYPES.keys()))
            sensor_config = SENSOR_TYPES[sensor_type].copy()
            
            # Generate a random initial value within the range
            initial_value = random.uniform(sensor_config["min"], sensor_config["max"])
            if sensor_type == "motion":
                initial_value = random.choice([0, 1])
            
            sensors.append({
                "id": f"{sensor_type}_{i+1}",
                "type": sensor_type,
                "location": f"room_{(i % 5) + 1}",
                "current_value": initial_value,
                "config": sensor_config
            })
        return sensors
    
    def connect(self):
        """Connect to the MQTT broker"""
        try:
            self.client.connect(self.mqtt_host, self.mqtt_port, 60)
            print(f"Connected to MQTT broker at {self.mqtt_host}:{self.mqtt_port}")
            return True
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
            return False
    
    def update_sensor_values(self):
        """Update sensor values with realistic changes"""
        for sensor in self.sensors:
            config = sensor["config"]
            current = sensor["current_value"]
            
            if sensor["type"] == "motion":
                # Motion sensors have a 10% chance of changing state
                if random.random() < 0.1:
                    sensor["current_value"] = 1 if current == 0 else 0
            else:
                # Add random drift within the drift_max range
                drift = random.uniform(-config["drift_max"], config["drift_max"])
                new_value = current + drift
                
                # Ensure the value stays within the defined range
                new_value = max(config["min"], min(config["max"], new_value))
                
                # Round to the specified precision
                sensor["current_value"] = round(new_value, config["precision"])
    
    def publish_sensor_data(self):
        """Publish sensor data to MQTT topics"""
        timestamp = datetime.now().isoformat()
        
        for sensor in self.sensors:
            topic = f"sensors/{sensor['type']}/{sensor['id']}"
            
            payload = {
                "sensor_id": sensor["id"],
                "type": sensor["type"],
                "location": sensor["location"],
                "value": sensor["current_value"],
                "unit": sensor["config"]["unit"],
                "timestamp": timestamp
            }
            
            self.client.publish(topic, json.dumps(payload))
            print(f"Published to {topic}: {payload}")
    
    def run(self):
        """Run the simulator"""
        if not self.connect():
            return
        
        try:
            while True:
                self.update_sensor_values()
                self.publish_sensor_data()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Simulator stopped by user")
        finally:
            self.client.disconnect()
            print("Disconnected from MQTT broker")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IoT Sensor Data Simulator")
    parser.add_argument("--host", default=DEFAULT_MQTT_HOST, help="MQTT broker host")
    parser.add_argument("--port", type=int, default=DEFAULT_MQTT_PORT, help="MQTT broker port")
    parser.add_argument("--sensors", type=int, default=DEFAULT_NUM_SENSORS, help="Number of sensors to simulate")
    parser.add_argument("--interval", type=float, default=DEFAULT_INTERVAL, help="Interval between readings in seconds")
    
    args = parser.parse_args()
    
    simulator = SensorSimulator(
        mqtt_host=args.host,
        mqtt_port=args.port,
        num_sensors=args.sensors,
        interval=args.interval
    )
    
    simulator.run() 