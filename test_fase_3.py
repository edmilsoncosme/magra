from src.data_source import load_csv, apply_standard_filters
from src.transform import incluir_situacao, TabelaPivot, selecionar_alunos


def limpar_dados(df):
    # Exemplo de limpeza de dados: remover linhas com valores NaN em 'cod_dis_sigra'
    df_limpo = df.dropna(subset=['cod_dis_sigra'])
    return df_limpo

df = load_csv()
# df = limpar_dados(df)
# print(type(df.isna().sum()))

# print("Dados carregados:") 
# # print(df.head())
# print(df.info())
# valor = df['cod_dis_sigra'].unique()
# contagem = df['cod_dis_sigra'].isna().sum()
# print(f"Contagem de valores NaN em 'cod_dis_sigra': {contagem}")
# print(valor)

nome_cursos = df[['nome_curso', 'opcao']].drop_duplicates()
print(nome_cursos.head())
# nome_cursos = df[['nome_curso', 'codigo_comp_curricular']].nunique()
# print("Cursos disponíveis:")
# for curso in nome_cursos:
#     print(curso)

# opcoes = df['opcao'].unique()
# print("Opções disponíveis:")
# for opcao in opcoes:
#     print(opcao)

df = apply_standard_filters(df)
df = incluir_situacao(df)
df_filtrado = selecionar_alunos(df, nome_curso="ENGENHARIA ELETRÔNICA", opcao=4005590)
# df_filtrado = selecionar_alunos(df, nome_curso="ENGENHARIA AUTOMOTIVA")

# print("Dados filtrados:")
# print(df_filtrado.info())
# print(df_filtrado.isnull().sum())
# print(df_filtrado['cod_dis_sigra'].unique())

pivot = TabelaPivot().montar(df_filtrado)
print("Tabela Pivot:")
print(pivot.head(20))
print(pivot.info())
