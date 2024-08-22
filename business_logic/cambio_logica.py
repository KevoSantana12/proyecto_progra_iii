from data_access.data_access_cambio_dolar import DataAccess
from datetime import datetime

class CambioLogica:
    def __init__(self) -> None:
        self.data_access = DataAccess()

    def cambio_formato_fechas(self, fecha) -> str:
        return fecha.strftime('%d/%m/%Y')
    
    def cambio_venta(self, fecha) -> int:
        try:
            fechaF = self.cambio_formato_fechas(fecha=fecha)
            return self.data_access.obtener_cambio(fechaF, 318)
        except Exception as e:
            print(f'Error en cambio_venta: {e}')
            return "Error en cambio_venta"