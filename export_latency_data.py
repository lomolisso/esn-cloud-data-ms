"""
This utility module exports all inference latency benchmark data to a CSV file
which follows the following format:

| gateway_name | sensor_name | inference_layer | inference_latency | registered_at |

"""

import csv
from app.db import SessionLocal
from app.db.crud import read_inference_latency_benchmarks
from app.db.models import InferenceLatencyBenchmark

def main():
    session = SessionLocal()

    with open(f"inference_latency_benchmarks.csv", mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["sensor_name", "inference_layer", "inference_latency", "registered_at"])

        benchs: list[InferenceLatencyBenchmark] = read_inference_latency_benchmarks(session=session)
        for bench in benchs:
            writer.writerow([bench.sensor_name, bench.inference_layer, bench.inference_latency, bench.registered_at])
    session.close()

if __name__ == "__main__":
    main()
