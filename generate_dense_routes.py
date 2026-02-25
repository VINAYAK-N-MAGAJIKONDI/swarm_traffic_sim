import random

def generate_routefile(filename, vehicles=1500, duration=2000):
    edges = [
        "A0A1", "A0B0", "A1A0", "A1A2", "A1B1", "A2A1", "A2B2", "B0A0", "B1A1",
        "B0B1", "B0C0", "B1B0", "B1B2", "B1C1", "B2A2", "B2B1", "B2C2", "C0B0",
        "C0C1", "C1B1", "C1C0", "C1C2", "C2B2", "C2C1"
    ]
    
    # Predefined routes that cover the grid to ensure meaningful traffic
    routes_raw = [
        "A0A1 A1A2 A2B2 B2C2",
        "C2C1 C1C0 C0B0 B0A0",
        "A0B0 B0B1 B1B2 B2A2",
        "C2B2 B2B1 B1B0 B0C0",
        "A1B1 B1C1 C1C2",
        "C1B1 B1A1 A1A0",
        "B0B1 B1A1 A1A2",
        "B2B1 B1C1 C1C0"
    ]
    
    vehicles_list = []
    for i in range(vehicles):
        depart = random.uniform(0, duration)
        route = random.choice(routes_raw)
        vehicles_list.append((depart, i, route))
    
    # Sort by departure time (crucial for SUMO)
    vehicles_list.sort()
    
    with open(filename, "w") as routes:
        print('<?xml version="1.0" encoding="UTF-8"?>', file=routes)
        print('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">', file=routes)
        print('    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="70"/>', file=routes)
        
        for depart, i, route in vehicles_list:
            print(f'    <vehicle id="v_{i}" depart="{depart:.2f}" type="car"><route edges="{route}"/></vehicle>', file=routes)

            
        print('</routes>', file=routes)

if __name__ == "__main__":
    generate_routefile("c:/Users/vinay/OneDrive/Desktop/mini Project/swarm_traffic_sim/sumo_sim/quick.rou.xml")
