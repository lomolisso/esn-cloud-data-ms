"""
This utility module exports all inference latency benchmark data to a CSV file
which follows the following format:

| gateway_name | sensor_name | inference_layer | inference_latency | registered_at |

"""

import csv
from app.db import SessionLocal
from app.db.crud import read_edge_gateways, read_edge_sensors

def main():
    session = SessionLocal()
    edge_gateways = read_edge_gateways(session=session)

    with open(f"inference_latency_benchmarks.csv", mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["gateway_name", "sensor_name", "inference_layer", "inference_latency", "registered_at"])
    
        for gateway in edge_gateways:
            edge_sensors = read_edge_sensors(session=session, gateway_name=gateway.device_name)
            for sensor in edge_sensors:
                for reading in sensor.sensor_readings:
                    if reading.prediction_result:
                        if reading.prediction_result.inference_latency_benchmark:
                            writer.writerow([gateway.device_name, sensor.device_name, reading.prediction_result.inference_layer, reading.prediction_result.inference_latency_benchmark.inference_latency, reading.prediction_result.inference_latency_benchmark.registered_at])

    session.close()

if __name__ == "__main__":
    main()
