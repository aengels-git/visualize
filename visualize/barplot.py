from typing import Union

import numpy as np
import pandas as pd
import seaborn.objects as so
from matplotlib.ticker import FuncFormatter


class BarPlot:
    """
    high level function to quickly create seaborn barplot
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
        stacked: bool = True,
        labels: bool = True,
        label_type: str = "absolute",
        digits: int = 2,
        bar_width: float = 0.8,
    ):
        """
        Args:
        df: a pandas dataframe
        x: variable to plot on the x axis
        y: variable to plot on the y axis
        col: optional color asthetic to color the bar segments based on another variable
        text: variable on which different labels are based, should be numeric to enable np.round
        stacked: boolean to indicate whether to use stacked barplots as opposed to dodged barplots
        labels: boolean to indicate whether to add labels
        label_type: should be either absolute or percent, percent transform a proportion to percent and adjusts the y axis appropriately
        digits: number of digits to round to, relevant for labels
        bar_width: should not be changed for the labeled version, but controls the barwidths
        """
        self.df = df
        self.plot_data = None
        self.p = None
        self.x = x
        self.y = y
        self.col = col
        self.text = text if text is not None else y
        self.stacked = stacked
        self.labels = labels
        self.label_type = label_type
        self.digits = digits
        self.bar_width = bar_width

    def _prepare_data(self):
        self.plot_data = self.df.copy()
        self.plot_data = self.plot_data.groupby(self.x, group_keys=True).apply(
            lambda grp: grp.assign(label_pos=lambda x: np.cumsum(x[self.y]) - x[self.y] / 2)
        )
        if self.labels and self.label_type == "percent":
            if self.digits == 0:
                self.plot_data = self.plot_data.assign(
                    label=lambda x: np.round(x[self.text] * 100, self.digits).astype("int").astype("string") + " %"
                )
            else:
                self.plot_data = self.plot_data.assign(
                    label=lambda x: np.round(x[self.text] * 100, self.digits).astype("string") + " %"
                )
        else:
            self.plot_data = self.plot_data.assign(label=lambda x: np.round(x[self.text], self.digits))

    def _prepare_plot(self):
        if self.col is not None:
            if self.stacked:
                self.p = so.Plot(self.plot_data, x=self.x, y=self.y, color=self.col).add(so.Bar(), so.Stack())
            else:
                self.p = so.Plot(self.plot_data, x=self.x, y=self.y, color=self.col).add(
                    so.Bar(width=self.bar_width), so.Dodge()
                )

        else:
            self.p = so.Plot(self.plot_data, x=self.x, y=self.y).add(so.Bar())

    def _add_labels(self):
        if self.labels and self.col is not None and self.x != self.col:
            if self.stacked:
                self.p = self.p.add(so.Text(color="black"), text="label", x=self.x, y="label_pos", color=self.col)
            else:
                self.p = self.p.add(so.Text(color="black", valign="bottom"), so.Dodge(by=[self.col]), text="label")
        elif self.labels and self.col is None:
            self.p = self.p.add(so.Text(valign="bottom", color="black"), text="label")
        elif self.x == self.col:
            self.p = self.p.add(so.Text(valign="bottom", color="black"), text="label")

    def plot(self, width: int = 10, height: int = 6):
        """
        Args:
        width: width of the plot
        height: height of the plot
        """
        self._prepare_data()
        self._prepare_plot()
        self._add_labels()
        if self.label_type == "percent":
            formatter = FuncFormatter(lambda x, pos: "${:.0f}$ %".format(np.round(x * 100, 0)))
            self.p = self.p.scale(y=so.Continuous().label(formatter=formatter))
        return self.p.layout(size=(width, height))
