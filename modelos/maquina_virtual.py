#maquina_virtual.py
from estructuras.listasimple import ListaSimple

class MaquinaVirtual:
    
    def __init__(self, identificador, nombre_vm, sistema_op, direccion_ip, 
                 cpu, ram, almacenamiento, id_centro):
        self.id = identificador
        self.nombre = nombre_vm
        self.so = sistema_op
        self.ip = direccion_ip
        
        # recursos que me asigno el centro
        self.cpu_asig = int(cpu)
        self.ram_asig = int(ram)
        self.almacen_asig = int(almacenamiento)
        
        # al inicio todo esta disponible para contenedores
        self.cpu_disponible = int(cpu)
        self.ram_disponible = int(ram)
        
        # guardo a que centro pertenezco
        self.id_centro = id_centro
        
        # lista de contenedores que tengo
        self.contenedores = ListaSimple()
        self.siguiente = None
    
    def porcentaje_cpu_usado(self):
        # calculo cuanto cpu estoy usando
        if self.cpu_asig == 0:
            return 0.0
        
        usado = self.cpu_asig - self.cpu_disponible
        pct = (usado * 100.0) / self.cpu_asig
        return pct
    
    def porcentaje_ram_usado(self):
        # lo mismo para ram
        if self.ram_asig == 0:
            return 0.0
        
        usado = self.ram_asig - self.ram_disponible
        pct = (usado * 100.0) / self.ram_asig
        return pct
    
    def puede_crear_contenedor(self, cpu_porcentaje, ram_megabytes):
        # el cpu del contenedor viene en porcentaje de mi cpu total
        cpu_necesario = (cpu_porcentaje / 100.0) * self.cpu_asig
        
        # la ram viene en MB, la convierto a GB
        ram_necesaria = ram_megabytes / 1024.0
        
        # verifico si tengo suficientes recursos
        if self.cpu_disponible >= cpu_necesario and self.ram_disponible >= ram_necesaria:
            return True
        else:
            return False
    
    def consumir_recursos_contenedor(self, cpu_pct, ram_mb):
        # calculo cuanto cpu necesito en unidades reales
        cpu_necesario = (cpu_pct / 100.0) * self.cpu_asig
        
        # convierto ram de MB a GB
        ram_necesaria = ram_mb / 1024.0
        
        # resto los recursos disponibles
        self.cpu_disponible -= cpu_necesario
        self.ram_disponible -= ram_necesaria
    
    def liberar_recursos_contenedor(self, cpu_pct, ram_mb):
        # cuando elimino un contenedor devuelvo sus recursos
        cpu_necesario = (cpu_pct / 100.0) * self.cpu_asig
        ram_necesaria = ram_mb / 1024.0
        
        # sumo los recursos de vuelta
        self.cpu_disponible += cpu_necesario
        self.ram_disponible += ram_necesaria
    
    def mostrar(self):
        # muestro toda la info de la vm
        print(f"\n{'='*65}")
        print(f"ID VM: {self.id}")
        print(f"Nombre: {self.nombre}")
        print(f"Sistema Operativo: {self.so}")
        print(f"IP: {self.ip}")
        print(f"Centro: {self.id_centro}")
        
        print(f"\nRECURSOS:")
        print(f"  CPU: {self.cpu_disponible:.2f}/{self.cpu_asig} disponibles")
        print(f"  RAM: {self.ram_disponible:.2f}/{self.ram_asig} GB disponibles")
        print(f"  Almacenamiento: {self.almacen_asig} GB")
        
        # cuento contenedores
        num_contenedores = self.contenedores.obtener_tamanio()
        print(f"Contenedores: {num_contenedores}")
        print(f"{'='*65}")
