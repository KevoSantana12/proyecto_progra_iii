from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

load_dotenv()

class EnvioCorreo:
    def __init__(self):
        self.password = "hzmj jmxf whxw gjjc"
    
    def envioCorreo(self, email_reciver=None, empleado=None, rebajos=None):
        email_sender = 'planillaplushelp@gmail.com'
        
        subject = f'Reporte Salario de {empleado}'
        body = f'Abajo encontrarás el reporte de salario de {empleado}.'
        
        # Redondeando los valores a dos decimales
        salario_bruto = round(rebajos['salario_bruto'], 2)
        impuesto_renta = round(rebajos['impuesto_renta'], 2)
        ivm = round(rebajos['ivm'], 2)
        sem = round(rebajos['sem'], 2)
        lpt = round(rebajos['lpt'], 2)
        total_impuestos = round(rebajos['total_impuestos'], 2)
        salario_neto = round(rebajos['salario_neto'], 2)
        aporte_patronal = round(rebajos['aporte_patronal'], 2)

        html_body = f"""
        <html>
        <body>
            <h2>Reporte de Salario de {empleado}</h2>
            <p>Estimado/a {empleado},</p>
            <p>A continuación se detallan los rebajos salariales:</p>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>Concepto</th>
                    <th>Monto</th>
                </tr>
                <tr>
                    <td>Salario bruto</td>
                    <td>{salario_bruto} CRC</td>
                </tr>
                <tr>
                    <td>Impuesto sobre la Renta</td>
                    <td>{impuesto_renta} CRC</td>
                </tr>
                <tr>
                    <td>Seguro de Invalidez, Vejez y Muerte (IVM)</td>
                    <td>{ivm} CRC</td>
                </tr>
                <tr>
                    <td>Seguro de Enfermedad y Maternidad (SEM)</td>
                    <td>{sem} CRC</td>
                </tr>
                <tr>
                    <td>Levantamiento Patrimonial Tributario (LPT)</td>
                    <td>{lpt} CRC</td>
                </tr>
                <tr>
                    <td>Total Rebajos</td>
                    <td>{total_impuestos} CRC</td>
                </tr>
                <tr>
                    <td>Salario neto</td>
                    <td>{salario_neto} CRC</td>
                </tr>
                <tr>
                    <td>Aporte patronal</td>
                    <td>{aporte_patronal} CRC</td>
                </tr>
            </table>
            <p>Por favor, si tienes alguna pregunta, no dudes en contactarnos.</p>
            <p>Saludos cordiales,</p>
            <p>Planilla Plus</p>
        </body>
        </html>
        """
        
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_reciver
        em['Subject'] = subject
        em.set_content(body)
        em.add_alternative(html_body, subtype='html')

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, self.password)
            smtp.send_message(em)
