library(readxl)
library(tidyverse)

# === 1. Cargar ambos archivos ===
archivo_gemini <- "resumen_gemini.xlsx"
archivo_deepseek <- "resumen_deepseek.xlsx"

df_gemini <- read_excel(archivo_gemini) %>%
  mutate(Evaluador = "Gemini")

df_deepseek <- read_excel(archivo_deepseek) %>%
  mutate(Evaluador = "DeepSeek")

# === 2. Unir ambos dataframes ===
df_completo <- bind_rows(df_gemini, df_deepseek)

# === 3. Convertir puntuaciones a numérico ===
df_completo <- df_completo %>%
  mutate(`Promedio General` = as.numeric(gsub(",", ".", `Promedio General`)))

# === 4. Reordenar los factores del modelo de MENOR a MAYOR ===
orden_modelos <- df_completo %>%
  group_by(modelo) %>%
  summarise(promedio_total = mean(`Promedio General`, na.rm = TRUE)) %>%
  arrange(desc(promedio_total)) %>%
  pull(modelo)

df_completo$modelo <- factor(df_completo$modelo, levels = rev(orden_modelos))

# === 5. Crear gráfico de barras comparativo ===
ggplot(df_completo, aes(x = modelo, y = `Promedio General`, fill = Evaluador)) +
  geom_col(position = position_dodge(width = 0.7), width = 0.6) +
  coord_flip() +
  labs(title = "",
       x = "Modelo",
       y = "Promedio General",
       fill = "Evaluador") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 8),
        plot.title = element_text(hjust = 0.5, face = "bold"))



# === Mostrar modelos con mayor diferencia entre evaluadores ===
promedios_por_modelo <- df_completo %>%
  group_by(modelo, Evaluador) %>%
  summarise(promedio = mean(`Promedio General`, na.rm = TRUE), .groups = "drop") %>%
  pivot_wider(names_from = Evaluador, values_from = promedio) %>%
  mutate(diferencia_absoluta = abs(DeepSeek - Gemini)) %>%
  arrange(desc(diferencia_absoluta))

# Imprimir los 10 con mayor diferencia
cat("Top 10 modelos con mayor diferencia entre evaluadores:\n")
print(head(promedios_por_modelo, 11))
