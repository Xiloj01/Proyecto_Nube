# GeneradorGraphviz.py
class GeneradorGraphviz:
    def __init__(self, g_centros, g_vms):
        self.g_centros = g_centros
        self.g_vms = g_vms

    def reporte_centros(self, ruta="reportes/centros.dot"):
        try:
            dot = []
            linea1 = "digraph CentrosDatos {"
            dot.append(linea1)
            dot.append('  rankdir=TB;')
            linea_nodo = '  node [shape=box, style="rounded,filled", fillcolor=lightblue];'
            dot.append(linea_nodo)
            dot.append('  graph [bgcolor=white];')
            dot.append('')
            linea_titulo = '  titulo [label="CENTROS DE DATOS\\nCloudSync", shape=note, fillcolor=gold, fontsize=16];'
            dot.append(linea_titulo)
            dot.append('')
            temp = self.g_centros.centros.cabeza
            while temp is not None:
                centro = temp.dato
                label = centro.id + "\\n" + centro.nombre + "\\n"
                cpu_info = "CPU: " + str(centro.cpu_disp) + "/" + str(centro.cpu_total)
                label = label + cpu_info + "\\n"
                ram_info = "RAM: " + str(centro.ram_disp) + "/" + str(centro.ram_total) + " GB"
                label = label + ram_info + "\\n"
                num_vms = centro.vms.obtener_tamanio()
                vms_info = "VMs: " + str(num_vms)
                label = label + vms_info
                linea_centro = '  ' + centro.id + ' [label="' + label + '"];'
                dot.append(linea_centro)
                linea_flecha = '  titulo -> ' + centro.id + ';'
                dot.append(linea_flecha)
                temp = temp.siguiente
            dot.append("}")
            archivo = open(ruta, 'w')
            contenido = '\n'.join(dot)
            archivo.write(contenido)
            archivo.close()
            mensaje = "Reporte: " + ruta
            return True, mensaje
        except Exception as e:
            error_msg = "Error: " + str(e)
            return False, error_msg

    def reporte_vms_centro(self, id_centro, ruta="reportes/vms_centro.dot"):
        try:
            centro = self.g_centros.obtener_centro(id_centro)
            if centro is None:
                msg = "Centro " + id_centro + " no existe"
                return False, msg
            dot = []
            dot.append("digraph VMsCentro {")
            dot.append('  rankdir=TB;')
            dot.append('  node [shape=box, style="rounded,filled"];')
            dot.append('')
            label_centro = centro.id + "\\n" + centro.nombre
            linea = '  centro [label="' + label_centro + '", fillcolor=lightblue, fontsize=14];'
            dot.append(linea)
            dot.append('')
            temp_vm = centro.vms.cabeza
            while temp_vm is not None:
                vm = temp_vm.dato
                label = vm.id + "\\n" + vm.nombre + "\\n" + vm.so + "\\n"
                cpu_disponible_str = f"{vm.cpu_disponible:.1f}"
                cpu_asig_str = str(vm.cpu_asig)
                cpu_texto = "CPU: " + cpu_disponible_str + "/" + cpu_asig_str
                label = label + cpu_texto + "\\n"
                ram_disponible_str = f"{vm.ram_disponible:.1f}"
                ram_asig_str = str(vm.ram_asig)
                ram_texto = "RAM: " + ram_disponible_str + "/" + ram_asig_str + " GB"
                label = label + ram_texto
                linea_vm = '  ' + vm.id + ' [label="' + label + '", fillcolor=lightgreen];'
                dot.append(linea_vm)
                linea_conexion = '  centro -> ' + vm.id + ';'
                dot.append(linea_conexion)
                temp_vm = temp_vm.siguiente
            dot.append("}")
            f = open(ruta, 'w')
            contenido = '\n'.join(dot)
            f.write(contenido)
            f.close()
            mensaje = "Reporte: " + ruta
            return True, mensaje
        except Exception as e:
            error_msg = "Error: " + str(e)
            return False, error_msg

    def reporte_contenedores_vm(self, id_vm, ruta="reportes/contenedores_vm.dot"):
        try:
            vm = self.g_vms.obtener_vm(id_vm)
            if vm is None:
                msg = "VM " + id_vm + " no existe"
                return False, msg
            dot = []
            dot.append("digraph ContenedoresVM {")
            dot.append('  rankdir=TB;')
            dot.append('  node [shape=box, style="rounded,filled"];')
            dot.append('')
            label_vm = vm.id + "\\n" + vm.nombre
            linea_vm = '  vm [label="' + label_vm + '", fillcolor=lightgreen, fontsize=14];'
            dot.append(linea_vm)
            dot.append('')
            temp_cont = vm.contenedores.cabeza  # ← Usa .cabeza
            while temp_cont is not None:
                cont = temp_cont.dato
                label = cont.id + "\\n" + cont.nombre + "\\n" + cont.imagen + "\\n"
                # ✅ CORREGIDO: usar cpu_pct, no cpu_porcentaje
                cpu_texto = "CPU: " + str(cont.cpu_pct) + "%"
                label = label + cpu_texto + "\\n"
                # ✅ CORREGIDO: usar ram_mb (ya estaba bien, pero verificamos)
                ram_texto = "RAM: " + str(cont.ram_mb) + " MB"
                label = label + ram_texto + "\\n"
                estado_texto = "Estado: " + cont.estado
                label = label + estado_texto
                color = "lightyellow"
                if cont.estado == "Activo":
                    color = "lightgreen"
                if cont.estado == "Pausado":
                    color = "orange"
                if cont.estado == "Detenido":
                    color = "lightcoral"
                linea_cont = '  ' + cont.id + ' [label="' + label + '", fillcolor=' + color + '];'
                dot.append(linea_cont)
                linea_conexion = '  vm -> ' + cont.id + ';'
                dot.append(linea_conexion)
                temp_cont = temp_cont.siguiente
            dot.append("}")
            archivo = open(ruta, 'w')
            texto = '\n'.join(dot)
            archivo.write(texto)
            archivo.close()
            mensaje = "Reporte: " + ruta
            return True, mensaje
        except Exception as e:
            error_msg = "Error: " + str(e)
            return False, error_msg

    def reporte_cola_solicitudes(self, cola, ruta="reportes/cola_solicitudes.dot"):
        try:
            dot = []
            dot.append("digraph ColaSolicitudes {")
            dot.append('  rankdir=LR;')
            dot.append('  node [shape=box, style="rounded,filled"];')
            dot.append('')
            dot.append('  inicio [label="COLA", shape=ellipse, fillcolor=gold];')
            dot.append('')
            temp = cola.frente
            anterior = "inicio"
            contador = 1
            while temp is not None:
                sol = temp.dato
                numero = "#" + str(contador)
                label = numero + "\\n" + sol.id + "\\n" + sol.cliente + "\\n"
                tipo_texto = "Tipo: " + sol.tipo
                label = label + tipo_texto + "\\n"
                prioridad_texto = "Prioridad: " + str(sol.prioridad)
                label = label + prioridad_texto
                color = "lightgreen"
                if sol.prioridad >= 8:
                    color = "red"
                elif sol.prioridad >= 5:  # ← Corregido: usar 'elif' para evitar conflicto
                    color = "orange"
                nombre_nodo = "sol" + str(contador)
                linea_nodo = '  ' + nombre_nodo + ' [label="' + label + '", fillcolor=' + color + '];'
                dot.append(linea_nodo)
                linea_conexion = '  ' + anterior + ' -> ' + nombre_nodo + ';'
                dot.append(linea_conexion)
                anterior = nombre_nodo
                temp = temp.siguiente
                contador = contador + 1
            esta_vacia = cola.vacia()
            if esta_vacia:
                dot.append('  vacio [label="(vacia)", shape=plaintext];')
                dot.append('  inicio -> vacio;')
            dot.append("}")
            archivo = open(ruta, 'w')
            contenido_completo = '\n'.join(dot)
            archivo.write(contenido_completo)
            archivo.close()
            mensaje = "Reporte: " + ruta
            return True, mensaje
        except Exception as e:
            error_msg = "Error: " + str(e)
            return False, error_msg