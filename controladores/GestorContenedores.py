from modelos.contenedor import Contenedor

class GestorContenedores:
    """Controlador de contenedores"""
    
    def __init__(self, gestor_vms):
        self.gestor_vms = gestor_vms
    
    def crear_contenedor(self, id_cont, nom, img, cpu_pct, ram_mb, puerto, id_vm):
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            return False, f"VM {id_vm} no existe"
        
        if vm.contenedores.buscar_por_id(id_cont) is not None:
            return False, f"Contenedor {id_cont} ya existe en {id_vm}"
        
        if not vm.puede_crear_contenedor(cpu_pct, ram_mb):
            return False, f"VM {id_vm} sin recursos para contenedor"
        
        cont_nuevo = Contenedor(id_cont, nom, img, cpu_pct, ram_mb, puerto)
        vm.contenedores.insertar(cont_nuevo)
        vm.consumir_recursos_contenedor(cpu_pct, ram_mb)
        
        return True, f"Contenedor {id_cont} creado en {id_vm}"
    
    def obtener_contenedores_de_vm(self, id_vm):
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            return None
        return vm.contenedores
    
    def cambiar_estado(self, id_cont, id_vm, estado_nuevo):
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            return False, f"VM {id_vm} no existe"
        
        cont = vm.contenedores.buscar_por_id(id_cont)
        if cont is None:
            return False, f"Contenedor {id_cont} no existe"
        
        if cont.modificar_estado(estado_nuevo):
            return True, f"Estado de {id_cont} cambiado a {estado_nuevo}"
        else:
            return False, "Estado invalido"
    
    def borrar_contenedor(self, id_cont, id_vm):
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            return False, f"VM {id_vm} no existe"
        
        cont = vm.contenedores.buscar_por_id(id_cont)
        if cont is None:
            return False, f"Contenedor {id_cont} no existe"
        
        vm.liberar_recursos_contenedor(cont.cpu_pct, cont.ram_mb)
        vm.contenedores.quitar(id_cont)
        
        return True, f"Contenedor {id_cont} eliminado"

