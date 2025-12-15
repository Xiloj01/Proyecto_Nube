from estructuras.ColaPrioridad import ColaPrioridad
from modelos.solicitud import Solicitud

class GestorSolicitudes:
    """Controlador de solicitudes"""
    
    def __init__(self, gestor_centros, gestor_vms):
        self.cola = ColaPrioridad()
        self.gestor_centros = gestor_centros
        self.gestor_vms = gestor_vms
        self.procesadas = []
    
    def nueva_solicitud(self, id_sol, cliente, tipo, prioridad, cpu, ram, almac, tiempo):
        sol = Solicitud(id_sol, cliente, tipo, prioridad, cpu, ram, almac, tiempo)
        self.cola.encolar(sol)
        return True, f"Solicitud {id_sol} agregada (prioridad {prioridad})"
    
    def procesar_una(self):
        if self.cola.vacia():
            return False, "Cola vacia"
        
        sol = self.cola.desencolar()
        
        if sol.tipo == "Deploy":
            resultado = self._hacer_deploy(sol)
        elif sol.tipo == "Backup":
            resultado = self._hacer_backup(sol)
        else:
            resultado = (False, f"Tipo desconocido: {sol.tipo}")
        
        if resultado[0]:
            self.procesadas.append(sol)
        
        return resultado
    
    def procesar_varias(self, cantidad):
        if self.cola.vacia():
            return False, "Cola vacia"
        
        procesadas_ok = []
        procesadas_fail = []
        
        for i in range(cantidad):
            if self.cola.vacia():
                break
            
            exito, msg = self.procesar_una()
            if exito:
                procesadas_ok.append(msg)
            else:
                procesadas_fail.append(msg)
        
        print(f"\n{'='*70}")
        print(f"  PROCESAMIENTO DE SOLICITUDES")
        print(f"{'='*70}")
        print(f"Exitosas: {len(procesadas_ok)}")
        for msg in procesadas_ok:
            print(f"  ✓ {msg}")
        
        if procesadas_fail:
            print(f"\nFallidas: {len(procesadas_fail)}")
            for msg in procesadas_fail:
                print(f"  ✗ {msg}")
        
        return True, f"Procesadas {len(procesadas_ok)} solicitudes"
    
    def _hacer_deploy(self, sol):
        centro = self.gestor_centros.centro_con_mayor_disponibilidad()
        if centro is None:
            return False, f"Deploy {sol.id}: Sin centros"
        
        id_nueva_vm = sol.id
        nombre_vm = f"VM-{sol.cliente}"
        so_default = "Ubuntu 22.04 LTS"
        total_vms = self.gestor_vms.todas_vms.obtener_tamanio()
        ip_nueva = f"192.168.1.{100 + total_vms}"
        
        exito, msg = self.gestor_vms.agregar_vm(
            id_nueva_vm, nombre_vm, so_default, ip_nueva,
            sol.cpu_necesario, sol.ram_necesaria, sol.almacen_necesario,
            centro.id
        )
        
        if exito:
            return True, f"Deploy {sol.id}: VM en {centro.id} para {sol.cliente}"
        else:
            return False, f"Deploy {sol.id}: {msg}"
    
    def _hacer_backup(self, sol):
        centro = self.gestor_centros.centro_con_mayor_disponibilidad()
        if centro is None:
            return False, f"Backup {sol.id}: Sin centros"
        
        id_nueva_vm = sol.id
        nombre_vm = f"Backup-{sol.cliente}"
        so_default = "Ubuntu 22.04 LTS"
        total_vms = self.gestor_vms.todas_vms.obtener_tamanio()
        ip_nueva = f"192.168.2.{100 + total_vms}"
        
        exito, msg = self.gestor_vms.agregar_vm(
            id_nueva_vm, nombre_vm, so_default, ip_nueva,
            sol.cpu_necesario, sol.ram_necesaria, sol.almacen_necesario,
            centro.id
        )
        
        if exito:
            return True, f"Backup {sol.id}: VM suspendida en {centro.id}"
        else:
            return False, f"Backup {sol.id}: {msg}"
    
    def ver_cola(self):
        return self.cola

