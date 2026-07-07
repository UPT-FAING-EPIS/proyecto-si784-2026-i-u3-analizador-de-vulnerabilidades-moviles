<div align="center">
  <img src="media/logo-upt.png" alt="AnzenCore Logo" width="200"/>
  
  # 🛡️ AnzenCore
  **Plataforma Avanzada de Análisis de Vulnerabilidades y Calidad de Código**

  [![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
</div>

<br/>

> **AnzenCore** es un analizador de vulnerabilidades móviles y de calidad de código. Permite analizar proyectos, realizar validaciones estáticas, registrar los hallazgos en bases de datos gestionadas de alta concurrencia y exportar reportes detallados.

**VIDEO DEMO:** https://drive.google.com/drive/folders/1yMdev7kdS-gvyCPDbb_FISKsSxXu5EmZ?usp=drive_link  
**Repositorio de la SKILL:** https://github.com/FabrizioPerezPeralta/Skill_AnzenCore.git  
**Extensión Visual Studio Code:** AnzenCore

---

## 🎯 Objetivos del Proyecto

- 🤖 **Análisis Automatizado:** Mecanismo rápido y fiable para detectar vulnerabilidades, *code smells* y métricas de complejidad en tu código fuente.
- ⚡ **Integración Continua (Stateless):** Capacidad para integrarse con microservicios externos mediante nuestra API, permitiendo analizar repositorios y carpetas sin requerir sesiones o autenticación compleja.
- 📊 **Visualización Centralizada:** Dashboard interactivo donde los desarrolladores pueden gestionar, filtrar y estudiar de cerca los hallazgos reportados.

## 💻 Stack Tecnológico

A continuación, se presentan las tecnologías que impulsan **AnzenCore**, acompañadas de sus respectivos íconos:

<details open>
<summary><b>Haz clic para contraer/expandir las tecnologías usadas</b></summary>

| Capa | Tecnologías |
| :--- | :--- |
| **Frontend / Dashboard** | <img src="https://cdn.simpleicons.org/python/3776AB" width="18"/> Python • <img src="https://cdn.simpleicons.org/streamlit/FF4B4B" width="18"/> Streamlit |
| **Backend / API REST** | <img src="https://cdn.simpleicons.org/python/3776AB" width="18"/> Python • <img src="https://cdn.simpleicons.org/fastapi/009688" width="18"/> FastAPI |
| **Base de Datos** | <img src="https://cdn.simpleicons.org/postgresql/4169E1" width="18"/> PostgreSQL • <img src="https://cdn.simpleicons.org/supabase/3ECF8E" width="18"/> Supabase |
| **Infraestructura** | <img src="https://cdn.simpleicons.org/docker/2496ED" width="18"/> Docker • <img src="https://cdn.simpleicons.org/terraform/844FBA" width="18"/> Terraform • <img src="https://cdn.simpleicons.org/microsoftazure/0078D4" width="18"/> Azure Container Apps |
| **DevSecOps** | <img src="https://cdn.simpleicons.org/githubactions/2088FF" width="18"/> GitHub Actions • <img src="https://cdn.simpleicons.org/sonarqube/4E9BCD" width="18"/> SonarQube • <img src="https://cdn.simpleicons.org/snyk/4C4A73" width="18"/> Snyk |
| **Testing** | <img src="https://cdn.simpleicons.org/pytest/0A9EDC" width="18"/> Pytest • Behave (BDD) • Mutmut |

</details>

---

## 🧩 Arquitectura del Sistema y Tecnologías

El siguiente diagrama ilustra cómo interactúan las distintas piezas de nuestro stack tecnológico para dar vida a la plataforma.

```mermaid
graph TD
    %% Estilos Base
    classDef default fill:#1E1E1E,stroke:#4A4A4A,stroke-width:2px,color:#FFFFFF,rx:8px,ry:8px;
    classDef azure fill:#0078D41A,stroke:#0078D4,stroke-width:2px,color:#FFFFFF,rx:8px,ry:8px;
    classDef github fill:#2088FF1A,stroke:#2088FF,stroke-width:2px,color:#FFFFFF,rx:8px,ry:8px;

    %% Nodos con Íconos (HTML)
    User(["👤 Usuario / Desarrollador"])
    External(["🤖 Sistemas Externos"])
    
    subgraph CI_CD [Pipeline DevSecOps]
        GH["<img src='https://cdn.simpleicons.org/githubactions/2088FF' width='30'/><br/>GitHub Actions"]
        SQ["<img src='https://cdn.simpleicons.org/sonarqube/4E9BCD' width='30'/><br/>SonarQube"]
        TF["<img src='https://cdn.simpleicons.org/terraform/844FBA' width='30'/><br/>Terraform"]
    end

    subgraph Azure_Cloud [Azure Container Apps]
        UI["<img src='https://cdn.simpleicons.org/streamlit/FF4B4B' width='35'/><br/>Dashboard (Streamlit)"]
        API["<img src='https://cdn.simpleicons.org/fastapi/009688' width='35'/><br/>API REST (FastAPI)"]
        Docker["<img src='https://cdn.simpleicons.org/docker/2496ED' width='35'/><br/>Contenedores Docker"]
    end

    DB["<img src='https://cdn.simpleicons.org/supabase/3ECF8E' width='40'/><br/>Base de Datos<br/>(Supabase/PostgreSQL)"]

    %% Conexiones de Uso
    User -->|Interactúa| UI
    External -->|Consume Endpoints| API
    UI -->|Peticiones HTTP| API
    API -->|Consulta / Guarda| DB

    %% Conexiones de Infraestructura
    Docker -.->|Empaqueta| UI
    Docker -.->|Empaqueta| API
    GH -->|Valida Código| SQ
    GH -->|Despliega Infraestructura| TF
    TF -->|Aprovisiona| Azure_Cloud

    %% Aplicación de Clases
    class Azure_Cloud azure;
    class CI_CD github;
```

---

## 📋 Requisitos Previos

- **Python 3.12+** instalado en el entorno.
- Una cuenta en **Supabase** (con base de datos aprovisionada).
- Archivo de configuraciones seguras (secrets) mapeados en `.streamlit/secrets.toml` y variables de entorno para la API.

---

## ⚙️ Configuración de Variables

Dependiendo del entorno de ejecución, es necesario configurar las siguientes variables:

### 1. Entorno Local (Streamlit)
Crear archivo `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_KEY = "tu_anon_key"
```

### 2. Entorno Backend (API & Contenedores)
Configurar mediante variables de sistema `.env`:
```env
SUPABASE_URL="https://tu-proyecto.supabase.co"
SUPABASE_KEY="tu_anon_key"
```

### 3. Entorno CI/CD (GitHub Actions)
```text
SONAR_TOKEN             # Integración con SonarCloud
SNYK_TOKEN              # Verificación de vulnerabilidades Snyk
SEMGREP_APP_TOKEN       # Análisis estático extendido
AZURE_CLIENT_ID         # Despliegue en Azure
AZURE_CLIENT_SECRET
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
```

---

## 🚀 Despliegue y Ejecución Local

### Instalación de Dependencias
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 🖥️ Arrancar el Dashboard
```powershell
streamlit run app.py
```
> URL Local: `http://localhost:8501`

### ⚙️ Arrancar la API REST
```powershell
uvicorn app.api.main:app --reload --port 8000
```
> Swagger Local: `http://localhost:8000/docs`

---

## 🐳 Ejecución vía Docker

Para ambientes aislados, el sistema provee Dockerfiles independientes.

**Dashboard:**
```powershell
docker build -f Dockerfile.dashboard -t anzencore-dashboard .
docker run -p 8501:8501 --env SUPABASE_URL=... --env SUPABASE_KEY=... anzencore-dashboard
```

**API:**
```powershell
docker build -f Dockerfile.api -t anzencore-api .
docker run -p 8000:8000 --env SUPABASE_URL=... --env SUPABASE_KEY=... anzencore-api
```

---

## ☁️ Despliegue Oficial en la Nube

El despliegue está orquestado mediante **Terraform** dirigido a la plataforma **Azure Container Apps**, garantizando escalabilidad y estabilidad.

```bash
cd infra/
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

---

## 🧪 Pruebas y Aseguramiento de Calidad

Ejecución unificada de pruebas unitarias y cobertura:
```powershell
pytest
pytest --cov=app --cov-report=xml
```

Pruebas orientadas al comportamiento (BDD):
```powershell
python -m behave tests\bdd
```

Pruebas de interfaz (UI):
```powershell
pytest tests/interface
```

Pruebas de Mutación *(Recomendado correr en WSL o Ubuntu)*:
```bash
python -m mutmut run --paths-to-mutate app/dashboard/services/report_export_service.py --runner "python -m pytest tests/unit/test_report_export_service.py"
```

---

## 📚 Roadmap & Documentación

- **Integración Externa:** Si deseas consumir la API desde otro servicio o frontend, revisa `API_INTEGRATION.md`.
- **Evolución del Proyecto:** Ver `docs/roadmap/roadmap.md`.

---

## 📐 Diagramas Complementarios de Arquitectura

<details>
<summary><b>1. Diagrama de Casos de Uso</b></summary>

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
</details>

<details>
<summary><b>2. Diagrama de Secuencia (Escaneo de APK)</b></summary>

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
</details>

<details>
<summary><b>3. Diagrama de Clases</b></summary>

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
</details>

<details>
<summary><b>4. Diagrama de Componentes</b></summary>

```mermaid
flowchart TD
    subgraph Frontend ["Frontend"]
        Dashboard["Streamlit Dashboard"]
    end
    
    subgraph BackendAPI ["Backend API"]
        Gateway["FastAPI Gateway"]
        Auth["Servicio de Autenticación"]
        Orquestador["Orquestador de Tareas"]
    end
    
    subgraph CoreAnalizador ["Core Analizador"]
        Semgrep["Motor Semgrep SAST"]
        Snyk["Motor Snyk DAST"]
        Decompilador["Decompilador APK"]
    end
    
    subgraph Almacenamiento ["Almacenamiento"]
        Postgres[("Supabase / PostgreSQL")]
        Archivos[("Almacenamiento de Archivos")]
    end

    Dashboard --> Gateway
    Gateway --> Auth
    Gateway --> Orquestador
    Orquestador --> Semgrep
    Orquestador --> Snyk
    Orquestador --> Archivos
    Semgrep --> Postgres
```
</details>

<details>
<summary><b>5. Diagrama de Despliegue e Infraestructura</b></summary>

```mermaid
graph TD
    subgraph "Cliente"
        A[Navegador Web]
    end
    
    subgraph "Nube (Ej. Azure Container Apps)"
        B[Load Balancer]
        
        subgraph "Contenedores Docker"
            C[Servidor Frontend - Streamlit]
            D[Servidor Backend API - FastAPI]
            E[Worker de Análisis]
        end
        
        subgraph "Servicios Administrados"
            F[(Supabase PostgreSQL)]
            G[(Almacenamiento Local / S3)]
        end
    end

    A -->|HTTPS| B
    B --> C
    B --> D
    D --> E
    D --> F
    E --> G
    E --> F
```
</details>
