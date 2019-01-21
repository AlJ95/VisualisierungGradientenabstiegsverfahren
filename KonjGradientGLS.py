# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 13:34:56 2019

@author: Pascal

edit @Jan with '#Jan Start ... Ende'
"""

import numpy as np

# @Jan Start
from sys import argv,exit

# String to Float / Integer Umwandlung
# argv Argumente, werden mit %run als String übergeben
script, A ,x0, b, epsilon, pause, konj, xyPlot = argv
A = np.fromstring(A, dtype=float, sep=',')

# Abfrage ob die Matrix Form nxn besitzt ( von 2x2 bis zu 100x100 )
for i in np.arange(2,101,1):
    if(i*i == len(A)):
        break
        pass
    else:
        if(i!=100):
            continue
            pass
        else:
            exit()
            pass
        pass
    pass

dim = int(np.sqrt(len(A)))
A = np.reshape(A,(dim,dim))

# Ist die Matrix symmetrisch?
for i in range(0, dim):
    for j in range(0, dim):
        if A[i,j] != A[j][i]:
            print("Matrix ist nicht symmetrisch")
            exit()
            pass
        pass
    pass

# Ist die Matrix pos. definit?
if(False == np.all(np.linalg.eigvals(A) > 0)):
    print("Matrix ist nicht positiv definit!")
    exit()
    pass
       
# String to Float / Integer Umwandlung
# argv Argumente, werden mit %run als String übergeben
x0 = np.fromstring(x0, dtype=float, sep=',')
b = np.fromstring(b, dtype=float, sep=',')
epsilon = float(epsilon)
pause = int(pause)
if(konj == "True"):
    konj = True
    pass
else:
    konj = False
    pass
if(xyPlot == "True"):
    xyPlot = True
    pass
else:
    xyPlot = False
    pass

# Fehlerabfangen bei unpassenden Dimensionen
if(A.shape[0]!=len(x0)):
    print("Matrix und Startvektor sind nicht multiplizierbar. Überprüfe die Dimensionen!")
    exit()
    pass
if(len(x0)!=len(b)):
    print("Die Vektoren x0 und b müssen die gleiche Dimension haben.")
    exit()
    pass

# @Jan Ende


# Konjugiertes Gradientenverfahren zum Lösen von Gleichungssystemen Ax = b
# Eingabe: symm. pos. def. Matrix A, Startvektor x0, b, Toleranz Epsilon
# Ausgabe: Array X, welches alle angenommenen Lösungsvektoren beinhaltet

def CG(A, x0, b, epsilon):
    # Berechnung vom ersten Residuum r0, Schrittrichtung d
    # Speichern des Startvektors in Array X
    r0 = b - np.dot(A, x0)
    d = r0
    r1 = r0
    X = np.array(x0)
    #@Jan Start
    count = 0      # Counter einfügen um notfalls abzubrechen
    #@Jan Ende
    # Solange Norm des Residuum größer als Toleranz ist:
    while np.linalg.norm(r1) > epsilon:
        count += 1
        # Matrix-Vektor Produkt zwischenspeichern
        z = np.dot(A, d)
        # Berechne neues x mit Schrittweite Alpha und Schrittrichtung d
        alpha = np.dot(r0.T, r0)/ np.dot(d.T, z)
        x0 += alpha*d
        # Berechnung des neuen Residuums
        r1 = r0 - alpha*z
        # Korrigieren der Schrittrichtung d mit Hilfe von neuem Residuum
        beta = np.dot(r1.T, r1)/ np.dot(r0.T, r0)
        d = r1 + beta*d
        
        # Aktualisierung des alten Residuums für weiteren Schleifendurchgang
        r0 = r1
        # Anfügen des neuen Lösungsvektors an Array X
        X = np.vstack((X, x0))
        if(count == 10000):
            exit()
            pass   
    return X



# Gradientenverfahren zum Lösen von Gleichungssystemen Ax = b
# Eingabe: symm. pos. def. Matrix A, Startvektor x0, b, Toleranz Epsilon
# Ausgabe: Array X, welches alle angenommenen Lösungsvektoren beinhaltet

def GradientGLS (A, x0, b, epsilon):
    # Berechnung Schrittrichtung d
    # Speichern des Startvektors in Array X
    d = b - np.dot(A, x0)
    X = np.array(x0)
    
    #@Jan Start
    count = 0      # Counter einfügen um notfalls abzubrechen
    #@Jan Ende
    # Solange d kleiner der Toleranz ist: 
    while np.linalg.norm(d) > epsilon:
        count += 1
        # Berechnung der Schrittweite Alpha
        alpha = np.dot(d.T, d)/ np.dot(d.T, np.dot(A, d))
        # Schritt wird ausgeführt in Richtung d
        x0 += alpha*d
        
        # neues d für nächsten Schleifendurchgang berechnen
        d = b - np.dot(A, x0)
        # neuer Lösungsvektor zu Array X hinzufügen
        X = np.vstack((X, x0))
        if(count == 10000):
            exit()
            pass   
    return X

# @Jan Start
# Funktionsaufruf für Konjugiert oder nicht konjugierte Verfahren
if(konj):
    x=CG(A, x0, b, epsilon)
    pass
else:
    x=GradientGLS (A, x0 , b ,epsilon)
    pass
# @Jan Ende

'''
A = [[3, 2], [2, 6]]

x0 = [1, 0]
b = [2, -8]

B = [[6, 1, 2], [1, 1, -2], [2, -2, 8]]
y0 = [1, 0, 0]
c = [-2, 1, 2]

'''
# @Jan Start
# If Abfrage damit nur geplottet wird, wenn die Matrix 2x2 groß ist.
if(A.shape[0]==2):
    
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    import matplotlib.animation as animation

    # Aus dem Gradientenverfahren die x Werte splitten in 2 extra Variabeln
    # Sie erzeugen den Graphen, der den steilsten Abstieg sucht
    y = x[:,1]
    x = x[:,0]
    z = np.array([])

    # z Variable berechnen (Residuum)
    for i in range(len(x)):
        z = np.append(z,np.linalg.norm(b-np.dot(A,np.transpose(np.array([x[i],y[i]])))+0.001))
        pass


    # initialisieren des Plots
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # X,Y,Z sind die Werte zu dem Oberflächen Plots 
    X = np.arange(min(x),max(x),0.01)
    Y = np.arange(min(y),max(y),0.01)
    Z = np.array([])
    for j in Y:
        z1 = np.array([])
        for i in X:
            z1 = np.append(z1,np.linalg.norm(b-np.dot(A,np.transpose(np.array([i,j])))))
            pass
        if(Z.size == 0):
            Z = z1
            pass
        else:
            Z = np.vstack((Z,z1))
            pass
        del z1
        pass
    
    # meshgrid erzeugt eine Oberfläche von 2 Dimensionen
    # sodass jeder X Wert mit jeden Y Wert zu einem Z Wert verrechnet werden kann.
    X,Y = np.meshgrid(X,Y)
    
    # Oberfläche plotten
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Achsen Einstellungen Min(), Max(), Z-Achsen Einteilung und Größe
    ax.set_zlim(Z.min(), Z.max())
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Farbskala zur besseren Übersicht der Z Werte
    fig.colorbar(surf, shrink=0.5, aspect=5)
    
    # Größe des Plotfensters einstellen
    plt.rcParams["figure.figsize"] = (11, 9) # (w, h)

    # run(index) wird dazu benutzt den Plot oder die Daten zu aktualisieren. 
    # Jeden Frame wird es mit index(Frame Nummer beginnend von 0) aufgerufen
    def run(index):
        surf2 = ax.plot(x[0:index+1],y[0:index+1], z[0:index+1],"r-", label='parametrix curve', 
                       linewidth=2, )
        if(xyPlot):
            line = ax.plot(x[0:index+1], y[0:index+1], Z.min() , "black" , label= 'parametrix curve' )
            pass
        
        return

    # Die Animationsfunktion mit Parameter 
    # fig = Plot Fenster (figure)
    # run = Funktion, welche bei jedem Frame aufgerufen werden soll
    # len(x) = range(len(x)) -> Argument "index" welches jeder Frame an "run" übergibt
    # intervall = pause  -> Zeit zwischen 2 Frames in MS
    # repeat -> Soll die Animation wiederholt werden?
    ani = animation.FuncAnimation(fig, run, len(x) , blit=False, interval=pause,repeat=False)
    plt.show()
    pass

# Falls die Matrix größer als 2x2 ist, wird nur noch geprinted.
else:
    print("Alle Zwischenergebnisse:")
    print("X = ")
    print(x)
    pass
    
# @Jan Ende