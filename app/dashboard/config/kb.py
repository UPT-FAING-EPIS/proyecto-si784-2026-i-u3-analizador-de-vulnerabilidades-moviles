APK_FINDING_KB = {
    "manifest": {
        "implicacion": "Sin el manifiesto principal, el sistema operativo Android no puede identificar los componentes, permisos, ni el punto de entrada de la aplicación, haciendo imposible su instalación o ejecución correcta.",
        "recommendation": "Verificar la integridad del archivo APK. Si fue compilado manualmente, asegúrese de que el archivo AndroidManifest.xml esté incluido correctamente en la raíz del paquete."
    },
    "dex": {
        "implicacion": "Los archivos DEX contienen el código compilado de la aplicación (Dalvik Executable). Su ausencia significa que la aplicación no contiene código ejecutable, lo cual indica que el archivo está corrupto o ha sido alterado.",
        "recommendation": "Validar la integridad del APK original y recompilar la aplicación asegurando que el proceso de compilación genere y empaquete las clases DEX."
    },
    "native_code": {
        "implicacion": "El uso de código nativo (.so) dificulta la ingeniería inversa estándar de Java/Kotlin, pero también aumenta el riesgo de vulnerabilidades de desbordamiento de memoria (buffer overflow) y puede utilizarse para ocultar comportamiento malicioso que evade la detección estática básica.",
        "recommendation": "Realizar un análisis dinámico y de desensamblado (con herramientas como Ghidra o IDA Pro) sobre las librerías nativas encontradas para verificar su comportamiento."
    },
    "insecure_communication": {
        "implicacion": "Las conexiones HTTP sin cifrar transmiten toda la información en texto plano. Un atacante en la misma red (como Wi-Fi público) puede interceptar o modificar el tráfico (ataques Man-in-the-Middle), robando credenciales, tokens o datos sensibles.",
        "recommendation": "Forzar el uso de HTTPS en todos los endpoints de comunicación. Implementar Network Security Config en Android para bloquear explícitamente el tráfico en texto plano."
    },
    "hardcoded_secret": {
        "implicacion": "Los secretos embebidos en el código (API Keys, tokens, contraseñas) son de fácil acceso mediante descompilación básica. Un atacante puede extraerlos y utilizarlos para acceder a servicios en la nube de terceros, APIs privadas o bases de datos a nombre de la aplicación.",
        "recommendation": "Eliminar todas las claves del código fuente. Utilizar servicios de gestión de secretos en el backend o implementar mecanismos de autenticación dinámica (OAuth, App Attest) para proteger los recursos."
    }
}

APK_ARTIFACT_KB = {
    "dex_count": {
        "titulo": "Cantidad de archivos DEX",
        "descripcion": "Indica el número de archivos Dalvik Executable (DEX) compilados dentro de la aplicación. Los archivos DEX contienen el código fuente de Java/Kotlin compilado en bytecode ejecutable por la máquina virtual de Android.",
        "recommendation": "Si el número de archivos DEX es alto (MultiDex), indica una base de código grande. Se recomienda habilitar la minificación y obfuscación (ProGuard/R8) en el archivo build.gradle para eliminar código no utilizado y reducir el tamaño total del APK."
    },
    "file_count": {
        "titulo": "Número de archivos totales",
        "descripcion": "El recuento total de archivos (código compilado, recursos, imágenes, layouts XML, manifiestos) contenidos en el paquete APK comprimido.",
        "recommendation": "Auditar periódicamente los recursos del proyecto. Elimine imágenes, layouts u otros archivos no utilizados (usando herramientas como Android Lint o habilitando 'shrinkResources' en Gradle) para optimizar el peso del APK."
    },
    "native_library": {
        "titulo": "Biblioteca nativa (.so)",
        "descripcion": "Archivos binarios de biblioteca compartida compilados en C/C++ usando el NDK para arquitecturas específicas de hardware (como ARM64 o x86). Se utilizan habitualmente para procesamiento de alta velocidad o integración de código binario de bajo nivel.",
        "recommendation": "Dado que las librerías nativas pueden ocultar código malicioso y son susceptibles a fallos de desbordamiento de memoria, se aconseja desensamblarlas (con Ghidra o IDA Pro) y auditar de forma estática su comportamiento y llamadas a APIs nativas de red."
    },
    "url": {
        "titulo": "URL encontrada",
        "descripcion": "Direcciones web o endpoints descubiertos dentro de las cadenas de texto del código o los recursos del APK. Suelen corresponder a APIs de backend de la aplicación, recursos externos, licencias de librerías o dominios de terceros.",
        "recommendation": "Verificar que todas las URLs detectadas pertenezcan a servidores o servicios legítimos controlados. Asegúrese de que todos los endpoints utilicen HTTPS en producción y bloquee conexiones a hosts no reconocidos."
    }
}
