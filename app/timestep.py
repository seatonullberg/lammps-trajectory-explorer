import numpy as np
import pandas as pd


class Timestep:
    """Representation of a single trajectory timestep."""

    def __init__(self) -> None:
        self._step: int = 0
        self._n_atoms: int = 0
        self._box_bounds: np.ndarray = np.array([])
        self._df: pd.DataFrame = pd.DataFrame()
