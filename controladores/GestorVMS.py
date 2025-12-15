from estructuras.listasimple import ListaSimple
from modelos.maquina_virtual import MaquinaVirtual

class GestorVMs:
    """Controlador de VMs"""
    
    def __init__(self, gestor_centros):
        self.gestor_centros = gestor_centros
        self.todas_vms = ListaSimple()
    
    def agregar_vm(self, id_vm, nom, so, ip, cpu, ram, almac, id_centro):
        if self.todas_vms.buscar_por_id(id_vm) is not None:
            return False, f"VM {id_vm} ya existe"
        
        centro = self.gestor_centros.obtener_centro(id_centro)
        if centro is None:
            return False, f"Centro {id_centro} no existe"
        
        if not centro.hay_recursos_suficientes(cpu, ram, almac):
            return False, f"Centro {id_centro} sin recursos"
        
        vm_nueva = MaquinaVirtual(id_vm, nom, so, ip, cpu, ram, almac, id_centro)
        
        self.todas_vms.insertar(vm_nueva)
        centro.vms.insertar(vm_nueva)
        centro.usar_recursos(cpu, ram, almac)
        
        return True, f"VM {id_vm} creada en {id_centro}"
    
    def obtener_vm(self, id_vm):
        return self.todas_vms.buscar_por_id(id_vm)
    
    def listar_vms_de_centro(self, id_centro):
        centro = self.gestor_centros.obtener_centro(id_centro)
        if centro is None:
            return None
        return centro.vms
    
    def mover_vm_entre_centros(self, id_vm, id_centro_destino):
        vm = self.obtener_vm(id_vm)
        if vm is None:
            return False, f"VM {id_vm} no encontrada"
        
        if vm.id_centro == id_centro_destino:
            return False, "VM ya esta en ese centro"
        
        centro_origen = self.gestor_centros.obtener_centro(vm.id_centro)
        centro_destino = self.gestor_centros.obtener_centro(id_centro_destino)
        
        if centro_destino is None:
            return False, f"Centro {id_centro_destino} no existe"
        
        if not centro_destino.hay_recursos_suficientes(vm.cpu_asig, vm.ram_asig, vm.almacen_asig):
            return False, f"Centro {id_centro_destino} sin recursos"
        
        # liberar en origen
        centro_origen.devolver_recursos(vm.cpu_asig, vm.ram_asig, vm.almacen_asig)
        centro_origen.vms.quitar(id_vm)
        
        # usar en destino
        centro_destino.usar_recursos(vm.cpu_asig, vm.ram_asig, vm.almacen_asig)
        centro_destino.vms.insertar(vm)
        
        vm.id_centro = id_centro_destino
        
        return True, f"VM {id_vm} migrada a {id_centro_destino}"
