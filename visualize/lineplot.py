from typing import Union

import numpy as np
import pandas as pd
import seaborn.objects as so


class LinePlot:
    def __init__(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        col: Union[None, str] = None,
        text: Union[None, str] = None,
        group: Union[None, str] = None,
        linewidth: int = 1,
        linestyle: str = "-",
        labels: bool = True,
        digits: int = 2,
        label_offset_y: float = 0.03,
    ):
        """
        Args:
        df: a pandas dataframe
        x: variable to plot on the x axis
        y: variable to plot on the y axis
        col: optional color asthetic to color and connect lines by the color variable
        text: variable on which different labels are based, should be numeric to enable np.round
        group: optional grouping variable to connect lines by group
        linewidth: width of the lines
        linestyle: style of the lines
        labels: boolean to indicate whether to add labels
        digits: number of digits to round to, relevant for labels
        label_offset_y: the location of the labels is adjusted by adding x.xx of the maximum y value to the true y value
        """
        self.df = df
        self.plot_data = None
        self.p = None
        self.x = x
        self.y = y
        self.col = col
        self.group = group
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.text = text if text is not None else y
        self.labels = labels
        self.label_offset_y = label_offset_y
        self.digits = digits

    def _prepare_data(self):
        self.plot_data = self.df.assign(
            label=lambda x: np.round(x[self.text], self.digits),
            label_pos_y=lambda x: x[self.y] + np.max(x[self.y]) * self.label_offset_y,
        )

    def _prepare_plot(self):
        self.p = so.Plot(self.plot_data, x=self.x, y=self.y, color=self.col).add(
            so.Line(linewidth=self.linewidth, linestyle=self.linestyle), group=self.group
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
