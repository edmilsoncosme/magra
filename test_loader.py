from src.data_source import load_csv, apply_standard_filters, get_cursos, get_coortes

df = load_csv()
print(f"Total registros: {len(df)}")
print(df.head())

df_filtrado = apply_standard_filters(df)
print(f"Após filtros: {len(df_filtrado)}")
print(df_filtrado.head())

cursos = get_cursos(df_filtrado)
print(f"Total cursos: {len(cursos)}")
print(cursos[:5])

coortes = get_coortes(df_filtrado)
print(f"Total coortes: {len(coortes)}")
print(coortes[:5])  