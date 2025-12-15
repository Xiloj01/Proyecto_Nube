from estructuras.nodos import Nodo

class ColaPrioridad:
    """Cola de prioridad - mayor numero = mas urgente"""
    
    def __init__(self):
        self.frente = None
        self.cantidad = 0
    
    def vacia(self):
        return self.frente is None
    
    def encolar(self, elemento):
        """Inserta por prioridad"""
        nodo_nuevo = Nodo(elemento)
        
        # si vacia o es mas prioritario
        if self.vacia() or elemento.prioridad > self.frente.dato.prioridad:
            nodo_nuevo.siguiente = self.frente
            self.frente = nodo_nuevo
        else:
            # buscar posicion
            temp = self.frente
            while (temp.siguiente is not None and 
                   temp.siguiente.dato.prioridad >= elemento.prioridad):
                temp = temp.siguiente
            nodo_nuevo.siguiente = temp.siguiente
            temp.siguiente = nodo_nuevo
        
        self.cantidad += 1
    
    def desencolar(self):
        """Saca el mas prioritario"""
        if self.vacia():
            return None
        elemento = self.frente.dato
        self.frente = self.frente.siguiente
        self.cantidad -= 1
        return elemento
    
    def ver_frente(self):
        if self.vacia():
            return None
        return self.frente.dato
    
    def mostrar_cola(self):
        """Muestra la cola completa"""
        if self.vacia():
            print("\n>> Cola vacia")
            return
        
        print(f"\n{'='*70}")
        print(f"  COLA DE SOLICITUDES - {self.cantidad} pendiente(s)")
        print(f"{'='*70}")
        temp = self.frente
        pos = 1
        while temp is not None:
            print(f"\n[Posicion {pos}]")
            temp.dato.mostrar()
            temp = temp.siguiente
            pos += 1
        print(f"{'='*70}")

