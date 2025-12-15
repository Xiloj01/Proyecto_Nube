from estructuras.listasimple import ListaSimple
from modelos.centros_datos import CentroDatos

class GestorCentros:
    """Controlador de centros"""
    
    def __init__(self):
        self.centros = ListaSimple()
    
    def agregar_centro(self, id_c, nom, pais, ciudad, cpu, ram, almac):
        if self.centros.buscar_por_id(id_c) is not None:
            return False, f"Centro {id_c} ya existe"
        
        centro_nuevo = CentroDatos(id_c, nom, pais, ciudad, cpu, ram, almac)
        self.centros.insertar(centro_nuevo)
        return True, f"Centro {id_c} creado"
    
    def obtener_centro(self, id_c):
        return self.centros.buscar_por_id(id_c)
    
    def obtener_todos(self):
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
        
        print(f"\n{'='*70}")
        print("  LISTADO DE CENTROS")
        print(f"{'='*70}")
        self.centros.listar_todo()
