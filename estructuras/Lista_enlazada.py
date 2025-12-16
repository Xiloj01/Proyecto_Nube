from estructuras.nodos import Nodo

class ListaSimple:
    
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0
    
    def vacia(self):
        return self.cabeza is None
    
    def insertar(self, elemento):
        # ve si hay un nodo
        nuevo = Nodo(elemento)
        
        # si no hay nada lo pongo de primero
        if self.vacia():
            self.cabeza = nuevo
        else:
            # si hay elementos voy al final
            temp = self.cabeza
            while temp.siguiente is not None:
                temp = temp.siguiente
            temp.siguiente = nuevo
        
        self.tamanio += 1
    
    def buscar_por_id(self, identificador):
        # recorro buscando el identificador
        actual = self.cabeza
        while actual is not None:
            if actual.dato.id == identificador:
                return actual.dato
            actual = actual.siguiente
        return None
    
    def quitar(self, identificador):
        # si esta vacia no hago nada
        if self.vacia():
            return False
        
        # si es el primero
        if self.cabeza.dato.id == identificador:
            self.cabeza = self.cabeza.siguiente
            self.tamanio -= 1
            return True
        
        # busco en el resto
        anterior = self.cabeza
        actual = self.cabeza.siguiente
        
        while actual is not None:
            if actual.dato.id == identificador:
                anterior.siguiente = actual.siguiente
                self.tamanio -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        
        return False
    
    def obtener_tamanio(self):
        return self.tamanio
    
    def listar_todo(self):
        # si no hay nada
        if self.vacia():
            print(">> Lista vacia")
            return
        
        # recorro mostrando
        temp = self.cabeza
        while temp is not None:
            temp.dato.mostrar()
            temp = temp.siguiente
