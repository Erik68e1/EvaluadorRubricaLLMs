library(tidyverse)
library(readxl)

# 1. Leer archivo Excel
df <- read_excel("resumen_modelos.xlsx")

# 2. Renombrar columnas para evitar problemas con guiones
df <- df %>%
  rename(
    J_Validas = `J-Validas`,
    J_Invalidas = `J-Invalidas`
  )

# 3. Calcular porcentaje válidas e inválidas en df_pct
df_pct <- df %>%
  mutate(
    pct_validas = J_Validas / Jugadas * 100,
    pct_invalidas = J_Invalidas / Jugadas * 100
  )

# 4. Definir orden según pct_validas
orden_modelos <- df_pct %>%
  arrange(pct_validas) %>%
  pull(model)

# 5. Preparar df_long con porcentajes y factor ordenado
df_long <- df_pct %>%
  select(model, pct_validas, pct_invalidas) %>%
  pivot_longer(cols = c(pct_validas, pct_invalidas),
               names_to = "Tipo",
               values_to = "Porcentaje") %>%
  mutate(
    Tipo = recode(Tipo,
                  pct_validas = "Válidas",
                  pct_invalidas = "Inválidas"),
    model = factor(model, levels = orden_modelos)
  )

# 6. Graficar
ggplot(df_long, aes(x = Porcentaje, y = model, fill = Tipo)) +
  geom_col(width = 0.7, position = "stack") +
  geom_text(aes(label = paste0(round(Porcentaje, 1), "%")),
            position = position_stack(vjust = 0.5),
            color = "white",
            size = 3) +
  scale_fill_manual(values = c("Válidas" = "#336699", "Inválidas" = "#990000")) +
  labs(title = "",
       x = "Porcentaje de Jugadas (%)",
       y = "Modelo",
       fill = "Tipo de Jugada") +
  coord_cartesian(xlim = c(0, 100)) +
  theme_minimal(base_size = 10) +
  theme(axis.text.y = element_text(size = 7),
        axis.title.y = element_text(margin = margin(r = 10)),
        axis.title.x = element_text(margin = margin(t = 10)),
        plot.title = element_text(face = "bold", hjust = 0.5, size = 14))
