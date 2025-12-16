class solicitud:
    
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
        # imprimo los datos de la solicitud
        print("  ID: " + self.id)
        print("  Cliente: " + self.cliente)
        print("  Tipo: " + self.tipo)
        
        # muestro la prioridad con su escala
        prioridad_texto = str(self.prioridad) + "/10"
        print("  Prioridad: " + prioridad_texto)
        
        recursos = f"CPU={self.cpu_necesario}, RAM={self.ram_necesaria}, Almacen={self.almacen_necesario}"
        print("  Recursos: " + recursos)
        
        # tiempo en minutos
        print(f"  Tiempo: {self.tiempo} min")