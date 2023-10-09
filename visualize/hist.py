import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
class HistPlot:
    """
    high level function to quickly create seaborn barplot
    uses the seaborn.objects interface internally to enable additional modification after creation
    https://seaborn.pydata.org/tutorial/objects_interface.html
    """

    def __init__(
        self,
        df: pd.DataFrame,
        x: str,
        bins:str ='auto'
    ):
        """
        Args:
        df: a pandas dataframe
        x: variable to plot on the x axis
        """
        self.df = df
        self.x = x
        self.bins = bins

    def plot(self, width: int = 10, height: int = 6):
        """
        Args:
        width: width of the plot
        height: height of the plot
        """
        with sns.axes_style("darkgrid"):
            fig, ax = plt.subplots(figsize=(width, height))
            sns.histplot(self.df[self.x].dropna(), bins=self.bins, ax = ax)
            plt.show()