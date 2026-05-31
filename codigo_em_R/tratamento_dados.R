#################################################################################
#  Autor: Edmilson Cosme da Silva (edmilsoncosme@unb.br)
#  Data: 04/setemblo/2022
#  Projeto: Previsao de evas?o para SIGAA/SIGRA
#
#  Arquivo: tratamento-dados.R
#  Descri??o: Func?es utilizadas para tratamento dos dados.
#################################################################################


incluir_Situacao = function(dados){
  
  # incluindo o campo situaÃ§Ã£o (FORMADO E TRANCADO) e exclusÃ£ do status_discente
  resultado <- dados %>%
    mutate( 
      situacao = ifelse((status_discente == "ATIVO - FORMANDO") | (status_discente == "CONCLUÍDO") | 
                          (status_discente == "Formatura") | (status_discente == "FORMADO"),
                        "FORMADO","EVADIDO"), .after = "status_discente"
    ) %>%
    select (-status_discente)
  
  return(resultado)
}

# atualiza a tabela do modelo com a situação do aluano
atualizarSituacaoAluno = function(aluno , situacao, dfDados){
  
  dfDados[as.character(aluno),"situacao"] <- situacao
  
  return(dfDados)
  
} 

montarTabelaDisciplinas = function(dfAlunos, dfDisciplinas){
  
  # transfoma a disciplina em um conjuto de fatores
  disciplinas <- dfDisciplinas$codigo_comp_curricular
  disciplinas <- as.factor(disciplinas)
  nomesColunas <- c(levels(disciplinas))
  
  # transfoma a matricula em um conjuto de fatores
  matricula <- dfAlunos$matricula
  matricula <- as.factor(matricula)
  matricula <- c(levels(matricula))
  
  # montando a estrutura em tabela com as linhas e as colunas basedos no total de
  # matriculas e disciplinas cursadas
  dfdadosTabela <- data.frame(matrix(0,
                                     nrow = length(matricula),
                                     ncol = length(nomesColunas)))
  rownames(dfdadosTabela) <- matricula
  colnames(dfdadosTabela) <- nomesColunas
  
  # incluindo a coluna de situação
  situacao <- "0"
  dfdadosTabela <- cbind(dfdadosTabela,situacao)
  
  return(dfdadosTabela)
  
}

inserirDisplinasCursadas = function(dfDados, dfTabela){
  
  # rotina constru?da para realizar a inclusão do número de disciplias que foram cursadas
  # pelo aluno. Ou seja, calcula quantas veze o aluno fez a disciplina
  for (i in 1:length(dfDados$mat)){
    
    valor<- dfDados[dfDados$matricula == dfDados[i,1],]$codigo_comp_curricular
    valor <- as.factor(valor)
    resultado <- summary(valor)
    
    dfTabela <- atualizarMatricula(dfDados[i,1], resultado, dfTabela)
    
  }
  
  return(dfTabela)
  
}

# recebe o dataframe com as disciplinas cursadas com total de vezes
atualizarMatricula = function(aluno , disciplinas, dfDados){
  
  for (i in 1: length(disciplinas)){
    
    dfDados[as.character(aluno),names(disciplinas[i])] <- disciplinas[i]
    
  }
  
  return(dfDados)
  
} 


inserirSituacaoAluno = function(dfDados, dfTabela){
  
  # Inserindo a situação do aluno a tabela do modelos. Foi realizado um agrupamento
  # dos alunos por situaÃ§Ã£o 
  dfAlunoSituacao <- as.data.frame(
    dfDados[,c(1,3)] %>%
      select(
        matricula, situacao
      ) %>%
      group_by(
        matricula, situacao
      ) %>% 
      distinct(
        matricula
      )
  ) 

  # atualiza a tabela do modelo com a situação do aluano
  for (i in 1:length(dfAlunoSituacao$matricula)){
    
    dfTabela[as.character(dfAlunoSituacao[i,1]),"situacao"] <- dfAlunoSituacao[i,2]
    
  }
  # transformando a situaçao em um fator
  dfTabela$situacao <- as.factor(dfTabela$situacao)
  
  return(dfTabela)
  
}

selecionarDisplinasPorOpacao = function(dfDados, dfFiltro, tpDisciplina = tp){
  
  dfResultado <- dfDados %>%
    filter(
      opcao == dfFiltro$opcao, 
      nome_curso == dfFiltro$nome_curso,
      tipo_integralizacao %in% tpDisciplina
    ) %>%
    select(
      matricula, codigo_comp_curricular          
    )
  
  return(dfResultado)
}

selecionarAlunos = function(dfDados, dfFiltro, tpDisciplina = tp){
  
  dfResultado <- dfDados %>%
    filter(
      opcao == dfFiltro$opcao, 
      nome_curso == dfFiltro$nome_curso,
      ano_ingresso == dfFiltro$ano_ingresso,
      periodo_ingresso == dfFiltro$periodo_ingresso,
      tipo_integralizacao %in% tpDisciplina
    ) %>%
    select(
      matricula, codigo_comp_curricular,status_discente          
    )
  
  return(dfResultado)
}

selecinarCursos = function(dfDados, tp_integralizacao){
  
  dfResultado <- dfDados %>%
    filter(
      tipo_integralizacao %in% tp_integralizacao,
    ) %>%
    select(
      opcao, nome_curso, ano_ingresso, periodo_ingresso          
    ) %>%
    arrange(nome_curso, opcao, ano_ingresso, periodo_ingresso) %>%
    distinct()
  
  return(as.data.frame(dfResultado))
}


selecionarAlunosAtivosOpco <- function(dfDados, vIntegralizacao, vOpcao, vNome_Curso, vAno, vPerido){
  dfResultado <- dfDados %>% filter(
    tipo_integralizacao %in% vIntegralizacao,
    opcao == vOpcao,
    nome_curso == vNome_Curso,
    ano_ingresso == vAno,
    periodo_ingresso == vPerido 
  ) %>% select(
    matricula, codigo_comp_curricular
  ) 
  
  return(dfResultado)
}