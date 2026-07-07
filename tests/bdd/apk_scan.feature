# language: es
Característica: Analisis de APK
  Como usuario autenticado
  Quiero subir un APK al sistema
  Para conocer sus vulnerabilidades moviles

  Escenario: Escaneo exitoso de APK
    Dado que el usuario inicio sesion
    Cuando sube un archivo APK valido
    Y presiona el boton de analizar
    Entonces el sistema registra el escaneo
    Y muestra los hallazgos encontrados

  Escenario: Archivo invalido
    Dado que el usuario inicio sesion
    Cuando intenta analizar un archivo que no es APK
    Entonces el sistema rechaza el archivo
    Y muestra un mensaje de error claro
