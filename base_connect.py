from dataclasses import dataclass


@dataclass
class Base:
    host: str = "localhost"
    port: int = 5000
