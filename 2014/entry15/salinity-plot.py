'''
Plot surface salinity from TXLA model. 
Script for John Hunter Visualization Contest
SciPy Conference 2014
Kristen Thyng and Rob Hetland
'''

import matplotlib as mpl
mpl.use("Agg") # set matplotlib to use the backend that does not require a windowing system
import numpy as np
import netCDF4 as netCDF
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import glob
import cmPong
import bisect
from mpl_toolkits.basemap import Basemap
from matplotlib.mlab import find

mpl.rcParams.update({'font.size': 14})
mpl.rcParams['font.sans-serif'] = 'Arev Sans, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Helvetica, Avant Garde, sans-serif'
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.cal'] = 'cursive'
mpl.rcParams['mathtext.rm'] = 'sans'
mpl.rcParams['mathtext.tt'] = 'monospace'
mpl.rcParams['mathtext.it'] = 'sans:italic'
mpl.rcParams['mathtext.bf'] = 'sans:bold'
mpl.rcParams['mathtext.sf'] = 'sans'
mpl.rcParams['mathtext.fallback_to_cm'] = 'True'

# All model info is on the thredds server
loc = 'http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_nesting6.nc'

## Grid info ##
g = netCDF.Dataset(loc)

# Basemap parameters.
llcrnrlon=-97.8; llcrnrlat=27.01; 
urcrnrlon=-87.7; urcrnrlat=30.5; projection='lcc'
lat_0=30; lon_0=-94; resolution='i'; area_thresh=0.
basemap = Basemap(llcrnrlon=llcrnrlon,
             llcrnrlat=llcrnrlat,
             urcrnrlon=urcrnrlon,
             urcrnrlat=urcrnrlat,
             projection=projection,
             lat_0=lat_0,
             lon_0=lon_0,
             resolution=resolution,
             area_thresh=area_thresh)
# get lon/lat coords and change to projected space
lonpsi = g.variables['lon_psi'][:]
latpsi = g.variables['lat_psi'][:]
xpsi, ypsi = basemap(lonpsi,latpsi)
lonr = g.variables['lon_rho'][:]
latr = g.variables['lat_rho'][:]
xr, yr = basemap(lonr,latr)
h = g.variables['h'][:]
##

## Model output ##
m = netCDF.Dataset(loc)

# Model time period to use
units = m.variables['ocean_time'].units
year = 2008
starttime = netCDF.date2num(datetime(year, 6, 24, 0, 0, 0), units)
endtime = netCDF.date2num(datetime(year, 6, 24, 4, 0, 0), units)
dt = m.variables['ocean_time'][1] - m.variables['ocean_time'][0] # 4 hours in seconds
ts = np.arange(starttime, endtime, dt)
itshift = find(starttime==m.variables['ocean_time'][:]) # shift to get to the right place in model output
datesModel = netCDF.num2date(m.variables['ocean_time'][:], units)
plotdates = netCDF.num2date(ts, units)
monthdates = [datetime(year, month, 1, 0, 0, 0) for month in np.arange(1,13)]

# Colormap for model output
levels = (37-np.exp(np.linspace(0,np.log(36.), 10)))[::-1]-1 # log for salinity
cmap = cmPong.salinity('YlGnBu_r', levels)
ilevels = [0,1,2,3,4,5,8] # which levels to label
ticks = [int(tick) for tick in levels[ilevels]] # plot ticks
##

## Wind forcing ##
w = np.load('wind.npz')
# Wind time period to use
unitsWind = str(w['units'])
datesWind = netCDF.num2date(w['t'], unitsWind)
wdx = 25; wdy = 30 # in indices
##

## River forcing ##
r = netCDF.Dataset('TXLA_river_4dyes_2011.nc')
# River timing
unitsRiver = r.variables['river_time'].units
datesRiver = netCDF.num2date(r.variables['river_time'][:], unitsRiver)
tRiver = r.variables['river_time'][:]
# all of river input
Q = np.abs(r.variables['river_transport'][:]).sum(axis=1)*2.0/3.0
# start and end indices in time for river discharge
itstartRiver = bisect.bisect_left(datesRiver, datetime(year, 1, 1, 0, 0, 0))
itendRiver = bisect.bisect_left(datesRiver, datetime(year+1, 1, 1, 0, 0, 0))
# ticks for months on river discharge
mticks = [bisect.bisect_left(datesRiver, monthdate) for monthdate in np.asarray(monthdates)]
mticknames = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
##

# Loop through times that simulations were started
for plotdate in plotdates:

    # Set up before plotting
    itmodel = bisect.bisect_left(datesModel, plotdate) # index for model output at this time
    itriver = bisect.bisect_left(datesRiver, plotdate) # index for river at this time

    figname = datesModel[itmodel].isoformat()[0:13] + '.png'
    fignamePDF = datesModel[itmodel].isoformat()[0:13] + '.pdf'

    # Set up plot
    fig = plt.figure(figsize=(10.1, 4.2))
    ax = fig.add_axes([0.04, 0.04, 0.97, 0.88])
    ax.set_frame_on(False) # kind of like it without the box
    basemap.drawcoastlines(ax=ax)
    basemap.fillcontinents('0.8', ax=ax)
    basemap.drawparallels(np.arange(28, 31), dashes=(1, 1), linewidth=0.15, labels=[1, 0, 0, 0], ax=ax)
    basemap.drawmeridians(np.arange(-97, -88), dashes=(1, 1), linewidth=0.15, labels=[0, 0, 1, 0], ax=ax)
    ax.contour(xr, yr, h, np.hstack(([10,20],np.arange(50,500,50))), colors='lightgrey', linewidths=0.5)

    # Date
    date = datesModel[itmodel].strftime('%Y %b %d')
    ax.text(0.8, 0.185, date, fontsize=14, color='0.2', transform=ax.transAxes, 
                bbox=dict(facecolor='white', edgecolor='white', boxstyle='round'))

    # Plot surface salinity
    # Note: skip ghost cells in x and y so that can properly plot grid cell boxes with pcolormesh
    salt = np.squeeze(m.variables['salt'][itmodel,-1,1:-1,1:-1])
    mappable = ax.pcolormesh(xpsi, ypsi, salt, cmap=cmap, vmin=0, vmax=36)

    # Mississippi river discharge rate
    axr = fig.add_axes([0.5, 0.05, 0.52, .11])
    axr.set_frame_on(False) # kind of like it without the box
    axr.fill_between(tRiver[itstartRiver:itriver+1], Q[itstartRiver:itriver+1], alpha=0.5, facecolor='0.4', edgecolor='0.4')
    axr.plot(tRiver[itstartRiver:itriver], Q[itstartRiver:itriver], '-', color='0.4')
    axr.plot(tRiver[itriver:itendRiver+1], Q[itriver:itendRiver+1], '-', color='0.4', alpha=0.3)
    axr.plot([tRiver[itstartRiver], tRiver[itendRiver]+13], [500, 500], '-', color='0.6', lw=0.5, alpha=0.5)
    axr.plot([tRiver[itstartRiver], tRiver[itendRiver]+13], [10000, 10000], '-', color='0.6', lw=0.5, alpha=0.5)
    axr.plot([tRiver[itstartRiver], tRiver[itendRiver]+13], [20000, 20000], '-', color='0.6', lw=0.5, alpha=0.5)
    axr.plot([tRiver[itstartRiver], tRiver[itendRiver]+13], [30000, 30000], '-', color='0.6', lw=0.5, alpha=0.5)
    # labels
    axr.text(tRiver[mticks[-1]]+38, 5, '0', fontsize=8, color='0.4', alpha=0.7)
    axr.text(tRiver[mticks[-1]]+39, 10000, '1', fontsize=8, color='0.4', alpha=0.7)
    axr.text(tRiver[mticks[-1]]+38, 20000, '2', fontsize=8, color='0.4', alpha=0.7)
    axr.text(tRiver[mticks[-1]]+38, 30000, '3', fontsize=8, color='0.4', alpha=0.7)
    axr.text(tRiver[mticks[-3]]+20, 30300, r'$\times10^4$ m$^3$s$^{-1}$', fontsize=8, color='0.4', alpha=0.7)
    axr.text(tRiver[mticks[-7]]+16, 30300, 'Mississippi discharge', fontsize=10, color='0.2')
    # no ticks
    axr.get_yaxis().set_visible(False)
    axr.get_xaxis().set_visible(False)
    # label months
    for i in xrange(len(mticks)):
        if mticknames[i]=='J':
            axr.text(tRiver[mticks[i]], 3000, mticknames[i], fontsize=8.8, color='0.2')
        else:
            axr.text(tRiver[mticks[i]], 1000, mticknames[i], fontsize=8.8, color='0.2')

    # Wind over the domain
    Uwind = w['Uwind'][:,:]
    Vwind = w['Vwind'][:,:]
    Q = ax.quiver(xr[::wdy,::wdx], yr[::wdy,::wdx], Uwind[::wdy,::wdx], Vwind[::wdy,::wdx], color='0.4', alpha=0.5)
    qk = ax.quiverkey(Q, 0.18, 0.65, 5, r'5 m$\cdot$s$^{-1}$ wind', labelcolor='0.2', fontproperties={'size': '10'})

    # Colorbar in upper left corner
    cax = fig.add_axes([0.09, 0.85, 0.35, 0.03]) #colorbar axes
    cb = fig.colorbar(mappable, cax=cax, orientation='horizontal')
    cb.set_label(r'Surface salinity [g$\cdot$kg$^{-1}$]', fontsize=14, color='0.2')
    cb.ax.tick_params(labelsize=14, length=2, color='0.2', labelcolor='0.2') 
    cb.set_ticks(ticks)
    # change colorbar tick color http://stackoverflow.com/questions/9662995/matplotlib-change-title-and-colorbar-text-and-tick-colors
    cbtick = plt.getp(cb.ax.axes, 'yticklabels')
    plt.setp(cbtick, color='0.2')

    plt.savefig(figname)
    plt.savefig(fignamePDF)
    plt.close(fig)

