from sys import argv,exit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.axisartist as AA
import matplotlib.patches as patches
import matplotlib.transforms as mtransforms
from scipy.misc import derivative

#
# Die Funktion AnimationFunc funktioniert folgenderweise:
# fig - Figur in der animiert werden soll
# run - Funktion, welche die Daten der animierten Graphen ändert 
#       Sie nutzt einen Integerwert oder ein array zum iterieren 
#       In unserem Fall haben wir st = Schritte und eine Iteration von 1:Schritte
# interval - Pause in MS zwischen Frames
# init_func ist zum "säubern" des Plottes zwischen Frames


# Einlesen der Argumente
script, f,x1,x2,y1,y2,Schritte,Startwert,sw,lr,pause = argv

# Fehler abfangen und Funktion bestimmen
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
    st = np.arange(0,Schritte,1)

    # Datengenerierung ( Das eigentliche Gradientenverfahren )
    def data_gen(f, x0, Schritte, sw, lr):

        X = [x0]
        Y = [f(x0)]
        D = [0]
        for i in range(Schritte):
            grad = derivative(f, x0, dx = 1e-6)
            d = -1*(grad/abs(grad))*sw
            if f(x0) <= f(x0+d):
                sw *= lr
                d = -1*(grad/abs(grad))*sw
            x0 += d
            X.append(x0)
            Y.append(f(x0))
            D.append(d)
            pass

        return X,Y,D
    

    # init Funktion zum Säubern des Plottes zwischen Frames
    def init():
        # Achsenlimit setzen

        ax.set_ylim(y1,y2)
        ax.set_xlim(x1,x2)
        axGrad.set_xlim(x1,x2)
        axGrad.set_ylim(-0.2,0.5)
        
        # Löschen der Einträge xdata und ydata und anschließendes initialisieren der Daten von line

        line.set_data([],[])
        lineGrad.set_data([],[])
        
        axGrad.add_patch(patch)

        return 

    # Fenster erstellen

    fig = plt.figure(figsize=(8, 8))
    ax = AA.Axes(fig, [0.1, 0.25, 0.8, 0.7])
    axGrad = AA.Axes(fig, [0.1, 0.1, 0.8, 0.05])
    fig.add_axes(ax)
    fig.add_axes(axGrad)
    axGrad.set_xticks(np.array([x1,x2]))

    
    axGrad.axis["right"].set_visible(False)
    axGrad.axis["top"].set_visible(False)
    axGrad.axis["left"].set_visible(False)
   
    # Plotten der Originalen Funktion
    xOrig = np.arange(x1,x2,0.01)
    yOrig = f(xOrig)   
    ax.plot(xOrig,yOrig)
    
    # Erzeugung des Gitters vom Koordinatensystem mit grid() und Deklaration der Daten 
    line, = ax.plot([], [], lw=2)
    lineGrad, = axGrad.plot([],[],lw=2)
    ax.grid()
    
    # Daten erzeugen für die Gradienten
    x, y, d = data_gen(f,Startwert,Schritte,sw,lr)
    
    # Pfeil erzeugen und außerhalb des Sichtbereiches setzen : y = 100
    patch = patches.Arrow(0, 100, 0, 0, color = 'orange')
   
    def run(index):
  
        # Setzt die Werte fest für die Graphen.
        line.set_ydata(y[0:index+1])
        line.set_xdata(x[0:index+1])
        
        # Der Block ist für die Pfeilanimation
        if(index > 0):
            # Skalierung des Pfeils in Kordinatenrichtungen x und y 
            trans1 = mtransforms.Affine2D().scale(1,0.35)
            # Settings des Pfeil ( LängeIn_X_Richtung,LängeIn_Y_Richtung,DickeDesPfeils, Verzerrung, PositionsVeränderung in X , "-" in Y )
            trans2 = mtransforms.Affine2D.from_values(x[index]-x[index-1],0, 0, 1,0,0)
            # Daten des Pfeils
            trans3 = mtransforms.Affine2D().translate(x[index-1],0.2)
            print(x[index-1] , x[index-1] - x[index] )
            trans = trans1 + trans2 + trans3
            patch._patch_transform = trans.frozen()
            
            axGrad.set_xticks(np.array([x1,min(x[index-1],x[index]),max(x[index-1],x[index]),x2]))
        else:
            # Pfeil außerhalb des Sichtbereiches setzen um die ersten Frames zu überbrücken
            trans1 = mtransforms.Affine2D().scale(1,0.5)
            # Settings des Pfeil ( LängeIn_X_Richtung,LängeIn_Y_Richtung,DickeDesPfeils, Verzerrung, PositionsVeränderung in X , "-" in Y )
            trans2 = mtransforms.Affine2D.from_values(1,0, 0, 1,0,0)
            # Daten des Pfeils
            trans3 = mtransforms.Affine2D().translate(1,100)
            print(x[index-1] , x[index-1] - x[index] )
            trans = trans1 + trans2 + trans3
            patch._patch_transform = trans.frozen()
          
        
        return patch,

    ani = animation.FuncAnimation(fig, run, st , blit=False, interval=pause,
                                  repeat=True, init_func=init)

    plt.show()
