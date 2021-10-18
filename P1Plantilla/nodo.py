class Nodo():
    
    destino=0
    mapi=0
    def __init__ (self,x,y):
        self.x=x
        self.y=y
        self.padre=None
        self.g=0
        self.h=self.calcularH(Nodo.destino)
        self.f=self.g+self.h
        
        
    def getHijos(self):
        x=self.x
        y=self.y
        #g=self.getG()
        lista=[]
        
        nodo=Nodo(x-1,y-1)
        celda=self.mapi.getCelda(nodo.y, nodo.x)
        if celda == 0:
            nodo.padre=self
            nodo.g=self.g+1.5
            lista.append(nodo)
            
        nodo=Nodo(x,y-1)
        celda=self.mapi.getCelda(nodo.y, nodo.x)
        if celda == 0:
            nodo.g=self.g+1
            nodo.padre=self
            lista.append(nodo)
            
        nodo=Nodo(x+1,y-1)
        celda=self.mapi.getCelda(nodo.y, nodo.x)
        if celda == 0:
            nodo.g=self.g+1.5
            nodo.padre=self
            lista.append(nodo)
            
        nodo=Nodo(x-1,y)
        celda=self.mapi.getCelda(nodo.y, nodo.x)
        if celda == 0:
            nodo.padre=self
            nodo.g=self.g+1
            lista.append(nodo)
            
        nodo=Nodo(x+1,y)
        celda=self.mapi.getCelda(nodo.y, nodo.x)
        if celda == 0:
            nodo.g=self.g+1
            nodo.padre=self
            lista.append(nodo)
            
        nodo=Nodo(x-1,y+1)
        celda=self.mapi.getCelda(nodo.y, nodo.x)
        if celda == 0:
            nodo.g=self.g+1.5
            nodo.padre=self
            lista.append(nodo)
            
        nodo=Nodo(x,y+1)
        celda=self.mapi.getCelda(nodo.y, nodo.x)
        if celda == 0:
            nodo.g=self.g+1
            nodo.padre=self
            lista.append(nodo)
            
        nodo=Nodo(x+1,y+1)
        celda=self.mapi.getCelda(nodo.y, nodo.x)
        if celda == 0:
            nodo.g=self.g+1.5
            nodo.padre=self
            lista.append(nodo)
        return lista
    
    def __eq__(self,nodo):
        if nodo is None:
            return False
        return self.x==nodo.x and self.y==nodo.y
    
    def getCoste(self):
        padre=self.padre
        if padre.x != self.x and padre.y != self.y:
            return 1.5
        return 1
    
    def calcularH(self,destino):
        columna=destino.getCol() - self.x
        fila=destino.getFila() - self.y
        if columna < 0:
            columna=columna * -1
        if fila < 0:
            fila=fila * -1
        self.h = columna + fila
        return self.h

