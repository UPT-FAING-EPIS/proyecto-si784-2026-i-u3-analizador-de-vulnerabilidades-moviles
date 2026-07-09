[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/hxeZOVSv)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=24118044)

# AnzenCore – Analizador de Vulnerabilidades Móviles

Sistema diseñado para detectar y reportar vulnerabilidades en aplicaciones móviles mediante análisis estático y dinámico.

---

## 1. Diagrama de Casos de Uso

```mermaid
flowchart LR
    %% Actores
    Usuario([Usuario])
    Administrador([Administrador])
    
    %% Casos de Uso
    SubirAPK(Subir aplicación APK)
    VerReporte(Visualizar Reporte de Vulnerabilidades)
    Exportar(Exportar Resultados)
    GestReglas(Gestionar Reglas de Escaneo)
    VerEst(Ver Estadísticas Generales)
    IniciarEscaneo(Iniciar Escaneo Estático)
    
    %% Relaciones
    Usuario --> SubirAPK
    Usuario --> VerReporte
    Usuario --> Exportar
    
    Administrador --> GestReglas
    Administrador --> VerEst
    
    SubirAPK -. "<<include>>" .-> IniciarEscaneo
```

## 2. Diagrama de Secuencia (Escaneo de APK)

```mermaid
sequenceDiagram
    actor Usuario
    participant InterfazWeb as Frontend UI
    participant APIGateway as API Gateway
    participant Scanner as Motor de Análisis
    participant DB as Base de Datos

    Usuario->>+InterfazWeb: Sube archivo APK
    InterfazWeb->>+APIGateway: POST /api/scan (APK)
    APIGateway->>+Scanner: Iniciar análisis de seguridad
    Scanner->>Scanner: Extraer código (Decompilación)
    Scanner->>Scanner: Ejecutar Semgrep / Snyk
    Scanner->>+DB: Guardar resultados del análisis
    DB-->>-Scanner: OK
    Scanner-->>-APIGateway: Resultados Listos (ID)
    APIGateway-->>-InterfazWeb: 200 OK (Reporte JSON)
    InterfazWeb-->>-Usuario: Muestra Dashboard con Vulnerabilidades
```

## 3. Diagrama de Clases

```mermaid
classDiagram
    class Usuario {
        +String idUsuario
        +String nombre
        +subirAPK()
        +verReporte()
    }
    
    class Analizador {
        +String apkPath
        +List~Regla~ reglas
        +iniciarEscaneoEstático()
        +iniciarEscaneoDinámico()
    }
    
    class Reporte {
        +String idReporte
        +Date fecha
        +List~Vulnerabilidad~ vulnerabilidades
        +generarPDF()
        +generarHTML()
    }
    
    class Vulnerabilidad {
        +String cve
        +String severidad
        +String descripcion
        +String lineaDeCodigo
    }

    Usuario "1" -- "*" Reporte : Genera
    Analizador "1" -- "*" Reporte : Produce
    Reporte "1" *-- "*" Vulnerabilidad : Contiene
```

## 4. Diagrama de Componentes

```mermaid
flowchart TD
    subgraph Frontend ["Frontend"]
        Dashboard["React/Next.js Dashboard"]
    end
    
    subgraph BackendAPI ["Backend API"]
        Gateway["API Gateway"]
        Auth["Servicio de Autenticación"]
        Orquestador["Orquestador de Tareas"]
    end
    
    subgraph CoreAnalizador ["Core Analizador"]
        Semgrep["Motor Semgrep SAST"]
        Snyk["Motor Snyk DAST"]
        Decompilador["Decompilador APK"]
    end
    
    subgraph Almacenamiento ["Almacenamiento"]
        Postgres[("PostgreSQL")]
        S3[("AWS S3 / Almacenamiento Local")]
    end

    Dashboard --> Gateway
    Gateway --> Auth
    Gateway --> Orquestador
    Orquestador --> Semgrep
    Orquestador --> Snyk
    Orquestador --> S3
    Semgrep --> Postgres
```
