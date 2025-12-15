#GestorContenedores.py
from modelos.contenedor import Contenedor

class GestorContenedores:
    
    def __init__(self, gestor_vms):
        self.gestor_vms = gestor_vms
    
    def crear_contenedor(self, id_cont, nom, img, cpu_pct, ram_mb, puerto, id_vm):
        # primero busco la vm donde va el contenedor
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            msg = f"VM {id_vm} no existe"
            return False, msg
        
        # verifico si ya existe un contenedor con ese id
        cont_existe = vm.contenedores.buscar_por_id(id_cont)
        if cont_existe is not None:
            return False, f"Contenedor {id_cont} ya existe en {id_vm}"
        
        # chequeo si la vm tiene recursos suficientes
        tiene_recursos = vm.puede_crear_contenedor(cpu_pct, ram_mb)
        if not tiene_recursos:
            return False, f"VM {id_vm} sin recursos para contenedor"
        
        # creo el contenedor nuevo
        cont_nuevo = Contenedor(id_cont, nom, img, cpu_pct, ram_mb, puerto)
        # lo agrego a la lista de contenedores de la vm
        vm.contenedores.insertar(cont_nuevo)
        # consumo los recursos de la vm
        vm.consumir_recursos_contenedor(cpu_pct, ram_mb)
        
        return True, f"Contenedor {id_cont} creado en {id_vm}"
    
    def obtener_contenedores_de_vm(self, id_vm):
        # busco la vm
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            return None
        # retorno su lista de contenedores
        return vm.contenedores
    
    def cambiar_estado(self, id_cont, id_vm, estado_nuevo):
        # busco la vm primero
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            return False, f"VM {id_vm} no existe"
        
        # busco el contenedor en esa vm
        cont = vm.contenedores.buscar_por_id(id_cont)
        if cont is None:
            return False, f"Contenedor {id_cont} no existe"
        
        # intento cambiar el estado
        resultado = cont.modificar_estado(estado_nuevo)
        if resultado:
            return True, f"Estado de {id_cont} cambiado a {estado_nuevo}"
        else:
            return False, "Estado invalido"
    
    def borrar_contenedor(self, id_cont, id_vm):
        # primero busco la vm
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            return False, f"VM {id_vm} no existe"
        
        # busco el contenedor
        cont = vm.contenedores.buscar_por_id(id_cont)
        if cont is None:
            return False, f"Contenedor {id_cont} no existe"
        
        # antes de eliminarlo libero los recursos que usaba
        vm.liberar_recursos_contenedor(cont.cpu_pct, cont.ram_mb)
        # ahora si lo elimino de la lista
        vm.contenedores.quitar(id_cont)
        
        return True, f"Contenedor {id_cont} eliminado"