# Daily Trips Project - Plataforma de Datos AWS

## 1. Objetivo

Desarrollar un framework ETL/ELT reutilizable y automatizado para un
lakehouse en AWS, permitiendo procesar datasets de viajes diarios y
registrar resultados en S3 y Glue Data Catalog. La solución es
metadata-driven y configurable vía JSON/YAML.

------------------------------------------------------------------------

## 2. Arquitectura

Capas en S3:

Landing → Raw → Gold

Estructura del bucket: s3://jeff-data-lake-2026/ - landing/ - raw/ -
gold/ - logs/ - quality-reports/ - quarantine/ - config/

Procesamiento: - AWS Glue (PySpark) - Athena para consultas analíticas -
Glue Data Catalog para metadatos

------------------------------------------------------------------------

## 3. Estructura del Repositorio

daily-trips-aws-data-lake/ - src/ - framework/ - pipelines/ - config/ -
sql/ - doc/ - tests/ - README.md

------------------------------------------------------------------------

## 4. Configuración Metadata-Driven

Ejemplo JSON:

{ "source_bucket": "jeff-data-lake-2026", "landing_prefix": "landing/",
"raw_prefix": "raw/", "gold_prefix": "gold/", "partitions":
\["pickup_date"\], "quality_rules": \[ "completitud", "unicidad",
"rangos", "referencial", "outliers", "frescura" \], "incremental": true
}

------------------------------------------------------------------------

## 5. Guía de Ejecución

1.  Subir CSV a landing/
2.  Ejecutar Glue Job:

python src/pipelines/daily_trips_etl.py --pipeline
config/pipeline_trips.json

3.  Verificar outputs en raw/ y gold/
4.  Revisar quality-reports/
5.  Ejecutar consultas en Athena

------------------------------------------------------------------------

## 6. Validaciones de Calidad

-   Completitud
-   Unicidad
-   Rangos válidos
-   Consistencia referencial
-   Detección de outliers
-   Frescura de datos

------------------------------------------------------------------------

## 7. Control de Costos

-   Uso de Parquet
-   Particionamiento
-   Column pruning
-   Glue con máximo 2 DPU
-   Validación de bytes escaneados en Athena

------------------------------------------------------------------------

## 8. Evidencias

En carpeta doc/: - Glue Job Runs - Logs - Consulta Athena con bytes
escaneados - Outputs en S3 - Documento de diseño (2--4 páginas)

------------------------------------------------------------------------


## 9. Procesamiento Incremental e Idempotencia

### Estrategia de Procesamiento Incremental

El pipeline implementa procesamiento incremental mediante un enfoque configurable y metadata-driven.

Principios clave:

- La carga incremental se controla a través de archivos de configuración (JSON).
- Estrategia basada en particiones (`year`, `month`).
- En cada ejecución solo se procesan nuevas particiones detectadas.
- Se pueden habilitar Glue Job Bookmarks para evitar reprocesar archivos previamente consumidos.
- La lógica puede extenderse mediante una marca de agua (watermark) basada en una columna de fecha (ej. `pickup_datetime`).

Este enfoque garantiza:

- Escalabilidad
- Optimización de costos
- Evitar recargas completas innecesarias

---

### Estrategia de Idempotencia

La solución es idempotente, lo que significa que:

- Re-ejecutar el job con el mismo input no genera registros duplicados.
- Las escrituras son conscientes de particiones (partition-aware).
- El modo de escritura puede configurarse (overwrite por partición / dynamic partition overwrite).
- Puede aplicarse deduplicación lógica usando claves primarias (ej. `trip_id`).

En escenarios de reprocesamiento:

- Las particiones existentes se sobrescriben de forma controlada.
- No se generan duplicados en la capa Gold.
- La integridad del modelo analítico se mantiene.

---

### Validación de Incrementalidad

Para demostrar el comportamiento incremental:

1. Ejecutar el pipeline con un primer conjunto de datos (Mes 1).
2. Agregar un nuevo conjunto de datos (Mes 2).
3. Re-ejecutar el pipeline.
4. Validar en Athena:
   - No existen registros duplicados.
   - Solo se crean nuevas particiones.
   - Los conteos de filas coinciden con lo esperado.

Esto demuestra una ingestión incremental controlada y transformaciones idempotentes.

------------------------------------------------------------------------

## 10. Limpieza de Recursos (Cost-Control)
Con el fin de evitar costos posteriores a la evaluación, se recomienda eliminar los siguientes recursos creados durante la prueba:

### 1. AWS Glue
Eliminar Glue Jobs creados para el pipeline.
Eliminar Crawlers (si aplica).
Eliminar tablas registradas en Glue Data Catalog.
Ruta:
AWS Console → Glue → Jobs / Crawlers / Tables → Delete

### 2. Amazon S3
Eliminar los buckets o prefijos creados exclusivamente para la prueba:
landing/
raw/
gold/
quarantine/
quality-reports/
Ruta:
AWS Console → S3 → Bucket → Delete objects → Delete bucket
-Asegurarse de vaciar el bucket antes de eliminarlo.

### 3. CloudWatch Logs (Opcional)
Eliminar grupos de logs asociados al Glue Job:
AWS Console → CloudWatch → Log Groups → /aws-glue/jobs/

### 11. Reproducibilidad
La solución puede reproducirse siguiendo estos pasos:
Crear bucket en S3.
Subir dataset a landing/.
Crear Glue Job con el script ubicado en /src.
Configurar archivo JSON correspondiente.
Ejecutar el Job.
Registrar tabla en Glue Data Catalog.
Consultar en Athena.
Todos los pasos están documentados en este repositorio.


Autor: Jefferson
