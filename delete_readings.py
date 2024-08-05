"""
This utility module cleans all reading-related entries on the following tables:
- inference_latency_benchmark_table
- prediction_result_table
- sensor_reading_table
in this order, as the tables are related by foreign keys.
"""
from app.db import SessionLocal
from app.db.crud import read_edge_gateways, read_edge_sensors, delete_inference_latency_benchmarks, delete_prediction_results, delete_sensor_readings

def main():
    session = SessionLocal()

    edge_gateways = read_edge_gateways(session=session)

    for edge_gateway in edge_gateways:
        edge_sensors = read_edge_sensors(session=session, gateway_name=edge_gateway.device_name)
        for edge_sensor in edge_sensors:
            delete_inference_latency_benchmarks(session=session, gateway_name=edge_gateway.device_name, device_name=edge_sensor.device_name)
            delete_prediction_results(session=session, gateway_name=edge_gateway.device_name, device_name=edge_sensor.device_name)
            delete_sensor_readings(session=session, gateway_name=edge_gateway.device_name, device_name=edge_sensor.device_name)

    session.close()
    
if __name__ == "__main__":
    main()