import xml.etree.ElementTree as ET

class ParserXML:
    """Procesa archivos XML de entrada"""

    def __init__(self, controlador_centros, controlador_vms, controlador_solicitudes):
        self.controlador_centros = controlador_centros
        self.controlador_vms = controlador_vms
        self.controlador_solicitudes = controlador_solicitudes

    def cargar_archivo(self, ruta):
        """Carga y procesa un archivo XML"""
        try:
            tree = ET.parse(ruta)
            root = tree.getroot()

            # Procesar configuración
            self._procesar_centros(root)
            self._procesar_vms(root)
            self._procesar_solicitudes(root)

            # Procesar instrucciones
            self._procesar_instrucciones(root)

            return True, "Archivo XML cargado exitosamente"
        except Exception as e:
            return False, f"Error al cargar XML: {str(e)}"

    def _procesar_centros(self, root):
        """Procesa la sección de centros de datos"""
        centros = root.find("./centrosDatos")
        if centros is None:
            return

        for centro_elem in centros.findall("centro"):
            id_centro = centro_elem.get("id")
            nombre = centro_elem.get("nombre")

            ubicacion = centro_elem.find("ubicacion")
            pais = ubicacion.find("pais").text
            ciudad = ubicacion.find("ciudad").text

            capacidad = centro_elem.find("capacidad")
            cpu = int(capacidad.find("cpu").text)
            ram = int(capacidad.find("ram").text)
            almacenamiento = int(capacidad.find("almacenamiento").text)

            self.controlador_centros.crear_centro(
                id_centro, nombre, pais, ciudad, cpu, ram, almacenamiento
            )

    def _procesar_vms(self, root):
        """Procesa la sección de máquinas virtuales"""
        vms = root.find("./maquinasVirtuales")
        if vms is None:
            return

        for vm_elem in vms.findall("vm"):
            id_vm = vm_elem.get("id")
            nombre = vm_elem.get("nombre")
            so = vm_elem.find("so").text
            ip = vm_elem.find("ip").text

            recursos = vm_elem.find("recursos")
            cpu = int(recursos.find("cpu").text)
            ram = int(recursos.find("ram").text)
            almacenamiento = int(recursos.find("almacenamiento").text)

            # Buscar el centro asignado
            centro_asignado = vm_elem.get("centroAsignado")
            centro = self.controlador_centros.buscar_centro(centro_asignado)

            if centro:
                # Crear la VM en el controlador
                exito, msg = self.controlador_vms.crear_vm(id_vm, nombre, so, ip, cpu, ram, almacenamiento, ip, centro.id)
                if not exito:
                    print(f"Error al cargar VM {id_vm}: {msg}")
            else:
                print(f"Centro asignado no encontrado para VM {id_vm}: {centro_asignado}")

    def _procesar_solicitudes(self, root):
        """Procesa la sección de solicitudes"""
        solicitudes = root.find("./solicitudes")
        if solicitudes is None:
            return

        for sol_elem in solicitudes.findall("solicitud"):
            id_solicitud = sol_elem.get("id")
            tipo = sol_elem.find("tipo").text
            prioridad = sol_elem.find("prioridad").text
            tiempo_estimado = int(sol_elem.find("tiempoEstimado").text)

            recursos = sol_elem.find("recursos")
            cpu = int(recursos.find("cpu").text)
            ram = int(recursos.find("ram").text)
            almacenamiento = int(recursos.find("almacenamiento").text)

            # Agregar la solicitud al controlador
            exito, msg = self.controlador_solicitudes.agregar_solicitud(
                id_solicitud, tipo, prioridad, tiempo_estimado, cpu, ram, almacenamiento
            )
            if not exito:
                print(f"Error al cargar solicitud {id_solicitud}: {msg}")

    def _procesar_instrucciones(self, root):
        """Procesa la sección de instrucciones"""
        instrucciones = root.find("./instrucciones")
        if instrucciones is None:
            return

        for inst in instrucciones.findall("instruccion"):
            tipo = inst.find("tipo").text

            if tipo == "crearVM":
                self._ejecutar_crear_vm(inst)
            elif tipo == "migrarVM":
                self._ejecutar_migrar_vm(inst)
            elif tipo == "procesarSolicitudes":
                self._ejecutar_procesar_solicitudes(inst)

    def _ejecutar_crear_vm(self, inst):
        """Ejecuta instrucción de crear VM"""
        id_vm = inst.find("idVm").text
        nombre = inst.find("nombre").text
        so = inst.find("so").text
        ip = inst.find("ip").text

        recursos = inst.find("recursos")
        cpu = int(recursos.find("cpu").text)
        ram = int(recursos.find("ram").text)
        almacenamiento = int(recursos.find("almacenamiento").text)

        centro_id = inst.find("centroId").text

        exito, msg = self.controlador_vms.crear_vm(id_vm, nombre, so, ip, cpu, ram, almacenamiento, ip, centro_id)
        print(f"{'✓' if exito else 'X'} {msg}")

    def _ejecutar_migrar_vm(self, inst):
        """Ejecuta instrucción de migrar VM"""
        vm_id = inst.find("vmId").text
        destino = inst.find("centroDestino").text

        exito, msg = self.controlador_vms.migrar_vm(vm_id, destino)
        print(f"{'✓' if exito else 'X'} {msg}")

    def _ejecutar_procesar_solicitudes(self, inst):
        """Ejecuta instrucción de procesar solicitudes"""
        cantidad = int(inst.find("cantidad").text)

        exito, msg = self.controlador_solicitudes.procesar_n_solicitudes(cantidad)
        print(f"{'✓' if exito else 'X'} {msg}")
