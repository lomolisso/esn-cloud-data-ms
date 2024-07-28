
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db import crud
from app.api import schemas
from app.api.dependencies import get_session

router = APIRouter()


# --- Edge Gateway ---

@router.get("/gateway", status_code=status.HTTP_200_OK, tags=["Edge Gateway"])
async def read_edge_gateways(session: Session = Depends(get_session)) -> list[schemas.ReadEdgeGateway]:
    """
    GET /gateway endpoint

    Endpoint to return all edge gateways.
    """

    return crud.read_edge_gateways(session=session)

@router.get("/gateway/{gateway_name}", status_code=status.HTTP_200_OK, tags=["Edge Gateway"])
async def read_edge_gateway(gateway_name: str, session: Session = Depends(get_session)) -> Optional[schemas.ReadEdgeGateway]:
    """
    GET /gateway/{gateway_name} endpoint
    
    Endpoint to return a specific edge gateway.
    """

    try:
        return crud.read_edge_gateway(session=session, device_name=gateway_name)
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

@router.post("/gateway", status_code=status.HTTP_201_CREATED, tags=["Edge Gateway"])
async def create_edge_gateway(gateway: schemas.CreateEdgeGateway, session: Session = Depends(get_session)):
    """
    POST /gateway endpoint

    Endpoint to create a new edge gateway.
    """

    try:
        crud.create_edge_gateway(session=session, fields=gateway.model_dump())
    except crud.EdgeGatewayAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Edge gateway already exists")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

    
@router.put("/gateway/{gateway_name}", status_code=status.HTTP_200_OK, tags=["Edge Gateway"])
async def update_edge_gateway(gateway_name: str, gateway: schemas.UpdateEdgeGateway, session: Session = Depends(get_session)):
    """
    PUT /gateway endpoint

    Endpoint to update an existing edge gateway.
    """

    try:
        crud.update_edge_gateway(session=session, device_name=gateway_name, fields=gateway.model_dump())
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

@router.delete("/gateway/{gateway_name}", status_code=status.HTTP_200_OK, tags=["Edge Gateway"])
async def delete_edge_gateway(gateway_name: str, session: Session = Depends(get_session)):
    """
    DELETE /gateway/{gateway_name} endpoint

    Endpoint to delete an existing edge gateway.
    """

    try:
        crud.delete_edge_gateway(session=session, device_name=gateway_name)
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    

# --- Edge Sensor ---


@router.get("/gateway/{gateway_name}/sensor", status_code=status.HTTP_200_OK, tags=["Edge Sensor"])
async def read_edge_sensors(gateway_name: str, session: Session = Depends(get_session)) -> list[schemas.ReadEdgeSensor]:
    """
    GET /gateway/{gateway_name}/sensor endpoint

    Endpoint to return all edge sensors for a specific gateway.
    """
    try:
        result = crud.read_edge_sensors(session=session, gateway_name=gateway_name)
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    return result

@router.get("/gateway/{gateway_name}/sensor/{sensor_name}", status_code=status.HTTP_200_OK, tags=["Edge Sensor"])
async def read_edge_sensor(gateway_name: str, sensor_name: str, session: Session = Depends(get_session)) -> Optional[schemas.ReadEdgeSensor]:
    """
    GET /gateway/{gateway_name}/sensor/{sensor_name} endpoint

    Endpoint to return a specific edge sensor for a specific gateway.
    """

    try:
        return crud.read_edge_sensor(session=session, gateway_name=gateway_name, device_name=sensor_name)
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

@router.post("/gateway/{gateway_name}/sensor", status_code=status.HTTP_201_CREATED, tags=["Edge Sensor"])
async def create_edge_sensor(gateway_name: str, sensor: schemas.CreateEdgeSensor, session: Session = Depends(get_session)):
    """
    POST /gateway/{gateway_name}/sensor endpoint

    Endpoint to create a new edge sensor for a specific gateway.
    """
    
    try:
        crud.create_edge_sensor(session=session, gateway_name=gateway_name, fields=sensor.model_dump())
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Edge sensor already exists")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    
@router.put("/gateway/{gateway_name}/sensor/{sensor_name}", status_code=status.HTTP_200_OK, tags=["Edge Sensor"])
async def update_edge_sensor(gateway_name: str, sensor_name: str, sensor: schemas.UpdateEdgeSensor, session: Session = Depends(get_session)):
    """
    PUT /gateway/{gateway_name}/sensor endpoint

    Endpoint to update an existing edge sensor for a specific gateway.
    """
    
    try:
        crud.update_edge_sensor(session=session, gateway_name=gateway_name, device_name=sensor_name, fields=sensor.model_dump())
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

@router.delete("/gateway/{gateway_name}/sensor/{sensor_name}", status_code=status.HTTP_200_OK, tags=["Edge Sensor"])
async def delete_edge_sensor(gateway_name: str, sensor_name: str, session: Session = Depends(get_session)):
    """
    DELETE /gateway/{gateway_name}/sensor/{sensor_name} endpoint

    Endpoint to delete an existing edge sensor for a specific gateway.
    """
    
    try:
        crud.delete_edge_sensor(session=session, gateway_name=gateway_name, device_name=sensor_name)
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

# --- Sensor Config ---
@router.get("/gateway/{gateway_name}/sensor/{sensor_name}/config", status_code=status.HTTP_200_OK, tags=["Sensor Config"])
async def read_sensor_config(gateway_name: str, sensor_name: str, session: Session = Depends(get_session)) -> Optional[schemas.SensorConfig]:
    """
    GET /gateway/{gateway_name}/sensor/{sensor_name}/config endpoint

    Endpoint to return the configuration of a specific sensor.
    """
    try:
        return crud.read_sensor_config(session=session, gateway_name=gateway_name, device_name=sensor_name)
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    except crud.SensorConfigNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor config not found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    
@router.post("/gateway/{gateway_name}/sensor/{sensor_name}/config", status_code=status.HTTP_201_CREATED, tags=["Sensor Config"])
async def create_or_update_sensor_config(gateway_name: str, sensor_name: str, config: schemas.SensorConfig, session: Session = Depends(get_session)):
    """
    POST /gateway/{gateway_name}/sensor/{sensor_name}/config endpoint

    Endpoint to create or update the configuration of a specific sensor.
    """
    
    try:
        crud.create_sensor_config(session=session, gateway_name=gateway_name, device_name=sensor_name, fields=config.model_dump())
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    except crud.SensorConfigAlreadyExists:
        crud.update_sensor_config(session=session, gateway_name=gateway_name, device_name=sensor_name, fields=config.model_dump())
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

@router.delete("/gateway/{gateway_name}/sensor/{sensor_name}/config", status_code=status.HTTP_200_OK, tags=["Sensor Config"])
async def delete_sensor_config(gateway_name: str, sensor_name: str, session: Session = Depends(get_session)):
    """
    DELETE /gateway/{gateway_name}/sensor/{sensor_name}/config endpoint

    Endpoint to delete an existing configuration for a specific sensor.
    """
    
    try:
        crud.delete_sensor_config(session=session, gateway_name=gateway_name, device_name=sensor_name)
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    except crud.SensorConfigNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor config not found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

# --- Sensor Reading ---

@router.get("/gateway/{gateway_name}/sensor/{sensor_name}/readings", status_code=status.HTTP_200_OK, tags=["Sensor Reading"])
async def read_sensor_readings(gateway_name: str, sensor_name: str, session: Session = Depends(get_session)) -> list[schemas.ReadSensorReading]:
    """
    GET /gateway/{gateway_name}/sensor/{sensor_name}/readings endpoint

    Endpoint to return all sensor readings for a specific sensor.
    """
    try:
        result = crud.read_sensor_readings(session=session, gateway_name=gateway_name, device_name=sensor_name)
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    return result

@router.get("/gateway/{gateway_name}/sensor/{sensor_name}/reading/{reading_uuid}", status_code=status.HTTP_200_OK, tags=["Sensor Reading"])
async def read_sensor_reading(gateway_name: str, sensor_name: str, reading_uuid: str, session: Session = Depends(get_session)) -> Optional[schemas.ReadSensorReading]:
    """
    GET /gateway/{gateway_name}/sensor/{sensor_name}/reading/{reading_uuid} endpoint

    Endpoint to return a specific sensor reading for a specific sensor.
    """
    try:
        return crud.read_sensor_reading(session=session, gateway_name=gateway_name, device_name=sensor_name, reading_uuid=reading_uuid)
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    except crud.SensorReadingNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor reading not found")
    except Exception as e:
        print("\n\n\n\n", e, "\n\n\n\n")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

@router.post("/gateway/{gateway_name}/sensor/{sensor_name}/reading", status_code=status.HTTP_201_CREATED, tags=["Sensor Reading"])
async def create_sensor_reading(gateway_name: str, sensor_name: str, reading: schemas.CreateSensorReading, session: Session = Depends(get_session)):
    """
    POST /gateway/{gateway_name}/sensor/{sensor_name}/reading endpoint

    Endpoint to create a new sensor reading for a specific sensor.
    """
    
    try:
        crud.create_sensor_reading(session=session, gateway_name=gateway_name, device_name=sensor_name, fields=reading.model_dump())
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    except crud.SensorReadingAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sensor reading already exists")

@router.delete("/gateway/{gateway_name}/sensor/{sensor_name}/readings", status_code=status.HTTP_200_OK, tags=["Sensor Reading"])
async def delete_sensor_readings(gateway_name: str, sensor_name: str, session: Session = Depends(get_session)):
    """
    DELETE /gateway/{gateway_name}/sensor/{sensor_name}/readings endpoint

    Endpoint to delete all sensor readings for a specific sensor.
    """
    
    try:
        crud.delete_sensor_readings(session=session, gateway_name=gateway_name, device_name=sensor_name)
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

# --- Inference Result ---

@router.post("/gateway/{gateway_name}/sensor/{sensor_name}/reading/{reading_uuid}/prediction", status_code=status.HTTP_201_CREATED, tags=["Prediction Result"])
async def create_prediction_result(gateway_name: str, sensor_name: str, reading_uuid: str, prediction_result: schemas.CreatePredictionResult, session: Session = Depends(get_session)):
    """
    POST /gateway/{gateway_name}/sensor/{sensor_name}/reading/{reading_uuid}/prediction endpoint

    Endpoint to create a new prediction result for a specific sensor reading.
    """
    
    try:
        crud.create_prediction_result(session=session, gateway_name=gateway_name, device_name=sensor_name, reading_uuid=reading_uuid, fields=prediction_result.model_dump())
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    except crud.SensorReadingNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor reading not found")
    except crud.PredictionResultAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Prediction result already exists")

# --- Inference Latency Benchmark ---
@router.post("/gateway/{gateway_name}/sensor/{sensor_name}/reading/{reading_uuid}/inference/latency", status_code=status.HTTP_201_CREATED, tags=["Inference Latency Benchmark"])
async def create_inference_latency_benchmark(gateway_name: str, sensor_name: str, reading_uuid: str, benchmark: schemas.InferenceLatencyBenchmark, session: Session = Depends(get_session)):
    """
    POST /gateway/{gateway_name}/sensor/{sensor_name}/reading/{reading_uuid}/inference/latency endpoint

    Endpoint to create a new inference latency benchmark for a specific sensor reading.
    """
    
    try:
        crud.create_inference_latency_benchmark(session=session, gateway_name=gateway_name, device_name=sensor_name, reading_uuid=reading_uuid, fields=benchmark.model_dump())
    except crud.EdgeGatewayNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge gateway not found")
    except crud.EdgeSensorNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Edge sensor not found")
    except crud.SensorReadingNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor reading not found")
    except crud.PredictionResultNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction result not found")
    except crud.InferenceLatencyBenchmarkAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Inference latency benchmark already exists")
    except Exception as e:
        print("\n\n\n\n", e, "\n\n\n\n")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")