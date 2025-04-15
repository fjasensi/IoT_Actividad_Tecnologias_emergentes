# Sistema de Monitoreo Ambiental con ThingSpeak

Aplicación para gestionar datos de monitoreo ambiental utilizando la plataforma ThingSpeak.

Grado Ingeniería informática UNIR. Tecnologías emergentes.

## Características

- Lectura y visualización de datos ambientales desde ThingSpeak
- Carga de nuevos datos al canal
- Generación de gráficos para cada parámetro
- Gestión segura de claves API

## Instalación

1. Clona el repositorio:
   
   ```
   git clone https://github.com/fjasensi/IoT_Actividad_Tecnologias_emergentes.git
   cd IoT_Actividad_Tecnologias_emergentes
   ```

2. Crea un entorno virtual e instala las dependencias:
   
   ```
   make setup
   ```

## Configuración

Para utilizar esta aplicación, necesitas configurar las credenciales de tu canal ThingSpeak:

### Variables de entorno

Crea un archivo `.env` en el directorio principal (puedes copiar o renombrar .env.example):

```
THINGSPEAK_CHANNEL_ID=TU_CHANNEL_ID
THINGSPEAK_READ_API_KEY=TU_READ_API_KEY
THINGSPEAK_WRITE_API_KEY=TU_WRITE_API_KEY
```

> **⚠️ IMPORTANTE**: Nunca subas tus claves API a repositorios públicos. Asegúrate de que `.env` está incluido en tu archivo `.gitignore`.

## Uso

Ejecuta la aplicación con:

```
make run
```

La aplicación mostrará un menú con las siguientes opciones:

1. Ver últimas lecturas
2. Ver estado del canal
3. Añadir nueva lectura manualmente
7. Salir

## Licencia

[MIT](LICENSE)
