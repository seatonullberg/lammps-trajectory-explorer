import os

from app.parser import Parser


def test_parser():
    filepath = os.path.abspath(__file__)
    filepath = os.path.dirname(filepath)
    filepath = os.path.join(filepath, "data", "PRL-NaCl-1ns.dump")
    parser = Parser(filepath)
    timestep = parser.parse_timestep(2004000)
    assert timestep.step == 2004000
    assert timestep.n_atoms == 19562
    assert -2.1 < timestep.box_bounds["xlo"] < -2.0
    assert 52 < timestep.box_bounds["xhi"] < 54
    assert -2.8 < timestep.box_bounds["ylo"] < -2.6
    assert 43 < timestep.box_bounds["yhi"] < 45
    assert -5.7 < timestep.box_bounds["zlo"] < -5.4
    assert 88 < timestep.box_bounds["zhi"] < 90
    assert len(timestep.atoms) == timestep.n_atoms
