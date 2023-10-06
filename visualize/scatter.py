from typing import Union

import numpy as np
import pandas as pd
import seaborn.objects as so


class ScatterPlot:
    """
    high level function to quickly create seaborn scatterplot
    uses the seaborn.objects interface internally to enable additional modification after creation
    https://seaborn.pydata.org/tutorial/objects_interface.html
    """

    def __init__(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        col: Union[None, str] = None,
        text: Union[None, str] = None,
        pointsize: int = 4,
        marker: str = "o",
        labels: bool = True,
        digits: int = 2,
        label_offset_y: float = 0.03,
    ):
        """
        Args:
        df: a pandas dataframe
        x: variable to plot on the x axis
        y: variable to plot on the y axis
        col: optional color asthetic to color the points based on another variable
        text: variable on which different labels are based, should be numeric to enable np.round
        labels: boolean to indicate whether to add labels
        label_offset_y: the location of the labels is adjusted by adding x.xx of the maximum y value to the true y value
        pointsize: size
        marker: how the points are displayed
        """
        self.df = df
        self.x = x
        self.y = y
        self.col = col
        self.pointsize = pointsize
        self.marker = marker
        self.text = text if text is not None else y
        self.labels = labels
        self.label_offset_y = label_offset_y
        self.digits = digits
        self.plot_data = None
        self.p = None

    def _prepare_data(self):
        self.plot_data = self.df.assign(
            label=lambda x: np.round(x[self.text], self.digits),
            label_pos_y=lambda x: x[self.y] + np.max(x[self.y]) * self.label_offset_y,
        )

    def _prepare_plot(self):
        self.p = so.Plot(self.plot_data, x=self.x, y=self.y, color=self.col).add(
            so.Dot(pointsize=self.pointsize, marker=self.marker)
        )

    def _add_labels(self):
        if self.labels:
            self.p = self.p.add(so.Text(color="black"), text="label", x=self.x, y="label_pos_y", color=self.col)

    def plot(self, width: int = 10, height: int = 6):
        """
        Args:
        width: width of the plot
        height: height of the plot
        """
        self._prepare_data()
        self._prepare_plot()
        self._add_labels()
        return self.p.layout(size=(width, height))
