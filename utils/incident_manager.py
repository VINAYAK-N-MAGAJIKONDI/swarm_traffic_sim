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
        try:
            traci.vehicle.setSpeed(self.vehicle_id, 0)
            self.active = True
            print(f"[INCIDENT] Vehicle {self.vehicle_id} stopped.")
        except traci.exceptions.TraCIException as e:
            print(f"[INCIDENT ERROR] Could not stop vehicle {self.vehicle_id}: {e}")
            self.vehicle_id = None
            self.active = False

    def clear_incident(self):
        if self.vehicle_id:
            try:
                # Check if vehicle still exists in simulation
                if self.vehicle_id in traci.vehicle.getIDList():
                    traci.vehicle.setSpeed(self.vehicle_id, -1) # Release to follow max speed
                    print(f"[INCIDENT CLEARED] Vehicle {self.vehicle_id} released.")
                else:
                    print(f"[INCIDENT WARNING] Vehicle {self.vehicle_id} left simulation before clearance.")
            except traci.exceptions.TraCIException as e:
                print(f"[INCIDENT ERROR] Could not release vehicle {self.vehicle_id}: {e}")

        self.active = False
        self.vehicle_id = None
