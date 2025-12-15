#GestorCentros.py
from estructuras.listasimple import ListaSimple
from modelos.centros_datos import CentroDatos

class GestorCentros:
    
    def __init__(self):
        # lista para guardar los centros
        self.centros = ListaSimple()
    
    def agregar_centro(self, id_c, nom, pais, ciudad, cpu, ram, almac):
        # primero verifico si ya existe
        centro_existe = self.centros.buscar_por_id(id_c)
        if centro_existe is not None:
            mensaje = f"Centro {id_c} ya existe"
            return False, mensaje
        
        # creo el nuevo centro
        centro_nuevo = CentroDatos(id_c, nom, pais, ciudad, cpu, ram, almac)
        self.centros.insertar(centro_nuevo)
        msg = f"Centro {id_c} creado"
        return True, msg
    
    def obtener_centro(self, id_c):
        # busco y retorno
        resultado = self.centros.buscar_por_id(id_c)
        return resultado
    
    def obtener_todos(self):
        return self.centros
    
    def centro_con_mayor_disponibilidad(self):
        if self.centros.vacia():
            return None
        
        mejor_centro = None
        max_recursos = -1
        
        # recorro la lista
        temp = self.centros.cabeza
        while temp is not None:
            centro = temp.dato
            # sumo todos los recursos disponibles
            total_disp = centro.cpu_disp + centro.ram_disp + centro.almacen_disp
            if total_disp > max_recursos:
                max_recursos = total_disp
                mejor_centro = centro
            temp = temp.siguiente
        
        return mejor_centro
    
    def mostrar_todos_centros(self):
        # si no hay nada muestro mensaje
        if self.centros.vacia():
            print("\n>> No hay centros registrados")
            return
        
        # imprimo titulo bonito
        print(f"\n{'='*70}")
        print("  LISTADO DE CENTROS")
        print(f"{'='*70}")
        self.centros.listar_todo()