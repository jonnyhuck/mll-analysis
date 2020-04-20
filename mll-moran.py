"""
* Moran's I analysis to demonstrate that there is no spatial autocorelation in MLL
*   locations.
*
* Results:
*     Global Moran's I Results
*     I:			 0.030234125855660057
*     Expected I:		 -0.003278688524590164
*     Simulated p:		 0.1605
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from pysal.lib.weights import Queen
from pysal.explore.esda import Moran
from pysal.viz.splot.esda import plot_moran

# open file
mll_counts = gpd.read_file("../distance-analysis/parishes_mll.shp")

# calculate and row standardise weights matrix
W = Queen.from_dataframe(mll_counts)
W.transform = 'r'

# calculate and report global I
mi = Moran(mll_counts['mll'], W, permutations=9999)
print("\nGlobal Moran's I Results")
print("I:\t\t\t", mi.I)					   # value of Moran's I
print("Expected I:\t\t", mi.EI)			   # expected Moran's I
print("Simulated p:\t\t", mi.p_sim, "\n")  # simulated p

# scatterplot for global moran
plot_moran(mi, zstandard=True, figsize=(12,4))
plt.savefig("./out/moran.png")
