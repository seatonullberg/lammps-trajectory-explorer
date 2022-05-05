import numpy as np
import pandas as pd


class Timestep:
    """Representation of a single trajectory timestep."""

    def __init__(self) -> None:
        self.step: int = 0
        self.n_atoms: int = 0
        self.box_bounds: dict = {}
        self.atoms: pd.DataFrame = pd.DataFrame()
