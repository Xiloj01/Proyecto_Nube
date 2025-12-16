#GestorSolicitudes.py
from estructuras.ColaPrioridad import ColaPrioridad
from modelos.solicitud import solicitud

class GestorSolicitudes:
    
    def __init__(self, gestor_centros, gestor_vms):
        # inicializo la cola de prioridades para manejar las solicitudes
        self.cola = ColaPrioridad()
        self.gestor_centros = gestor_centros
        self.gestor_vms = gestor_vms
        self.procesadas = []
    
    def nueva_solicitud(self, id_sol, cliente, tipo, prioridad, cpu, ram, almac, tiempo):
        # creo el objeto solicitud con los datos que me pasan
        sol = solicitud(id_sol, cliente, tipo, prioridad, cpu, ram, almac, tiempo)
        self.cola.encolar(sol)
        mensaje = "Solicitud " + id_sol + " agregada (prioridad " + str(prioridad) + ")"
        return True, mensaje
    
    def procesar_una(self):
        # reviso si hay algo en la cola primero
        if self.cola.vacia():
            return False, "Cola vacia"
        
        # saco la solicitud con mayor prioridad
        sol = self.cola.desencolar()
        
        # dependiendo del tipo llamo al metodo correspondiente
        if sol.tipo == "Deploy":
            resultado = self._hacer_deploy(sol)
        elif sol.tipo == "Backup":
            resultado = self._hacer_backup(sol)
        else:
            mensaje = "Tipo desconocido: " + sol.tipo
            resultado = (False, mensaje)
        
        # si todo salio bien la agrego a procesadas
        if resultado[0]:
            self.procesadas.append(sol)
        
        return resultado
    
    def procesar_varias(self, cantidad):
        if self.cola.vacia():
            return False, "Cola vacia"
        
        exitosas = []
        fallidas = []
        
        # proceso la cantidad que me pidieron o hasta que se acabe la cola
        for i in range(cantidad):
            if self.cola.vacia():
                break
            
            exito, mensaje = self.procesar_una()
            if exito:
                exitosas.append(mensaje)
            else:
                fallidas.append(mensaje)
        
        # imprimo un resumen de lo que paso
        linea_separadora = "=" * 70
        print("")
        print(linea_separadora)
        print("  PROCESAMIENTO DE SOLICITUDES")
        print(linea_separadora)
        print("Exitosas: " + str(len(exitosas)))
        for msg in exitosas:
            print("  ✓ " + msg)
        
        # si hubo fallas tambien se muestra
        if fallidas:
            print("\nFallidas: " + str(len(fallidas)))
            for msg in fallidas:
                print("  ✗ " + msg)
        
        mensaje_final = "Procesadas " + str(len(exitosas)) + " solicitudes"
        return True, mensaje_final
    
    def _hacer_deploy(self, sol):
        # busco el centro con mas recursos disponibles
        centro = self.gestor_centros.centro_con_mayor_disponibilidad()
        if centro is None:
            mensaje = "Deploy " + sol.id + ": Sin centros"
            return False, mensaje
        
        # armo los datos para la nueva VM
        id_nueva_vm = sol.id
        nombre_vm = "VM-" + sol.cliente
        sistema_operativo = "Ubuntu 22.04 LTS"
        
        # genero una IP basandome en cuantas VMs ya hay
        total_vms = self.gestor_vms.todas_vms.obtener_tamanio()
        ip_nueva = "192.168.1." + str(100 + total_vms)
        
        # intento crear la VM
        exito, mensaje = self.gestor_vms.agregar_vm(
            id_nueva_vm, nombre_vm, sistema_operativo, ip_nueva,
            sol.cpu_necesario, sol.ram_necesaria, sol.almacen_necesario,
            centro.id
        )
        
        if exito:
            mensaje_final = "Deploy " + sol.id + ": VM en " + centro.id + " para " + sol.cliente
            return True, mensaje_final
        else:
            mensaje_error = "Deploy " + sol.id + ": " + mensaje
            return False, mensaje_error
    
    def _hacer_backup(self, sol):
        # igual que deploy pero para backup
        centro = self.gestor_centros.centro_con_mayor_disponibilidad()
        if centro is None:
            mensaje = "Backup " + sol.id + ": Sin centros"
            return False, mensaje
        
        id_nueva_vm = sol.id
        nombre_vm = "Backup-" + sol.cliente
        sistema_operativo = "Ubuntu 22.04 LTS"
        
        total_vms = self.gestor_vms.todas_vms.obtener_tamanio()
        ip_nueva = "192.168.2." + str(100 + total_vms)
        
        exito, mensaje = self.gestor_vms.agregar_vm(
            id_nueva_vm, nombre_vm, sistema_operativo, ip_nueva,
            sol.cpu_necesario, sol.ram_necesaria, sol.almacen_necesario,
            centro.id
        )
        
        if exito:
            mensaje_final = "Backup " + sol.id + ": VM suspendida en " + centro.id
            return True, mensaje_final
        else:
            mensaje_error = "Backup " + sol.id + ": " + mensaje
            return False, mensaje_error
    
    def ver_cola(self):
        return self.cola