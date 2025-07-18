library(tidyverse)
library(readxl)

# === 1. Cargar datos desde archivo .xlsx ===
archivo <- "promedios_tiempo_respuesta.xlsx"
df <- read_excel(archivo)

# === 2. Gráfico de barras ===
ggplot(df, aes(x = execution_time, y = reorder(model, execution_time), fill = execution_time)) +
  geom_col(width = 0.7, show.legend = FALSE) +
  geom_text(aes(label = round(execution_time, 2)), 
            hjust = -0.1, size = 3, color = "black") +
  scale_fill_gradient(low = "#add8e6", high = "#003366") +
  labs(
    title = "Tiempo Promedio de Respuesta por Modelo",
    x = "Tiempo Promedio (segundos)",
    y = "Modelo"
  ) +
  coord_cartesian(xlim = c(0, max(df$execution_time) * 1.1)) +
  theme_minimal(base_size = 10) +
  theme(
    axis.text.y = element_text(size = 7),
    axis.title.y = element_text(margin = margin(r = 10)),
    axis.title.x = element_text(margin = margin(t = 10)),
    plot.title = element_text(face = "bold", hjust = 0.5, size = 14),
    plot.subtitle = element_text(hjust = 0.5, size = 10)
  )
