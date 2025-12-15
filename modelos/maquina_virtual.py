from estructuras.listasimple import ListaSimple

class MaquinaVirtual:
    """Modelo de maquina virtual"""
    
    def __init__(self, identificador, nombre_vm, sistema_op, direccion_ip, 
                 cpu, ram, almacenamiento, id_centro):
        self.id = identificador
        self.nombre = nombre_vm
        self.so = sistema_op
        self.ip = direccion_ip
        # asignados
        self.cpu_asig = int(cpu)
        self.ram_asig = int(ram)
        self.almacen_asig = int(almacenamiento)
        # disponibles para contenedores
        self.cpu_disponible = int(cpu)
        self.ram_disponible = int(ram)
        # centro
        self.id_centro = id_centro
        # contenedores
        self.contenedores = ListaSimple()
        self.siguiente = None
    
    def porcentaje_cpu_usado(self):
        if self.cpu_asig == 0:
            return 0.0
        usado = self.cpu_asig - self.cpu_disponible
        return (usado * 100.0) / self.cpu_asig
    
    def porcentaje_ram_usado(self):
        if self.ram_asig == 0:
            return 0.0
        usado = self.ram_asig - self.ram_disponible
        return (usado * 100.0) / self.ram_asig
    
    def puede_crear_contenedor(self, cpu_porcentaje, ram_megabytes):
        # cpu en porcentaje de la VM
        cpu_necesario = (cpu_porcentaje / 100.0) * self.cpu_asig
        # ram en MB, convertir a GB
        ram_necesaria = ram_megabytes / 1024.0
        return self.cpu_disponible >= cpu_necesario and self.ram_disponible >= ram_necesaria
    
    def consumir_recursos_contenedor(self, cpu_pct, ram_mb):
        cpu_necesario = (cpu_pct / 100.0) * self.cpu_asig
        ram_necesaria = ram_mb / 1024.0
        self.cpu_disponible -= cpu_necesario
        self.ram_disponible -= ram_necesaria
    
    def liberar_recursos_contenedor(self, cpu_pct, ram_mb):
        cpu_necesario = (cpu_pct / 100.0) * self.cpu_asig
        ram_necesaria = ram_mb / 1024.0
        self.cpu_disponible += cpu_necesario
        self.ram_disponible += ram_necesaria
    
    def mostrar(self):
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
        print(f"Contenedores: {self.contenedores.obtener_tamanio()}")
        print(f"{'='*65}")
