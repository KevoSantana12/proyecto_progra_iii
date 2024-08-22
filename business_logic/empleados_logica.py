from data_access.data_access_db import EmpleadoCRUD
from entities.entities import Empleado
from decimal import Decimal
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class Empleado_logica:

    #Empleados CRUD
    def __init__(self):
        self.data_access = EmpleadoCRUD()

    def crear_empleado(self, empleado: Empleado):
        self.data_access.insertar_empleados(empleado=empleado)
    
    def get_empleados_por_user_id(self, user_id: int):
        return self.data_access.obtener_empleados_por_user_id(user_id=user_id)
    
    def get_empleados_por_id(self, empleados_id: int) -> Empleado:
        return self.data_access.obtener_empleados_por_id(id=empleados_id)
    
    def editar_empleado(self, empleadoeditado:Empleado, id:int):
        empleado = self.get_empleados_por_id(id)
        if empleado:
            empleado.nombre = empleadoeditado.nombre
            empleado.apellido = empleadoeditado.apellido
            empleado.email = empleadoeditado.email
            empleado.telefono = empleadoeditado.telefono
            empleado.salarioBruto = empleadoeditado.salarioBruto
            empleado.posicion = empleadoeditado.posicion
            empleado.userId = empleadoeditado.userId
            self.data_access.actualizar_empleado(empleado)
        else:
            print(f"No se encontró un empleado con ID {id}")

    def borrar_empleado(self, id:int):
        self.data_access.eliminar_empleado(id=id)

    #Funciones
    def cantidad_empleados(self, user_id:int):
        return self.data_access.obtener_cantidad_empleados_por_user_id(user_id=user_id)

    def sumaSalarios(self, user_id:int):
        return self.data_access.obtener_suma_salarios_por_user_id(user_id=user_id)

    #Calculo de impuestos
    def impuesto_renta(self, salario_bruto: int) -> Decimal:
        if salario_bruto <= 929000:
            impuesto_renta = Decimal(0)
        elif salario_bruto <= 1363000:
            exceso = Decimal(salario_bruto) - Decimal(929000)
            impuesto_renta = exceso * Decimal(0.10)
        elif salario_bruto <= 2392000:
            exceso = Decimal(salario_bruto) - Decimal(1363000)
            impuesto_renta = (Decimal(1363000) - Decimal(929000)) * Decimal(0.10) + exceso * Decimal(0.15)
        elif salario_bruto <= 4783000:
            exceso = Decimal(salario_bruto) - Decimal(2392000)
            impuesto_renta = (Decimal(1363000) - Decimal(929000)) * Decimal(0.10) + (Decimal(2392000) - Decimal(1363000)) * Decimal(0.15) + exceso * Decimal(0.20)
        else:
            exceso = Decimal(salario_bruto) - Decimal(4783000)
            impuesto_renta = (Decimal(1363000) - Decimal(929000)) * Decimal(0.10) + (Decimal(2392000) - Decimal(1363000)) * Decimal(0.15) + (Decimal(4783000) - Decimal(2392000)) * Decimal(0.20) + exceso * Decimal(0.25)
        return impuesto_renta
    
    def ivm(self, salario_bruto: int) -> Decimal:
        return Decimal(salario_bruto) * Decimal(0.0334)
    
    def sem(self, salario_bruto: int) -> Decimal:
        return Decimal(salario_bruto) * Decimal(0.055)
    
    def lpt(self, salario_bruto: int) -> Decimal:
        return Decimal(salario_bruto) * Decimal(0.01)
    
    def aporte_banco_popular(self, salario_bruto: int) -> Decimal:
        return Decimal(salario_bruto) * Decimal(0.01)
    
    def aporte_patronal(self, salario_bruto: int) -> Decimal:
        return Decimal(salario_bruto) * Decimal(0.1433)
    
    def total_impuestos(self, salario_bruto: int) -> Decimal:
        total_impuestos = self.impuesto_renta(salario_bruto) + self.ivm(salario_bruto) + self.sem(salario_bruto) + self.lpt(salario_bruto)
        return total_impuestos

    def salario_neto(self, salario_bruto: int) -> Decimal:
        salario_neto = Decimal(salario_bruto) - self.total_impuestos(salario_bruto)
        return salario_neto

    #Creacion de pdfs
    #Este es para el registro individual
    def generar_pdf_nomina(self, tipo='individual', fecha=None, empleado=None):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, title=f'Comprobante de pago {empleado.nombre} {empleado.apellido}')
        elements = []
        styles = getSampleStyleSheet()
        estilo_titulo = styles['Heading1']
        estilo_normal = styles['BodyText']

        # Título
        if tipo == 'general':
            titulo = Paragraph("Planilla General de Nóminas", estilo_titulo)
        else:
            titulo = Paragraph("Comprobante de Pago Individual", estilo_titulo)
        periodo = Paragraph(f'Fecha: {fecha}', estilo_normal)
        elements.append(titulo)
        elements.append(Spacer(1, 12))
        elements.append(periodo)
        elements.append(Spacer(1, 12))

        # Datos Generales
        datos_generales = [
            [Paragraph("<b>Datos Generales</b>", estilo_normal)],
            [f'Posición: {empleado.posicion}'],
            [f'Nombre: {empleado.nombre} {empleado.apellido}']
        ]

        tabla_datos_generales = Table(datos_generales, colWidths=[450])
        tabla_datos_generales.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (1, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (1, 1), (-1, -1), 6),
            ('LINEABOVE', (0, 1), (-1, 1), 1, colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.grey),
        ]))
        elements.append(tabla_datos_generales)
        elements.append(Spacer(1, 12))

        # Deducciones
        deducciones = [
            [Paragraph("<b>Deducciones</b>", estilo_normal), Paragraph("<b>Monto</b>", estilo_normal)],
            ["Impuesto renta", f'{round(self.impuesto_renta(empleado.salarioBruto), 2)}'],
            ["IVM", f'{round(self.ivm(empleado.salarioBruto), 2)}'],
            ["Sem", f'{round(self.sem(empleado.salarioBruto), 2)}'],
            ["Lpt", f'{round(self.lpt(empleado.salarioBruto), 2)}'],
            [Paragraph("<b>Total deducciones</b>", estilo_normal), f'{round(self.total_impuestos(empleado.salarioBruto), 2)}'],
            ["Aporte patronal", f'{round(self.aporte_patronal(empleado.salarioBruto), 2)}']
        ]

        tabla_deducciones = Table(deducciones, colWidths=[250, 200])
        tabla_deducciones.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (1, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (1, 1), (-1, -1), 6),
            ('LINEABOVE', (0, 1), (-1, 1), 1, colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.grey),
        ]))
        elements.append(tabla_deducciones)
        elements.append(Spacer(1, 12))

        # Total a Pagar
        total_a_pagar = Paragraph(f"<b>Total salario:</b> {round(self.salario_neto(empleado.salarioBruto), 2)}", estilo_normal)
        elements.append(total_a_pagar)

        # Generar PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
        
    def generar_pdf_planilla_general(self, id: int, empresa:str):
    # Obtener la lista de empleados por ID
        nominas = self.get_empleados_por_user_id(id)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, title="Empleados")
        elements = []

        # Estilo
        styles = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle(
            name='CenteredTitle',
            fontName='Helvetica-Bold',
            fontSize=14,
            alignment=1,  # Centered
            spaceAfter=12
        )

        estilo_empresa = ParagraphStyle(
            name='CenteredTitle',
            fontName='Helvetica-Bold',
            fontSize=10,
            alignment=1,  # Centered
            spaceAfter=12
        )
        estilo_normal = styles['BodyText']
        titulo = Paragraph(f'{empresa}', estilo_titulo)
        elements.append(titulo)
        nombreEmpresa = Paragraph("Planilla General de Empleados", estilo_empresa)
        elements.append(nombreEmpresa)
        encabezado_tabla = [
            ["Nombre", "Posición", "Número", "Salario Bruto"]
        ]

        # Filas de la tabla
        filas_tabla = []
        for nomina in nominas:
            empleado = nomina
            filas_tabla.append([
                f"{empleado.nombre} {empleado.apellido}",
                empleado.posicion,
                empleado.telefono,
                f"{round(empleado.salarioBruto, 2):,.2f}" 
            ])

        # Crear la tabla con anchos de columna ajustados
        tabla = Table(encabezado_tabla + filas_tabla, colWidths=[200, 150, 100, 100])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(tabla)

        # Generar PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer