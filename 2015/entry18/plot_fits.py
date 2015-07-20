import numpy as np
import matplotlib.pyplot as plt


plt.rcParams['axes.linewidth']=2
plt.rc('xtick.major', size=7, pad=7)
plt.rc('xtick.minor', size=4, pad=5)
plt.rc('ytick.major', size=7, pad=7)
plt.rc('ytick.minor', size=4, pad=5)

fig = plt.figure(figsize=(18,13))
plt.gcf().subplots_adjust(bottom=0.15, wspace=0.15, hspace=0.3, top=0.95, right=0.95, left=0.1)




yr = 3.1557926e7
G = 6.673e-8
Msun = 1.989e33
p = np.pi



datvals = np.loadtxt('data5.txt', usecols=[0,1,2,3,4])

tplot = np.linspace(2010, 2015, 200)

time    = datvals[:,0]
septrue = datvals[:,1]
seperr  = datvals[:,2]
postrue = datvals[:,3]
poserr  = datvals[:,4]

Xtrue   = septrue*np.cos(postrue*p/180)
Ytrue   = septrue*np.sin(postrue*p/180)
Xerr    = np.sqrt((seperr*np.cos(postrue*p/180))**2 + 
                  (septrue*np.sin(postrue*p/180)*poserr*p/180)**2)
Yerr    = np.sqrt((seperr*np.sin(postrue*p/180))**2 + 
                  (septrue*np.cos(postrue*p/180)*poserr*p/180)**2)


def calculate_E(e,M):
  

    E = np.zeros(len(M))
    prec = 1e-5
    right_side = M + e*np.sin(E)
    iv = np.where(np.abs(E - right_side) > prec)[0]
 
    E[iv] = M[iv] + np.sin(M[iv])*e + 0.5*e*e*np.sin(2.0*M[iv])
 
    En = E + 0.0

    F = E - e*np.sin(E) - M
    while len(iv) > 0:
       
        E = E - F/(1.0-(e*np.cos(E)))
        F = E - e*np.sin(E) - M
        
        iv = np.where(np.abs(F) > prec)[0]

   
    E = np.mod(E, 2*p)
    return E

def calcrv(arrvals, times, flag):
    
    ecos, esin, tp, period, totmass, inc, Comega, dist = arrvals

    
    ecc = ecos**2 + esin**2
    w   = np.arctan2(esin, ecos)
    
    M = np.mod(2*p*(times-tp)/period, 2*p)

    E = calculate_E(ecc, M)
    tanf2 = (np.sqrt((1+ecc)/(1-ecc))*np.tan(E/2))
    f = 2*np.arctan(tanf2)
    

    
    K12 = (2*p*G/period/yr)**(1./3) * (totmass*Msun)**(1./3) * np.sin(inc) / np.sqrt(1-ecc**2) / 1e5
    
    RV12 = K12 * (np.cos(f+w) + ecc*np.cos(w))
    
    if flag == 1:
        print K12
        plt.plot(times, RV12)
    
    
    
    return RV12
    
    
    

def calcorbit(arrvals, times, flag):

 
    ecos, esin, tp, period, totmass, inc, Comega, dist = arrvals
    

    ecc = ecos**2 + esin**2
    w   = np.arctan2(esin, ecos)

    sW = np.sin(Comega)
    cW = np.cos(Comega)

    M = np.mod(2*p*(times-tp)/period, 2*p)

    E = calculate_E(ecc, M)
    tanf2 = (np.sqrt((1+ecc)/(1-ecc))*np.tan(E/2))
    f = 2*np.arctan(tanf2)


    a = (period**2*(totmass))**(1./3) # a in AU
 
    r = a*(1-ecc**2)/(1+ecc*np.cos(f)) # r in AU at obs. epochs

 
    X = r*(cW*np.cos(w + f) -(sW*np.sin(w+f)*np.cos(inc)))/dist # in arcsec
  
    Y = r*(sW*np.cos(w + f) +(cW*np.sin(w+f)*np.cos(inc)))/dist # in arcsec

    angsep = (Y**2 + X**2)**.5 * 1000.0
    posang = np.arctan2(Y,X)*180/p

    X *= 1000.0
    Y *= 1000.0
  
    if flag == 1:
        print 'angular separation: ' + str(angsep)
        print 'position angle: ' +str(posang)
 
   
    return [-1*Y, X]


if __name__ == '__main__':

    a  = np.load('rvchains_OUT_a.npy')
    b  = np.load('rvchains_OUT_b.npy')



    ecc = a[:,0]**2 + a[:,1]**2



    ax = plt.subplot(211)


    g = np.random.randint(0, len(a[:,0]), 200)


    for i in g:
        xval, yval = calcorbit(a[i], tplot, 0)
        plt.plot(xval, yval, 'b', linewidth=1, alpha=0.03)


    for i in g:
        xval, yval = calcorbit(b[i], tplot, 0)
        plt.plot(xval, yval, 'r', linewidth=1, alpha=0.03)

    for i in g:
        x2014, y2014 = calcorbit(a[i], np.array([2015.50]), 0)
        plt.plot(x2014, y2014, 'w.', markersize=7, markeredgecolor='k')

    arrowx = np.arange(-45, -10, 1)
    arrowy = 0.01*(arrowx)**2 - 80

    slope = arrowy[-1] - arrowy[-2]

    plt.plot(arrowx+20, arrowy, 'silver', linewidth=10)
    plt.arrow(arrowx[-1]+20, arrowy[-1], 0.01, 0.0025*slope, color='silver', linewidth=10, head_width=5, head_length=4)




    plt.errorbar(-1*Ytrue, Xtrue,
                         xerr=Yerr, yerr=Xerr, fmt='k.', markersize=8,
                  markeredgewidth=1, linewidth=1, markeredgecolor='k')

    plt.plot(0,0, 'ko', markersize=12, linewidth=9)

    plt.xlabel('$\Delta$RA (mas)', fontsize=24)
    plt.ylabel('$\Delta$Dec (mas)', fontsize=24)

    plt.xticks(fontsize=20)
    plt.yticks(np.arange(-120, 60.01, 30), fontsize=20)

    Xcorr = np.array([-20, -20, 10, -14])
    Ycorr = np.array([0, -3, 10, 3])

    for i in xrange(len(datvals)):  # plot error bars!
        plt.text(-1*(Ytrue[i]+Ycorr[i]), Xtrue[i]+Xcorr[i], str(time[i])[0:7],
                 fontsize=18)

    plt.text(-56, -110, 'GJ4185Aab', fontsize=20)
    plt.text(60, 0, '2015.85', fontsize=18)

    plt.xlim(-60, 100)
    ax.get_yaxis().set_label_coords(-0.05,0.5)
    ax.get_xaxis().set_label_coords(0.5, -0.12)

    ax = plt.subplot(224)

    plt.hist(a[:,3], np.arange(2.1, 2.35, 0.005), normed=False, alpha=0.3, color='b', weights=np.ones(len(a))*3)
    plt.hist(b[:,3], np.arange(2.1, 2.35, 0.005), normed=False, alpha=0.3, color='r')
    plt.axis([2.1, 2.35, 0, 2000])
    plt.errorbar(np.mean(a[:,3]), 1900, xerr=np.std(a[:,3]), fmt='b.', markersize=12, linewidth=2.5, capsize=2.5)
    plt.errorbar(np.mean(b[:,3]), 1775, xerr=np.std(b[:,3]), fmt='r.', markersize=12, linewidth=2.5, capsize=2.5)

    plt.text(2.270, 1875, 'Three Observations', color='b', fontsize=16)
    plt.text(2.273, 1750, 'Four Observations', color='r', fontsize=16)

    plt.xlabel('Period (years)', fontsize=24)
    plt.ylabel('Likelihood', fontsize=24)

    ax.get_yaxis().set_label_coords(-0.05,0.5)
    plt.xticks(fontsize=20)
    plt.yticks([], [], fontsize=20)

    ax = plt.subplot(223)

    t_rvs = np.linspace(2015, 2020, 200)

    plt.plot(t_rvs, np.zeros(len(t_rvs)), 'k--', linewidth=1)
    plt.plot(t_rvs, np.zeros(len(t_rvs))-15, 'k--', linewidth=1)

    for i in g:
        RV1 = calcrv(a[i], t_rvs, 0)
        plt.plot(t_rvs, RV1, 'b', linewidth=1, alpha=0.1) 

    for i in g:
        RV2 = calcrv(b[i], t_rvs, 0) - 15.0
        plt.plot(t_rvs, RV2, 'r', linewidth=1, alpha=0.1) 
        
    plt.plot([2015.25], [5.0], 'k.', markersize=6)
    plt.errorbar([2015.25], [5.0], yerr =[1.0], markersize=15, color='k')

    plt.xticks(np.arange(2015, 2020.01, 1), ['2015', '2016', '2017', '2018', '2019', '2020'], fontsize=20)
    plt.yticks(fontsize=20)

    plt.xlabel('Year', fontsize=24)
    plt.ylabel('Radial Velocity + Offset (km/s)', fontsize=24)



    ax.get_yaxis().set_label_coords(-0.05*1/(0.85/2),0.5)
    plt.xlim(2015, 2020)
    plt.ylim(-20, 15)
    #plt.show()
    plt.savefig('figure1.pdf')