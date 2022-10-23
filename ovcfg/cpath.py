from dataclasses import dataclass


@dataclass
class Cpath:
    path: str
    selected: bool = False
