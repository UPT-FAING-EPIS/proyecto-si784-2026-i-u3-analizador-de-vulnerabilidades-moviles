# UNIVERSIDAD PRIVADA DE TACNA
## FACULTAD DE INGENIERIA
### Escuela Profesional de Ingeniería de Sistemas

**Proyecto AnzenCore - Analizador de Vulnerabilidades Moviles**

**Curso:** Calidad y Pruebas de Software  
**Docente:** Mg. Ing. Patrick Jose Cuadros Quiroga

**Integrantes:**
* Arocutipa Arocutipa, Gian Franco (2023076790)
* Perez Peralta, Fabrizio Salvador Elias (2023077476)

**Tacna – Perú**  
**2026**

---

# Sistema AnzenCore – Analizador de Vulnerabilidades Moviles
## Documento de Visión
**Versión 1.0**

---

## CONTROL DE VERSIONES
| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2.0 | FSEPP, GFAA | PCQ | PCQ | 27/06/2026 | Versión Final |

*(Nota: en el índice menciona 10/10/2020 para la v2.0 y v1.0 en la carátula, mantendremos lo del texto)*

---

## INDICE GENERAL
1. Introducción
    1.1 Propósito
    1.2 Alcance
    1.3 Definiciones, Siglas y Abreviaturas
    1.4 Referencias
    1.5 Visión General
2. Posicionamiento 
    2.1 Oportunidad de negocio
    2.2 Definición del problema
3. Descripción de los interesados y usuarios
    3.1 Resumen de los interesados
    3.2 Resumen de los usuarios 
    3.3 Entorno de usuario
    3.4 Perfiles de los interesados 
    3.5 Perfiles de los Usuarios 
    3.6 Necesidades de los interesados y usuarios
4. Vista General del Producto 
    4.1 Perspectiva del producto
    4.2 Resumen de capacidades
    4.3 Suposiciones y dependencias
    4.4 Costos y precios 
    4.5 Licenciamiento e instalación
5. Característica de Productos 
6. Restricciones
7. Rangos de calidad
8. Precedencia y Prioridad
9. Otros requerimientos del producto
CONCLUSIONES
RECOMENDACIONES 
BIBLIOGRAFÍA
WEBGRAFÍA

---

## 1. Introducción

### 1.1 Propósito
El propósito de este documento es recopilar, analizar y definir las necesidades y características de alto nivel del sistema AnzenCore: una plataforma web con componente móvil orientada a la auditoría de seguridad de aplicaciones Android y al análisis estático de código fuente. El documento se centra en la funcionalidad esencial requerida por los interesados y usuarios finales, así como en las razones que motivan su desarrollo, y sirve de referencia para los requerimientos detallados que se especifican en el documento ERS del proyecto.

### 1.2 Alcance
Este documento de Visión abarca el desarrollo integral del sistema AnzenCore: el motor de ingeniería inversa sobre APKs (desempaquetado, extracción DEX, desofuscación de strings y clases ofuscadas con ProGuard/R8, detección de vulnerabilidades), la plataforma web MVC (FastAPI como backend y Streamlit como dashboard), el agente móvil Android (Kivy, API 26+) y la base de datos Supabase. No se incluyen integraciones con servicios externos de análisis de código.

### 1.3 Definiciones, Siglas y Abreviaturas
| Término | Descripción |
| :--- | :--- |
| **APK** | Android Package; archivo de instalación de aplicaciones para Android. |
| **MVC** | Modelo-Vista-Controlador; patrón de arquitectura de software. |
| **OWASP** | Open Web Application Security Project; fundación de referencia en seguridad de aplicaciones. |
| **RUP** | Rational Unified Process; proceso de desarrollo de software del cual deriva este documento de Visión. |
| **RF / RNF** | Requerimiento Funcional / Requerimiento No Funcional. |
| **ERS** | Especificación de Requerimientos de Software. |
| **TLS** | Transport Layer Security; protocolo de cifrado de comunicaciones. |
| **API** | Application Programming Interface; interfaz de comunicación entre sistemas. |
| **LOC** | Lines of Code; métrica de líneas de código. |
| **NOM / NOA** | Number of Methods / Number of Attributes; métricas de complejidad de clases. |
| **SHA-256** | Algoritmo de hash criptográfico de 256 bits, usado para identificar de forma única cada APK analizada. |
| **CU** | Caso de Uso. |

### 1.4 Referencias
* Google LLC. (2024). Android Developer Documentation — Security best practices.
* OWASP Foundation. (2024). OWASP Mobile Top 10.
* C4 Model (2024). The C4 model for visualizing software architecture.
* FD03-EPIS-Informe_SRS_Proyecto-AnzenCore: Especificación de Requerimientos de Software del sistema AnzenCore (2026).

### 1.5 Visión General
Este documento se organiza en nueve secciones. Tras esta introducción, la sección 2 presenta el posicionamiento del producto: la oportunidad de negocio y el problema que resuelve. La sección 3 describe a los interesados y usuarios del sistema. La sección 4 ofrece una vista general del producto, su perspectiva, capacidades, suposiciones y modelo de licenciamiento. Las secciones 5 a 9 detallan las características del producto, sus restricciones, los rangos de calidad esperados, la precedencia de las funcionalidades y otros requerimientos. El documento cierra con las conclusiones, recomendaciones y referencias bibliográficas.

## 2. Posicionamiento

### 2.1 Oportunidad de negocio 
El ecosistema Android concentra mas del 70% de los dispositivos moviles activos en el mercado latinoamericano. Sin embargo, la gran mayoria de los usuarios desconoce los permisos que sus aplicaciones solicitan, las vulnerabilidades que contienen sus APKs ni los riesgos de seguridad a los que estan expuestos. Las herramientas de analisis existentes (MobSF, Jadx, Apktool) estan orientadas a investigadores con conocimientos avanzados de seguridad, son de instalacion local y carecen de una experiencia de usuario accesible. Existe por tanto una oportunidad concreta para una plataforma web que permita a cualquier usuario subir una APK, obtener un reporte de seguridad comprensible y aprender sobre las vulnerabilidades detectadas, sin necesidad de instalar software ni tener conocimientos tecnicos previos. AnzenCore ocupa este espacio combinando ingenieria inversa sobre bytecode Dalvik/DEX con un dashboard educativo y un modelo freemium que lo hace accesible desde el primer dia.

| N° | Objetivo de negocio | Indicador de éxito |
| :--- | :--- | :--- |
| 1 | Ofrecer auditoría de seguridad Android sin instalación permanente | APK temporal funcional con desinstalación automática |
| 2 | Integrar AnzenCore en el pipeline CI/CD de empresas de desarrollo Android mediante API REST documentada | Al menos 3 empresas integradas vía API REST durante el primer año de operación |
| 3 | Generar historial de seguridad trazable por usuario | Dashboard web con gráfico de evolución de puntuación |
| 4 | Establecer contratos Empresarial (S/.89.90/$24.00 USD/mes) con empresas del sector tecnológico latinoamericano | Mínimo 2 contratos Empresarial activos al finalizar el primer semestre de operación |

### 2.2 Definición del problema
| | |
| :--- | :--- |
| **El problema de** | la falta de visibilidad y comprensión sobre los riesgos de seguridad presentes en los dispositivos Android, y la dispersión de herramientas para auditar código, URLs y repositorios |
| **Afecta a** | usuarios de dispositivos Android sin conocimientos técnicos avanzados, estudiantes y desarrolladores que desean verificar la seguridad de sus proyectos de software |
| **El impacto de esto es** | exposición a vulnerabilidades no detectadas, pérdida de información sensible y desinterés por aprender sobre ciberseguridad debido a la complejidad de las herramientas existentes |
| **Una solución exitosa debería** | permitir auditar la seguridad de un dispositivo Android sin instalación permanente, presentar los hallazgos de forma clara y accionable, e integrar verificación de código, URLs y repositorios en una sola plataforma |

La ausencia de herramientas accesibles para el analisis de seguridad de aplicaciones Android genera que la mayoria de los usuarios instale apps sin conocer los permisos peligrosos que otorgan ni las vulnerabilidades que contienen. Cuando el codigo del APK esta ofuscado con ProGuard o R8, incluso los analistas tecnicos encuentran dificultades para identificar secretos hardcodeados, comunicaciones inseguras o criptografia debil. El siguiente marco define el problema central que AnzenCore resuelve:

## 3. Descripción de los interesados y usuarios

### 3.1 Resumen de los interesados
| Nombre | Representa | Rol |
| :--- | :--- | :--- |
| Patrick Jose Cuadros Quiroga | Docente del curso Calidad y Pruebas de Software — UPT | Evaluador académico; valida el cumplimiento de los objetivos de calidad y aprueba la documentación del proyecto |
| Equipo de desarrollo AnzenCore (Gian Franco Arocutipa Arocutipa, Fabrizio Salvador Elias Perez Peralta) | Estudiantes de la Escuela Profesional de Ingeniería de Sistemas | Analizan, diseñan, desarrollan y prueban el sistema AnzenCore |
| Administrador de base de datos | Plataforma Supabase | Administra la base de datos del sistema; sin panel web dedicado en la implementación actual |

### 3.2 Resumen de los usuarios
| Perfil | Descripción | Acceso |
| :--- | :--- | :--- |
| Usuario Final (Novato) | Usuario sin conocimientos técnicos que desea analizar una APK o verificar la seguridad de un sitio web o código. | Dashboard APK, Motor IR, API REST (plan Empresarial) |
| Usuario Final (Avanzado) | Usuario con conocimientos de seguridad que usa AnzenCore para auditoría de APKs, análisis estático de código y seguimiento de historial de hallazgos. | Dashboard APK, historial, Motor IR, Exportación PDF, API REST, SLA (plan Empresarial) |
| Administrador | Administra la base de datos Supabase del sistema. | Supabase dashboard (externo al sistema) |

### 3.3 Entorno de usuario
La plataforma web de AnzenCore es accesible desde cualquier navegador moderno (Chrome, Firefox, Safari o Edge), con un dashboard responsivo utilizable desde pantallas a partir de 320 px de ancho, por lo que no requiere instalación en el equipo del usuario. La APK de análisis, en cambio, se instala temporalmente en dispositivos Android con versión 8.0 (API 26) o superior, exclusivamente durante el proceso de auditoría, y no necesita acceso a contactos, mensajes ni fotos del usuario. El usuario final típico interactúa con el sistema de forma esporádica, cada vez que desea auditar su dispositivo o un proyecto de software, mientras que el administrador interactúa directamente con Supabase de forma puntual.

### 3.4 Perfiles de los interesados
**Docente del curso**
* **Representante:** Patrick Jose Cuadros Quiroga
* **Descripción:** Docente responsable del curso Calidad y Pruebas de Software
* **Responsabilidades:** Definir los criterios de calidad del entregable, revisar avances y aprobar la documentación
* **Criterios de éxito:** El documento de Visión y la ERS reflejan fielmente el alcance y los objetivos del proyecto
* **Implicación:** Revisión periódica de entregables (FD02, FD03 y subsiguientes)
* **Restricciones:** Disponibilidad limitada a los horarios de clase y asesoría del curso

**Equipo de desarrollo**
* **Representante:** Gian Franco Arocutipa Arocutipa, Fabrizio Salvador Elias Perez Peralta
* **Descripción:** Estudiantes de la Escuela Profesional de Ingeniería de Sistemas responsables del análisis, diseño, desarrollo y pruebas de AnzenCore
* **Responsabilidades:** Construir el sistema cumpliendo los requerimientos funcionales y no funcionales definidos
* **Criterios de éxito:** Entrega de un sistema funcional, desplegado y evaluado positivamente por el docente
* **Implicación:** Desarrollo activo durante todo el semestre académico
* **Restricciones:** Tiempo limitado al cronograma del curso; conocimientos previos en Python, FastAPI y Streamlit

### 3.5 Perfiles de los Usuarios
**Usuario Final (Novato)**
* **Descripción:** Usuario sin conocimientos técnicos que desea conocer el estado de seguridad de su dispositivo o de un sitio web
* **Tipo:** Usuario final
* **Responsabilidades:** Descargar la APK de análisis, ejecutar el escaneo y revisar el dashboard
* **Criterios de éxito:** Comprende los hallazgos sin necesitar conocimientos técnicos previos
* **Implicación:** Uso esporádico, orientado a la consulta puntual
* **Restricciones:** Sin conocimientos de ciberseguridad ni de desarrollo de software

**Usuario Final (Avanzado)**
* **Descripción:** Usuario con conocimientos de seguridad que utiliza AnzenCore para auditoría de APKs, análisis estático de código y seguimiento de historial
* **Tipo:** Usuario final
* **Responsabilidades:** Analizar APKs propias o de terceros; interpretar hallazgos del motor IR; consultar historial de escaneos y exportar reportes PDF; usar la API REST para integraciones propias (plan Profesional o Empresarial).
* **Criterios de éxito:** Obtiene hallazgos precisos y trazables a lo largo del tiempo
* **Implicación:** Uso recurrente, orientado al seguimiento continuo
* **Restricciones:** Requiere conocimientos básicos de seguridad informática

**Administrador**
* **Descripción:** Responsable de administrar la base de datos Supabase del sistema
* **Tipo:** Usuario técnico
* **Responsabilidades:** Mantener la disponibilidad e integridad de los datos almacenados
* **Criterios de éxito:** La base de datos permanece disponible y consistente
* **Implicación:** Intervención puntual ante incidencias
* **Restricciones:** No cuenta con un panel web dedicado en la implementación actual; administra directamente desde Supabase

### 3.6 Necesidades de los interesados y usuarios
| Necesidad | Prioridad | Inquietudes | Solución actual | Solución propuesta |
| :--- | :--- | :--- | :--- | :--- |
| Conocer los riesgos de seguridad del dispositivo | Alta | Falta de visibilidad sobre permisos y vulnerabilidades | Revisión manual de configuraciones, o ninguna | Dashboard de seguridad con score y hallazgos clasificados por severidad |
| Evitar instalar software de seguridad de forma permanente | Alta | Privacidad y consumo de recursos del dispositivo | Apps antivirus de la Play Store | Análisis server-side mediante APK temporal, con desinstalación automática |
| Verificar la seguridad de código, URLs y repositorios | Alta | Herramientas dispersas y de uso técnico complejo | Linters y escáneres independientes | Motor de Ingeniería Inversa con desofuscación DEX y detección de 8+ vulnerabilidades OWASP Mobile Top 10 sin instalación permanente |
| Dar seguimiento histórico al estado de seguridad | Media | Falta de un historial unificado y trazable | Ninguna solución existente | Historial de escaneos con fecha, tamaño y estado por usuario |
| Aprender ciberseguridad de forma accesible | Media | La educación en ciberseguridad suele ser técnica y poco motivadora | Cursos y documentación dispersa | Enfoque educativo y empresarial integrado en la plataforma |

## 4. Vista General del Producto

### 4.1 Perspectiva del producto
AnzenCore es un sistema independiente que no requiere integrarse con servicios externos de análisis de código. El motor de ingeniería inversa (Python stdlib: zipfile, struct, re) analiza el APK de forma nativa sin dependencias de terceros. Su arquitectura se organiza en el patrón MVC: SupabaseModel (datos), DashboardController (lógica) y DashboardView (presentación Streamlit).

### 4.2 Resumen de capacidades
| Beneficio para el usuario | Características que lo soportan |
| :--- | :--- |
| Auditoría de seguridad sin instalación permanente | Descarga y análisis server-side de la APK (RF-03, RF-04, RF-05) |
| Visibilidad clara del estado de seguridad | Dashboard interactivo con score y hallazgos clasificados (RF-06, RF-07) |
| Verificación de seguridad más allá del dispositivo | Motor IR: extracción del bytecode DEX, desofuscación de strings/clases ProGuard/R8, detección de 8+ vulnerabilidades OWASP Mobile Top 10 (RF-04, RF-05) |
| Evaluación de calidad de código | Agente Android: escaneo local de permisos peligrosos, certificados de red y configuración de seguridad del dispositivo (RF-12) |
| Trazabilidad histórica de los análisis | Historial de escaneos por usuario (RF-12) |
| Sentido de comunidad entre usuarios | Indicador de usuarios conectados en tiempo real (RF-13) |

### 4.3 Suposiciones y dependencias
* El equipo de desarrollo cuenta con conocimientos previos de Python, FastAPI, Streamlit y arquitectura MVC.
* Las tecnologías utilizadas son de código abierto y no generan costos de licenciamiento.
* Supabase y Azure Container Apps ofrecen niveles gratuitos suficientes para el desarrollo y las pruebas académicas del proyecto.
* El motor de ingeniería inversa opera con Python stdlib (zipfile, struct, re) sin depender de servicios externos de análisis; esto garantiza disponibilidad y control total del análisis de APKs.
* Se dispone de dispositivos o emuladores Android 8.0+ para validar el funcionamiento de la APK de análisis.

### 4.4 Costos y precios
AnzenCore opera con un único plan Empresarial: S/.89.90/mes ($24.00 USD/mes), orientado a empresas de desarrollo Android que requieren auditorías de seguridad continuas, integración vía API REST en sus pipelines CI/CD, reportes PDF ejecutivos y gestión multi-usuario (hasta 5 usuarios) con SLA 99.9%. El stack tecnológico (Python, FastAPI, Streamlit) es de código abierto sin costos de licencia. El despliegue opera en Azure Container Apps via Terraform; la base de datos en Supabase (PostgreSQL 15).

### 4.5 Licenciamiento e instalación
La plataforma web no requiere instalación: se accede directamente desde el navegador. La APK de análisis se descarga e instala temporalmente en el dispositivo Android del usuario, y se desinstala automáticamente al finalizar el proceso de auditoría, conforme al objetivo de negocio de no exigir instalación permanente. En el contexto académico actual, el sistema se distribuye bajo licencia de uso educativo; como recomendación a futuro, se evaluará su publicación en F-Droid bajo una licencia de código abierto.

## 5. Característica de Productos
A partir de las necesidades identificadas, AnzenCore ofrecerá las siguientes características principales:
* **Autenticación.** Registro e inicio de sesión seguro de usuarios.
* **Distribución de la APK.** Descarga de la APK de análisis precompilada desde la plataforma web.
* **Análisis de APK.** Análisis server-side de permisos peligrosos, secretos hardcodeados, código ofuscado, vulnerabilidades y metadatos del paquete.
* **Dashboard de seguridad.** Visualización de la puntuación de seguridad y de los hallazgos clasificados por severidad, con exportación de reportes en PDF.
* **Motor de Ingeniería Inversa.** Desempaquetado del APK, extracción del bytecode Dalvik/DEX mediante parseo binario (struct), aplicación de algoritmos de desofuscación sobre strings y clases ofuscadas con ProGuard/R8, y ejecución de detectores de 8+ tipos de vulnerabilidades OWASP Mobile Top 10: secretos hardcodeados, HTTP inseguro, criptografía débil, WebView inseguro, Random inseguro, IPs hardcodeadas, librerías nativas y BD empaquetada.
* **Agente Móvil Android.** Aplicación Android (Python/Kivy, API 26+) que realiza escaneo local del dispositivo: permisos peligrosos de apps instaladas, certificados de red y configuración de seguridad del sistema. Envía el reporte JSON al backend para persistencia y visualización en el dashboard.
* **Historial de escaneos.** Registro y consulta del historial de análisis realizados por cada usuario.
* **Comunidad en línea.** Visualización de usuarios conectados en tiempo real.

## 6. Restricciones
* El sistema debe implementarse con arquitectura MVC en Python, utilizando FastAPI para el backend y Streamlit para el dashboard web.
* La base de datos debe ser Supabase (PostgreSQL).
* El despliegue debe realizarse en Azure Container Apps mediante Terraform, dentro de los créditos estudiantiles Microsoft disponibles. Se mantienen dos contenedores: dashboard (puerto 8501) y API (puerto 8000).
* La APK de análisis debe ser compatible con Android 8.0 (API 26) o superior.
* El sistema no debe almacenar contenido personal del usuario (contactos, mensajes, fotos); solo hallazgos y metadatos del análisis.
* El desarrollo está limitado al cronograma y los recursos de un equipo de dos estudiantes durante un semestre académico.

## 7. Rangos de calidad
| Categoría | Rango de calidad esperado |
| :--- | :--- |
| **Seguridad** | Todos los reportes de análisis se transmiten cifrados con TLS 1.2 o superior. |
| **Privacidad** | La APK no lee, accede ni almacena contactos, mensajes o fotos del usuario. |
| **Rendimiento** | El análisis del dispositivo se completa en menos de 60 segundos. |
| **Disponibilidad** | La plataforma web está disponible el 99% del tiempo (24/7). |
| **Usabilidad** | El dashboard es responsivo y usable en pantallas a partir de 320 px. |
| **Compatibilidad** | La APK es compatible con Android 8.0 (API 26) o superior. |
| **Mantenibilidad** | El backend sigue estrictamente el patrón MVC en Python (FastAPI + Streamlit). |
| **Escalabilidad** | La arquitectura soporta hasta 10 000 usuarios concurrentes. |
| **Portabilidad** | La plataforma web funciona en Chrome, Firefox, Safari y Edge. |

## 8. Precedencia y Prioridad
La mayoría de los requerimientos funcionales del sistema (autenticación, análisis de APK y dashboard) tienen prioridad Alta, mientras que el historial de escaneos y integración empresarial y el indicador de comunidad en tiempo real tienen prioridad Media. En consecuencia, se propone el siguiente orden de implementación:

| Fase | Funcionalidad | Justificación |
| :--- | :--- | :--- |
| 1 | Autenticación y análisis de APK (RF-01 a RF-05) | Constituye el núcleo del sistema: sin estas funciones no es posible auditar ningún dispositivo |
| 2 | Dashboard de seguridad e historial (RF-06, RF-07, RF-12) | Permite visualizar y dar seguimiento a los resultados obtenidos en la fase 1 |
| 3 | Motor IR: desofuscación + detectores + Agente Android + API REST Empresarial (RF-04, RF-05, RF-11, RF-12) | Permite detectar vulnerabilidades en APKs ofuscadas e integrar los resultados en pipelines CI/CD de clientes empresariales via API REST |
| 4 | Comunidad en tiempo real (RF-13) | Funcionalidad de prioridad Media, complementaria al objetivo educativo y social del producto |

## 9. Otros requerimientos del producto
Además de los requerimientos funcionales y no funcionales descritos, el producto debe satisfacer los siguientes estándares transversales:

**a) Estándares de manuales de usuario**
El dashboard debe incluir ayuda contextual y descripciones de cada hallazgo en lenguaje no técnico, de modo que un usuario sin conocimientos de seguridad pueda comprender el resultado de su análisis sin recurrir a documentación externa, en coherencia con el objetivo educativo del sistema.

**b) Estándares legales**
El sistema debe cumplir con políticas de privacidad de datos: no almacenar contenido personal del usuario, informar claramente qué datos se procesan, y respetar las licencias de código abierto de las librerías utilizadas (FastAPI y Streamlit, ambas bajo licencias permisivas tipo MIT/Apache 2.0).

**c) Estándares de comunicación**
La comunicación entre el dashboard, la APK y el backend se realiza mediante una API REST con contratos en formato JSON, códigos de estado HTTP estándar y documentación generada automáticamente por FastAPI (OpenAPI/Swagger).

**d) Estándares de cumplimiento de la plataforma**
La plataforma web debe ser compatible con los navegadores modernos más utilizados (Chrome, Firefox, Safari y Edge) y la APK debe ser compatible con dispositivos Android 8.0 (API 26) o superior. El despliegue se realiza en Azure Container Apps mediante Terraform.

**e) Estándares de calidad y seguridad**
Las comunicaciones deben cifrarse con TLS 1.2 o superior, las contraseñas deben almacenarse con un esquema seguro (PBKDF2), los hallazgos deben clasificarse según una escala estándar de severidad (critical, high, medium, low, info), y las métricas de calidad de código deben basarse en indicadores reconocidos (LOC, complejidad ciclomática, NOM, NOA).

## CONCLUSIONES
* AnzenCore responde a una necesidad real y validada empíricamente (el 85% de los estudiantes encuestados desconoce los permisos de sus propias aplicaciones), mediante un modelo de auditoría sin instalación permanente.
* La arquitectura MVC en Python (FastAPI + Streamlit) permite cumplir la visión de un sistema accesible desde cualquier navegador, educativo en su presentación de resultados y mantenible para el equipo de desarrollo.
* El motor de ingeniería inversa sobre APKs, combinado con el agente móvil Android, constituye la propuesta técnica diferenciadora de AnzenCore: permite detectar vulnerabilidades incluso en código ofuscado con ProGuard/R8, sin depender de servicios externos de análisis de código o verificadores de URLs.
* El uso de tecnologías de código abierto y de niveles gratuitos de Supabase y Azure Container Apps hace viable el proyecto dentro de un contexto académico, sin incurrir en costos de licenciamiento.
* La identificación clara de interesados, usuarios y necesidades en este documento de Visión sienta las bases para la Especificación de Requerimientos de Software ya elaborada para el sistema AnzenCore.

## RECOMENDACIONES
* Priorizar el desarrollo de las funcionalidades de prioridad Alta antes de abordar las de prioridad Media, conforme al orden propuesto en la sección 8.
* Mantener la coherencia entre este documento de Visión y la Especificación de Requerimientos de Software del proyecto conforme el alcance se vaya refinando.
* Evaluar en iteraciones futuras la incorporación de bases de datos de vulnerabilidades CVE y la publicación de la APK en F-Droid, conforme se sugiere en el documento ERS.

## BIBLIOGRAFÍA
* Jacobson, I., Booch, G., & Rumbaugh, J. (1999). The Unified Software Development Process. Addison-Wesley.
* OWASP Foundation. (2024). OWASP Mobile Application Security Verification Standard (MASVS).

## WEBGRAFÍA
* Jacobson, I., Booch, G., & Rumbaugh, J. (1999). The Unified Software Development Process. Addison-Wesley.
* OWASP Foundation. (2024). OWASP Mobile Application Security Verification Standard (MASVS).
