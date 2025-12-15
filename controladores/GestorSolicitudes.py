#GestorSolicitudes.py
from estructuras.ColaPrioridad import ColaPrioridad
from modelos.solicitud import Solicitud

class GestorSolicitudes:
    
    def __init__(self, gestor_centros, gestor_vms):
        self.cola = ColaPrioridad()
        self.gestor_centros = gestor_centros
        self.gestor_vms = gestor_vms
        self.procesadas = []  #aca guardo las que ya procese
    
    def nueva_solicitud(self, id_sol, cliente, tipo, prioridad, cpu, ram, almac, tiempo):
        # creo la solicitud nueva
        sol = Solicitud(id_sol, cliente, tipo, prioridad, cpu, ram, almac, tiempo)
        # la meto en la cola
        self.cola.encolar(sol)
        msg = f"Solicitud {id_sol} agregada (prioridad {prioridad})"
        return True, msg
    
    def procesar_una(self):
        # verifico que haya solicitudes
        if self.cola.vacia():
            return False, "Cola vacia"
        
        # saco la de mayor prioridad
        sol = self.cola.desencolar()
        
        # dependiendo del tipo hago diferentes cosas
        if sol.tipo == "Deploy":
            resultado = self._hacer_deploy(sol)
        elif sol.tipo == "Backup":
            resultado = self._hacer_backup(sol)
        else:
            resultado = (False, f"Tipo desconocido: {sol.tipo}")
        
        # si funciono la guardo en procesadas
        if resultado[0]:
            self.procesadas.append(sol)
        
        return resultado
    
    def procesar_varias(self, cantidad):
        # verifico que haya solicitudes
        if self.cola.vacia():
            return False, "Cola vacia"
        
        # listas para guardar resultados
        procesadas_ok = []
        procesadas_fail = []
        
        # proceso N solicitudes
        for i in range(cantidad):
            # si ya no hay mas salgo del ciclo
            if self.cola.vacia():
                break
            
            # proceso una solicitud
            exito, msg = self.procesar_una()
            if exito:
                procesadas_ok.append(msg)
            else:
                procesadas_fail.append(msg)
        
        # muestro resultados en pantalla
        print(f"\n{'='*70}")
        print(f"  PROCESAMIENTO DE SOLICITUDES")
        print(f"{'='*70}")
        print(f"Exitosas: {len(procesadas_ok)}")
        for msg in procesadas_ok:
            print(f"  ✓ {msg}")
        
        # si hubo fallidas las muestro
        if procesadas_fail:
            print(f"\nFallidas: {len(procesadas_fail)}")
            for msg in procesadas_fail:
                print(f"  ✗ {msg}")
        
        return True, f"Procesadas {len(procesadas_ok)} solicitudes"
    
    def _hacer_deploy(self, sol):
        # busco el centro que tenga mas recursos disponibles
        centro = self.gestor_centros.centro_con_mayor_disponibilidad()
        if centro is None:
            return False, f"Deploy {sol.id}: Sin centros"
        
        # genero los datos para crear la vm nueva
        id_nueva_vm = sol.id
        nombre_vm = f"VM-{sol.cliente}"
        so_default = "Ubuntu 22.04 LTS"
        
        # genero una ip automatica
        total_vms = self.gestor_vms.todas_vms.obtener_tamanio()
        ip_nueva = f"192.168.1.{100 + total_vms}"
        
        # intento crear la vm en el centro
        exito, msg = self.gestor_vms.agregar_vm(
            id_nueva_vm, nombre_vm, so_default, ip_nueva,
            sol.cpu_necesario, sol.ram_necesaria, sol.almacen_necesario,
            centro.id
        )
        
        # verifico si funciono
        if exito:
            return True, f"Deploy {sol.id}: VM en {centro.id} para {sol.cliente}"
        else:
            return False, f"Deploy {sol.id}: {msg}"
    
    def _hacer_backup(self, sol):
        # busco el centro con mas espacio libre
        centro = self.gestor_centros.centro_con_mayor_disponibilidad()
        if centro is None:
            return False, f"Backup {sol.id}: Sin centros"
        
        # datos para la vm de backup
        id_nueva_vm = sol.id
        nombre_vm = f"Backup-{sol.cliente}"
        so_default = "Ubuntu 22.04 LTS"
        
        # para backups uso otra red (192.168.2.x)
        total_vms = self.gestor_vms.todas_vms.obtener_tamanio()
        ip_nueva = f"192.168.2.{100 + total_vms}"
        
        # creo la vm para el backup
        exito, msg = self.gestor_vms.agregar_vm(
            id_nueva_vm, nombre_vm, so_default, ip_nueva,
            sol.cpu_necesario, sol.ram_necesaria, sol.almacen_necesario,
            centro.id
        )
        
        # chequeo resultado
        if exito:
            return True, f"Backup {sol.id}: VM suspendida en {centro.id}"
        else:
            return False, f"Backup {sol.id}: {msg}"
    
    def ver_cola(self):
        # retorno la cola completa
        return self.cola