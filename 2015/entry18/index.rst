Entry 18
========

.. image:: entry18.png
   :width: 800

Authors
-------
- Ben Montet

By analyzing the spectrum of a star, the temperature, surface gravity,
and abundance of heavy elements can be measured. However, for the vast
majority of stars, the stellar mass and radius are not directly
observable. Instead, they must be inferred by combining these direct
observables with theoretical stellar models. Models faithfully
reproduce the fundamental parameters of sunlike stars, but are poorly
calibrated for stars with masses or ages considerably different than
the Sun. Two different models can often predict masses different by a
factor of two for stars that are young (less than 100 million years
old) and low-mass (smaller than 50% the mass of the Sun).

To better calibrate stellar models, we need a collection of benchmark
stars with directly measured masses. The most efficient way to measure
masses is to observe the orbits of binary stars. In a binary system,
the total mass depends on the orbital period and physical separation
between the two stars, both of which are directly observable.

This figure comes from a proposal to directly measure orbital periods
of young, low-mass binaries. The top subfigure shows the relative
orbit of the two stars in the GJ4185Aab system. The fainter,
“secondary” star orbits counterclockwise around the brighter,
“primary” star as viewed from Earth. There are currently three
observations of this binary system from 2011 and 2012. The blue curves
represent possible orbits of the secondary, plotted by drawing samples
from the posterior distribution of each orbital element. In fall 2015,
there is a large uncertainty in the relative positions of the two
stars. Each white circle represents the location of the secondary star
along one of the possible orbits in November, 2015. Selecting one
observation, we then show possible orbits of the secondary after this
additional hypothetical data point.

The spread in possible orbits is considerably larger than the typical
uncertainty in each data point, so an additional observation will
provide a significant improvement on the measured period. The lower
right subfigure shows the observed period posterior distribution
before and after adding the additional data point. With the additional
point, the uncertainty in the period is reduced by a factor of 5!

Once we have the total mass, we can collect radial velocity (RV)
observations to measure the mass ratio, and thus the individual mass
of each star (lower left). The RV of each star changes during the
orbit as a function of the position of the star and its mass. (The
data point shows the typical uncertainty in one observation.) Once the
orbit is characterized (red, as previously) the variation in RV is
dominated by the uncertainty in the individual mass of each
star. However, with the current data only (blue) the uncertainty in
the orbit contributes significantly to the scatter in the RVs, making
RV observations less useful. Therefore, an additional imaging
observation is essential both to characterize the orbit of the binary
to measure the total mass, and to be able to eventually measure
individual masses.

Products
--------

- :download:`PDF <figure1.pdf>`

Source
------

.. literalinclude:: plot_fits.py

- :download:`data5.txt <data5.txt>`

- :download:`rvchains_out_a.npy <rvchains_out_a.npy>`

- :download:`rvchains_out_b.npy <rvchains_out_b.npy>`
