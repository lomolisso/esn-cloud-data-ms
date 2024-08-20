import uuid
import enum
import pytz
from app.db import Base


from sqlalchemy import Boolean, ForeignKey, Column, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, DateTime, Text, Float, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime
from app.core.config import TIMEZONE


def tz_now():
    tz = pytz.timezone(TIMEZONE)
    return datetime.now(tz)

class SensorState(str, enum.Enum):
    INITIAL = "initial"
    UNLOCKED = "unlocked"
    LOCKED = "locked"
    WORKING = "working"
    IDLE = "idle"
    ERROR = "error"

class InferenceLayer(int, enum.Enum):
    CLOUD = 2
    GATEWAY = 1
    SENSOR = 0

    
class EdgeGateway(Base):
    """
    Edge gateway table

    Attributes:
    uuid: UUID, primary key
    jwt_token: String, JSON Web Token for the edge gateway
    device_name: String, name of the edge gateway
    device_address: String, address of the edge gateway
    url: Text, URL of the edge gateway
    registered_at: DateTime, timestamp when the edge gateway was registered in the database.
    edge_sensors: relationship to the EdgeSensor
    """

    __tablename__ = "edge_gateway_table"

    uuid = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    jwt_token = Column(String(1000), unique=True, nullable=True)
    device_name = Column(String(50), unique=True)
    device_address = Column(String(17), unique=True)
    url = Column(Text, nullable=False, unique=True)
    registered_at = Column(DateTime, default=tz_now)    
    
    edge_sensors = relationship("EdgeSensor", backref="edge_gateway")


class EdgeSensor(Base):
    """
    Edge sensor table

    Attributes:
    uuid: UUID, primary key
    device_name: String, name of the edge sensor
    device_address: String, address of the edge sensor
    working_state: Boolean, working state of the edge sensor
    registered_at: DateTime, timestamp when the edge sensor was registered in the database.
    gateway_uuid: UUID, foreign key to the edge_gateway_table.
    sensor_readings: relationship to the SensorReading
    """

    __tablename__ = "edge_sensor_table"

    uuid = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    device_name = Column(String(50), nullable=False, unique=True)
    device_address = Column(String(50), nullable=False, unique=True)
    state = Column(Enum(SensorState), nullable=False, default=SensorState.INITIAL)
    registered_at = Column(DateTime, default=tz_now)

    gateway_uuid = Column(UUID(as_uuid=False), ForeignKey("edge_gateway_table.uuid"))
    sensor_readings = relationship("SensorReading", backref="edge_sensor")
    sensor_config = relationship("SensorConfig", uselist=False, backref="edge_sensor")
    sensor_config = relationship(
        "SensorConfig",
        uselist=False,
        back_populates="edge_sensor"
    )

class SensorConfig(Base):
    """
    Sensor configuration table

    Attributes:
    uuid: UUID, primary key
    sleep_interval_ms: Integer, sleep interval of the sensor
    edge_sensor_uuid: UUID, foreign key to the edge_sensor_table.
    """

    __tablename__ = "sensor_config_table"

    uuid = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    sleep_interval_ms = Column(Integer, nullable=False)
    registered_at = Column(DateTime, default=tz_now) 

    edge_sensor_uuid = Column(UUID(as_uuid=False), ForeignKey("edge_sensor_table.uuid"), unique=True)
    edge_sensor = relationship("EdgeSensor", back_populates="sensor_config")




class SensorReading(Base):
    """
    Sensor reading table

    Attributes:
    uuid: UUID, primary key
    values: Text, sensor reading values
    registered_at: DateTime, timestamp when the sensor reading was stored in the database.
    sensor_uuid: UUID, foreign key to the edge_sensor_table.
    prediction_result: relationship to the PredictionResult
    """

    __tablename__ = "sensor_reading_table"

    uuid = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    values = Column(Text, nullable=False)
    registered_at = Column(DateTime, default=tz_now)

    sensor_uuid = Column(UUID(as_uuid=False), ForeignKey("edge_sensor_table.uuid"))
    prediction_result = relationship("PredictionResult", uselist=False, back_populates="sensor_reading")


class PredictionResult(Base):
    """
    Prediction result table
    
    Attributes:
    uuid: UUID, primary key
    prediction: Integer, prediction result
    inference_layer: Enum(InferenceLayer), prediction layer of the prediction result: "sensor", "edge" or "cloud"
    sensor_reading_uuid: UUID, foreign key to the sensor_reading_table.
    sensor_reading: relationship to the SensorReading table.
    """

    __tablename__ = "prediction_result_table"

    uuid = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    prediction = Column(Integer, nullable=False)
    inference_layer = Column(Enum(InferenceLayer), nullable=False)
    registered_at = Column(DateTime, default=tz_now) 

    sensor_reading_uuid = Column(UUID(as_uuid=False), ForeignKey("sensor_reading_table.uuid"))
    sensor_reading = relationship("SensorReading", back_populates="prediction_result")

class InferenceLatencyBenchmark(Base):
    """
    Inference latency benchmark table

    Attributes:
    uuid: UUID, primary key
    send_timestamp: Optional[int] = Noneeger, timestamp when the inference request was sent by the sensor, taken from the on-board timer.
    recv_timestamp: Integer, timestamp when the prediction result was received by the sensor, taken from the on-board timer.
    inference_latency: Integer, latency of the prediction result, calculated as the difference between the recv_timestamp and the send_timestamp.
    prediction_result_uuid: UUID, foreign key to the prediction_result_table.
    prediction_result: relationship to the PredictionResult table.
    """

    __tablename__ = "inference_latency_benchmark_table"

    uuid = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    sensor_name = Column(String(50), nullable=False)
    inference_layer = Column(Enum(InferenceLayer), nullable=False)
    send_timestamp = Column(BigInteger, nullable=False)
    recv_timestamp = Column(BigInteger, nullable=False)
    inference_latency = Column(BigInteger, nullable=False)
    registered_at = Column(DateTime, default=tz_now) 
