# Arquitecturas Avanzadas de Computadores - código docente

Colección de programas de ejemplo utilizada en la asignatura **Arquitecturas Avanzadas de Computadores** del **Grado en Ingeniería Informática** de la Universidad Rey Juan Carlos.

- Autor: Alberto Fernández Isabel
- Curso académico: 2026-2027
- Categoría de la convocatoria: 6 - Programas
- Licencia del software: MIT (SPDX: `MIT`)

## Finalidad docente

La colección reúne ejemplos autocontenidos para estudiar preparación en Python, segmentación, paralelismo a nivel de instrucción, memoria compartida, memoria distribuida y aceleradores. Algunos programas se relacionan también con las soluciones orientativas de prácticas, pero aquí se publican como una colección autónoma, organizada y reutilizable.

## Organización

| Directorio | Contenido |
|---|---|
| `00_preparacion/` | Estructura modular y programación orientada a objetos. |
| `01_introduccion/` | Ejemplo básico de RDD y modelo de ejecución distribuida. |
| `02_segmentacion/` | Simulador compacto de un cauce IF-ID-EX-MEM-WB. |
| `03_paralelismo_nivel_instruccion/` | Predicción, especulación y medición de tiempos. |
| `04_memoria_compartida/` | Simulación concurrente con estado compartido y exclusión mutua. |
| `05_memoria_distribuida/` | Ejemplos de PySpark con RDD, DataFrames, Spark SQL y TF-IDF. |
| `06_aceleradores/` | Ejemplos con Numba, CUDA mediante Numba y Parsl. |

`MANIFEST.txt` documenta la procedencia y el tratamiento editorial y técnico de cada fichero.

## Requisitos

Se requiere **Python 3.10 o posterior**. Para instalar las bibliotecas opcionales:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows, la activación del entorno virtual se realiza con `.venv\Scripts\activate`.

Los ejemplos de PySpark requieren además un entorno Java compatible con la versión de Spark instalada. El ejemplo CUDA necesita una GPU NVIDIA y un entorno CUDA compatible. Los demás ejemplos pueden ejecutarse sin ese hardware especializado.

## Ejecución

Cada fichero Python puede ejecutarse desde la raíz del repositorio. Por ejemplo:

```bash
python 02_segmentacion/tema2_pipeline.py
python 03_paralelismo_nivel_instruccion/tema3_especulacion.py
python 04_memoria_compartida/tema4_simulacion_concurrente.py
```

Los notebooks de `05_memoria_distribuida/notebooks/` se publican sin salidas almacenadas ni trazas locales.

## Validación

El repositorio incluye una validación estructural que comprueba:

- sintaxis de todos los ficheros `.py`;
- presencia del identificador SPDX `MIT` en el código Python;
- validez JSON de los notebooks;
- ausencia de salidas de ejecución almacenadas en los notebooks;
- metadatos de autoría, licencia y curso en los notebooks.

Puede ejecutarse con:

```bash
python scripts/validate.py
```

## Preservación y BURJC Digital

Este repositorio es la publicación pública exigida para la categoría 6. La versión definitiva se archivará en **Software Heritage**. Después se incorporarán aquí y a la documentación del depósito:

- el SWHID de la versión exacta archivada;
- el enlace permanente de Software Heritage;
- la referencia del depósito único de la asignatura en BURJC Digital.

Hasta que se archive la versión definitiva, esos identificadores no deben sustituirse por valores provisionales.

## Licencia

Copyright © 2026 Alberto Fernández Isabel.

El software y la documentación de este repositorio se distribuyen bajo la [licencia MIT](LICENSE).
