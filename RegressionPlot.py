# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 15:49:13 2018

@author: Pascal
"""
# Jan Start
from sys import argv, exit
import numpy as np

script , lv, x, y, iterations, sw = argv

iterations = int(iterations)
sw = float(sw)

# Zufällig generierte x-Werte
if (x == "random"):
    x = np.random.rand(100, 1)
    pass
else:
    x = np.fromstring(x, dtype=float, sep=',')
    pass

if (y == "random"):
    y = 3*x+5+np.random.rand(100, 1)
    pass
else:
    y = np.fromstring(y, dtype=float, sep=',')
    pass

lv = np.fromstring(lv, dtype=float, sep=',').reshape((2,1))
# Jan Ende

import numpy as np
import matplotlib.pyplot as plt

# Berechnung der Kosten
# Eingabe: Lösungsvektor, x-Werte, y-Werte 
# Rückgabe: Kosten
def Kosten(lv, x, y):
    # Generiert eine Matrix mit 1 in 1. Zeile, x-Werte in 2. Zeile
    n = len(y)
    ones = np.ones((len(x), 1))
    X = np.hstack((ones, x))
    
    # Berechnete Lösung mit unseren Startwerten
    guess = np.dot(X, lv)
    
    # Berechnung der Kosten über die Summe der quadrierten Differenzen
    kosten = 1/n*sum(np.square(guess-y))
    return kosten

# Regressionsfunktion
# Eingabe: Lösungsvektor, x, y, Anzahl der Durchläufe, Schrittweite
# Rückgabe: Lösungsvektor, Verlauf des LV, Verlauf der Kosten
def Regression(lv, x, y, iterations=1000, sw=0.01):
    # Generiert eine Matrix mit 1 in 1. Zeile, x-Werte in 2. Zeile
    ones = np.ones((len(x), 1))
    X = np.hstack((ones, x))
    
    # Arrays für Verläufe mit 0 initialisieren
    # werden später mit Werten befüllt
    kosten_verlauf = np.zeros(iterations)
    lv_verlauf = np.zeros((iterations, 2))
    
    # für die Anzahl der Iterationen werden hier die Lösungsvektoren berechnen
    for i in range(iterations):
        
        n = len(y)
        # Berechnung Lösung mit Startwerten
        guess = np.dot(X, lv)
        # Verbesserung des Lösungsvektors durch Gradientenabstieg
        lv = lv - 1/n*sw*np.dot(X.T, (guess-y))
        # Hinzufügen des neuen Lösungsvektors und der Kosten zum Verlauf
        lv_verlauf[i, :] = lv.T
        kosten_verlauf[i] = Kosten(lv, x, y)
        
    return lv, lv_verlauf, kosten_verlauf

# Funktion zum Plotten der Kostenfunktion
# Eingabe: Lösung, Verlauf der Lösungsvektoren, x-Werte, y-Werte
def PlotKosten (loesung, verlauf, x, y):
    
    # Größe des zu plottenden Bereiches festlegen (lv0 = x-Achse, lv1 = y-Achse)
    # Num_samp ist die Anzahl der x- und y-Werte
    lv0 = np.arange(loesung[0]-1, loesung[0]+1, 2/num_samp)
    lv1 = np.arange(loesung[1]-1, loesung[1]+1, 2/num_samp)
    
    # Kostenmatrix der Größe x*y initialisieren
    # wird in folgender Schleife befüllt 
    cost_grid = np.zeros((num_samp, num_samp))
    
    # Jeder Eintrag der Kostenmatrix wird berechnet
    for i in range(len(cost_grid)):
        for j in range(len(cost_grid)):
            # Eintrag[i][j] = Kosten aus x-Achsenwert[i] und y-Achsenwert[j]
            cost_grid[i][j] = Kosten(np.array([[lv0[i]], [lv1[j]]]), x, y)
            
    X, Y = np.meshgrid(lv0, lv1)
    
    # Beginn des Plots
    fig0, ax0 = plt.subplots()
    # Contourplot zeichnet Konturlinien 
    cost_plot = ax0.contour(X, Y, cost_grid, 25)
    # Anzeigen der Kosten zur jeweiligen Konturlinie
    ax0.clabel(cost_plot)
    
    # Punkte zur Position des Lösungsvektors nach 1/3, 1/2 und aller Iterationen
    ax0.scatter(verlauf[num_it//3][0], verlauf[num_it//3][1],s=[20,20], color=['k','w'])
    ax0.scatter(verlauf[num_it//2][0], verlauf[num_it//2][1],s=[20,20], color=['k','w'])
    ax0.scatter(loesung[0], loesung[1],s=[20,20], color=['k','w'])
    
    # Beschriftung der x- und y-Achse
    ax0.set_xlabel("$l_0$")
    ax0.set_ylabel("$l_1$")
    return cost_plot


# Beginn des Beispiel
# Festlegen der Iterationen und der Anzahl der x- und y-Werte
num_it = iterations
num_samp = 100
'''
# Zufällig generierte x-Werte
x = np.random.rand(num_samp, 1)
y = 3*x+5+np.random.rand(num_samp, 1)
# Startwerte des Lösungsvektor (0,0)
lv = np.array([[0], [0]])
'''
# Regressionsfunktion
loesung, verlauf, kosten = Regression(lv, x, y, num_it)

print(loesung, "\n")

# Plot der Punkte
fig1, ax1 = plt.subplots()
ax1.plot(x,y,"k.")
ax1.set_xlabel("x")
ax1.set_ylabel("y")

# Kosten in Abhängigkeit der Iterationen
fig2, ax2 = plt.subplots()
ax2.plot(np.arange(0, num_it, 1), kosten, "k.")
ax2.set_xlabel("Iterationen")
ax2.set_ylabel("Kosten")

# Kostenfunktion
PlotKosten(loesung, verlauf, x, y)
plt.show()
