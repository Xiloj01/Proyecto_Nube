from estructuras.nodos import NodoSimple

class ListaSimpleEnlazada:
    """Lista simplemente enlazada"""

    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def esta_vacia(self):
        """Verifica si la lista está vacía"""
        return self.primero is None

    def agregar_inicio(self, dato):
        """Agrega un nodo al inicio de la lista"""
        nuevo_nodo = NodoSimple(dato)
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.primero
            self.primero = nuevo_nodo
        self.tamanio += 1

    def agregar_final(self, dato):
        """Agrega un nodo al final de la lista"""
        nuevo_nodo = NodoSimple(dato)
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
        self.tamanio += 1

    def eliminar_inicio(self):
        """Elimina el primer nodo de la lista"""
        if self.esta_vacia():
            return None
        dato_eliminado = self.primero.dato
        if self.primero == self.ultimo:  # Solo hay un nodo
            self.primero = None
            self.ultimo = None
        else:
            self.primero = self.primero.siguiente
        self.tamanio -= 1
        return dato_eliminado

    def eliminar_final(self):
        """Elimina el último nodo de la lista"""
        if self.esta_vacia():
            return None
        dato_eliminado = self.ultimo.dato
        if self.primero == self.ultimo:  # Solo hay un nodo
            self.primero = None
            self.ultimo = None
        else:
            actual = self.primero
            while actual.siguiente != self.ultimo:
                actual = actual.siguiente
            actual.siguiente = None
            self.ultimo = actual
        self.tamanio -= 1
        return dato_eliminado

    def buscar_por_id(self, clave_busqueda, comparador):
        """Busca un nodo en la lista usando una función comparadora"""
        actual = self.primero
        while actual is not None:
            if comparador(actual.dato, clave_busqueda):
                return actual.dato
            actual = actual.siguiente
        return None

    def obtener_todos(self):
        """Obtiene todos los elementos de la lista como una lista Python"""
        elementos = []
        actual = self.primero
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def recorrer(self):
        """Recorre e imprime todos los elementos de la lista"""
        actual = self.primero
        while actual is not None:
            print(actual.dato)
            actual = actual.siguiente

    def __len__(self):
        """Devuelve el tamaño de la lista"""
        return self.tamanio

    def __iter__(self):
        """Permite iterar sobre la lista"""
        actual = self.primero
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
