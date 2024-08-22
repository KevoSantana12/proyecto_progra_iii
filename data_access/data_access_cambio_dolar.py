import requests
from lxml import etree

class DataAccess:
    def __init__(self):
        self.token = "2MCN4ILC40"
        self.nombre = "Kevin Santana"
        self.correo = "klinarte258@gmail.com"
        self.subnivel = "N"

    def obtener_cambio(self, fecha, codigo_indicador) -> str:
        try:
            # Realizar la solicitud
            url = f'https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/ObtenerIndicadoresEconomicos'
            params = {
                'Indicador': codigo_indicador,
                'FechaInicio': fecha,
                'FechaFinal': fecha,
                'Nombre': self.nombre,
                'SubNiveles': self.subnivel,
                'CorreoElectronico': self.correo,
                'Token': self.token
            }
            respuesta_compra = requests.get(url, params=params)  
            
            # Se convierte la respuesta a XML
            root = etree.fromstring(respuesta_compra.content)
            
            # Se crean namespaces para ubicar las respuestas del servidor
            namespaces = {
                'diffgr': 'urn:schemas-microsoft-com:xml-diffgram-v1',
                'msdata': 'urn:schemas-microsoft-com:xml-msdata',
            }

            # Extraer el valor de NUM_VALOR y lo formatea para solo devolver 2 decimales
            num_valor_elements = root.xpath('//diffgr:diffgram/Datos_de_INGC011_CAT_INDICADORECONOMIC/INGC011_CAT_INDICADORECONOMIC/NUM_VALOR', namespaces=namespaces)
            if num_valor_elements:
                num_valor = float(num_valor_elements[0].text)
                num_valor_formateado = f"{num_valor:.2f}"
                return num_valor_formateado
            else:
                print("No se encontró el elemento NUM_VALOR")
                return "No se encontró el valor"

        except Exception as e:
            print(f'Error colectando la info: {e}')
            return "Error"
    