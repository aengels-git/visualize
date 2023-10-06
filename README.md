# Visualisierung mit seaborn.object interface

Alle Klassen verwenden das seaborn.objects interface um Abbildungen zu erstellen. Dies erlaubt eine einfache Weiterverarbeitung der erstellten Abbildungen.
Schaue für nähere Informationen zu den Möglichkeit von seaborn.objects auf die offizielle Dokumentation: https://seaborn.pydata.org/tutorial/objects_interface.html

## Features
- schnell Balkendiagramme für verschiedene Szenarien erstellen
- unterstützt automatische Umwandlung von Anteilen in Prozente und automatische Beschriftung von Balken
- unterstützt gestappelte/verschobene Balkendiagramme zum Darstellen von Unterschiedenen zwischen Kategorie
- beschriftete Liniendiagramme für mehrere Gruppen werden unterstützt
- Streudiagramme werden ebenfalls unterstützt
- format kann leicht über height / width in der plot function übergeben werden

## Usage:

Jede Klasse wird zunächst erstellt. Die Visualisierung wird dann mit der plot() Funktion umgesetzt.
Objekte zum Visualisieren generieren:
import pandas as pd
import seaborn as sns
import numpy as np 

diamonds = sns.load_dataset("diamonds")

freq_tab_1 = diamonds.cut.value_counts().reset_index().rename(columns = {'index':'cut', 'cut':'n'})
freq_tab_2 = diamonds.assign(n=lambda x:1).groupby(["cut","color"]).n.count().to_frame().reset_index()
freq_tab_3 = freq_tab_2.assign(prop=lambda x:x.n / np.sum(x.n))
freq_tab_3["prop_cut"] = freq_tab_3.groupby("cut").prop.transform(lambda x:x.div(x.sum()))

Beispiele Balkendiagramme:

Beispiele Liniendiagramme:

Beispiele Streudiagramme:

