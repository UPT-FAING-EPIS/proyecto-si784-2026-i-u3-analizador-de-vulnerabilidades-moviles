# language: es
Característica: Escaneo de APK mediante ingeniería inversa
  Como analista de seguridad
  Quiero subir un archivo APK al sistema
  Para identificar vulnerabilidades en el código y configuración

  Escenario: Análisis exitoso de un APK válido
    Dado que el usuario inicio sesion
    Cuando sube un archivo APK valido
    Y presiona el boton de analizar
    Entonces el sistema registra el escaneo
    Y muestra los hallazgos encontrados

  Escenario: Rechazo de archivo inválido
    Cuando intenta analizar un archivo que no es APK
    Entonces el sistema rechaza el archivo
    Y muestra un mensaje de error claro