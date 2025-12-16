#parser_xml.py
import xml.etree.ElementTree as ET

class ParserXML:
    
    def __init__(self, gestor_centros, gestor_vms, gestor_contenedores, gestor_solicitudes):
        self.g_centros = gestor_centros
        self.g_vms = gestor_vms
        self.g_contenedores = gestor_contenedores
        self.g_solicitudes = gestor_solicitudes
    
    def cargar_archivo(self, ruta):
        # cargo y proceso el archivo xml
        try:
            # parseo el archivo
            arbol = ET.parse(ruta)
            raiz = arbol.getroot()
            
            # muestro mensaje
            print(f"\n{'='*70}")
            print("CARGANDO ARCHIVO XML")
            print(f"{'='*70}")
            
            # busco la configuracion
            config = raiz.find('configuracion')
            if config is not None:
                # proceso cada parte
                self._procesar_centros(config)
                self._procesar_vms(config)
                self._procesar_solicitudes(config)
            
            # ahora proceso las instrucciones
            instrucciones = raiz.find('instrucciones')
            if instrucciones is not None:
                self._ejecutar_instrucciones(instrucciones)
            
            # muestro mensaje de exito
            print(f"\n{'='*70}")
            print("ARCHIVO CARGADO EXITOSAMENTE")
            print(f"{'='*70}")
            
            return True
            
        except FileNotFoundError:
            print(f"\n[ERROR] Archivo no encontrado: {ruta}")
            return False
        except ET.ParseError:
            print(f"\n[ERROR] Error al parsear XML")
            return False
        except Exception as error:
            mensaje = str(error)
            print(f"\n[ERROR] {mensaje}")
            return False
    
    def _procesar_centros(self, config):
        # proceso todos los centros de datos
        centros = config.find('centrosDatos')
        if centros is None:
            return
        
        print("\n[Procesando Centros de Datos]")
        
        # recorro cada centro
        for centro in centros.findall('centro'):
            # obtengo atributos
            id_c = centro.get('id')
            nombre = centro.get('nombre')
            
            # obtengo ubicacion
            ubicacion = centro.find('ubicacion')
            pais = ubicacion.find('pais').text
            ciudad = ubicacion.find('ciudad').text
            
            # obtengo capacidad
            capacidad = centro.find('capacidad')
            cpu = capacidad.find('cpu').text
            ram = capacidad.find('ram').text
            almacen = capacidad.find('almacenamiento').text
            
            # muestro info
            print(f"  - Centro: {id_c}")
            print(f"    Nombre: {nombre}")
            print(f"    Ubicacion: {ciudad}, {pais}")
            print(f"    CPU: {cpu}, RAM: {ram}GB, Almacen: {almacen}GB")
            
            # intento agregar el centro
            exito, msg = self.g_centros.agregar_centro(id_c, nombre, pais, ciudad, cpu, ram, almacen)
            if exito:
                print(f"    >> {msg}")
            else:
                print(f"    >> ERROR: {msg}")
    
    def _procesar_vms(self, config):
        # proceso todas las maquinas virtuales
        vms = config.find('maquinasVirtuales')
        if vms is None:
            return
        
        print("\n[Procesando Maquinas Virtuales]")
        
        # recorro cada vm
        for vm in vms.findall('vm'):
            # obtengo datos basicos
            id_vm = vm.get('id')
            centro_asig = vm.get('centroAsignado')
            
            # sistema operativo e ip
            so = vm.find('sistemaOperativo').text
            ip = vm.find('ip').text
            
            # recursos de la vm
            recursos = vm.find('recursos')
            cpu = recursos.find('cpu').text
            ram = recursos.find('ram').text
            almacen = recursos.find('almacenamiento').text
            
            # muestro informacion
            print(f"  - VM: {id_vm}")
            print(f"    SO: {so}")
            print(f"    IP: {ip}")
            print(f"    Centro: {centro_asig}")
            print(f"    CPU: {cpu}, RAM: {ram}GB, Almacen: {almacen}GB")
            
            # creo la vm
            nombre_vm = f"VM-{id_vm}"
            exito, msg = self.g_vms.agregar_vm(id_vm, nombre_vm, so, ip, cpu, ram, almacen, centro_asig)
            
            if exito:
                print(f"    >> {msg}")
                
                # ahora proceso los contenedores de esta vm
                contenedores = vm.find('contenedores')
                if contenedores is not None:
                    self._procesar_contenedores(contenedores, id_vm)
            else:
                print(f"    >> ERROR: {msg}")
    
    def _procesar_contenedores(self, contenedores, id_vm):
        # proceso los contenedores de una vm
        for cont in contenedores.findall('contenedor'):
            # obtengo datos del contenedor
            id_cont = cont.get('id')
            nombre = cont.find('nombre').text
            imagen = cont.find('imagen').text
            puerto = cont.find('puerto').text
            
            # obtengo recursos
            recursos = cont.find('recursos')
            cpu_pct = recursos.find('cpu').text
            ram_mb = recursos.find('ram').text
            
            # muestro info
            print(f"      * Contenedor: {id_cont}")
            print(f"        Nombre: {nombre}, Imagen: {imagen}")
            print(f"        CPU: {cpu_pct}%, RAM: {ram_mb}MB, Puerto: {puerto}")
            
            # intento crear el contenedor
            exito, msg = self.g_contenedores.crear_contenedor(
                id_cont, nombre, imagen, int(cpu_pct), int(ram_mb), puerto, id_vm
            )
            
            if exito:
                print(f"        >> {msg}")
            else:
                print(f"        >> ERROR: {msg}")
                
    def _procesar_solicitudes(self, config):
        # proceso todas las solicitudes
        solicitudes = config.find('solicitudes')
        if solicitudes is None:
            return
        
        print("\n[Procesando Solicitudes]")
        
        # recorro cada solicitud
        for sol in solicitudes.findall('solicitud'):
            # datos de la solicitud
            id_sol = sol.get('id')
            cliente = sol.find('cliente').text
            tipo = sol.find('tipo').text
            prioridad = sol.find('prioridad').text
            tiempo = sol.find('tiempoEstimado').text
            
            # recursos necesarios
            recursos = sol.find('recursos')
            cpu = recursos.find('cpu').text
            ram = recursos.find('ram').text
            almacen = recursos.find('almacenamiento').text
            
            # muestro info
            print(f"  - Solicitud: {id_sol}")
            print(f"    Cliente: {cliente}")
            print(f"    Tipo: {tipo}, Prioridad: {prioridad}")
            print(f"    CPU: {cpu}, RAM: {ram}GB, Almacen: {almacen}GB")
            print(f"    Tiempo estimado: {tiempo} min")
            
            # agrego la solicitud a la cola
            exito, msg = self.g_solicitudes.nueva_solicitud(
                id_sol, cliente, tipo, prioridad, cpu, ram, almacen, tiempo
            )
            
            if exito:
                print(f"    >> {msg}")
            else:
                print(f"    >> ERROR: {msg}")
    
    def _ejecutar_instrucciones(self, instrucciones):
        # ejecuto las instrucciones del xml
        print("\n[Ejecutando Instrucciones]")
        
        # recorro cada instruccion
        for inst in instrucciones.findall('instruccion'):
            tipo = inst.get('tipo')
            
            print(f"\n  >> Instruccion: {tipo}")
            
            # ejecuto segun el tipo
            if tipo == "crearVM":
                self._instruccion_crear_vm(inst)
            elif tipo == "migrarVM":
                self._instruccion_migrar_vm(inst)
            elif tipo == "procesarSolicitudes":
                self._instruccion_procesar_solicitudes(inst)
            else:
                print(f"     ERROR: Tipo de instruccion desconocida")
    
    def _instruccion_crear_vm(self, inst):
        # ejecuto instruccion de crear vm
        id_vm = inst.find('id').text
        centro = inst.find('centro').text
        so = inst.find('so').text
        cpu = inst.find('cpu').text
        ram = inst.find('ram').text
        almacen = inst.find('almacenamiento').text
        
        # genero ip automatica
        total = self.g_vms.todas_vms.obtener_tamanio()
        ip = f"192.168.1.{100 + total}"
        
        # genero nombre
        nombre = f"VM-{id_vm}"
        
        # muestro info
        print(f"     Creando VM {id_vm} en {centro}")
        print(f"     SO: {so}, IP: {ip}")
        print(f"     CPU: {cpu}, RAM: {ram}GB, Almacen: {almacen}GB")
        
        # intento crear la vm
        exito, msg = self.g_vms.agregar_vm(id_vm, nombre, so, ip, cpu, ram, almacen, centro)
        
        if exito:
            print(f"     ✓ {msg}")
        else:
            print(f"     ✗ {msg}")
    
    def _instruccion_migrar_vm(self, inst):
        # ejecuto instruccion de migrar vm
        vm_id = inst.find('vmId').text
        origen = inst.find('centroOrigen').text
        destino = inst.find('centroDestino').text
        
        # muestro info
        print(f"     Migrando VM {vm_id}")
        print(f"     Origen: {origen} -> Destino: {destino}")
        
        # intento migrar
        exito, msg = self.g_vms.mover_vm_entre_centros(vm_id, destino)
        
        if exito:
            print(f"     ✓ {msg}")
        else:
            print(f"     ✗ {msg}")
    
    def _instruccion_procesar_solicitudes(self, inst):
        # ejecuto instruccion de procesar solicitudes
        cantidad = int(inst.find('cantidad').text)
        
        print(f"     Procesando {cantidad} solicitud(es)")
        
        # proceso las solicitudes
        exito, msg = self.g_solicitudes.procesar_varias(cantidad)
        
        # no imprimo nada aca porque procesar_varias ya lo hace