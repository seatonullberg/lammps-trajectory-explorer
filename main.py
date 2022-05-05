"""
Bokeh dashboard to visualize LAMMPS trajectory files.
"""

import os
from random import random

from bokeh.io import curdoc
from bokeh.layouts import column, row, grid
from bokeh.models import Button, Div, FileInput, TextInput, Select, DataTable, TableColumn, MultiChoice
from bokeh.plotting import figure

p = figure(
    toolbar_location="right", 
    output_backend="webgl",
    visible=True,
    width=950,
    height=500,
    x_range=(0, 100),
    y_range=(0, 100),
)

file_input_title = Div(text="Trajectory File:", margin=(5, 5, -5, 5))
file_input = FileInput()
projection_options = ["X", "Y", "Z"]
x_axis_projection = Select(title="X Axis Projection:", options=projection_options, value=projection_options[0])
y_axis_projection = Select(title="Y Axis Projection:", options=projection_options, value=projection_options[1])
atom_types_input = MultiChoice(title="Atom Types:", options=[str(i) for i in range(5)])
selection_report_title = Div(text="Selection Report:", margin=(5, 5, -5, 5))
selection_report_table = DataTable(
    editable=False,
    height=100,
    columns=[
        TableColumn(title="Atom Type"),
        TableColumn(title="Percentage"),
    ]
)
curdoc().add_root(
    column(
        row(
            column(
                file_input_title, file_input,
                x_axis_projection,
                y_axis_projection,
                atom_types_input, 
            ),
            column(
                selection_report_title,
                selection_report_table
            )
        ),
        p,
    )
)
