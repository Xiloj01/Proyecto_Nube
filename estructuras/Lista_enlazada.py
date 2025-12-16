from estructuras.nodos import Nodo

class ListaSimple:
    
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0
        self.primero = None 
        # apunta al primer nodo igual que cabeza
    
    def vacia(self):
        # si no hay cabeza entonces no hay nada en la lista
        esta_vacia = self.cabeza is None
        return esta_vacia
    
    def insertar(self, elemento):
        # creo un nuevo nodo con el elemento
        nuevo = Nodo(elemento)
        
        # si la lista esta vacia pongo el nuevo como cabeza
        if self.vacia():
            self.cabeza = nuevo
            self.primero = nuevo
        else:
            # si ya hay elementos recorro hasta el final
            temp = self.cabeza
            while temp.siguiente is not None:
                temp = temp.siguiente
            temp.siguiente = nuevo
        
        self.tamanio += 1
    
    def buscar_por_id(self, identificador):
        # empiezo desde la cabeza y voy avanzando
        actual = self.cabeza
        while actual is not None:
            # si encuentro el id que busco lo retorno
            if actual.dato.id == identificador:
                return actual.dato
            actual = actual.siguiente
        # si llego aqui es porque no lo encontre
        return None
    
    def quitar(self, identificador):
        # primero verifico que la lista no este vacia
        if self.vacia():
            return False
        
        # si el elemento esta en la cabeza
        if self.cabeza.dato.id == identificador:
            self.cabeza = self.cabeza.siguiente
            self.primero = self.cabeza
            self.tamanio -= 1
            return True
        
        # si no esta en la cabeza busco en el resto
        anterior = self.cabeza
        actual = self.cabeza.siguiente
        
        while actual is not None:
            if actual.dato.id == identificador:
                # se encontro
                anterior.siguiente = actual.siguiente
                self.tamanio -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        
        # no lo encontre en toda la lista
        return False
    
    def obtener_tamanio(self):
        return self.tamanio
    
    def listar_todo(self):
        # si no hay nada solo aviso y salgo
        if self.vacia():
            print(">> Lista vacia")
            return
        
        # recorro toda la lista e imprimo cada elemento
        temp = self.cabeza
        while temp is not None:
            temp.dato.mostrar()
            temp = temp.siguiente