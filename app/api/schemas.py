from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import enum

# --- Device Schemas ---
class BaseDeviceSchema(BaseModel):
    """
    Basic device schema.
    """
    device_name: str

# --- Edge Gateway Schemas ---

class CreateEdgeGateway(BaseDeviceSchema):
    """
    Schema for creating an edge gateway.
    """

    url: str
    device_address: str

class UpdateEdgeGateway(BaseDeviceSchema):
    """
    Schema for updating an edge gateway.
    """

    url: Optional[str] = None
    device_address:  Optional[str] = None

class ReadEdgeGateway(BaseDeviceSchema):
    """
    Schema for returning an edge gateway.
    """

    uuid: str
    device_address: str
    url: str
    registered_at: datetime

    class Config:
        from_attributes = True


# --- Sensor Config Schemas ---
class SensorConfig(BaseModel):
    """
    Schema for a sensor configuration.
    """

    sleep_interval_ms: int

    class Config:
        from_attributes = True

# --- Edge Sensor Schemas ---

class SensorState(str, enum.Enum):
    INITIAL = "initial"
    UNLOCKED = "unlocked"
    LOCKED = "locked"
    WORKING = "working"
    IDLE = "idle"
    ERROR = "error"

class CreateEdgeSensor(BaseDeviceSchema):
    """
    Schema for creating an edge sensor.
    """
    device_address: str

class UpdateEdgeSensor(BaseDeviceSchema):
    """
    Schema for updating an edge sensor.
    """

    state:  Optional[SensorState] = None

class ReadEdgeSensor(BaseDeviceSchema):
    """
    Schema for returning an edge sensor.
    """

    uuid: str
    device_address: str
    registered_at: datetime

    sensor_config : Optional[SensorConfig] = None

    class Config:
        from_attributes = True



# --- Inference Latency Benchmark Schemas ---
class InferenceLayer(int, enum.Enum):
    CLOUD = 2
    GATEWAY = 1
    SENSOR = 0
    
class InferenceLatencyBenchmark(BaseModel):
    """
    Schema for an inference latency benchmark.
    """
    sensor_name: str
    inference_layer: InferenceLayer
    send_timestamp: int
    recv_timestamp: int
    inference_latency: int
    
    class Config:
        from_attributes = True


# --- Inference Result Schemas ---


class CreatePredictionResult(BaseModel):
    """
    Schema for creating a prediction result.
    """

    prediction: int
    inference_layer: InferenceLayer

class ReadPredictionResult(BaseModel):
    """
    Schema for an prediction result.
    """

    prediction: int
    inference_layer: InferenceLayer
    inference_latency_benchmark: Optional[InferenceLatencyBenchmark] = None

    class Config:
        from_attributes = True


class BaseSensorReading(BaseModel):
    """
    Base schema for a sensor reading.
    """

    uuid: str
    values: str # JSON encoded list[list[float]]

class CreateSensorReading(BaseSensorReading):
    """
    Schema for creating a sensor reading.
    """
    pass

class ReadSensorReading(BaseSensorReading):
    """
    Schema for returning a sensor reading.
    """

    registered_at: datetime
    prediction_result: Optional[ReadPredictionResult] = None

    class Config:
        from_attributes = True

