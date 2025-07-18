# === Librerías ===
library(readxl)
library(tidyverse)
library(fmsb)

# === Cargar datos ===
ruta_deepseek <- "resumen_deepseek.xlsx"
ruta_gemini   <- "resumen_gemini.xlsx"

df_deepseek <- read_excel(ruta_deepseek)
df_gemini   <- read_excel(ruta_gemini)

# === Dimensiones ===
dimensiones <- c(
  "Comprensión de Reglas", "Validez y Legalidad", "Razonamiento Estratégico",
  "Factualidad", "Coherencia Explicativa", "Claridad Lingüística", "Adaptabilidad"
)

# === Función para graficar con colores y leyenda clara ===
graficar_modelo_comparado <- function(modelo, titulo_grafica) {
  fila_ds <- df_deepseek %>% filter(modelo == !!modelo)
  fila_gm <- df_gemini %>% filter(modelo == !!modelo)
  
  if (nrow(fila_ds) == 0 || nrow(fila_gm) == 0) {
    cat("Modelo no encontrado en ambos datasets:", modelo, "\n")
    return(NULL)
  }
  
  df_radar <- bind_rows(fila_ds, fila_gm) %>%
    select(all_of(dimensiones)) %>%
    as.data.frame()
  
  rownames(df_radar) <- c("DeepSeek", "Gemini")
  
  df_radar <- rbind(rep(3, length(dimensiones)), rep(1, length(dimensiones)), df_radar)
  
  radarchart(df_radar,
             axistype = 1,
             pcol = c("#0072B2", "#D55E00"),           
             pfcol = c(NA, NA),                         
             plwd = 3,
             cglcol = "gray80", cglty = 1,
             axislabcol = "gray40",
             caxislabels = seq(1, 3, 0.5),
             cglwd = 0.8,
             vlcex = 0.9,
             title = titulo_grafica
  )
  
  legend("bottom", inset = c(0, -0.1),
         legend = c(paste0("DeepSeek: ", fila_ds$modelo),
                    paste0("Gemini: ", fila_gm$modelo)),
         col = c("#0072B2", "#D55E00"),
         lty = 1, lwd = 3,
         bty = "n", cex = 0.9,
         horiz = TRUE, xpd = TRUE)
}

# === Extraer modelos ===
top3_deepseek <- df_deepseek %>% arrange(desc(`Promedio General`)) %>% slice(1:3) %>% pull(modelo)
top3_gemini   <- df_gemini   %>% arrange(desc(`Promedio General`)) %>% slice(1:3) %>% pull(modelo)
bot3_deepseek <- df_deepseek %>% arrange(`Promedio General`) %>% slice(1:3) %>% pull(modelo)
bot3_gemini   <- df_gemini   %>% arrange(`Promedio General`) %>% slice(1:3) %>% pull(modelo)

modelos_comparar <- c(top3_deepseek, top3_gemini, bot3_deepseek, bot3_gemini)

# === Mostrar gráficas ===
for (i in seq_along(modelos_comparar)) {
  modelo <- modelos_comparar[i]
  
  tipo <- case_when(
    i <= 3 ~ paste("Top", i, "- según DeepSeek"),
    i <= 6 ~ paste("Top", i - 3, "- según Gemini"),
    i <= 9 ~ paste("Bottom", i - 6, "- según DeepSeek"),
    TRUE   ~ paste("Bottom", i - 9, "- según Gemini")
  )
  
  cat(paste0("Gráfica ", i, " - ", tipo, " - Modelo: ", modelo, "\n"))
  graficar_modelo_comparado(modelo, titulo_grafica = tipo)
  readline(prompt = "Presiona Enter para continuar...")
}
