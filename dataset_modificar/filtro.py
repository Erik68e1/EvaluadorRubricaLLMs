########################################################################################################
#############################  QUITAR/REEMPLAZAR SOBRANTES DEL DATASET  ################################
########################################################################################################

import pandas as pd

dataset = r"dataset1.csv"  
df = pd.read_csv(dataset)
df['model'] = df['model'].str.replace(':free', '', regex=False)

archivoData = dataset.replace(".csv", ".csv")
df.to_csv(archivoData, index=False, encoding="utf-8")

print(f"Modelos limpiados y guardados en: {archivoData}")
