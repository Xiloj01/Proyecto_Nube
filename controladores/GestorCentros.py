#GestorCentros.py
from modelos.centros_datos import CentroDatos
from estructuras.Lista_enlazada import ListaSimple

class GestorCentros:
    
    def __init__(self):
        self.centros = ListaSimple()
    
    def agregar_centro(self, id_c, nom, pais, ciudad, cpu, ram, almac):
        centro_existe = self.centros.buscar_por_id(id_c)
        if centro_existe is not None:
            mensaje = "Centro " + id_c + " ya existe"
            return False, mensaje
        
        centro_nuevo = CentroDatos(id_c, nom, pais, ciudad, cpu, ram, almac)
        self.centros.insertar(centro_nuevo)
        msg = "Centro " + id_c + " creado"
        return True, msg
    
    def obtener_centro(self, id_c):
        resultado = self.centros.buscar_por_id(id_c)
        return resultado
    
    def obtener_todos(self):
        return self.centros
    
    def listar_todos(self):
        return self.centros
    
    def centro_con_mayor_disponibilidad(self):
        if self.centros.vacia():
            return None
        
        mejor_centro = None
        max_recursos = -1
        
        temp = self.centros.cabeza
        while temp is not None:
            centro = temp.dato
            total_disp = centro.cpu_disp + centro.ram_disp + centro.almacen_disp
            if total_disp > max_recursos:
                max_recursos = total_disp
                mejor_centro = centro
            temp = temp.siguiente
        
        return mejor_centro
    
    def mostrar_todos_centros(self):
        if self.centros.vacia():
            print("\n>> No hay centros registrados")
            return
        
        separador = "=" * 70
        print("")
        print(separador)
        print("  LISTADO DE CENTROS")
        print(separador)
        self.centros.listar_todo()