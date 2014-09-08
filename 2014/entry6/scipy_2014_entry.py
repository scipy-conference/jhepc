import numpy as np
from hyperion.model import ModelOutput
import matplotlib.pyplot as plt
from yt.mods import write_bitmap, ColorTransferFunction

plt.rcParams['font.family'] = 'Arial'

# Read in model from Hyperion

m = ModelOutput('pla704850_lev7_129.rtout')
grid = m.get_quantities()

# Convert quantities to yt
pf = grid.to_yt()

# Instantiate the ColorTransferfunction.
tmin, tmax = 1.3, 2.3
tf_temp = ColorTransferFunction((tmin, tmax))
dmin, dmax = -20, -16
tf_dens = ColorTransferFunction((dmin, dmax))

# Set up the camera parameters: center, looking direction, width, resolution
c = (pf.domain_right_edge + pf.domain_left_edge) / 2.0

L = np.array([1.0, 1.0, 1.0])
W = 0.7 / pf["unitary"]
N = 512

# Create camera objects

cam_temp = pf.h.camera(c, L, W, N, tf_temp,
                       fields=['temperature'], log_fields=[True],
                       no_ghost=False)

cam_dens = pf.h.camera(c, L, W, N, tf_dens,
                       fields=['density'], log_fields=[True],
                       no_ghost=False)

# Set up layers
tf_temp.add_layers(10, 0.0001, colormap='RdBu_r')
tf_dens.add_layers(10, 0.003, colormap='winter')

# Fly around

N = 36 * 4

images_temp = []

for i, snapshot in enumerate(cam_temp.rotation(2. * np.pi, N, clip_ratio=8.0)):
    images_temp.append(cam_temp.snapshot())

images_dens = []

for i, snapshot in enumerate(cam_dens.rotation(2. * np.pi, N, clip_ratio=8.0)):
    images_dens.append(cam_dens.snapshot())

temp = np.zeros(images_temp[0].shape[:2] + (4,))
dens = np.zeros(images_temp[0].shape[:2] + (4,))

# Initialize figure

fig = plt.figure(figsize=(10, 10))

fig.set_facecolor('black')
fig.set_alpha(1.0)

ax = fig.add_axes([0.15, 0.15, 0.7, 0.7])

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

ax.patch.set_facecolor('black')
ax.patch.set_edgecolor('black')

# Temperature colorbar

axcbt = fig.add_axes([0.87, 0.15, 0.04, 0.7])

cm_temp = tf_temp.get_colormap_image(10, 10)
axcbt.imshow(cm_temp, aspect='auto', extent=[0., 1., tmin, tmax])
axcbt.xaxis.set_ticklabels('')

temps = [20, 40, 80, 160]
axcbt.yaxis.set_ticks(np.log10(temps))
axcbt.yaxis.set_ticklabels([str(x) for x in temps])

axcbt.set_ylabel("Temperature [K]", size=16, color='white',
                 rotation=270, labelpad=15)
axcbt.yaxis.set_label_position('right')

for tick in axcbt.yaxis.get_major_ticks():
    tick.label1On = False
    tick.label2On = True

# Density colorbar

axcbd = fig.add_axes([0.09, 0.15, 0.04, 0.7])

cm_dens = tf_dens.get_colormap_image(10, 10)
axcbd.imshow(cm_dens, aspect='auto', extent=[0., 1., dmin, dmax])
axcbd.xaxis.set_ticklabels('')

densities = [-20, -19, -18, -17, -16]
axcbd.yaxis.set_ticks(densities)
axcbd.yaxis.set_ticklabels([str(x) for x in densities])

axcbd.set_ylabel("Log10(Density) [cgs]", size=16, color='white')

# Esthetics for colorbars

for colorbar_ax in [axcbd, axcbt]:

    colorbar_ax.patch.set_facecolor('black')
    colorbar_ax.patch.set_edgecolor('black')

    for label in colorbar_ax.yaxis.get_ticklabels():
        label.set_color('white')
        label.set_size(12)

    for tick in colorbar_ax.yaxis.get_ticklines():
        tick.set_color('white')

    for tick in colorbar_ax.xaxis.get_ticklines():
        tick.set_visible(False)

# Show the RGB images

prev = None

for i in range(N):

    # Blend the RGB images
    image_total = images_temp[i] * 1.50 + images_dens[i] * 0.33

    bitmap = write_bitmap(image_total, 'dens_temp_{0:03d}.png'.format(i + 1),
                          max_val=0.0085, transpose=True)

    # Remove alpha
    bitmap = bitmap[:, :, :3]

    if prev is None:
        prev = ax.imshow(bitmap)
    else:
        prev.set_data(bitmap)

    fig.savefig('output/frame_{0:03d}.png'.format(i + 1),
                facecolor=fig.get_facecolor(),
                edgecolor='none', bbox_inches='tight')

    fig.savefig('output/frame_{0:03d}.pdf'.format(i + 1),
                facecolor=fig.get_facecolor(),
                edgecolor='none', bbox_inches='tight')
