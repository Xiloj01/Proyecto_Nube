#ColaPrioridad.py
from estructuras.nodos import Nodo

class ColaPrioridad:
    
    def __init__(self):
        self.frente = None
        self.cantidad = 0
    
    def vacia(self):
        esta_vacia = self.frente is None
        return esta_vacia
    
    def encolar(self, elemento):
        nodo_nuevo = Nodo(elemento)
        
        if self.vacia():
            nodo_nuevo.siguiente = self.frente
            self.frente = nodo_nuevo
        else:
            prioridad_elemento = elemento.prioridad
            prioridad_frente = self.frente.dato.prioridad
            
            if prioridad_elemento > prioridad_frente:
                nodo_nuevo.siguiente = self.frente
                self.frente = nodo_nuevo
            else:
                temp = self.frente
                while temp.siguiente is not None:
                    prioridad_siguiente = temp.siguiente.dato.prioridad
                    if prioridad_siguiente < prioridad_elemento:
                        break
                    temp = temp.siguiente
                
                nodo_nuevo.siguiente = temp.siguiente
                temp.siguiente = nodo_nuevo
        
        self.cantidad = self.cantidad + 1
    
    def desencolar(self):
        if self.vacia():
            return None
        
        elemento = self.frente.dato
        self.frente = self.frente.siguiente
        self.cantidad = self.cantidad - 1
        return elemento
    
    def ver_frente(self):
        if self.vacia():
            return None
        return self.frente.dato
    
    def mostrar_cola(self):
        if self.vacia():
            print("\n>> Cola vacia")
            return
        
        separador = "=" * 70
        print("")
        print(separador)
        cantidad_str = str(self.cantidad)
        titulo = "  COLA DE SOLICITUDES - " + cantidad_str + " pendiente(s)"
        print(titulo)
        print(separador)
        
        temp = self.frente
        pos = 1
        while temp is not None:
            pos_str = str(pos)
            texto_pos = "\n[Posicion " + pos_str + "]"
            print(texto_pos)
            temp.dato.mostrar()
            temp = temp.siguiente
            pos = pos + 1
        
        print(separador)