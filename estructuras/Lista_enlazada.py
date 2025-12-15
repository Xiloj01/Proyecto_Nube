class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.primero = None
        self.size = 0
    
    def esta_vacia(self):
        return self.primero is None
    
    def add(self, dato):
        nuevo_nodo = Nodo(dato)

        if self.esta_vacia():
            self.primero = nuevo_nodo
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        
        self.size += 1
    
    def show(self):
        if self.esta_vacia():
            print("La lista esta vacia")
            return
        
        actual = self.primero
        while actual is not None:
            if hasattr(actual.dato, 'mostrar_informacion'):
                actual.dato.mostrar_informacion()
            else:
                print(actual.dato)
            actrual = actual.siguiente
    
    def find_b_id(self, id_buscado, atributo_id='id_centro'):
        actual = self.primero
        while actual is not None:
            if getattr(acutal.dato, atributo_id):
                if
