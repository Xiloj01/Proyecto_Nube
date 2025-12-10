class NodoSimple:
    """Nodo para lista simplemente enlazada"""
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class NodoDoble:
    """Nodo para lista doblemente enlazada"""
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class NodoPila:
    """Nodo para pila"""
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None