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
from pysal.explore.esda import Moran, Moran_Local
from pysal.viz.splot.esda import plot_moran, lisa_cluster

# p value threshold for LISA outputs
significance = 0.05

# convert
quadList = ["NA", "HH", "LH", "LL", "HL"]

def getQuadrants(qs, sigs, acceptableSig):
    """
    * Return list of quadrant codes depending upon specified significance level
    """
    # return quad code rather than number
    out = []
    for q in range(len(qs)):
        # overrride non-significant values as N/A
        if sigs[q] < acceptableSig:
            out.append(quadList[qs[q]])
        else:
            out.append(quadList[0])
    return out

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

# calculate local I
lisa = Moran_Local(mll_counts['mll'], W, transformation='R', permutations=9999)

# update GeoDataFrame
mll_counts['Morans_I'] = lisa.Is                                # value of Moran's I
mll_counts['sig'] = lisa.p_sim                                  # simulated p
mll_counts['quadrant'] = getQuadrants(lisa.q, lisa.p_sim, significance) # quadrant (HH, HL, LH, LL)

# output shapefile
mll_counts.to_file("../distance-analysis/parishes_mll_moran.shp")

# combined plot for local moran
lisa_cluster(lisa, mll_counts, significance)
plt.savefig("./out/lisa.png")
