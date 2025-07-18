# Diseño de una Rúbrica para la Evaluación de Jugadas por LLMs
 
Este repositorio contiene un sistema de evaluación para modelos de lenguaje (LLMs) aplicados a decisiones en el juego **Tres en Raya**. A través de una rúbrica de 7 dimensiones, se analizan los turnos generados por distintos modelos, evaluadas por sistemas como **DeepSeek** y **Gemini**.

## 📋 Objetivo
Evaluar la calidad de los movimientos generados por LLMs en partidas de Tic-Tac-Toe, utilizando una rúbrica detallada que considera tanto el cumplimiento de reglas como la calidad explicativa.

<h2>🧠 Rúbrica de Evaluación por Dimensión</h2>

<p>Cada jugada fue evaluada en siete dimensiones, con niveles de desempeño del 1 (Deficiente) al 3 (Alto):</p>

<table style="width:100%; border-collapse: collapse; font-size: 14px;">
  <thead style="background-color: #003366; color: white;">
    <tr>
      <th style="padding: 10px; border: 1px solid #ccc;">Dimensión</th>
      <th style="padding: 10px; border: 1px solid #ccc;">Nivel 1 – Deficiente</th>
      <th style="padding: 10px; border: 1px solid #ccc;">Nivel 2 – Aceptable</th>
      <th style="padding: 10px; border: 1px solid #ccc;">Nivel 3 – Alto</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #ccc;">Comprensión de Reglas</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Viola reglas básicas: casilla ocupada o fuera del tablero.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Cumple reglas básicas, pero omite situaciones menos evidentes.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Siempre movimientos legales, respeta todas las reglas del turno.</td>
    </tr>
    <tr style="background-color:#f9f9f9;">
      <td style="padding: 10px; border: 1px solid #ccc;">Validez y Legalidad</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Movimiento inválido o ilegal (fuera de límites).</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Movimiento válido, sin análisis profundo.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Movimiento válido y elegido tras un análisis completo del tablero.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ccc;">Razonamiento Estratégico</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Acción sin lógica, aleatoria o contraproducente.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Intención estratégica simple (bloquear/avanzar), sin anticipación.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Justificación clara y anticipada, maximiza chances de ganar.</td>
    </tr>
    <tr style="background-color:#f9f9f9;">
      <td style="padding: 10px; border: 1px solid #ccc;">Factualidad</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Explicación incorrecta o no relacionada con el tablero real.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Justificación generalmente correcta, con imprecisiones menores.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Explicación precisa, basada en hechos concretos del tablero.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ccc;">Coherencia Explicativa</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Explicación confusa o contradictoria.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Explicación clara pero superficial.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Explicación lógica, completa y alineada con el movimiento.</td>
    </tr>
    <tr style="background-color:#f9f9f9;">
      <td style="padding: 10px; border: 1px solid #ccc;">Claridad Lingüística</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Lenguaje poco claro o con errores graves.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Lenguaje claro con pequeños errores.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Lenguaje preciso, gramaticalmente correcto y fácil de entender.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ccc;">Adaptabilidad</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Ignora el cambio o jugada previa del oponente.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Se adapta de forma básica o tardía.</td>
      <td style="padding: 10px; border: 1px solid #ccc;">Se adapta rápidamente y ajusta su estrategia eficazmente.</td>
    </tr>
  </tbody>
</table>

## ⚙️ Contenido del Repositorio
📁 1. Dataset (Preprocesamiento)
- Conversión de datos: Unifica múltiples archivos .json en un único archivo .csv.
- Limpieza: Elimina comillas, espacios y errores de formato.
- Ejemplos (ejemplos.csv): Sirve como few-shot prompt de referencia en la evaluación.

🤖 2. Evaluadores (Generación de Puntuaciones)
- Evaluador Gemini 
- Evaluador DeepSeek 

Ambos evaluadores generan puntuaciones para cada jugada utilizando prompts estructurados junto con ejemplos (few-shot) como referencia. Analizan el estado del tablero, el movimiento realizado y la explicación proporcionada para asignar una calificación en cada dimensión de la rúbrica.

🧪 3. Scripts de Análisis (.py)
Scripts en Python para el preprocesamiento y análisis de resultados:
- Promedios por dimensión y por modelo.
- Clasificación de jugadas válidas e inválidas.
- Comparaciones entre evaluadores.
- Ranking general por desempeño.

📉 4. Visualización en R
Scripts desarrollados en RStudio para generar gráficos analíticos:
- Tiempo de ejecución promedio por modelo.
- Promedios por dimensión (según modelo y evaluador).
- Promedio de movimientos válidos e inválidos.
- Los 3 Mejores y Peores modelos evaluados por DeepSeek y Gemini.

📂 5. Resultados y Recursos
- Archivos .csv y .xlsx exportados.
- Resúmenes por dimensión y modelo.
- Gráficos listos para informes o presentaciones.
- Datos ya procesados para carga directa.

✅ 6. Requisitos
- 🐍 Python: pandas, requests, etc.
- 📊 R / RStudio: tidyverse, ggplot2, readxl, etc.
- 🔑 OpenRouter/GoogleCloud: Claves API (para acceso a modelos LLM como Gemini y DeepSeek)
