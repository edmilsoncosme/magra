from src.data_source import load_csv, apply_standard_filters
from src.transform import incluir_situacao, TabelaPivot, selecionar_alunos

df = load_csv()
print("Dados carregados:")
print(df.head())
print(df.info())
nome_cursos = df['nome_curso'].unique()
print("Cursos disponíveis:")
for curso in nome_cursos:
    print(curso)

# opcoes = df['opcao'].unique()
# print("Opções disponíveis:")
# for opcao in opcoes:
#     print(opcao)

df = apply_standard_filters(df)
df = incluir_situacao(df)
df_filtrado = selecionar_alunos(df, nome_curso="ENGENHARIA DE SOFTWARE", opcao="140")
# df_filtrado = selecionar_alunos(df, nome_curso="ENGENHARIA DE SOFTWARE")
# print(df_filtrado['opcao'].unique())
print("Dados filtrados:")
print(df_filtrado.head())

# pivot = TabelaPivot().montar(df_filtrado)