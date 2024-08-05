from app.db import models

from sqlalchemy.orm import Session
from sqlalchemy import select, update

# --- Exception classes ---
class EdgeGatewayNotFound(Exception):
    def __init__(self, message="Edge gateway not found."):
        self.message = message
        super().__init__(self.message)

class EdgeSensorNotFound(Exception):
    def __init__(self, message="Edge sensor not found."):
        self.message = message
        super().__init__(self.message)

class EdgeGatewayAlreadyExists(Exception):
    def __init__(self, message="Edge gateway already exists."):
        self.message = message
        super().__init__(self.message)

class EdgeSensorAlreadyExists(Exception):
    def __init__(self, message="Edge sensor already exists."):
        self.message = message
        super().__init__(self.message)

class SensorConfigAlreadyExists(Exception):
    def __init__(self, message="Sensor configuration already exists."):
        self.message = message
        super().__init__(self.message)

class SensorConfigNotFound(Exception):
    def __init__(self, message="Sensor configuration not found."):
        self.message = message
        super().__init__(self.message)

class SensorReadingNotFound(Exception):
    def __init__(self, message="Sensor reading not found."):
        self.message = message
        super().__init__(self.message)

class PredictionResultNotFound(Exception):
    def __init__(self, message="Prediction result not found."):
        self.message = message
        super().__init__(self.message)

class PredictionResultAlreadyExists(Exception):
    def __init__(self, message="Prediction result already exists."):
        self.message = message
        super().__init__(self.message)

class InferenceLatencyBenchmarkAlreadyExists(Exception):
    def __init__(self, message="Inference latency benchmark already exists."):
        self.message = message
        super().__init__(self.message)

# --- CRUD methods for EdgeGateway ---

def read_edge_gateways(session: Session, paginate=False, page=0, page_size=10) -> list[models.EdgeGateway]:
    query = select(models.EdgeGateway)
    if paginate:
        query = query.offset(page).limit(page_size)
    result = session.execute(query)
    return result.scalars().all()

def read_edge_gateway(session: Session, device_name) -> models.EdgeGateway:
    query = select(models.EdgeGateway).where(
        models.EdgeGateway.device_name == device_name
    )
    result = session.execute(query).scalars().first()
    
    # Check if the edge gateway exists
    if not result:
        raise EdgeGatewayNotFound

    return result

def create_edge_gateway(session: Session, fields: dict):
    device_name = fields["device_name"]
    
    # Check if the edge gateway already exists
    query = select(models.EdgeGateway).where(
        models.EdgeGateway.device_name == device_name
    )
    result = session.execute(query).scalars().first()
    if result:
        raise EdgeGatewayAlreadyExists
    
    db_instance = models.EdgeGateway(**fields)
    session.add(db_instance)
    session.commit()
    session.refresh(db_instance)

def update_edge_gateway(session: Session, device_name: str, fields: dict):
    # Check if the device_name is the same
    assert fields["device_name"] == device_name

    # Check if the edge gateway exists
    read_edge_gateway(session=session, device_name=device_name)

    query = update(models.EdgeGateway).where(
        models.EdgeGateway.device_name == device_name
    ).values(fields)
    session.execute(query)
    session.commit()

def delete_edge_gateway(session: Session, device_name: str):
    # Check if the edge gateway exists and get the gateway
    gateway = read_edge_gateway(session=session, device_name=device_name)
    session.delete(gateway)
    session.commit()

# --- CRUD methods for EdgeSensor ---

def read_edge_sensors(session: Session, gateway_name: str, paginate=False, page=0, page_size=10) -> list[models.EdgeSensor]:
    # Check if the edge gateway exists and get the gateway
    gateway = read_edge_gateway(session=session, device_name=gateway_name)

    query = select(models.EdgeSensor).where(
        models.EdgeSensor.gateway_uuid == gateway.uuid
    )
    if paginate:
        query = query.offset(page).limit(page_size)
    result = session.execute(query)

    return result.scalars().all()

def read_edge_sensor(session: Session, gateway_name: str, device_name: str) -> models.EdgeSensor:
    # Check if the edge gateway exists and get the gateway
    gateway = read_edge_gateway(session=session, device_name=gateway_name)

    query = select(models.EdgeSensor).where(
        models.EdgeSensor.gateway_uuid == gateway.uuid,
        models.EdgeSensor.device_name == device_name
    )
    result = session.execute(query).scalars().first()

    # Check if the edge sensor exists
    if not result:
        raise EdgeSensorNotFound
    
    return result

def create_edge_sensor(session: Session, gateway_name: str, fields: dict):
    # Check if the edge gateway exists and get the gateway
    gateway = read_edge_gateway(session=session, device_name=gateway_name)

    device_name = fields["device_name"]
    query = select(models.EdgeSensor).where(
        models.EdgeSensor.gateway_uuid == gateway.uuid,
        models.EdgeSensor.device_name == device_name
    )
    result = session.execute(query).scalars().first()
    if result:
        raise EdgeSensorAlreadyExists
    
    db_instance = models.EdgeSensor(gateway_uuid=gateway.uuid, **fields)
    session.add(db_instance)
    session.commit()
    session.refresh(db_instance)
    
def update_edge_sensor(session: Session, gateway_name: str, device_name: str, fields: dict):
    # Check if the device_name is the same
    assert fields["device_name"] == device_name

    # Check if the edge gateway exists and get the gateway
    gateway = read_edge_gateway(session=session, device_name=gateway_name)

    # Check if the edge sensor exists
    read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    query = update(models.EdgeSensor).where(
        models.EdgeSensor.gateway_uuid == gateway.uuid,
        models.EdgeSensor.device_name == device_name
    ).values(fields)
    session.execute(query)
    session.commit()


def delete_edge_sensor(session: Session, gateway_name: str, device_name: str):
    # Check if the edge gateway exists
    read_edge_gateway(session=session, device_name=gateway_name)
    
    # Check if the edge sensor exists
    sensor = read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    session.delete(sensor)
    session.commit()

# --- CRUD methods for SensorConfig ---
def create_sensor_config(session: Session, gateway_name: str, device_name: str, fields: dict):
    # Check if the edge sensor exists
    sensor = read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    # Check if the sensor config already exists
    if sensor.sensor_config:
        raise SensorConfigAlreadyExists

    db_instance = models.SensorConfig(edge_sensor_uuid=sensor.uuid, **fields)
    session.add(db_instance)
    session.commit()

def read_sensor_config(session: Session, gateway_name: str, device_name: str) -> models.SensorConfig:
    # Check if the edge sensor exists
    sensor = read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    # Check if the sensor config exists
    if not sensor.sensor_config:
        raise SensorConfigNotFound

    return sensor.sensor_config

def update_sensor_config(session: Session, gateway_name: str, device_name: str, fields: dict):
    # Check if the edge sensor exists
    sensor = read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    # Check if the sensor config exists
    if not sensor.sensor_config:
        raise SensorConfigNotFound

    query = update(models.SensorConfig).where(
        models.SensorConfig.edge_sensor_uuid == sensor.uuid
    ).values(fields)
    session.execute(query)
    session.commit()

def delete_sensor_config(session: Session, gateway_name: str, device_name: str):
    # Check if the edge sensor exists
    sensor = read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    # Check if the sensor config exists
    if not sensor.sensor_config:
        raise SensorConfigNotFound

    session.delete(sensor.sensor_config)
    session.commit()



# --- CRUD methods for SensorReading ---
def read_sensor_reading(session: Session, gateway_name: str, device_name: str, reading_uuid: str) -> models.SensorReading:
    # Check if the edge gateway exists
    read_edge_gateway(session=session, device_name=gateway_name)

    # Check if the edge sensor exists 
    read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    query = select(models.SensorReading).where(
        models.SensorReading.uuid == reading_uuid
    )
    result = session.execute(query).scalars().first()
    if not result:
        raise SensorReadingNotFound
    return result


def read_sensor_readings(session: Session, gateway_name: str, device_name: str, paginate=False, page=0, page_size=10) -> list[models.SensorReading]:
    # Check if the edge gateway exists
    read_edge_gateway(session=session, device_name=gateway_name)
    
    # Check if the edge sensor exists and get the sensor
    sensor = read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)
    query = select(models.SensorReading).where(
        models.SensorReading.sensor_uuid == sensor.uuid
    )
    if paginate:
        query = query.offset(page).limit(page_size)
    result = session.execute(query)
    return result.scalars().all()

def create_sensor_reading(session: Session, gateway_name: str, device_name: str, fields: dict):
    # Check if the edge gateway exists
    read_edge_gateway(session=session, device_name=gateway_name)

    # Check if the edge sensor exists and get the sensor
    sensor = read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    db_instance = models.SensorReading(sensor_uuid=sensor.uuid, **fields)
    session.add(db_instance)
    session.commit()
    session.refresh(db_instance)
    
def delete_sensor_readings(session: Session, gateway_name: str, device_name: str):
    # check if the edge gateway exists
    read_edge_gateway(session=session, device_name=gateway_name)

    # Check if the edge sensor exists
    read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)
    
    readings = read_sensor_readings(session=session, gateway_name=gateway_name, device_name=device_name)
    for reading in readings:
        session.delete(reading)
    session.commit()

# --- CRUD methods for PredictionResult ---

def create_prediction_result(session: Session, gateway_name: str, device_name: str, reading_uuid: str, fields: dict):
    # Check if the edge gateway exists
    read_edge_gateway(session=session, device_name=gateway_name)

    # Check if the edge sensor exists
    read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    # Check if the sensor reading exists and get the reading
    reading = read_sensor_reading(session=session, gateway_name=gateway_name, device_name=device_name, reading_uuid=reading_uuid)

    # Check if the prediction result already exists
    if reading.prediction_result:
        raise PredictionResultAlreadyExists

    db_instance = models.PredictionResult(sensor_reading_uuid=reading_uuid, **fields)
    session.add(db_instance)
    session.commit()

def delete_prediction_results(session: Session, gateway_name: str, device_name: str):
    # Check if the edge gateway exists
    read_edge_gateway(session=session, device_name=gateway_name)

    # Check if the edge sensor exists
    read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    readings = read_sensor_readings(session=session, gateway_name=gateway_name, device_name=device_name)
    for reading in readings:
        if reading.prediction_result:
            session.delete(reading.prediction_result)
    session.commit()

# --- CRUD methods for InferenceLatencyBenchmark ---
def create_inference_latency_benchmark(session: Session, gateway_name: str, device_name: str, reading_uuid: str, fields: dict):
    # Check if the edge gateway exists
    read_edge_gateway(session=session, device_name=gateway_name)

    # Check if the edge sensor exists
    read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    # Check if the sensor reading exists
    reading = read_sensor_reading(session=session, gateway_name=gateway_name, device_name=device_name, reading_uuid=reading_uuid)

    # Check if the prediction result exists
    if not reading.prediction_result:
        raise PredictionResultNotFound
    
    # Check if the inference latency benchmark already exists
    if reading.prediction_result.inference_latency_benchmark:
        raise InferenceLatencyBenchmarkAlreadyExists
    
    db_instance = models.InferenceLatencyBenchmark(prediction_result_uuid=reading.prediction_result.uuid, **fields)
    session.add(db_instance)
    session.commit()


def delete_inference_latency_benchmarks(session: Session, gateway_name: str, device_name: str):
    # Check if the edge gateway exists
    read_edge_gateway(session=session, device_name=gateway_name)

    # Check if the edge sensor exists
    read_edge_sensor(session=session, gateway_name=gateway_name, device_name=device_name)

    readings = read_sensor_readings(session=session, gateway_name=gateway_name, device_name=device_name)
    for reading in readings:
        if reading.prediction_result and reading.prediction_result.inference_latency_benchmark:
            session.delete(reading.prediction_result.inference_latency_benchmark)
    session.commit()
