#GestorVMS.py
from estructuras.Lista_enlazada import ListaSimple
from modelos.maquina_virtual import MaquinaVirtual

class GestorVMs:
    
    def __init__(self, gestor_centros):
        self.gestor_centros = gestor_centros
        self.todas_vms = ListaSimple()
    
    def agregar_vm(self, id_vm, nom, so, ip, cpu, ram, almac, id_centro):
        vm_existe = self.todas_vms.buscar_por_id(id_vm)
        if vm_existe is not None:
            msg = "VM " + id_vm + " ya existe"
            return False, msg
        
        centro = self.gestor_centros.obtener_centro(id_centro)
        if centro is None:
            msg = "Centro " + id_centro + " no existe"
            return False, msg
        
        cpu_int = int(cpu)
        ram_int = int(ram)
        almac_int = int(almac)
        
        tiene_recursos = centro.hay_recursos_suficientes(cpu_int, ram_int, almac_int)
        if not tiene_recursos:
            msg = "Centro " + id_centro + " sin recursos"
            return False, msg
        
        vm_nueva = MaquinaVirtual(id_vm, nom, so, ip, cpu, ram, almac, id_centro)
        
        self.todas_vms.insertar(vm_nueva)
        centro.vms.insertar(vm_nueva)
        centro.usar_recursos(cpu_int, ram_int, almac_int)
        
        msg = "VM " + id_vm + " creada en " + id_centro
        return True, msg
    
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
            msg = "VM " + id_vm + " no encontrada"
            return False, msg
        
        if vm.id_centro == id_centro_destino:
            return False, "VM ya esta en ese centro"
        
        centro_origen = self.gestor_centros.obtener_centro(vm.id_centro)
        centro_destino = self.gestor_centros.obtener_centro(id_centro_destino)
        
        if centro_destino is None:
            msg = "Centro " + id_centro_destino + " no existe"
            return False, msg
        
        tiene_recursos = centro_destino.hay_recursos_suficientes(vm.cpu_asig, vm.ram_asig, vm.almacen_asig)
        if not tiene_recursos:
            msg = "Centro " + id_centro_destino + " sin recursos"
            return False, msg
        
        centro_origen.devolver_recursos(vm.cpu_asig, vm.ram_asig, vm.almacen_asig)
        centro_origen.vms.quitar(id_vm)
        
        centro_destino.usar_recursos(vm.cpu_asig, vm.ram_asig, vm.almacen_asig)
        centro_destino.vms.insertar(vm)
        
        vm.id_centro = id_centro_destino
        
        msg = "VM " + id_vm + " migrada a " + id_centro_destino
        return True, msg