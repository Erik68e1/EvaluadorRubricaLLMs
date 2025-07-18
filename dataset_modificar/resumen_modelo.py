########################################################################################################
################################  VISUALIZAR NUM - PARTIDAS Y JUGADAS  #################################
########################################################################################################
# Muestra el nuemro de partidas, jugadas, jugadas válidas e inválidas
import pandas as pd

df = pd.read_csv(r"dataset1.csv")

# Agrupar por modelo
resumen = df.groupby('model').agg(
    partidas_unicas=('id_match', pd.Series.nunique),
    jugadas_totales=('id_match', 'count'),
    jugadas_validas=('valid', lambda x: (x == 1).sum()),
    jugadas_invalidas=('valid', lambda x: (x == 0).sum())
).reset_index()

# Exportar a archivo Excel
resumen.to_excel("resumen_modelos.xlsx", index=False)

print("Archivo 'resumen_modelos.xlsx' generado con éxito.", resumen)
