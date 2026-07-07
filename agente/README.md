# AnzenCore Mobile Reverse Engineering Skill

Este repositorio contiene una **Skill para Agentes de IA** que instruye al agente en la construcción de una herramienta avanzada de **Ingeniería Inversa y Análisis de Vulnerabilidades Móviles**, extrayendo las lógicas y heurísticas de seguridad del proyecto AnzenCore.

## Enfoque
A diferencia de proyectos full-stack monolíticos, este Blueprint entrena al agente para crear un sistema **100% Stateless** (sin estado, sin bases de datos complejas):
- Un motor robusto en **FastAPI** encargado de extraer el APK, decompilar en memoria y cazar vulnerabilidades por análisis estático (secrets, criptografía débil, fallos de WebView, IPs hardcodeadas).
- Un dashboard interactivo en **Streamlit** para que el ingeniero de seguridad suba el binario y visualice el reporte al instante.

## Instalación

1. Clona este repositorio o copia la carpeta `skills/anzencore-mobile-vuln-analyzer` en tu directorio `.agents/skills/`.
2. El agente de IA detectará la nueva skill automáticamente por su archivo `SKILL.md`.

## Uso

Simplemente pídele a tu agente:
> "Construye una herramienta de analizador de vulnerabilidades móviles usando ingeniería inversa y el blueprint de AnzenCore."

El agente invocará esta skill, procesará los patrones arquitectónicos y la lógica de detección, y comenzará a generar tu herramienta sin pedirte configurar bases de datos ni logins.
