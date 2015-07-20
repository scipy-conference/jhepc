import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines
import skew_projection


#==========================
# Loading data
#==========================

AP = np.load("Average_emission.npy")

I_AP = AP[0, 1:, 1:]  # Total intensity
L_AP = AP[1, 1:, 1:]  # Linearly polarized emission	
V_AP = AP[2, 1:, 1:]  # Circularly polarized emission
ph_spin_AP = AP[0, 0, 1:] # Spin phase of each emission sample
ph_orb_AP = AP[0, 1:, 0]  # Orbital phase of each emission sample

# Loading orbital phase, spin phase and energy of single pulses
ph_orb_SP, ph_spin_SP, E_SP = np.loadtxt("Single_pulses.txt", usecols=(0,1,2), unpack=True, dtype=float)

Nsub = len(AP[0, 1:, 0])

# Offset between side plots
dph = 0.35

# Average emission data have been normed in such way that the offpulse mean == 0 and std == 1. Rescale is needed to 
#fit profiles in the image.
rescale=600

#===========================
# Plotting
#==========================-

fig = plt.figure()
title='Average and single-pulse emission of PSR B1744$-$24A'
ax = fig.add_subplot(111, projection='skewx', axisbg='0.98', title=title)

for k in range(Nsub):
  plt.plot(ph_spin_AP, I_AP[k,:]/rescale+ph_orb_AP[k], '0.3', lw=1.1, zorder=10) 
  bright = np.abs(V_AP[k,:])>2.
  plt.fill_between(ph_spin_AP, V_AP[k,:]/rescale+ph_orb_AP[k], ph_orb_AP[k], where=bright, color='b', interpolate=True, alpha=0.25, zorder=10)
  bright = np.abs(L_AP[k,:])>2.
  plt.fill_between(ph_spin_AP, L_AP[k,:]/rescale+ph_orb_AP[k], ph_orb_AP[k], where=bright, color='r', interpolate=True, alpha=0.35, zorder=10)

for k in np.arange(5,Nsub-1, 5):
  plt.plot(ph_spin_AP+dph, I_AP[k,:]/rescale+ph_orb_AP[k], '0.3', lw=1.1, zorder=10) 
  bright = np.abs(V_AP[k,:])>2.
  plt.fill_between(ph_spin_AP+dph, V_AP[k,:]/rescale+ph_orb_AP[k], ph_orb_AP[k], where=bright, color='b', interpolate=True, alpha=0.3, zorder=10)
  bright = np.abs(L_AP[k,:])>2.
  plt.fill_between(ph_spin_AP+dph, L_AP[k,:]/rescale+ph_orb_AP[k], ph_orb_AP[k], where=bright, color='r', interpolate=True, alpha=0.4, zorder=10)

sps = plt.scatter(2*ph_spin_SP-dph, ph_orb_SP, marker='o', s=5*(E_SP-3)**2, facecolor='w', edgecolor='k', zorder=10)


# Making legend
L_legend = plt.Rectangle((0, 0), 1, 1, fc="r", alpha=0.3, ec='r', label='Linear')
V_legend = plt.Rectangle((0, 0), 1, 1, fc="b", alpha=0.2, ec='b', label='Circular')
I_legend = mlines.Line2D([],[], color='0.3', lw=1.1) 
ax.legend([I_legend, L_legend, V_legend, sps], ['Total intensity', 'Linear polarization', 'Circular polarization', 'Bright single pulses'], loc=3, frameon=False, prop={'size':9})

# Organizing ticks and labels

xticks = np.array([0-dph, 0.1-dph, 0.2-dph, 0, 0.1, 0.2, 0+dph, 0.1+dph, 0.2+dph])
xtick_labels = np.array(['0.0', '0.05', '0.1', '0.0', '0.1', '0.2', '0.0', '0.1', '0.2'])
plt.xticks(xticks, xtick_labels)
plt.yticks(np.arange(0,1.1,0.1))
plt.xlim(-0.6,0.7)
plt.ylim(-0.05,1.05)
plt.xlabel("Pulsar spin phase")
ax.xaxis.set_label_coords(0.55, -0.05)
plt.ylabel("Orbital phase")
plt.grid(color='w', ls='-', lw=2)

plt.savefig("Ter5A.pdf", format="pdf")
plt.show()

