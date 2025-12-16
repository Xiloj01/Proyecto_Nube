#GestorContenedores.py
from modelos.contenedor import Contenedor

class GestorContenedores:
    
    def __init__(self, gestor_vms):
        self.gestor_vms = gestor_vms
    
    def crear_contenedor(self, id_cont, nom, img, cpu_pct, ram_mb, puerto, id_vm):
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            msg = "VM " + id_vm + " no existe"
            return False, msg
        
        cont_existe = vm.contenedores.buscar_por_id(id_cont)
        if cont_existe is not None:
            msg = "Contenedor " + id_cont + " ya existe en " + id_vm
            return False, msg
        
        tiene_recursos = vm.puede_crear_contenedor(cpu_pct, ram_mb)
        if not tiene_recursos:
            msg = "VM " + id_vm + " sin recursos para contenedor"
            return False, msg
        
        cont_nuevo = Contenedor(id_cont, nom, img, cpu_pct, ram_mb, puerto)
        vm.contenedores.insertar(cont_nuevo)
        vm.consumir_recursos_contenedor(cpu_pct, ram_mb)
        
        msg = "Contenedor " + id_cont + " creado en " + id_vm
        return True, msg
    
    def obtener_contenedores_de_vm(self, id_vm):
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            return None
        return vm.contenedores
    
    def cambiar_estado(self, id_cont, id_vm, estado_nuevo):
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            msg = "VM " + id_vm + " no existe"
            return False, msg
        
        cont = vm.contenedores.buscar_por_id(id_cont)
        if cont is None:
            msg = "Contenedor " + id_cont + " no existe"
            return False, msg
        
        resultado = cont.modificar_estado(estado_nuevo)
        if resultado:
            msg = "Estado de " + id_cont + " cambiado a " + estado_nuevo
            return True, msg
        else:
            return False, "Estado invalido"
    
    def borrar_contenedor(self, id_cont, id_vm):
        vm = self.gestor_vms.obtener_vm(id_vm)
        if vm is None:
            msg = "VM " + id_vm + " no existe"
            return False, msg
        
        cont = vm.contenedores.buscar_por_id(id_cont)
        if cont is None:
            msg = "Contenedor " + id_cont + " no existe"
            return False, msg
        
        vm.liberar_recursos_contenedor(cont.cpu_pct, cont.ram_mb)
        vm.contenedores.quitar(id_cont)
        
        msg = "Contenedor " + id_cont + " eliminado"
        return True, msg