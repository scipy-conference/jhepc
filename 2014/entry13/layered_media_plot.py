from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica Neue']})
rc('text', usetex=True)

from matplotlib import font_manager
ticks_font = font_manager.FontProperties(family='Bitstream Vera Sans')

import matplotlib.pyplot as plt
from clawpack.petclaw.solution import Solution
import numpy as np


nullfmt = plt.NullFormatter()
nullloc = plt.NullLocator()

def sound_speed(kx,ky,iparam):

    if iparam == 0:
        K1=1.; rho1=1.; K2=1.; rho2=1.
    elif iparam == 1:
        K1=5./8; rho1=8./5; K2=5./2; rho2=2./5;
    elif iparam == 2:
        K1=1.; rho1=1.; K2=4.; rho2=4.;
    elif iparam == 3:
        RC = 2.15; RZ = 8.;
        K1 = 1.; rho1 = 1.;
        K2 = RC/RZ; rho2 = 1./(RZ*RC);

    ph=2*rho1*rho2/(rho1+rho2);
    Kh=2*K1*K2/(K1+K2);
    pm=(rho1+rho2)/2;
    d=1

    # alpha coefficients
    a1 = (-1./24)*(K1+(-1)*K2)*(K1+K2)**(-2)*(rho1+rho2)**(-1)*(K1*rho1+(-1)*K2*rho2);
    a2 = (-1./96)*(K1+(-1)*K2)*(K1+K2)**(-2)*rho1**(-1)*rho2**(-1)*(rho1+rho2)*((-1)*K2*rho1+K1*rho2);
    a3=(-1./5760)*(K1+(-1)*K2)*(K1+K2)**(-4)*(rho1+rho2)**(-3)*(K1*rho1+(-1)*K2*rho2)*(K1**2*(3*rho1**2+(-38)*rho1*rho2+(-21)*rho2**2)+ 
      K2**2*((-21)*rho1**2+(-38)*rho1*rho2+3*rho2**2)+(-2)*K1*K2*(29*rho1**2+78*rho1*rho2+29*rho2**2));
    a4=(-1./11520)*(K1+(-1)*K2)*(K1+K2)**(-4)*rho1**(-2)*rho2**(-2)*(rho1+rho2)*(K2*rho1+(-1)*K1*rho2)**2*(3*K1*rho1+(-2)*K2*rho1+2*K1*rho2+(-3)*K2*rho2);
    a5=(1./552960)*((-1)*K1+K2)*(K1+K2)**(-5)*rho1**(-1)*rho2**(-1)*(rho1+ 
        rho2)**(-1)*(K2*rho1+(-1)*K1*rho2)*(24*K2**3*(21*rho1**2+22*rho1*rho2+(-27)*rho2**2)+K1**3*((-147)*rho1**2+1010*rho1*rho2+505*rho2**2)+ 
        K1*K2**2*(2281*rho1**2+4938*rho1*rho2+677*rho2**2)+2*K1**2*K2*(805*rho1**2+2690*rho1*rho2+897*rho2**2));
    a6=(-1./30965760)*(K1+(-1)*K2)*(K1+K2)**(-6)*rho1**(-3)*rho2**(-3)*((-1)*K2*rho1+K1*rho2)**3*(7*K2*rho1+(204*K1**2+(-383)*K1*K2+ 
        43*K2**2)*rho1**3+7*(K2+(68*K1**2+(-167)*K1*K2+35*K2**2)*rho1**2)*rho2+7*(50*K1**2+(-171)*K1*K2+49*K2**2)*rho1*rho2**2+7*( 
        10*K1**2+(-61)*K1*K2+19*K2**2)*rho2**3);

    # beta coefficients
    b1=(1./24)*(K1+K2)**(-1)*(rho1+(-1)*rho2)*(rho1+rho2)**(-2)*(K1*rho1+(-1)*K2*rho2);
    b2=(-1./96)*(K1+K2)**(-1)*rho1**(-1)*(rho1+(-1)*rho2)*rho2**(-1)*(K2*rho1+(-1)*K1*rho2);
    b3=(-1./5760)*(K1+K2)**(-3)*(rho1+(-1)*rho2)*(rho1+rho2)**(-4)*(K1*rho1+(-1)*K2*rho2)*(8*K1*K2*(6*rho1**2+17*rho1*rho2+6*rho2**2)+K2**2*( 
        21*rho1**2+48*rho1*rho2+7*rho2**2)+K1**2*(7*rho1**2+48*rho1*rho2+21*rho2**2));
    b4=(-1./46080)*(K1+K2)**(-3)*rho1**(-2)*(rho1+(-1)*rho2)*rho2**(-2)*( 
        K2*rho1+(-1)*K1*rho2)**2*((-7)*K1*rho1+3*K2*rho1+(-3)*K1*rho2+7*K2*rho2);
    b5=(1./23040)*(K1+K2)**(-3)*rho1**(-1)*(rho1+(-1)*rho2)*rho2**(-1)*(rho1+rho2)**(-2)*(K2*rho1+(-1)*K1*rho2)*((-7)*K1**2*(rho1**2+(-6)*rho1* 
        rho2+(-3)*rho2**2)+7*K2**2*(3*rho1**2+6*rho1*rho2+(-1)*rho2**2)+2*K1*K2*(27*rho1**2+82*rho1*rho2+27*rho2**2));
    b6=(-1./30965760)*(K1+K2)**(-5)*rho1**(-3)*rho2**(-3)*((-1)*rho1+rho2)*( 
        rho1+rho2)**(-1)*(K2*rho1+(-1)*K1*rho2)**3*((-7)*K2*rho1+((-71)*K1**2+173*K1*K2+34*K2**2)*rho1**3+(-7)*(K2+(19*K1**2+(-77)* 
        K1*K2+(-6)*K2**2)*rho1**2)*rho2+(-63)*K1*(K1+(-9)*K2)*rho1*rho2**2+7*K1*(K1+31*K2)*rho2**3);

    # gamma coefficients

    g1=(-1./24)*(K1+K2)**(-1)*(rho1+(-1)*rho2)*(rho1+rho2)**(-2)*(K1*rho1+(-1)*K2*rho2);
    g2=(-1./96)*(K1+K2)**(-1)*rho1**(-1)*(rho1+(-1)*rho2)*rho2**(-1)*((-1)*K2*rho1+K1*rho2);
    g3=(-1./5760)*(K1+K2)**(-3)*(rho1+(-1)*rho2)*(rho1+rho2)**(-4)*(K1*rho1+(-1)*K2*rho2)*(K1**2*(3*rho1**2+(-58)*rho1*rho2+(-21)*rho2**2)+ 
        K2**2*((-21)*rho1**2+(-58)*rho1*rho2+3*rho2**2)+(-2)*K1*K2*(19*rho1**2+78*rho1*rho2+19*rho2**2));
    g4=(-1./23040)*(K1+K2)**(-3)*rho1**(-1)*(rho1+(-1)*rho2)*rho2**(-1)*(rho1+ 
        rho2)**(-2)*(K2*rho1+(-1)*K1*rho2)*(((-37)*K1**2+24*K1*K2+21*K2**2)*rho1**2+2*rho1*(4*(9*K1**2+28*K1*K2+9*K2**2)+(-5)*K1* 
        (K1+K2)*rho1**2)*rho2+(21*K1**2+24*K1*K2+(-37)*K2**2+10*(K1+K2)**2*rho1**2)*rho2**2+(-10)*K2*(K1+K2)*rho1*rho2**3);
    g5=(-1./23040)*(K1+K2)**(-3)*rho1**(-2)*(rho1+(-1)*rho2)*rho2**(-2)*(K2*rho1+(-1)*K1*rho2)**2*((6*K1+K2)*rho1+(-1)*(K1+6*K2)*rho2);

    w2 = (ph**(-1)*pm**(-1)*(Kh*ky**2*ph+Kh*kx**2*pm)
        +d**2*ph**(-1)*pm**(-1)*(a2*Kh*kx**2*ky**2*ph+g2*Kh*kx**2*ky**2* 
        ph+a1*Kh*ky**4*ph+g1*Kh*ky**4*ph+a2*Kh*kx**4*pm+b2*Kh*kx**4*pm+a1*Kh*kx**2*ky**2*pm+b1*Kh*kx**2*ky**2*pm)
        +1*d**4*ph**(-1)*pm**(-1)*(a4*Kh*kx**4*ky**2*ph+a2*g2*Kh*kx**4*ky**2*ph+(-1)*g5*Kh*kx**4*ky**2*ph+(-1)*a5* 
        Kh*kx**2*ky**4*ph+a2*g1*Kh*kx**2*ky**4*ph+a1*g2*Kh*kx**2*ky**4*ph+(-1)*g4*Kh*kx**2*ky**4*ph+a3*Kh* 
        ky**6*ph+a1*g1*Kh*ky**6*ph+(-1)*g3*Kh*ky**6*ph+a4*Kh*kx**6*pm+a2*b2*Kh*kx**6*pm+(-1)*b4*Kh*kx**6*pm+( 
        -1)*a5*Kh*kx**4*ky**2*pm+a2*b1*Kh*kx**4*ky**2*pm+a1*b2*Kh*kx**4*ky**2*pm+(-1)*b5*Kh*kx**4*ky**2*pm+ 
        a3*Kh*kx**2*ky**4*pm+a1*b1*Kh*kx**2*ky**4*pm+(-1)*b3*Kh*kx**2*ky**4*pm))

    c = np.sqrt(w2)/np.sqrt(kx**2+ky**2)
    return c



tick_vals = np.array( (0,25,50,75,100),dtype=int )

frame = [65,65,95,65]
skip = 1

p   = np.load('p'+str(skip)+'.npy')
pc  = np.load('pc'+str(skip)+'.npy')
pz  = np.load('pz'+str(skip)+'.npy')
pcz = np.load('pcz'+str(skip)+'.npy')
xx = np.load('x'+str(skip)+'.npy')
yy = np.load('y'+str(skip)+'.npy')

yfrac = yy-np.floor(yy)
mat = yfrac>0.5

fig = plt.figure(1,figsize=(10,10))
rect = fig.patch
rect.set_facecolor('#333333')

d2 = 5./16
d1 = d2/5.
d0 = d1*2.

mainframe = [0]*4
xframe    = [0]*4
yframe    = [0]*4
dispframe = [0]*4

# Indexing: 0 = Top left
#           1 = Top right
#           2 = Bottom left
#           3 = Bottom right

mainframe[0] = [d0+d1,d0+d1+d2   ,d2,d2]
xframe[0] =    [d0+d1,d0+d1+d2+d2,d2,d1]
yframe[0] =    [d0   ,d0+d1+d2   ,d1,d2]
dispframe[0] = [d0   ,d0+d1+d2+d2,d1,d1]

mainframe[1] = [d0+d1+d2   ,d0+d1+d2,d2,d2]
xframe[1]    = [d0+d1+d2   ,d0+d1+d2+d2,d2,d1]
yframe[1]    = [d0+d1+d2+d2,d0+d1+d2,d1,d2]
dispframe[1] = [d0+d1+d2+d2,d0+d1+d2+d2,d1,d1]

mainframe[2] = [d0+d1,d0+d1,d2,d2]
xframe[2] =    [d0+d1,d0   ,d2,d1]
yframe[2] =    [d0   ,d0+d1,d1,d2]
dispframe[2] = [d0   ,d0   ,d1,d1]

mainframe[3] = [d0+d1+d2   ,d0+d1,d2,d2]
xframe[3] =    [d0+d1+d2   ,d0   ,d2,d1]
yframe[3] =    [d0+d1+d2+d2,d0+d1,d1,d2]
dispframe[3] = [d0+d1+d2+d2,d0   ,d1+0.011,d1]

on_top   = [ 1,1,-1,-1]
on_right = [-1,1,-1, 1]

axmain = []
axx = []
axy = []
axd = []

kx = np.linspace(0.01,3,500)
ky = np.linspace(0.01,3,500)
kkx,kky = np.meshgrid(kx,ky)

for i,p in enumerate([p,pc,pz,pcz]):
    # Main plot
    axmain.append(plt.axes(mainframe[i]))
    #if i>0:
        #plt.imshow(mat.T,extent=[xx.min(),xx.max(),yy.min(),yy.max()],interpolation='nearest',origin='lower',cmap='bone',alpha=0.5)
    p_scaled = (np.abs(p)**(1./3))*np.sign(p)
    #plt.pcolormesh(on_right[i]*xx,on_top[i]*yy,p_scaled,cmap='RdBu_r')
    p_scaled = p_scaled.T
    if on_right[i] == -1:
        p_scaled = np.fliplr(p_scaled)
    if on_top[i] == -1:
        p_scaled = np.flipud(p_scaled)
    plt.imshow(p_scaled, cmap='RdBu_r',extent=[xx.min(),xx.max(),yy.min(),yy.max()],interpolation='nearest',origin='lower',alpha=1.0)
    plt.clim([-0.6,0.6])
    plt.axis('equal'); plt.axis('tight')
    axmain[-1].yaxis.set_major_locator(plt.NullLocator())
    axmain[-1].xaxis.set_major_locator(plt.NullLocator())

    # x-slice
    axx.append(plt.axes(xframe[i], frameon=True, axisbg='#DDDDDD'))
    axx[-1].grid(color='w', linewidth=2, linestyle='solid',alpha=0.4)
    axx[-1].set_axisbelow(True)
    axx[-1].plot(on_right[i]*xx[:,0],p[:,0],'-r',lw=2,alpha=0.8)
    axx[-1].yaxis.set_major_locator(plt.MaxNLocator(nbins=5))
    axx[-1].set_yticklabels([])
    if on_right[i] == -1:
        axx[-1].set_xlim((-100,0)); 
    else:
        axx[-1].set_xlim((0,100)); 
    if on_top[i] == 1:
        axx[-1].set_xticklabels([]); 
    else:
        axx[-1].set_xticks(on_right[i]*tick_vals)
        axx[-1].set_xticklabels(axx[-1].get_xticks(),ticks_font,color='#EEEEEE')

    # Homogenized solution x-slice
    if i == 1:
        import scipy.io
        D = scipy.io.loadmat('c-dispersion_layered.mat')
    elif i == 2:
        D = scipy.io.loadmat('z-dispersion.mat')
    elif i == 3:
        D = scipy.io.loadmat('cz-dispersion.mat')
    if i>0:
        nt = frame[i]/0.5+1
        phom = D['U'][nt,:,:]
        mx = D['mx']
        x  = np.squeeze(D['x'])[mx/2:]-100
        xslice = np.squeeze(phom[mx/2,mx/2:])
        axx[i].plot(on_right[i]*x,xslice,'--k',lw=2)

    # y-slice
    axy.append(plt.axes(yframe[i],frameon=True, axisbg='#DDDDDD'))
    axy[-1].grid(color='w', linewidth=2, linestyle='solid',alpha=0.4)
    axy[-1].set_axisbelow(True)
    axy[-1].plot(on_right[i]*p[0,:],on_top[i]*yy[0,:],'-r',lw=2,alpha=0.8)
    axy[-1].xaxis.set_major_locator(plt.MaxNLocator(nbins=5))
    axy[-1].set_xticklabels([])
    if on_top[i] == -1:
        axy[-1].set_ylim((-100,0)); 
    else:
        axy[-1].set_ylim((0,100)); 
    if on_right[i] == -1:  # Tick labels on left
        axy[-1].set_yticks(on_top[i]*tick_vals)
        axy[-1].set_yticklabels(axy[-1].get_yticks(),ticks_font,color='#EEEEEE')
    else:
        axy[-1].set_yticklabels([])

    # Homogenized solution x-slice
    if i > 0:
        my = D['my']
        y  = np.squeeze(D['y'])[my/2:]-100
        yslice = np.squeeze(phom[my/2:,my/2])
        axy[i].plot(on_right[i]*yslice,on_top[i]*y,'--k',lw=2)


    # dispersion relation
    axd.append(plt.axes(dispframe[i],frameon=True))
    axd[-1].yaxis.set_major_locator(plt.NullLocator())
    axd[-1].xaxis.set_major_locator(plt.NullLocator())
    c = sound_speed(kkx,kky,i)
    plt.pcolormesh(on_right[i]*kkx,on_top[i]*kky,c,cmap='RdGy_r')
    if i == 0:
        plt.clim(0.9,1.1)
    elif i == 1:
        axd[-1].text(0.5,1.02,'$k_x$',color='w',fontsize=15,transform=axd[-1].transAxes,verticalalignment='bottom',horizontalalignment='center')
        axd[-1].text(1.08,0.5,'$k_y$',color='w',fontsize=15,transform=axd[-1].transAxes,verticalalignment='center',horizontalalignment='left')
    elif i == 3:
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(axd[-1])
        cax = divider.append_axes("right", size="10%", pad=0.05)
        
        cbar = plt.colorbar(cax=cax, drawedges=False)
        cbar.outline.set_linewidth(0.5)
        cbar.outline.set_color('white')
        cbar.ax.set_yticklabels([])
        #cbar.set_label('sound speed',color='w',fontsize=10)



# Top left
axmain[0].text(0.02,0.98,'Homogeneous\n medium',transform=axmain[0].transAxes,verticalalignment='top')
axx[0].set_ylim((-0.38,0.38))
axy[0].set_xlim((-0.38,0.38))


# Top right
axmain[1].text(0.98,0.98,'Sound speed\n mismatched',horizontalalignment='right',transform=axmain[1].transAxes,verticalalignment='top')
axx[1].set_ylim((-0.27,0.27))
axy[1].set_xlim((-0.3,0.3))


#Bottom left
axmain[2].text(0.02,0.02,'Impedance\n mismatched',transform=axmain[2].transAxes)
axx[2].set_ylim((-0.35,0.35))
axy[2].set_xlim((-0.2,0.2))
axx[2].xaxis.set_label_coords(1, -0.5)

# Bottom right
axmain[3].text(0.98,0.02,'Both\n mismatched',horizontalalignment='right',transform=axmain[3].transAxes)
axx[3].set_ylim((-0.27,0.27))
axy[3].set_xlim((-0.21,0.21))


#Inset
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

axins = zoomed_inset_axes(axmain[2],6,loc=1)


#skip = 1
#K = np.loadtxt('K.txt')
#rho = np.loadtxt('rho.txt')[::skip,::skip]
#eps = np.loadtxt('sw4_q0.txt')[::skip,::skip]
#sigma = np.exp(K*eps[-1])-1
#xmom = np.loadtxt('sw4_q1.txt')[::skip,::skip]
#ymom = np.loadtxt('sw4_q2.txt')[::skip,::skip]
#u = xmom/rho
#v = ymom/rho
#x = np.linspace(0,150,9600)
#y = np.linspace(0,1,128)
#X,Y = np.meshgrid(x,y,indexing='ij')
#x_skip = 8
#y_skip = 4
#plt.pcolormesh(x,y,sigma.T,cmap='RdBu_r')
#plt.quiver(X[::x_skip,::y_skip],Y[::x_skip,::y_skip],u[::x_skip,::y_skip],v[::x_skip,::y_skip],pivot='center',units='width',headaxislength=5,scale=7)
#axins.set_xlim(155*1./2,157.5*1./2)
#axins.set_ylim(0,1)

yfrac = yy-np.floor(yy)
mat = yfrac>0.5

axins.imshow(mat.T,vmin=-0.5, vmax=1.5, extent=[55,60,55,60],interpolation='nearest',origin='lower',cmap='binary',alpha=0.8)
#plt.pcolormesh(xx,yy,mat,cmap='bone')
#plt.clim([-1.5,1.5])
#axins.set_xlim(-10,-20)
#axins.set_ylim(-10,-20)
#axins.set_xlim(80,90)
#axins.set_ylim(80,90)
axins.xaxis.set_major_locator(nullloc)
axins.yaxis.set_major_locator(nullloc)
mark_inset(axmain[2],axins,2,4,fc='none',ec='0.5')

plt.suptitle('Acoustic wave propagation in layered periodic media',fontsize=25,color='#EEEEEE')
plt.figtext(0.5,0.05,'Units scaled to medium period', fontsize=15, horizontalalignment='center',color='#EEEEEE')
plt.figtext(0.5,0.075,'$x$', fontsize=25, horizontalalignment='center',color='#EEEEEE')
plt.figtext(0.05,0.5,'$y$', fontsize=25, verticalalignment='center',color='#EEEEEE')

plt.savefig('_dispersion.png',dpi=100, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
