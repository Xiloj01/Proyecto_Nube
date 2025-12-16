#GestorSolicitudes.py
from estructuras.ColaPrioridad import ColaPrioridad
from modelos.solicitud import solicitud

class GestorSolicitudes:
    
    def __init__(self, gestor_centros, gestor_vms):
        self.cola = ColaPrioridad()
        self.gestor_centros = gestor_centros
        self.gestor_vms = gestor_vms
        self.procesadas = []
    
    def nueva_solicitud(self, id_sol, cliente, tipo, prioridad, cpu, ram, almac, tiempo):
        sol = solicitud(id_sol, cliente, tipo, prioridad, cpu, ram, almac, tiempo)
        self.cola.encolar(sol)
        msg = "Solicitud " + id_sol + " agregada (prioridad " + str(prioridad) + ")"
        return True, msg
    
    def procesar_una(self):
        if self.cola.vacia():
            return False, "Cola vacia"
        
        sol = self.cola.desencolar()
        
        if sol.tipo == "Deploy":
            resultado = self._hacer_deploy(sol)
        elif sol.tipo == "Backup":
            resultado = self._hacer_backup(sol)
        else:
            msg = "Tipo desconocido: " + sol.tipo
            resultado = (False, msg)
        
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
        
        separador = "=" * 70
        print("")
        print(separador)
        print("  PROCESAMIENTO DE SOLICITUDES")
        print(separador)
        exitosas_str = str(len(procesadas_ok))
        print("Exitosas: " + exitosas_str)
        for msg in procesadas_ok:
            texto = "  ✓ " + msg
            print(texto)
        
        if procesadas_fail:
            fallidas_str = str(len(procesadas_fail))
            print("\nFallidas: " + fallidas_str)
            for msg in procesadas_fail:
                texto = "  ✗ " + msg
                print(texto)
        
        procesadas_num = str(len(procesadas_ok))
        msg_final = "Procesadas " + procesadas_num + " solicitudes"
        return True, msg_final
    
    def _hacer_deploy(self, sol):
        centro = self.gestor_centros.centro_con_mayor_disponibilidad()
        if centro is None:
            msg = "Deploy " + sol.id + ": Sin centros"
            return False, msg
        
        id_nueva_vm = sol.id
        nombre_vm = "VM-" + sol.cliente
        so_default = "Ubuntu 22.04 LTS"
        
        total_vms = self.gestor_vms.todas_vms.obtener_tamanio()
        numero_ip = 100 + total_vms
        ip_nueva = "192.168.1." + str(numero_ip)
        
        exito, msg = self.gestor_vms.agregar_vm(
            id_nueva_vm, nombre_vm, so_default, ip_nueva,
            sol.cpu_necesario, sol.ram_necesaria, sol.almacen_necesario,
            centro.id
        )
        
        if exito:
            msg_final = "Deploy " + sol.id + ": VM en " + centro.id + " para " + sol.cliente
            return True, msg_final
        else:
            msg_error = "Deploy " + sol.id + ": " + msg
            return False, msg_error
    
    def _hacer_backup(self, sol):
        centro = self.gestor_centros.centro_con_mayor_disponibilidad()
        if centro is None:
            msg = "Backup " + sol.id + ": Sin centros"
            return False, msg
        
        id_nueva_vm = sol.id
        nombre_vm = "Backup-" + sol.cliente
        so_default = "Ubuntu 22.04 LTS"
        
        total_vms = self.gestor_vms.todas_vms.obtener_tamanio()
        numero_ip = 100 + total_vms
        ip_nueva = "192.168.2." + str(numero_ip)
        
        exito, msg = self.gestor_vms.agregar_vm(
            id_nueva_vm, nombre_vm, so_default, ip_nueva,
            sol.cpu_necesario, sol.ram_necesaria, sol.almacen_necesario,
            centro.id
        )
        
        if exito:
            msg_final = "Backup " + sol.id + ": VM suspendida en " + centro.id
            return True, msg_final
        else:
            msg_error = "Backup " + sol.id + ": " + msg
            return False, msg_error
    
    def ver_cola(self):
        return self.cola