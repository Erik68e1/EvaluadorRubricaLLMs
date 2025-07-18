library(tidyverse)
library(readr)
library(stringr)

archivo_ds <- "evaluadoDeepseek.csv"
archivo_gm <- "evaluadoGemini.csv"

df_ds <- read_csv(archivo_ds, show_col_types = FALSE) %>%
  mutate(evaluador = "DeepSeek")

df_gm <- read_csv(archivo_gm, show_col_types = FALSE) %>%
  mutate(evaluador = "Gemini")

df <- bind_rows(df_ds, df_gm)

# === 3. Función para extraer rubrica ===
extraer_rubrica <- function(rubrica_str) {
  rubrica_str <- gsub("[{}\"]", "", rubrica_str)        # eliminar llaves y comillas
  items <- str_split(rubrica_str, ",\\s*")[[1]]          # separar por coma
  claves_valores <- str_match(items, "(.*?):\\s*(\\d+(\\.\\d+)?)")
  
  tibble(
    dimension = str_trim(claves_valores[, 2]),
    puntaje = as.numeric(claves_valores[, 3])
  )
}

# === 4. Expandir la columna rubrica y calcular promedio general por jugada ===
df_promedios <- df %>%
  filter(!is.na(rubrica)) %>%
  rowwise() %>%
  mutate(
    detalle = list(extraer_rubrica(rubrica)),
    promedio_general = mean(detalle$puntaje)
  ) %>%
  ungroup()

# === 5. Graficar boxplot de evaluación general por modelo y evaluador ===
ggplot(df_promedios, aes(x = promedio_general, y = reorder(modelo, promedio_general), fill = evaluador)) +
  geom_boxplot(width = 0.6, alpha = 0.8, outlier.shape = 21, outlier.size = 2,
               outlier.fill = "white", outlier.color = "black") +
  scale_fill_manual(values = c("DeepSeek" = "#3B7BFF", "Gemini" = "#FF6B3B")) +
  scale_x_continuous(breaks = seq(1, 3, 0.5), limits = c(0.9, 3.1)) +
  labs(
    title = "",
    x = "Evaluación Promedio",
    y = "Modelo Evaluado",
    fill = "Evaluador"
  ) +
  theme_minimal(base_size = 13) +
  theme(
    legend.position = "top",
    panel.grid.major.y = element_blank(),
    axis.text.y = element_text(size = 8)
  )

# === Estadísticas resumen por modelo y evaluador ===
resumen_estadistico <- df_promedios %>%
  group_by(modelo, evaluador) %>%
  summarise(
    media = mean(promedio_general),
    mediana = median(promedio_general),
    q1 = quantile(promedio_general, 0.25),
    q3 = quantile(promedio_general, 0.75),
    min = min(promedio_general),
    max = max(promedio_general),
    n = n(),
    .groups = "drop"
  )

print(resumen_estadistico)
