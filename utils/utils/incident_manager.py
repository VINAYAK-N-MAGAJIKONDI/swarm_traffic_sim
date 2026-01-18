# utils/incident_manager.py

import traci
import random

class IncidentManager:
    def __init__(self, start_step=200, duration=100):
        """
        start_step: when accident starts
        duration: how long accident lasts
        """
        self.start_step = start_step
        self.duration = duration
        self.active = False
        self.vehicle_id = None

    def update(self, step):
        # Start incident
        if step == self.start_step and not self.active:
            self.trigger_incident()

        # End incident
        if self.active and step == self.start_step + self.duration:
            self.clear_incident()

    def trigger_incident(self):
        vehicles = traci.vehicle.getIDList()
        if not vehicles:
            return

        self.vehicle_id = random.choice(vehicles)
        traci.vehicle.setSpeed(self.vehicle_id, 0)

        self.active = True
        print(f"[INCIDENT] Vehicle {self.vehicle_id} stopped.")

    def clear_incident(self):
        if self.vehicle_id:
            traci.vehicle.setSpeed(self.vehicle_id, -1)

        print(f"[INCIDENT CLEARED] Vehicle {self.vehicle_id} released.")
        self.active = False
        self.vehicle_id = None
