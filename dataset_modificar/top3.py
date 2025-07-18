########################################################################################################
################################  VISUALIZAR TOP - BOTTOM EVALUADORES  #################################
########################################################################################################
# Indica los 3 mejores y peores modeloes segun el evaluador

import pandas as pd

ruta = r"resumen_deepseek.xlsx"
df = pd.read_excel(ruta) 

# === 2. Verificar que exista la columna 'Promedio'
if "Promedio General" not in df.columns:
    raise ValueError("No se encontró la columna 'Promedio' en el archivo.")

# === 3. Ordenar y extraer top y bottom 3
top_3 = df.sort_values(by="Promedio General", ascending=False).head(3)
bottom_3 = df.sort_values(by="Promedio General", ascending=True).head(3)

# === 4. Mostrar resultados
print("=== Mejores 3 modelos según promedio general ===")
print(top_3[["modelo", "Promedio General"]].to_string(index=False))

print("\n=== Peores 3 modelos según promedio general ===")
print(bottom_3[["modelo", "Promedio General"]].to_string(index=False))
