from typing import List

from app.timestep import Timestep


class Trajectory:
    """Collection of timesteps.
    
    Args:
        timesteps: List of Timestep objects.
    """

    def __init__(self, timesteps: List[Timestep]) -> None:
        self._timesteps = timesteps
