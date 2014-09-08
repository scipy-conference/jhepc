import argparse
import numpy as np
from numpy import ma
import matplotlib
import matplotlib.image as mpimg
import matplotlib.cm as cm

# constants for unit conversion
AU_TO_KM = 149597870.691

parser = argparse.ArgumentParser(description='combined plot.')
parser.add_argument('--pdf', action='store_true', default=False, help='output to PDF')
parser.add_argument('iteration', type=int, help='iteration number')

args = parser.parse_args()
iteration = args.iteration

iterationsFilename = 'data/iterations.csv'
incumbentFilename = 'data/incumbent-trajectory-' + str(iteration) + '.csv'

# render to PDF
if args.pdf == True:
    matplotlib.use("PDF")

# this must be after any matplotlib.use() calls
import matplotlib.pyplot as plt


# iterations data
iterationsData = np.genfromtxt(iterationsFilename, delimiter=',', names=True)

# modify best objective values, since final object doesn't count in GTOC4 objective
for index, value in enumerate(iterationsData['bestCompleteObjectiveAll']):
    if value < 0:
        iterationsData['bestCompleteObjectiveAll'][index] = value + 1


# incumbent trajectory data
incumbentData = np.genfromtxt(incumbentFilename, delimiter=',', names=True, dtype=None)

# convert from kilometers to AU
xAU = incumbentData['X'] / AU_TO_KM
yAU = incumbentData['Y'] / AU_TO_KM
zAU = incumbentData['Z'] / AU_TO_KM

distanceAU = np.sqrt(xAU*xAU + yAU*yAU + zAU*zAU)

# get deltaV times
# ignore first deltaV at t=0.0, since this is allowed in problem statement
tDeltaV = ma.masked_where((incumbentData['deltaVMag'] == 0.0) | (incumbentData['t'] == 0.0), incumbentData['t'])

# get intermediate intercept times and indices
tIntercept = ma.masked_where(incumbentData['targetObject'] == '', incumbentData['t'])
interceptIndices = np.flatnonzero(~tIntercept.mask)

# get X, Y values at intercepts
xIntercepts = xAU[interceptIndices]
yIntercepts = yAU[interceptIndices]


# matplotlib plots

# change font size
matplotlib.rcParams.update({'font.size': 10})

# adjust figure aspect ratio and size
w, h = plt.figaspect(1.)
fig = plt.figure(figsize=(3.*w,3.*h))

# graph image
# we use the rasterized graph since the graph PDF could reach sizes > 50MB
img = mpimg.imread('graph-iteration-' + "{0:06d}".format(iteration) + '.png')
ax = plt.subplot2grid((3,3), (0, 0), rowspan=2, colspan=2)
ax.imshow(img, interpolation='none')
ax.axis('off')
ax.set_title('Search tree for ' + "{:,}".format(iteration) + ' iterations')

# graph image color bar
sm = plt.cm.ScalarMappable(cmap=cm.jet, norm=plt.normalize(vmin=0, vmax=iteration))
sm._A = []
cb = plt.colorbar(sm, orientation='horizontal', fraction=0.025, aspect=40, pad=0.0)
cb.set_label('Iteration')

# incumbent trajectory: X, Y
ax = plt.subplot2grid((3,3), (0, 2))
ax.set_title('Incumbent solution\n')
ax.set_xlabel('X (AU)')
ax.set_ylabel('Y (AU)')
ax.plot(xAU, yAU, 'k-')
ax.plot(xAU[0], yAU[0], 'bo', label='Earth departure')
ax.plot(xIntercepts, yIntercepts, 'o', color='gray', label='Intercept')
lgd1 = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=2, numpoints=1)
ax.grid(True)
ax.axis('equal')
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-1.5, 1.5)

# incumbent trajectory: distance to sun vs time
ax = plt.subplot2grid((3,3), (1, 2))
ax.set_title('Incumbent solution')
ax.set_xlabel('Time (days since departure)')
ax.set_ylabel('Distance to Sun (AU)')
ax.plot(incumbentData['t'], distanceAU, 'k-', lw=2, label='')

for i in interceptIndices:
    if i == interceptIndices[0]:
        ax.axvline(incumbentData['t'][i], color='0.8', ls='solid', label='Intercept')
    else:
        ax.axvline(incumbentData['t'][i], color='0.8', ls='solid')

ax.plot(tDeltaV, distanceAU, 'r^', ms=8.0, label='Impulsive maneuver') # default ms=6
lgd2 = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=2, numpoints=1)
ax.grid(True)
ax.set_xlim(0.0, 3700)
ax.set_ylim(0.7, 1.6)

# iteration history
ax = plt.subplot2grid((3,3), (2, 0), colspan=3)
ax.set_xlabel('Iteration')
ax.set_ylabel('Objective')

# plot actual data, and bound to it; for bestObjectives, use the value for one iteration ahead
ax.plot(iterationsData['iteration'][:iteration+1], iterationsData['objective'][:iteration+1], 'k-', alpha=0.5, linewidth=1, label='Incumbent solution')
ax.plot(iterationsData['iteration'][:iteration+1], iterationsData['bestObjectiveAll'][1:iteration+2], 'b-', linewidth=2, label='Best partial solution')
ax.plot(iterationsData['iteration'][:iteration+1], iterationsData['bestCompleteObjectiveAll'][1:iteration+2], 'g--', linewidth=4, label='Best complete solution')

# incumbent with gray circle
ax.plot(iterationsData['iteration'][iteration], iterationsData['objective'][iteration], 'ko', alpha=0.5, markersize=10) # no label

# make sure y axis minimum lets us see the bestObjectiveAll line
ax.set_ylim(min(iterationsData['bestObjectiveAll'])-1, 0)

ax.set_xlim(0, iteration+1)
ax.get_xaxis().set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

# hide last x-axis tick if it's near the border of the plot... to keep all movie frames exactly the same size
for i in range(len(ax.xaxis.get_majorticklocs())):
    if float(ax.xaxis.get_majorticklocs()[i]) >= float(0.95 * float(iteration+1.)) or ax.xaxis.get_majorticklocs()[i] == iteration+1:
        ax.xaxis.get_major_ticks()[i].label1.set_visible(False)

lgd3 = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, numpoints=1)
ax.grid(True)


plt.show()

if args.pdf == True:
    fig.savefig("iteration-" + str(iteration) + ".pdf", bbox_extra_artists=(lgd1,lgd2,lgd3), bbox_inches='tight', dpi=600)
