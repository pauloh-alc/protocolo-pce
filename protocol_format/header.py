from dataclasses import dataclass
from datetime import datetime


@dataclass
class Header:
    version_protocol: float = 1.0
    message_type: str = "SENSOR_CONNECT"
    device_id: str = "sensor_01"
    timestamp: datetime = datetime.now()
