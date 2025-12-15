import os
from controladores.GestorCentros import GestorCentros
from controladores.GestorVMS import GestorVMs
from controladores.GestorContenedores import GestorContenedores
from controladores.GestorSolicitudes import GestorSolicitudes
from xml_handler.paser_xml import ParserXML
from xml_handler.generador_xml import GeneradorXML
from reportes.GeneradorGraphizv import GeneradorGraphviz



def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input("\nPresione ENTER para continuar...")


class SistemaCloudSync:
    """Sistema principal CloudSync"""
    
    def __init__(self):
        # inicializar gestores
        self.g_centros = GestorCentros()
        self.g_vms = GestorVMs(self.g_centros)
        self.g_contenedores = GestorContenedores(self.g_vms)
        self.g_solicitudes = GestorSolicitudes(self.g_centros, self.g_vms)
        
        # parser y generador XML
        self.parser = ParserXML(self.g_centros, self.g_vms, self.g_contenedores, self.g_solicitudes)
        self.generador_xml = GeneradorXML(self.g_centros)
        
        # generador de reportes
        self.generador_reportes = GeneradorGraphviz(self.g_centros, self.g_vms)
    
    def ejecutar(self):
        """Inicia el sistema"""
        while True:
            self.menu_principal()
    
    def menu_principal(self):
        limpiar_pantalla()
        print("="*70)
        print("  CLOUDSYNC - SISTEMA DE GESTION EN LA NUBE")
        print("="*70)
        print("\n1. Cargar archivo XML")
        print("2. Gestión de centros de datos")
        print("3. Gestión de máquinas virtuales")
        print("4. Gestión de contenedores")
        print("5. Gestión de solicitudes")
        print("6. Generar reportes")
        print("7. Generar archivo XML de salida")
        print("8. Salir")
        print("="*70)
        
        opcion = input("\nSeleccione una opción: ").strip()
        
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
            print("\n¡Hasta luego!")
            exit(0)
        else:
            print("\n✗ Opción inválida")
            pausar()
    
    def cargar_xml(self):
        limpiar_pantalla()
        print("="*70)
        print("  CARGAR ARCHIVO XML")
        print("="*70)
        
        ruta = input("\nIngrese la ruta del archivo XML: ").strip()
        
        if not ruta:
            print("\n✗ Debe ingresar una ruta")
            pausar()
            return
        
        exito, msg = self.parser.cargar(ruta)
        print(f"\n{'✓' if exito else '✗'} {msg}")
        pausar()
    
    def menu_centros(self):
        while True:
            limpiar_pantalla()
            print("="*70)
            print("  GESTIÓN DE CENTROS DE DATOS")
            print("="*70)
            print("\n1. Listar todos los centros")
            print("2. Buscar centro por ID")
            print("3. Ver centro con más recursos")
            print("4. Volver al menú principal")
            print("="*70)
            
            op = input("\nSeleccione una opción: ").strip()
            
            if op == "1":
                self.listar_centros()
            elif op == "2":
                self.buscar_centro()
            elif op == "3":
                self.centro_mas_recursos()
            elif op == "4":
                break
            else:
                print("\n✗ Opción inválida")
                pausar()
    
    def listar_centros(self):
        limpiar_pantalla()
        self.g_centros.mostrar_todos_centros()
        pausar()
    
    def buscar_centro(self):
        limpiar_pantalla()
        id_c = input("\nIngrese ID del centro: ").strip()
        centro = self.g_centros.obtener_centro(id_c)
        
        if centro:
            centro.mostrar()
        else:
            print(f"\n✗ Centro {id_c} no encontrado")
        pausar()
    
    def centro_mas_recursos(self):
        limpiar_pantalla()
        centro = self.g_centros.centro_con_mayor_disponibilidad()
        
        if centro:
            print("\n>> Centro con mayor disponibilidad:")
            centro.mostrar()
        else:
            print("\n✗ No hay centros registrados")
        pausar()
    
    def menu_vms(self):
        while True:
            limpiar_pantalla()
            print("="*70)
            print("  GESTIÓN DE MÁQUINAS VIRTUALES")
            print("="*70)
            print("\n1. Buscar VM por ID")
            print("2. Listar VMs de un centro")
            print("3. Migrar VM entre centros")
            print("4. Volver al menú principal")
            print("="*70)
            
            op = input("\nSeleccione una opción: ").strip()
            
            if op == "1":
                self.buscar_vm()
            elif op == "2":
                self.listar_vms_centro()
            elif op == "3":
                self.migrar_vm()
            elif op == "4":
                break
            else:
                print("\n✗ Opción inválida")
                pausar()
    
    def buscar_vm(self):
        limpiar_pantalla()
        id_vm = input("\nIngrese ID de la VM: ").strip()
        vm = self.g_vms.obtener_vm(id_vm)
        
        if vm:
            vm.mostrar()
        else:
            print(f"\n✗ VM {id_vm} no encontrada")
        pausar()
    
    def listar_vms_centro(self):
        limpiar_pantalla()
        id_c = input("\nIngrese ID del centro: ").strip()
        vms = self.g_vms.listar_vms_de_centro(id_c)
        
        if vms is None:
            print(f"\n✗ Centro {id_c} no encontrado")
        elif vms.vacia():
            print(f"\n>> Centro {id_c} no tiene VMs")
        else:
            print(f"\n{'='*70}")
            print(f"  VMs DEL CENTRO {id_c}")
            print(f"{'='*70}")
            vms.listar_todo()
        pausar()
    
    def migrar_vm(self):
        limpiar_pantalla()
        print("="*70)
        print("  MIGRAR MÁQUINA VIRTUAL")
        print("="*70)
        
        id_vm = input("\nID de la VM a migrar: ").strip()
        id_destino = input("ID del centro destino: ").strip()
        
        exito, msg = self.g_vms.mover_vm_entre_centros(id_vm, id_destino)
        print(f"\n{'✓' if exito else '✗'} {msg}")
        pausar()
    
    def menu_contenedores(self):
        while True:
            limpiar_pantalla()
            print("="*70)
            print("  GESTIÓN DE CONTENEDORES")
            print("="*70)
            print("\n1. Desplegar contenedor en VM")
            print("2. Listar contenedores de una VM")
            print("3. Cambiar estado de contenedor")
            print("4. Eliminar contenedor")
            print("5. Volver al menú principal")
            print("="*70)
            
            op = input("\nSeleccione una opción: ").strip()
            
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
                print("\n✗ Opción inválida")
                pausar()
    
    def crear_contenedor(self):
        limpiar_pantalla()
        print("="*70)
        print("  DESPLEGAR CONTENEDOR")
        print("="*70)
        
        try:
            id_vm = input("\nID de la VM: ").strip()
            id_cont = input("ID del contenedor: ").strip()
            nombre = input("Nombre: ").strip()
            imagen = input("Imagen (ej. nginx:latest): ").strip()
            cpu_pct = int(input("CPU (porcentaje): "))
            ram_mb = int(input("RAM (MB): "))
            puerto = input("Puerto: ").strip()
            
            exito, msg = self.g_contenedores.crear_contenedor(id_cont, nombre, imagen, cpu_pct, ram_mb, puerto, id_vm)
            print(f"\n{'✓' if exito else '✗'} {msg}")
        except ValueError:
            print("\n✗ Valores numéricos inválidos")
        pausar()
    
    def listar_contenedores(self):
        limpiar_pantalla()
        id_vm = input("\nID de la VM: ").strip()
        conts = self.g_contenedores.obtener_contenedores_de_vm(id_vm)
        
        if conts is None:
            print(f"\n✗ VM {id_vm} no encontrada")
        elif conts.vacia():
            print(f"\n>> VM {id_vm} no tiene contenedores")
        else:
            print(f"\n{'='*70}")
            print(f"  CONTENEDORES DE {id_vm}")
            print(f"{'='*70}")
            conts.listar_todo()
        pausar()
    
    def cambiar_estado_contenedor(self):
        limpiar_pantalla()
        print("="*70)
        print("  CAMBIAR ESTADO DE CONTENEDOR")
        print("="*70)
        print("\nEstados válidos: Activo, Pausado, Detenido, Reiniciando")
        
        id_vm = input("\nID de la VM: ").strip()
        id_cont = input("ID del contenedor: ").strip()
        estado = input("Nuevo estado: ").strip()
        
        exito, msg = self.g_contenedores.cambiar_estado(id_cont, id_vm, estado)
        print(f"\n{'✓' if exito else '✗'} {msg}")
        pausar()
    
    def eliminar_contenedor(self):
        limpiar_pantalla()
        print("="*70)
        print("  ELIMINAR CONTENEDOR")
        print("="*70)
        
        id_vm = input("\nID de la VM: ").strip()
        