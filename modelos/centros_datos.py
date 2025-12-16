from estructuras.Lista_enlazada import ListaSimple

class CentroDatos:
    
    def __init__(self, identificador, nombre_centro, pais, ciudad, cpu, ram, almacenamiento):
        self.id = identificador
        self.nombre = nombre_centro
        self.pais = pais
        self.ciudad = ciudad
        
        # se guardo la capacidad maxima de cada uno
        self.cpu_total = int(cpu)
        self.ram_total = int(ram)
        self.almacenamiento_total = int(almacenamiento)

        self.cpu_disp = int(cpu)
        self.ram_disp = int(ram)
        self.almacen_disp = int(almacenamiento)
        
        self.cpu_disponible = int(cpu)
        self.ram_disponible = int(ram)
        
        self.vms = ListaSimple()
        self.siguiente = None
    
    def uso_cpu_porcentaje(self):
        if self.cpu_total == 0:
            return 0.0
        
        # se resta lo disponible del total para saber lo usado
        usado = self.cpu_total - self.cpu_disp
        porcentaje = (usado * 100.0) / self.cpu_total
        return porcentaje
    
    def calcular_utilizacion_cpu(self):
        return self.uso_cpu_porcentaje()
    
    def uso_ram_porcentaje(self):
        # se revisa primero para no dividir por cero
        if self.ram_total == 0:
            return 0.0
        
        usado = self.ram_total - self.ram_disp
        porcentaje = (usado * 100.0) / self.ram_total
        return porcentaje
    
    def calcular_utilizacion_ram(self):
        return self.uso_ram_porcentaje()
    
    def hay_recursos_suficientes(self, cpu_req, ram_req, almac_req):
        # me fijo si tengo suficiente de cada cosa
        tiene_cpu = self.cpu_disp >= cpu_req
        tiene_ram = self.ram_disp >= ram_req
        tiene_almacen = self.almacen_disp >= almac_req
        
        # tiene que cumplir las 3 condiciones
        return tiene_cpu and tiene_ram and tiene_almacen
    
    def usar_recursos(self, cpu, ram, almac):
        # cuando asigno una VM le resto los recursos
        self.cpu_disp -= cpu
        self.ram_disp -= ram
        self.almacen_disp -= almac
        
        # sincronizo con las otras variables
        self.cpu_disponible = self.cpu_disp
        self.ram_disponible = self.ram_disp
    
    def devolver_recursos(self, cpu, ram, almac):
        # cuando elimino una VM los devuelvo
        self.cpu_disp += cpu
        self.ram_disp += ram
        self.almacen_disp += almac
        
        self.cpu_disponible = self.cpu_disp
        self.ram_disponible = self.ram_disp
    
    def mostrar(self):
        linea = "=" * 65
        print("")
        print(linea)
        print("ID Centro: " + self.id)
        print("Nombre: " + self.nombre)
        ubicacion = self.ciudad + ", " + self.pais
        print("Ubicacion: " + ubicacion)
        
        print("\nRECURSOS:")
        
        # calculo y muestro el uso de CPU
        pct_cpu = self.uso_cpu_porcentaje()
        info_cpu = f"  CPU: {self.cpu_disp}/{self.cpu_total} disponibles ({pct_cpu:.2f}% usado)"
        print(info_cpu)
        
        # ahora la RAM
        pct_ram = self.uso_ram_porcentaje()
        info_ram = f"  RAM: {self.ram_disp}/{self.ram_total} GB disponibles ({pct_ram:.2f}% usado)"
        print(info_ram)
        
        # el almacenamiento sin porcentaje
        info_disco = f"  Almacenamiento: {self.almacen_disp}/{self.almacenamiento_total} GB"
        print(info_disco)
        
        # cuento las VMs activas
        cantidad_vms = self.vms.obtener_tamanio()
        print("VMs activas: " + str(cantidad_vms))
        print(linea)