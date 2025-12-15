class solicitud:
    """Modelo de solicitud"""
    
    def __init__(self, identificador, nombre_cliente, tipo_solicitud, 
                 nivel_prioridad, cpu, ram, almacenamiento, tiempo_est):
        self.id = identificador
        self.cliente = nombre_cliente
        self.tipo = tipo_solicitud
        self.prioridad = int(nivel_prioridad)
        self.cpu_necesario = int(cpu)
        self.ram_necesaria = int(ram)
        self.almacen_necesario = int(almacenamiento)
        self.tiempo = int(tiempo_est)
        self.siguiente = None
    
    def mostrar(self):
        print(f"  ID: {self.id}")
        print(f"  Cliente: {self.cliente}")
        print(f"  Tipo: {self.tipo}")
        print(f"  Prioridad: {self.prioridad}/10")
        print(f"  Recursos: CPU={self.cpu_necesario}, RAM={self.ram_necesaria}, Almacen={self.almacen_necesario}")
        print(f"  Tiempo: {self.tiempo} min")
