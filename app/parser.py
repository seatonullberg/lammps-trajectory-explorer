import os
from typing import TextIO, Union

from app.timestep import Timestep


class Parser:
    """LAMMPS trajectory file parser.

    Args:
        f: File path or any readable text object.
    """

    def __init__(self, f: Union[str, TextIO]) -> None:
        pass

    def parse_timestep(self, step: int) -> Timestep:
        """Reads one timestep into a Timestep object.

        Args:
            step: Timestep number.
        """
        pass
