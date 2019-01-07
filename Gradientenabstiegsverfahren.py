from sys import argv,exit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.misc import derivative

script, f,x1,x2,y1,y2,Schritte,Startwert,sw,lr,pause = argv


if(f=="x**4-x**3"):
    def f(x):
        return x**4-x**3
    pass
elif(f=="x**4-x"):
    def f(x):
        return x**4 - x
    pass
elif(f=="2*x**2"):
    def f(x):
        return 2*x**2
    pass
elif(f=="sin(1/10*x)*x**2"):
    def f(x):
        return x**2 * np.sin(1/10*x) 
    pass
elif(f=="x**7-x**6-x**5+x**2"):
    def f(x):
        return x**7-x**6-x**5+x**2
    pass
else:
    print("Falsche Funktion! Siehe Dokumentation!")
    exit()
    pass
   
        
x1=float(x1)
x2=float(x2)
y1=float(y1)
y2=float(y2)
Schritte=int(Schritte)
Startwert=float(Startwert)
lr=float(lr)
sw=float(sw)
pause=int(pause)

if(True):
    ##### %matplotlib notebook


    ##############################################
    st = np.arange(0,Schritte-1,1)


    

    def data_gen(f, x0, Schritte, sw, lr):

        X = [x0]
        Y = [f(x0)]
        for i in range(Schritte):
            grad = derivative(f, x0, dx = 1e-6)
            d = -1*(grad/abs(grad))*sw
            if f(x0) <= f(x0+d):
                sw *= lr
                d = -1*(grad/abs(grad))*sw
            x0 += d
            X.append(x0)
            Y.append(f(x0))
            pass

        return X,Y
    


    def init():
        # Achsenlimit setzen
        ax.set_ylim(y1,y2)
        ax.set_xlim(x1,x2)

        # Löschen der Einträge xdata und ydata und anschließendes initialisieren der Daten von line
        del xdata[:]
        del ydata[:]
        line.set_data(xdata, ydata)
        return line,

    # Fenster erstellen
    fig, ax = plt.subplots()

    # Plotten der Originalen Funktion
    xOrig = np.arange(x1,x2,0.01)
    yOrig = f(xOrig)
    ax.plot(xOrig,yOrig)

    # Erzeugung des Gitters vom Koordinatensystem mit grid() und Deklaration der Daten 
    line, = ax.plot([], [], lw=2)
    ax.grid()
    xdata, ydata = [], []

    # Daten erzeugen für die Gradienten
    x, y = data_gen(f,Startwert,Schritte,sw,lr)

    def run(index):
        # update the data
        line.set_ydata(y[0:index])
        line.set_xdata(x[0:index])
        return

    ani = animation.FuncAnimation(fig, run, st , blit=False, interval=pause,
                                  repeat=True, init_func=init)

    plt.show()

