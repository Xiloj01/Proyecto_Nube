#main.py
import os
from controladores.GestorCentros import GestorCentros
from controladores.GestorVMS import GestorVMs
from controladores.GestorContenedores import GestorContenedores
from controladores.GestorSolicitudes import GestorSolicitudes
from xml_handler.paser_xml import ParserXML
from xml_handler.generador_xml import GeneradorXML
from reportes.GeneradorGraphizv import GeneradorGraphviz

def limpiar_pantalla():
    comando = 'cls' if os.name == 'nt' else 'clear'
    os.system(comando)

def pausar():
    input("\nPresione ENTER para continuar...")

class SistemaCloudSync:
    
    def __init__(self):
        self.g_centros = GestorCentros()
        self.g_vms = GestorVMs(self.g_centros)
        self.g_contenedores = GestorContenedores(self.g_vms)
        self.g_solicitudes = GestorSolicitudes(self.g_centros, self.g_vms)
        
        self.parser = ParserXML(self.g_centros, self.g_vms, self.g_contenedores, self.g_solicitudes)
        self.generador_xml = GeneradorXML(self.g_centros)
        
        self.generador_reportes = GeneradorGraphviz(self.g_centros, self.g_vms)
    
    def ejecutar(self):
        while True:
            self.menu_principal()
    
    def menu_principal(self):
        limpiar_pantalla()
        separador = "=" * 70
        print(separador)
        print("  CLOUDSYNC - SISTEMA DE GESTION EN LA NUBE")
        print(separador)
        print("\n1. Cargar archivo XML")
        print("2. Gestion de centros de datos")
        print("3. Gestion de maquinas virtuales")
        print("4. Gestion de contenedores")
        print("5. Gestion de solicitudes")
        print("6. Generar reportes")
        print("7. Generar archivo XML de salida")
        print("8. Salir")
        print(separador)
        
        opcion = input("\nSeleccione una opcion: ")
        opcion = opcion.strip()
        
        if opcion == "1":
            self.cargar_xml()
        elif opcion == "2":
            self.menu_centros()
        elif opcion == "3":
            self.menu_vms()
        elif opcion == "4":
            self.menu_contenedores()
        elif opcion == "5":
            self.menu_solicitudes()
        elif opcion == "6":
            self.menu_reportes()
        elif opcion == "7":
            self.generar_xml_salida()
        elif opcion == "8":
            print("\nHasta luego!")
            exit(0)
        else:
            print("\nOpcion invalida")
            pausar()
    
    def cargar_xml(self):
        limpiar_pantalla()
        separador = "=" * 70
        print(separador)
        print("  CARGAR ARCHIVO XML")
        print(separador)
        
        ruta = input("\nIngrese la ruta del archivo XML: ")
        ruta = ruta.strip()
        
        if not ruta:
            print("\nDebe ingresar una ruta")
            pausar()
            return
        
        exito = self.parser.cargar_archivo(ruta)
        if exito:
            print("\nArchivo cargado correctamente")
        pausar()
    
    def menu_centros(self):
        while True:
            limpiar_pantalla()
            separador = "=" * 70
            print(separador)
            print("  GESTION DE CENTROS DE DATOS")
            print(separador)
            print("\n1. Listar todos los centros")
            print("2. Buscar centro por ID")
            print("3. Ver centro con mas recursos")
            print("4. Volver al menu principal")
            print(separador)
            
            op = input("\nSeleccione una opcion: ")
            op = op.strip()
            
            if op == "1":
                self.listar_centros()
            elif op == "2":
                self.buscar_centro()
            elif op == "3":
                self.centro_mas_recursos()
            elif op == "4":
                break
            else:
                print("\nOpcion invalida")
                pausar()
    
    def listar_centros(self):
        limpiar_pantalla()
        self.g_centros.mostrar_todos_centros()
        pausar()
    
    def buscar_centro(self):
        limpiar_pantalla()
        id_c = input("\nIngrese ID del centro: ")
        id_c = id_c.strip()
        centro = self.g_centros.obtener_centro(id_c)
        
        if centro:
            centro.mostrar()
        else:
            mensaje = "\nCentro " + id_c + " no encontrado"
            print(mensaje)
        pausar()
    
    def centro_mas_recursos(self):
        limpiar_pantalla()
        centro = self.g_centros.centro_con_mayor_disponibilidad()
        
        if centro:
            print("\n>> Centro con mayor disponibilidad:")
            centro.mostrar()
        else:
            print("\nNo hay centros registrados")
        pausar()
    
    def menu_vms(self):
        while True:
            limpiar_pantalla()
            separador = "=" * 70
            print(separador)
            print("  GESTION DE MAQUINAS VIRTUALES")
            print(separador)
            print("\n1. Buscar VM por ID")
            print("2. Listar VMs de un centro")
            print("3. Migrar VM entre centros")
            print("4. Volver al menu principal")
            print(separador)
            
            op = input("\nSeleccione una opcion: ")
            op = op.strip()
            
            if op == "1":
                self.buscar_vm()
            elif op == "2":
                self.listar_vms_centro()
            elif op == "3":
                self.migrar_vm()
            elif op == "4":
                break
            else:
                print("\nOpcion invalida")
                pausar()
    
    def buscar_vm(self):
        limpiar_pantalla()
        id_vm = input("\nIngrese ID de la VM: ")
        id_vm = id_vm.strip()
        vm = self.g_vms.obtener_vm(id_vm)
        
        if vm:
            vm.mostrar()
        else:
            mensaje = "\nVM " + id_vm + " no encontrada"
            print(mensaje)
        pausar()
    
    def listar_vms_centro(self):
        limpiar_pantalla()
        id_c = input("\nIngrese ID del centro: ")
        id_c = id_c.strip()
        vms = self.g_vms.listar_vms_de_centro(id_c)
        
        if vms is None:
            mensaje = "\nCentro " + id_c + " no encontrado"
            print(mensaje)
        elif vms.vacia():
            mensaje = "\nCentro " + id_c + " no tiene VMs"
            print(mensaje)
        else:
            separador = "=" * 70
            print("")
            print(separador)
            titulo = "  VMs DEL CENTRO " + id_c
            print(titulo)
            print(separador)
            vms.listar_todo()
        pausar()
    
    def migrar_vm(self):
        limpiar_pantalla()
        separador = "=" * 70
        print(separador)
        print("  MIGRAR MAQUINA VIRTUAL")
        print(separador)
        
        id_vm = input("\nID de la VM a migrar: ")
        id_vm = id_vm.strip()
        id_destino = input("ID del centro destino: ")
        id_destino = id_destino.strip()
        
        exito, msg = self.g_vms.mover_vm_entre_centros(id_vm, id_destino)
        print("")
        print(msg)
        pausar()
    
    def menu_contenedores(self):
        while True:
            limpiar_pantalla()
            separador = "=" * 70
            print(separador)
            print("  GESTION DE CONTENEDORES")
            print(separador)
            print("\n1. Desplegar contenedor en VM")
            print("2. Listar contenedores de una VM")
            print("3. Cambiar estado de contenedor")
            print("4. Eliminar contenedor")
            print("5. Volver al menu principal")
            print(separador)
            
            op = input("\nSeleccione una opcion: ")
            op = op.strip()
            
            if op == "1":
                self.crear_contenedor()
            elif op == "2":
                self.listar_contenedores()
            elif op == "3":
                self.cambiar_estado_contenedor()
            elif op == "4":
                self.eliminar_contenedor()
            elif op == "5":
                break
            else:
                print("\nOpcion invalida")
                pausar()
    
    def crear_contenedor(self):
        limpiar_pantalla()
        separador = "=" * 70
        print(separador)
        print("  DESPLEGAR CONTENEDOR")
        print(separador)
        
        try:
            id_vm = input("\nID de la VM: ")
            id_vm = id_vm.strip()
            id_cont = input("ID del contenedor: ")
            id_cont = id_cont.strip()
            nombre = input("Nombre: ")
            nombre = nombre.strip()
            imagen = input("Imagen (ej. nginx:latest): ")
            imagen = imagen.strip()
            cpu_pct_str = input("CPU (porcentaje): ")
            cpu_pct = int(cpu_pct_str)
            ram_mb_str = input("RAM (MB): ")
            ram_mb = int(ram_mb_str)
            puerto = input("Puerto: ")
            puerto = puerto.strip()
            
            exito, msg = self.g_contenedores.crear_contenedor(id_cont, nombre, imagen, cpu_pct, ram_mb, puerto, id_vm)
            print("")
            print(msg)
        except ValueError:
            print("\nValores numericos invalidos")
        pausar()
    
    def listar_contenedores(self):
        limpiar_pantalla()
        id_vm = input("\nID de la VM: ")
        id_vm = id_vm.strip()
        conts = self.g_contenedores.obtener_contenedores_de_vm(id_vm)
        
        if conts is None:
            mensaje = "\nVM " + id_vm + " no encontrada"
            print(mensaje)
        elif conts.vacia():
            mensaje = "\nVM " + id_vm + " no tiene contenedores"
            print(mensaje)
        else:
            separador = "=" * 70
            print("")
            print(separador)
            titulo = "  CONTENEDORES DE " + id_vm
            print(titulo)
            print(separador)
            conts.listar_todo()
        pausar()
    
    def cambiar_estado_contenedor(self):
        limpiar_pantalla()
        separador = "=" * 70
        print(separador)
        print("  CAMBIAR ESTADO DE CONTENEDOR")
        print(separador)
        print("\nEstados validos: Activo, Pausado, Detenido, Reiniciando")
        
        id_vm = input("\nID de la VM: ")
        id_vm = id_vm.strip()
        id_cont = input("ID del contenedor: ")
        id_cont = id_cont.strip()
        estado = input("Nuevo estado: ")
        estado = estado.strip()
        
        exito, msg = self.g_contenedores.cambiar_estado(id_cont, id_vm, estado)
        print("")
        print(msg)
        pausar()
    
    def eliminar_contenedor(self):
        limpiar_pantalla()
        separador = "=" * 70
        print(separador)
        print("  ELIMINAR CONTENEDOR")
        print(separador)
        
        id_vm = input("\nID de la VM: ")
        id_vm = id_vm.strip()
        id_cont = input("ID del contenedor: ")
        id_cont = id_cont.strip()
        
        exito, msg = self.g_contenedores.borrar_contenedor(id_cont, id_vm)
        print("")
        print(msg)
        pausar()
    
    def menu_solicitudes(self):
        while True:
            limpiar_pantalla()
            separador = "=" * 70
            print(separador)
            print("  GESTION DE SOLICITUDES")
            print(separador)
            print("\n1. Agregar nueva solicitud")
            print("2. Procesar solicitud de mayor prioridad")
            print("3. Procesar N solicitudes")
            print("4. Ver cola de solicitudes")
            print("5. Volver al menu principal")
            print(separador)
            
            op = input("\nSeleccione una opcion: ")
            op = op.strip()
            
            if op == "1":
                self.agregar_solicitud()
            elif op == "2":
                self.procesar_una_solicitud()
            elif op == "3":
                self.procesar_n_solicitudes()
            elif op == "4":
                self.ver_cola_solicitudes()
            elif op == "5":
                break
            else:
                print("\nOpcion invalida")
                pausar()
    
    def agregar_solicitud(self):
        limpiar_pantalla()
        separador = "=" * 70
        print(separador)
        print("  AGREGAR SOLICITUD")
        print(separador)
        
        try:
            id_sol = input("\nID de la solicitud: ")
            id_sol = id_sol.strip()
            cliente = input("Cliente: ")
            cliente = cliente.strip()
            tipo = input("Tipo (Deploy/Backup): ")
            tipo = tipo.strip()
            prioridad_str = input("Prioridad (1-10): ")
            prioridad = prioridad_str.strip()
            cpu_str = input("CPU necesaria: ")
            cpu = cpu_str.strip()
            ram_str = input("RAM necesaria (GB): ")
            ram = ram_str.strip()
            almac_str = input("Almacenamiento necesario (GB): ")
            almac = almac_str.strip()
            tiempo_str = input("Tiempo estimado (min): ")
            tiempo = tiempo_str.strip()
            
            exito, msg = self.g_solicitudes.nueva_solicitud(id_sol, cliente, tipo, prioridad, cpu, ram, almac, tiempo)
            print("")
            print(msg)
        except ValueError:
            print("\nValores invalidos")
        pausar()
    
    def procesar_una_solicitud(self):
        limpiar_pantalla()
        exito, msg = self.g_solicitudes.procesar_una()
        print("")
        print(msg)
        pausar()
    
    def procesar_n_solicitudes(self):
        limpiar_pantalla()
        try:
            cantidad_str = input("\nCuantas solicitudes procesar: ")
            cantidad = int(cantidad_str)
            exito, msg = self.g_solicitudes.procesar_varias(cantidad)
        except ValueError:
            print("\nValor invalido")
        pausar()
    
    def ver_cola_solicitudes(self):
        limpiar_pantalla()
        cola = self.g_solicitudes.ver_cola()
        cola.mostrar_cola()
        pausar()
    
    def menu_reportes(self):
        while True:
            limpiar_pantalla()
            separador = "=" * 70
            print(separador)
            print("  GENERAR REPORTES")
            print(separador)
            print("\n1. Reporte de centros de datos")
            print("2. Reporte de VMs de un centro")
            print("3. Reporte de contenedores de una VM")
            print("4. Reporte de cola de solicitudes")
            print("5. Volver al menu principal")
            print(separador)
            
            op = input("\nSeleccione una opcion: ")
            op = op.strip()
            
            if op == "1":
                self.reporte_centros()
            elif op == "2":
                self.reporte_vms()
            elif op == "3":
                self.reporte_contenedores()
            elif op == "4":
                self.reporte_solicitudes()
            elif op == "5":
                break
            else:
                print("\nOpcion invalida")
                pausar()
    
    def reporte_centros(self):
        limpiar_pantalla()
        exito, msg = self.generador_reportes.reporte_centros()
        print("")
        print(msg)
        pausar()
    
    def reporte_vms(self):
        limpiar_pantalla()
        id_centro = input("\nID del centro: ")
        id_centro = id_centro.strip()
        exito, msg = self.generador_reportes.reporte_vms_centro(id_centro)
        print("")
        print(msg)
        pausar()
    
    def reporte_contenedores(self):
        limpiar_pantalla()
        id_vm = input("\nID de la VM: ")
        id_vm = id_vm.strip()
        exito, msg = self.generador_reportes.reporte_contenedores_vm(id_vm)
        print("")
        print(msg)
        pausar()
    
    def reporte_solicitudes(self):
        limpiar_pantalla()
        cola = self.g_solicitudes.ver_cola()
        exito, msg = self.generador_reportes.reporte_cola_solicitudes(cola)
        print("")
        print(msg)
        pausar()
    
    def generar_xml_salida(self):
        limpiar_pantalla()
        separador = "=" * 70
        print(separador)
        print("  GENERAR XML DE SALIDA")
        print(separador)
        
        ruta = input("\nIngrese ruta del archivo de salida: ")
        ruta = ruta.strip()
        
        if not ruta:
            ruta = "salida.xml"
        
        exito, msg = self.generador_xml.generar_salida(ruta)
        print("")
        print(msg)
        pausar()

if __name__ == "__main__":
    sistema = SistemaCloudSync()
    sistema.ejecutar()