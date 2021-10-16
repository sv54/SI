import sys, pygame
import tkinter
from casilla import *
from mapa import *
from pygame.locals import *


MARGEN=5
MARGEN_INFERIOR=60
TAM=30
NEGRO=(0,0,0)
BLANCO=(255, 255,255)
VERDE=(0, 255,0)
ROJO=(255, 0, 0)
AZUL=(0, 0, 255)
AMARILLO=(255, 255, 0)

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

# Devuelve si una casilla del mapa se puede seleccionar como destino
def bueno(mapi, pos):
    res= False
    
    if mapi.getCelda(pos.getFila(),pos.getCol())==0:
       res=True
    
    return res
    
# Devuelve si una posición de la ventana corresponde al mapa
def esMapa(mapi, posicion):
    res=False     
    
    if posicion[0] > MARGEN and posicion[0] < mapi.getAncho()*(TAM+MARGEN)+MARGEN and \
    posicion[1] > MARGEN and posicion[1] < mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True       
    
    return res
    
#PDevuelve si se ha pulsado el botón. Posición del botón: 20, mapa.getAlto()*(TAM+MARGEN)+MARGEN+10]
def pulsaBoton(mapi, posicion):
    res=False
    
    if posicion[0] > 20 and posicion[0] < 70 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True
    
    return res
    
    
# Construye la matriz para guardar el camino
def inic(mapi):    
    cam=[]
    for i in range(mapi.alto):        
        cam.append([])
        for j in range(mapi.ancho):            
            cam[i].append('.')
    
    return cam

        
# función principal
def main():
    
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    file=tkinter.filedialog.askopenfilename() #abre el explorador de archivos    
    
    pygame.init()
    destino=Casilla(-1,-1)
    
    reloj=pygame.time.Clock()    
    
    if not file:     #si no se elige un fichero coge el mapa por defecto   
        file='mapa.txt'
    
    mapi=Mapa(file)
    origen=mapi.getOrigen()
    #print(origen.getFila(), origen.getCol())
    print(mapi.getCelda(origen.getFila()+1,origen.getCol()))
    camino=inic(mapi)   
    
    anchoVentana=mapi.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1")
    
    boton=pygame.image.load("boton.png").convert()
    boton=pygame.transform.scale(boton,[50, 30])
    
    personaje=pygame.image.load("pig.png").convert()
    personaje=pygame.transform.scale(personaje,[TAM, TAM])   
    
    coste=-1
    running= True
    primeraVez=True
    
    while running:        
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                running=False               
                
            if event.type==pygame.MOUSEBUTTONDOWN:                
                #obtener posición y calcular coordenadas matriciales
                pos=pygame.mouse.get_pos()                
                colDestino=pos[0]//(TAM+MARGEN)
                filDestino=pos[1]//(TAM+MARGEN)
                casi=Casilla(filDestino, colDestino)
                if pulsaBoton(mapi, pos): #reinicializar                    
                    origen=mapi.getOrigen()
                    destino=Casilla(-1,-1)                    
                    camino=inic(mapi)
                    coste=-1
                    primeraVez=True
                elif esMapa(mapi, pos):
                    if bueno(mapi, casi):
                        if not primeraVez: #la primera vez el origen está en el mapa
                            origen=destino                            
                        else:                          
                            mapi.setCelda(int(origen.getFila()), int(origen.getCol()), 0) #se marca como libre la celda origen
                        destino=casi                        
                        camino=inic(mapi)
                        # llamar al A*
                        #coste=aEstrella(mapi, origen, destino, camino)      
                        if coste==-1:
                            tkinter.messagebox.showwarning(title='Error', message='No existe un camino entre origen y destino')                     
                        else:
                            primeraVez=False  # hay un camino y el destino será el origen para el próximo movimiento
                    else: # se ha hecho click en una celda roja                
                        tkinter.messagebox.showwarning(title='Error', message='Esa casilla no es valida')
                
          
        #código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        #pinta mapa
        for fil in range(mapi.getAlto()):
            for col in range(mapi.getAncho()):
                if mapi.getCelda(fil, col)==2 and not primeraVez: #para que no quede negro el origen inicial
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)                    
                if mapi.getCelda(fil,col)==0:
                    if camino[fil][col]=='.':
                        pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    else:
                        pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
                elif mapi.getCelda(fil,col)==1:
                    pygame.draw.rect(screen, ROJO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
        #pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol()+MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])    
        #pinta destino
        pygame.draw.rect(screen, VERDE, [(TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN, TAM, TAM], 0)
        #pinta boton
        screen.blit(boton, [20, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        #pinta coste
        if coste!=-1:            
            fuente= pygame.font.Font(None, 30)
            texto= fuente.render("Coste "+str(coste), True, AMARILLO)            
            screen.blit(texto, [anchoVentana-120, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])            
            
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)        
       
        
    pygame.quit()
    
#---------------------------------------------------------------------
if __name__=="__main__":
    main()
    
    
def aEstrella(mapi, origen, destino, camino):
    nodo=Nodo(origen.getCol(), origen.getFila())
    nodoDestino=Nodo(destino.getCol(), destino.getFila())
    listaCerrada=[]
    listaAbierta=[nodo]
    
    while not listaAbierta:
        j=0
        if len(listaAbierta)>1:
            for i in range(len(listaAbierta)):
                if listaAbierta[i].getF()<nodo.getF():
                    nodo=listaAbierta[i]
                    j=i
        
        
        if nodo==nodoDestino: #n==destino: #reconstruir camino
            return 1
        else:
            listaAbierta.pop(j)
            listaCerrada.append(nodo)
            #print(mapi.getCelda(origen.getFila()+1,origen.getCol()))
            hijos=nodo.getHijos(mapi)
            #eliminamos hijos que apuntan a una pared o origen
            i=0
            while i<len(hijos):
                celda=mapi.getCelda(hijos[i].getY(),hijos[i].getX())
                if celda==1 or celda == 2:
                    hijos.pop(i)
                i=i+1
            
            for k in hijos:
                padre=k.getPadre()
                coste=k.getCoste()
                if !(k is in listaAbierta):
                    g=padre.getG()+coste
                    k.setG(g)
                    listaAbierta.append(k)
                else:
                    if k.getG()<padre.getG()+coste:
                        k.setPadre(padre)
                        k.setG(padre.getG()+coste)
                
            #Comprobar si los hijos estan en la lista cerrada
    return -1 #coste
    
    
class Nodo():
    def __init__(self,x,y,h=0,padre=None):
        self.x=x
        self.y=y
        self.h=h
        self.padre=padre
        
    def getHijos(self, mapi):
        x=self.x
        y=self.y
        lista=[]
        nodo=Nodo(x-1,y-1,self)
        lista.append(nodo)
        nodo=Nodo(x,y-1,self)
        lista.append(nodo)
        nodo=Nodo(x+1,y-1,self)
        lista.append(nodo)
        nodo=Nodo(x-1,y,self)
        lista.append(nodo)
        nodo=Nodo(x+1,y,self)
        lista.append(nodo)
        nodo=Nodo(x-1,y+1,self)
        lista.append(nodo)
        nodo=Nodo(x,y+1,self)
        lista.append(nodo)
        nodo=Nodo(x+1,y+1,self)
        lista.append(nodo)
        return lista
        
        
    def calcularF(self,coste,h=0):
        return self.g + coste + h
    
    def getPadre(self):
        return self.padre
    
    def getCoste(self):
        padre=self.padre
        if padre.getX() != self.getX() and padre.getY() != self.getY():
            return 1.5
        return 1
        
    def getF(self):
        return self.f

    def getG(self):
        return self.g
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def setG(self,g):
        self.g=g
        
    def setPadre(self, padre):
        self.padre=padre
        
    def __eq__(self, nodo):
        return self.getX() == nodo.getX() and self.getY()==nodo.getY()