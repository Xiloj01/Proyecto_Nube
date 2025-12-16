from estructuras.Lista_enlazada import ListaSimple

class MaquinaVirtual:
    def __init__(self, identificador, nombre_vm, sistema_op, direccion_ip, 
                 cpu, ram, almacenamiento, id_centro):
        self.id = identificador
        self.nombre = nombre_vm
        self.so = sistema_op
        self.ip = direccion_ip
        
        self.cpu_asig = int(cpu)
        self.ram_asig = int(ram)
        self.almacen_asig = int(almacenamiento)
        
        self.cpu_disponible = int(cpu)
        self.ram_disponible = int(ram)
        
        self.id_centro = id_centro
        self.contenedores = ListaSimple()
        self.siguiente = None

    def porcentaje_cpu_usado(self):
        if self.cpu_asig == 0:
            return 0.0
        
        usado = self.cpu_asig - self.cpu_disponible
        pct = (usado * 100.0) / self.cpu_asig
        return pct

    def porcentaje_ram_usado(self):
        if self.ram_asig == 0:
            return 0.0
        
        # calculo cuanta memoria estoy ocupando
        usado = self.ram_asig - self.ram_disponible
        pct = (usado * 100.0) / self.ram_asig
        return pct

    def puede_crear_contenedor(self, cpu_porcentaje, ram_megabytes):
        cpu_necesario = (cpu_porcentaje / 100.0) * self.cpu_asig
        
        # convierto los MB a GB para poder comparar
        ram_necesaria = ram_megabytes / 1024.0
        
        # me fijo si me alcanza
        tiene_cpu = self.cpu_disponible >= cpu_necesario
        tiene_ram = self.ram_disponible >= ram_necesaria
        
        return tiene_cpu and tiene_ram

    def consumir_recursos_contenedor(self, cpu_pct, ram_mb):
        # cuando creo un contenedor tengo que restarle recursos a la VM
        cpu_necesario = (cpu_pct / 100.0) * self.cpu_asig
        ram_necesaria = ram_mb / 1024.0
        
        self.cpu_disponible -= cpu_necesario
        self.ram_disponible -= ram_necesaria

    def liberar_recursos_contenedor(self, cpu_pct, ram_mb):
        # esto es basicamente lo opuesto al metodo de arriba
        cpu_necesario = (cpu_pct / 100.0) * self.cpu_asig
        ram_necesaria = ram_mb / 1024.0
        
        # los sumo de vuelta
        self.cpu_disponible += cpu_necesario
        self.ram_disponible += ram_necesaria

    def mostrar(self):
        separador = "=" * 65
        print("")
        print(separador)
        print("ID VM: " + self.id)
        print("Nombre: " + self.nombre)
        print("Sistema Operativo: " + self.so)
        print("IP: " + self.ip)
        print("Centro: " + self.id_centro)
        
        print("\nRECURSOS:")
        # muestro cpu con formato de 2 decimales
        info_cpu = f"  CPU: {self.cpu_disponible:.2f}/{self.cpu_asig} disponibles"
        print(info_cpu)
        
        # lo mismo con ram
        info_ram = f"  RAM: {self.ram_disponible:.2f}/{self.ram_asig} GB disponibles"
        print(info_ram)
        
        print(f"  Almacenamiento: {self.almacen_asig} GB")
        
        # cuento cuantos contenedores tengo corriendo
        cant_contenedores = self.contenedores.obtener_tamanio()
        print("Contenedores: " + str(cant_contenedores))
        print(separador)