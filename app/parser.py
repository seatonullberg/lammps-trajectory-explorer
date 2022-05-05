import os
import warnings
from typing import TextIO, Union

import pandas as pd

from app.timestep import Timestep
from app.utils import has_method
from app.warnings import WARNING_NON_ORTHOGONAL


class Parser:
    """LAMMPS trajectory file parser.

    Args:
        f: File path or any readable text object.
    """

    def __init__(self, f: Union[str, TextIO]) -> None:
        source = None
        # If a file path is passed, open it and read its lines.
        if type(f) is str:
            source = open(f, "r")
        # If a readable object is passed, read its lines directly.
        elif has_method(f, "readlines"):
            source = f
        # Else, raise a type error indicating the source is invalid.
        else:
            raise TypeError("`f` must be a file path or a readable object")

        assert source is not None
        lines = [line.strip() for line in source.readlines()]
        lines = [line for line in lines if line != ""]
        self._lines = lines
        source.close()

    def parse_timestep(self, step: int) -> Timestep:
        """Reads one timestep into a Timestep object.

        Args:
            step: Timestep number.
        """
        timestep = Timestep()
        timestep.step = step

        # Find the desired timestep.
        success = False
        for i, line in enumerate(self._lines):
            if line == "ITEM: TIMESTEP":
                next_line = self._lines[i + 1]
                if int(next_line) == timestep.step:
                    success = True
                    break

        # Raise error if end of file is reached before timestep is found.
        if not success:
            raise EOFError("Step number {} not found.".format(step))

        # Parse all other timestep properties.
        n_atoms_line = i + 2
        timestep.n_atoms = self._parse_n_atoms(n_atoms_line)
        box_bounds_line = i + 4
        timestep.box_bounds = self._parse_box_bounds(box_bounds_line)
        atoms_line = i + 8
        timestep.atoms = self._parse_atoms(atoms_line)

        # Return fully initialized Timestep.
        return timestep

    def _parse_n_atoms(self, line_number) -> int:
        """Returns the number of atoms in a single timestep."""
        assert self._lines[line_number] == "ITEM: NUMBER OF ATOMS"
        return int(self._lines[line_number + 1])

    def _parse_box_bounds(self, line_number) -> dict:
        """Returns the bounds of the simulation cell of a single timestep."""
        parts = self._lines[line_number].split()
        assert parts[0] == "ITEM:"
        assert parts[1] == "BOX"
        assert parts[2] == "BOUNDS"
        x_line = line_number + 1
        y_line = line_number + 2
        z_line = line_number + 3
        xlo, xhi, xtilt = self._lines[x_line].split()
        ylo, yhi, ytilt = self._lines[y_line].split()
        zlo, zhi, ztilt = self._lines[z_line].split()
        tilts = [float(tilt) for tilt in [xtilt, ytilt, ztilt]]
        if any(tilts) > 0:
            warnings.warn(WARNING_NON_ORTHOGONAL)
        return {
            "xlo": float(xlo),
            "xhi": float(xhi),
            "ylo": float(ylo),
            "yhi": float(yhi),
            "zlo": float(zlo),
            "zhi": float(zhi),
        }

    def _parse_atoms(self, line_number) -> pd.DataFrame:
        """Returns the per-atom information of a single timestep."""
        parts = self._lines[line_number].split()
        assert parts[0] == "ITEM:"
        assert parts[1] == "ATOMS"
        column_headings = parts[2:]
        column_values = {heading: [] for heading in column_headings}
        column_types = {heading: float for heading in column_headings}
        column_types["id"] = int  # special case
        column_types["type"] = int  # special case
        start = line_number + 1
        for line in self._lines[start:]:
            if line == "ITEM: TIMESTEP":
                break
            atom_data = line.split()
            for i, data in enumerate(atom_data):
                heading = column_headings[i]
                typ = column_types[heading]
                column_values[heading].append(typ(data))
        return pd.DataFrame(column_values)
