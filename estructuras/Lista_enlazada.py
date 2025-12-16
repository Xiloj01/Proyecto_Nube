#Lista_enlazada.py
from estructuras.nodos import Nodo

class ListaSimple:
    
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0
        self.primero = None
    
    def vacia(self):
        esta_vacia = self.cabeza is None
        return esta_vacia
    
    def insertar(self, elemento):
        nuevo = Nodo(elemento)
        
        if self.vacia():
            self.cabeza = nuevo
            self.primero = nuevo
        else:
            temp = self.cabeza
            while temp.siguiente is not None:
                temp = temp.siguiente
            temp.siguiente = nuevo
        
        self.tamanio = self.tamanio + 1
    
    def buscar_por_id(self, identificador):
        actual = self.cabeza
        while actual is not None:
            if actual.dato.id == identificador:
                return actual.dato
            actual = actual.siguiente
        return None
    
    def quitar(self, identificador):
        if self.vacia():
            return False
        
        if self.cabeza.dato.id == identificador:
            self.cabeza = self.cabeza.siguiente
            self.primero = self.cabeza
            self.tamanio = self.tamanio - 1
            return True
        
        anterior = self.cabeza
        actual = self.cabeza.siguiente
        
        while actual is not None:
            if actual.dato.id == identificador:
                anterior.siguiente = actual.siguiente
                self.tamanio = self.tamanio - 1
                return True
            anterior = actual
            actual = actual.siguiente
        
        return False
    
    def obtener_tamanio(self):
        return self.tamanio
    
    def listar_todo(self):
        if self.vacia():
            print(">> Lista vacia")
            return
        
        temp = self.cabeza
        while temp is not None:
            temp.dato.mostrar()
            temp = temp.siguiente