import sys, pygame
import tkinter
import tkinter.filedialog
import math
import numpy as np
from casilla import *
from mapa import *
from nodo import *
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

def ActualizarTraza(traza,x,y,orden):
    if orden<10:
        traza[y][x]='0'+str(orden)
    else:
        traza[y][x]=orden
    return traza

def crearTraza(mapi):
    matriz = []
    for i in range(mapi.getAlto()):
        matriz.append([])
        for j in range(mapi.getAncho()):
            matriz[i].append(-1)
    return matriz

def imprimirTraza(traza,alto,ancho):
    filas = len(traza)
    columnas = len(traza[0])
    for i in range(filas):
        for j in range(columnas):
            #print("| {0} ".format(traza[i][j]), sep=',', end='')
            print("\t{0}".format(traza[i][j]), sep=',', end='')
        print('')

def aEstrella(mapi, origen, destino, camino):
    Nodo.destino=destino
    Nodo.mapi=mapi
    nodoOrigen=Nodo(origen.getCol(),origen.getFila())
    nodoDestino=Nodo(destino.getCol(),destino.getFila())
    traza= crearTraza(mapi)
    traza= ActualizarTraza(traza,origen.getCol(),origen.getFila(),0)
    orden=1
    
    #estadisticas
    nodosExplorados=0
    nodosActualizados=0
    
    listaInterior=[]
    listaFrontera=[nodoOrigen]
    
    while len(listaFrontera)>0:
        #nodo con menor f
        nodo=listaFrontera[0]
        for i in listaFrontera:
            if nodo.f>i.f:
                nodo=i
        
        if nodo==nodoDestino:
            coste = nodo.g
            imprimirTraza(traza,mapi.getAlto(),mapi.getAncho())
            while nodo!=nodoOrigen and nodo is not None:
                nodo=nodo.padre
                if nodo is not None:
                    camino[nodo.y][nodo.x]=","
            print('Nodos Explorados: ' ,str(nodosExplorados))
            print('Nodos Actualizados: ', str(nodosActualizados))
            return coste
        
        else:
            listaFrontera.remove(nodo)
            listaInterior.append(nodo)
            hijos=nodo.getHijos()
            
            for hijo in hijos:
                if hijo not in listaInterior:
                    if hijo not in listaFrontera:
                        coste= hijo.getCoste()
                        #hijo.f=hijo.g + 0
                        #hijo.f=hijo.g + hijo.calcularHManhattan(destino)
                        hijo.f=hijo.g + hijo.calcularHEuclidea(destino)
                        #hijo.f=hijo.g + hijo.calcularChebyshev(destino)
                        camino[hijo.y][hijo.x]=hijo.g
                        traza=ActualizarTraza(traza,hijo.x,hijo.y,orden)
                        orden=orden+1
                        nodosExplorados = nodosExplorados +1
                        listaFrontera.append(hijo)
                        
                    else:
                        if hijo in listaFrontera and hijo != nodoDestino and hijo != nodoOrigen:
                            for i in range(len(listaFrontera)):
                                if listaFrontera[i]==hijo:
                                    if(listaFrontera[i].g>hijo.g):
                                        print("Actualizamos nodo que ya esta en la lista abierta "+ "x: "+str(hijo.x) + " y: " + str(hijo.y))
                                        print("g anterior: "+ str(listaFrontera[i].g) + "; Nueva g: " + str(hijo.g) + ';')
                                        traza=ActualizarTraza(traza,hijo.x,hijo.y,orden)
                                        orden=orden+1
                                        #hijo.f=hijo.g + hijo.calcularHManhattan(destino)
                                        hijo.f=hijo.g + hijo.calcularHEuclidea(destino)
                                        #hijo.f=hijo.g + hijo.calcularChebyshev(destino)
                                        listaFrontera[i]=hijo
                                        nodosActualizados = nodosActualizados +1
                                    break
    return -1



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
                        #print(camino)
                        # llamar al A*
                        coste=aEstrella(mapi, origen, destino, camino)      
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
                    if camino[fil][col]==',':
                        pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    if isinstance(camino[fil][col],int) or isinstance(camino[fil][col],float):
                        pygame.draw.rect(screen, AZUL, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
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
    
    
