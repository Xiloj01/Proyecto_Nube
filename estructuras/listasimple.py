from estructuras.nodos import NodoSimple

class ListaSimpleEnlazada:

    def __init__(self):
        # inicio sin ningun nodo
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def esta_vacia(self):
        #se vesi hay elementos en la lista o no
        return self.primero is None

    def agregar_inicio(self, dato):
        #se agrega un nuevo nodo al principio
        nuevo_nodo = NodoSimple(dato)
        if self.esta_vacia():
            # si esta vacia el nuevo es primero y ultimo a la vez
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            # si ya hay nodos enlazo el nuevo con el primero actual
            nuevo_nodo.siguiente = self.primero
            self.primero = nuevo_nodo
        self.tamanio += 1

    def agregar_final(self, dato):
        """Agrega un nodo nuevo al final de todo"""
        nuevo_nodo = NodoSimple(dato)
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            # enlazo el ultimo actual con el nuevo
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
        self.tamanio += 1

    def eliminar_inicio(self):
        """Quita el primer nodo y retorna su dato"""
        if self.esta_vacia():
            return None
        dato_eliminado = self.primero.dato
        # solo hay un nodo
        if self.primero == self.ultimo:
            self.primero = None
            self.ultimo = None
        else:
            # muevo el primero al siguiente nodo
            self.primero = self.primero.siguiente
        self.tamanio -= 1
        return dato_eliminado

    def eliminar_final(self):
        """Elimina el ultimo nodo de la lista"""
        if self.esta_vacia():
            return None
        dato_eliminado = self.ultimo.dato
        if self.primero == self.ultimo:
            self.primero = None
            self.ultimo = None
        else:
            # tengo que recorrer hasta el penultimo
            actual = self.primero
            while actual.siguiente != self.ultimo:
                actual = actual.siguiente
            # corto la conexion y actualizo el ultimo
            actual.siguiente = None
            self.ultimo = actual
        self.tamanio -= 1
        return dato_eliminado

    def buscar_por_id(self, clave_busqueda, comparador):
        """Busca usando una funcion de comparacion"""
        actual = self.primero
        while actual is not None:
            # uso el comparador que me pasaron para verificar
            if comparador(actual.dato, clave_busqueda):
                return actual.dato
            actual = actual.siguiente
        # si llegue hasta aca es que no lo encontre
        return None

    def obtener_todos(self):
        """Convierte la lista enlazada en una lista normal"""
        elementos = []
        actual = self.primero
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def recorrer(self):
        """Imprime cada elemento de la lista en orden"""
        actual = self.primero
        while actual is not None:
            print(actual.dato)
            actual = actual.siguiente

    def __len__(self):
        """Retorna cuantos elementos hay"""
        return self.tamanio

    def __iter__(self):
        """Hace que la lista sea iterable con for"""
        actual = self.primero
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente