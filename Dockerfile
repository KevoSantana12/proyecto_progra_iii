# Usamos la imagen base de Python 3
FROM python:3

# Actualizamos y mejoramos el sistema
RUN apt -qq -y update \
    && apt -qq -y upgrade \
    && apt-get install -y build-essential python3-dev

# Definimos una variable de entorno con el directorio de la app
ENV APP /app

# Creamos el directorio de la app y establecemos el directorio de trabajo
RUN mkdir $APP
WORKDIR $APP

# Exponemos el puerto que uWSGI escuchará
EXPOSE 56734

# Copiamos el archivo de requisitos y lo usamos para instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código fuente en el contenedor
COPY . .

# Ejecutamos uWSGI con el archivo de configuración app.ini
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:8000"]

