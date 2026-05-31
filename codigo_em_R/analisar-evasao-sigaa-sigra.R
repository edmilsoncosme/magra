#################################################################################
#  Autor: Edmilson Cosme da Silva (edmilsoncosme@unb.br)
#  Data: 15/agosto/2022
#  Projeto: Previsao de evasão para SIGAA/SIGRA
#
#  Arquivo: analisar-evasao-sigaa-sigra.R
#  Descri??o: Arquivo com as análises nas bases.
#################################################################################

#install.packages("dplyr")
#install.packages('randomflorest')
#install.packages("C50")

install.packages("janitor")
install.packages("tidyverse")
#install.packages('randomForest')
install.packages("h2o")
install.packages("caTools")
install.packages("caret")
install.packages("rpart.plot")
install.packages('ranger')

# apagar todos os objetos
rm(list = ls())

library(tidyverse)
library(C50)
library(caTools)
library(caret)
library(rpart)
library(rpart.plot)
library(h2o)
#library(randomForest)
library(ranger)

######### Carrega o arquivo de conexão com as bases de dados.
source("data_source.R", encoding = "ISO-8859-1")

######### Fun??es para o tratamento de daods.
source("tratamento_dados.R", encoding = "ISO-8859-1")

####################### ALTERA??O NA ESTRUTURA DE CONTRU??O DOS MODELOS #########################

# F1 CORTE > 60
# Coortes com alunos somente EVADIDOS OU FORMADOS ser?o rejeitados por n?o haver possibilidade de montar a 
# matriz de confus?o. Tumas com um aluno devem ser rejeitadas de inicio se for poss?vel. 

# Montar a tabela de disciplinas com todas as disciplinas poss?veis de serem feitas por alunoas de uma mesma op??o
# Os alunos devem ser definidos por coorte (ano_ingresso e periodo_ingresso)
# O modelo gerados em um coorte, dever ser testado em outros coortes para verificar qual o melhor conjuto de daods 
# gera o melhor modelo.
#################################################################################################

h2o.init(nthreads = -1)

# define os tipos de disciplinas
#tipo_integralizacao <- c("OB", "OBR", "OBS", "OPT")
tipo_integralizacao <- c("OB", "OBR")
# especifica uma fonte para a constru??o do nome do arquivo de sa?da.
#fonte_informacao <- "FGA"s
fonte_informacao <- "UnB"


gerar_modelos <- function() {
  

    
    if (fonte_informacao == 'FGA'){
      con <- conectar()
      dados_SIGAA <- le_dados1(con, sql = sigaa)
      con <- conectar()
      dados_SIGRA <- le_dados1(con, sql = sigra)
      dados_UnB <- rbind(dados_SIGAA, dados_SIGRA)  
    }else{
      con <- conectar()
      dados_UnB <- le_dados1(con, sql = sigaa_sigra_unb)
    }
  
  
   # capturando o nome dos cursos
   dfCursos <- dados_UnB %>% select (nome_curso) %>% distinct() %>% arrange(nome_curso)
   nomes_cursos<- unique(str_to_upper(dfCursos$nome_curso))
   
   arquivo_nome_curso_Rdata <-
     paste0(
       "arquivos/modelos/nome_cursos_",
       fonte_informacao,".Rdata"
     )
   save(nomes_cursos, file =  arquivo_nome_curso_Rdata)
  
   for (i in 1:length(nomes_cursos)){
     strDisciplina <- ''
     dados <- dados_UnB %>% filter(str_to_upper(nome_curso) == nomes_cursos[i])
     
     # concatenando o nome da universidade com a disciplina
     strDisciplina <-
       paste0(fonte_informacao, "_", str_to_lower(nomes_cursos[i]))
     # removendo espços em branco
     strDisciplina <- gsub(" ", "", strDisciplina)
     
     # filtrando o curso por opcao
     dfOpcoes <- selecinarCursos(dados, tipo_integralizacao)
     # verifica se retornou alguma opção para o curso. Se não, vai para o proximo curso
     if (length(dfOpcoes$opcao) == 0){
       next
     }
     # dataframe que recebe dos valores dos modelos gerados
     dfMod_Resultado <- data.frame()
     
     # listas que recebem os modelos
     listaC5 <- list()
     listaRF <- list()
     listaRpart <- list()
     listaRegLog <- list()
     listaRN <- list()
     
     for (i in 1:length(dfOpcoes$opcao)) {
       print(paste("Opção: ", dfOpcoes$opcao[i]))
       print(paste("Curso: ", dfOpcoes$nome_curso[i]))
       print(paste("Ano Ingresso: ", dfOpcoes$ano_ingresso[i]))
       print(paste("Periodo Ingresso: ", dfOpcoes$periodo_ingresso[i]))
       
       # selecionando as disciplinas que forarm cursadas em uma opcao especifica.
       dfDisplinasOpcao <-
         selecionarDisplinasPorOpacao(dados, dfOpcoes[i,], tpDisciplina = tipo_integralizacao)
       
       # seleciona os alunos de uma coorte por opção cursada.
       dfAlunos <-
         selecionarAlunos(dados, dfOpcoes[i,], tpDisciplina =  tipo_integralizacao)
       
       dfAlunos <- incluir_Situacao(dfAlunos)
       
       # verifica se existe a classe formado ou evadido.
       # Se os alunos selecionados só tiverem um tipo de classe não é possivel fazer a previsão.
       if (length(unique(dfAlunos$situacao)) >= 2) {
         
         # if (!is.null(dfdadosT)) {
         #   rm(dfdadosT) 
         # }
         
         dfdadosT  <-
           montarTabelaDisciplinas(dfAlunos, dfDisplinasOpcao)
         #break
         
         dfdadosT  <-
           inserirDisplinasCursadas(dfAlunos[, 1:2], dfdadosT)
         
         # total de alunos e disciplinas por coorte
         total_alunos <- length(dfdadosT[, 1])
         total_disciplinas <- length(dfdadosT) - 1
         
         print(paste("Total de alunos: ", total_alunos))
         print(paste("Total de disciplinas: ", total_disciplinas))
         
         dfdadosT  <- inserirSituacaoAluno(dfAlunos, dfdadosT)
         
         ###### divisão das basese de treinamento e teste ##################
         # set.seed(1)
         # divisao = sample.split(dfdadosT$situacao, SplitRatio = 0.75)
         # dfdadosT_treinamento <- subset(dfdadosT,divisao == TRUE)
         # dfdadosT_teste <- subset(dfdadosT,divisao == FALSE)
         
         # C5.O
         tryCatch({
           myFormula <- as.formula(situacao ~ .)
           modelo_C5 <-
             C5.0(myFormula, data = dfdadosT, trials = 10)
           #plot(modelo_C5)
           previsoes <-
             predict(modelo_C5, newdata = dfdadosT %>% select(-situacao))
           matriz_confusao <- table(dfdadosT$situacao, previsoes)
           F1_C5O <-
             confusionMatrix(matriz_confusao, mode = "everything")$byClass[7]
           #confusionMatrix(matriz_confusao, mode = "everything", positive="FORMADO")
           print(paste("F1_C5O: ", F1_C5O))
           
           if (!is.na(F1_C5O) & F1_C5O >= 0.7) {
             listaC5 <-
               c(
                 listaC5,
                 list(
                   F1_C5O,
                   modelo_C5,
                   dfOpcoes$opcao[i],
                   dfOpcoes$nome_curso[i],
                   dfOpcoes$ano_ingresso[i],
                   dfOpcoes$periodo_ingresso[i],
                   'C5'
                 )
               )
           }
         },
         specialError = function(e) {
           print("Erro no C5.O\n")
         },
         error = function(e) {
           F1_C5O <- "Erro"
           print(paste("F1_C5O: ", F1_C5O))
         })
         
         # RONDOMFLOREST
         tryCatch({
           myFormula <- as.formula(situacao ~ .)
           modelo_RF <-
             ranger(myFormula, data = dfdadosT, num.trees = 10)
           previsoes_RF <-
             predict(modelo_RF, data = dfdadosT %>% select(-situacao))
           
           ## Classification forest
           ranger(Species ~ ., data = iris)
           train.idx <- sample(nrow(iris), 2 / 3 * nrow(iris))
           iris.train <- iris[train.idx, ]
           iris.test <- iris[-train.idx, ]
           rg.iris <- ranger(Species ~ ., data = iris.train)
           pred.iris <- predict(rg.iris, data = iris.test)
           table(iris.test$Species, pred.iris$predictions)
           
           
           matriz_confusao <-
             table(dfdadosT$situacao, previsoes_RF$predictions)
           
           F1_RF <-
             confusionMatrix(matriz_confusao, mode = "everything")$byClass[7]
           
           print(paste("F1_RF: ", F1_RF))
           
           if (!is.na(F1_RF) & F1_RF >= 0.7) {
             listaRF <-
               c(
                 listaRF,
                 list(
                   F1_RF,
                   modelo_RF,
                   dfOpcoes$opcao[i],
                   dfOpcoes$nome_curso[i],
                   dfOpcoes$ano_ingresso[i],
                   dfOpcoes$periodo_ingresso[i],
                   'RF'
                 )
               )
           }
         },
         specialError = function(e) {
           print("Erro no RANDOM FOREST\n")
         },
         error = function(e) {
           F1_RPART <- "Erro"
           print(paste("F1_RF: ", F1_RF))
         })
         
         # RPART
         tryCatch({
           modelo_Rpart <- rpart(myFormula, data = dfdadosT)
           #rpart.plot(modelo_Rpart)
           previsoes_Rpart <-
             predict(modelo_Rpart,
                     newdata = dfdadosT %>% select(-situacao),
                     type = 'class')
           matriz_confusao <-
             table(dfdadosT$situacao, previsoes_Rpart)
           F1_RPART <-
             confusionMatrix(matriz_confusao, mode = "everything")$byClass[7]
           #confusionMatrix(matriz_confusao, mode = "everything")
           print(paste("F1_RPART: ", F1_RPART))
           
           if (!is.na(F1_RPART) & F1_RPART >= 0.7) {
             listaRpart <-
               c(
                 listaRpart,
                 list(
                   F1_RPART,
                   modelo_Rpart,
                   dfOpcoes$opcao[i],
                   dfOpcoes$nome_curso[i],
                   dfOpcoes$ano_ingresso[i],
                   dfOpcoes$periodo_ingresso[i],
                   'RPART'
                 )
               )
           }
         },
         specialError = function(e) {
           print("Erro no RPART\n")
         },
         error = function(e) {
           F1_RPART <- "Erro"
           print(paste("F1_RPART: ", F1_RPART))
         })
         
         # Regressao Logistica
         tryCatch({
           modelo_Reg_logistica <-
             glm(myFormula, data = dfdadosT, family = binomial)
           probabilidades <-
             predict(
               modelo_Reg_logistica,
               newdata = dfdadosT %>% select(-situacao),
               type = 'response'
             )
           previsoes_Reg_logistica <-
             ifelse(probabilidades > 0.5, "FORMADO", "EVADIDO")
           matriz_confusao <-
             table(dfdadosT$situacao, previsoes_Reg_logistica)
           F1_RegLog <-
             confusionMatrix(matriz_confusao, mode = "everything")$byClass[7]
           print(paste("F1_RegLog: ", F1_RegLog))
           
           if (!is.na(F1_RegLog) & F1_RegLog >= 0.7) {
             listaRegLog <-
               c(
                 listaRegLog,
                 list(
                   F1_RegLog,
                   modelo_Reg_logistica,
                   dfOpcoes$opcao[i],
                   dfOpcoes$nome_curso[i],
                   dfOpcoes$ano_ingresso[i],
                   dfOpcoes$periodo_ingresso[i],
                   'RegLog'
                 )
               )
           }
         },
         specialError = function(e) {
           print("Erro na regress?o\n")
         },
         error = function(e) {
           F1_RegLog <- "Erro"
           print(paste("F1_RegLog: ", F1_RegLog))
         })
         
         # Rede Neural
         tryCatch({
           modelo_RN <- h2o.deeplearning(
             y = 'situacao',
             training_frame = as.h2o(dfdadosT),
             hidden = c(100),
             #camadas ocultas
             epochs = 1000
           ) # quantas vezes vai ajustar os pesos
           previsoes_RN <-
             h2o.predict(modelo_RN, newdata = as.h2o(dfdadosT %>% select(-situacao)))
           previsoes_RN <- as.vector(previsoes_RN$predict)
           matriz_confusao <- table(dfdadosT$situacao, previsoes_RN)
           F1_RN <-
             confusionMatrix(matriz_confusao, mode = "everything")$byClass[7]
           print(paste("F1_RN: ", F1_RN))
           
           if (!is.na(F1_RN) & F1_RN >= 0.7) {
             listaRN <-
               c(
                 listaRN,
                 list(
                   F1_RN,
                   modelo_RN,
                   dfOpcoes$opcao[i],
                   dfOpcoes$nome_curso[i],
                   dfOpcoes$ano_ingresso[i],
                   dfOpcoes$periodo_ingresso[i],
                   'RN'
                 )
               )
           }
         },
         specialError = function(e) {
           print("Erro na rede neural\n")
         },
         error = function(e) {
           F1_RN <- "Erro"
           print(paste("F1_RN: ", F1_RN))
         })
         
         print("___________________________________________________")
         
         opcao <- dfOpcoes$opcao[i]
         curso <- dfOpcoes$nome_curso[i]
         ano_ingresso <- dfOpcoes$ano_ingresso[i]
         periodo_ingresso <- dfOpcoes$periodo_ingresso[i]
         status <- "OK"
         tp_integralizacao <-
           paste(tipo_integralizacao, collapse = "_")
         
         dfMod_Resultado  <- rbind(
           dfMod_Resultado,
           data.frame(
             opcao,
             curso,
             ano_ingresso,
             periodo_ingresso,
             total_alunos,
             total_disciplinas,
             F1_C5O,
             F1_RF,
             F1_RPART,
             F1_RegLog,
             F1_RN,
             tp_integralizacao,
             status
           )
         )
         
       }# fim if sitacao
       else{
         opcao <- dfOpcoes$opcao[i]
         curso <- dfOpcoes$nome_curso[i]
         ano_ingresso <- dfOpcoes$ano_ingresso[i]
         periodo_ingresso <- dfOpcoes$periodo_ingresso[i]
         total_alunos <- ""
         total_disciplinas <- ""
         status <- "Erro de classe"
         F1_C5O <- ""
         F1_RF <- ""
         F1_RPART <- ""
         F1_RegLog <- ""
         F1_RN <- ""
         tp_integralizacao <-
           paste(tipo_integralizacao, collapse = "_")
         
         dfMod_Resultado  <- rbind(
           dfMod_Resultado,
           data.frame(
             opcao,
             curso,
             ano_ingresso,
             periodo_ingresso,
             total_alunos,
             total_disciplinas,
             F1_C5O,
             F1_RF,
             F1_RPART,
             F1_RegLog,
             F1_RN,
             tp_integralizacao,
             status
           )
         )
         
         print("___________________________________________________")
         
       }# fim else situacao
       
     } # fim for
     
     listaModelos <-
       list(listaC5, listaRpart, listaRF, listaRegLog, listaRN)
     
     # removendo lista de modelos vazia
     contaLista <- 1
     tamanhoLista <- length(listaModelos)
     while (tamanhoLista >= 1) {
       if (length(listaModelos[[contaLista]]) == 0) {
         listaModelos[[contaLista]] <- NULL
         tamanhoLista <- tamanhoLista - 1
       } else{
         contaLista <- contaLista + 1
       }
       tamanhoLista <- tamanhoLista - 1
     }
     
     # salvando os modelos
     arquivo_Rdata <-
       paste0(
         "arquivos/modelos/modelos_treinados_",
         strDisciplina,
         "_",
         stringr::str_to_lower(paste(tipo_integralizacao, collapse = "_")),
         ".Rdata"
       )
     # save(listaModelos, file =  "modelos_treinados_ob_fga.Rdata")
     save(listaModelos, file =  arquivo_Rdata)
     
     # salvando listagem do andamento dos modelos
     arquivo_csv <-
       paste0(
         "arquivos/resultado/modelo_resultado_",
         strDisciplina,
         "_",
         stringr::str_to_lower(paste(tipo_integralizacao, collapse = "_")),
         ".csv"
       )
     #write.csv2(dfMod_Resultado, file = "modelo_resultado_ob_fga.csv", row.names = TRUE, fileEncoding = "UTF-16")
     write.csv2(
       dfMod_Resultado,
       file = arquivo_csv,
       row.names = TRUE,
       fileEncoding = "UTF-16"
     )
     
   } # fim for cursos
  
}
 
inicio <- Sys.time() 
gerar_modelos()
Sys.time() - inicio


realizar_previsao <- function(){
  
  if (fonte_informacao == 'FGA'){
    con <- conectar()
    todos_alunos <- le_dados1(conexao = con, sql = sigaa_sigra_todos)
    con <- conectar()
    alunos_ativos_sigaa <- le_dados1(conexao = con, sql = sigaa_ativos)
  }else{
    con <- conectar()
    todos_alunos <- le_dados1(conexao = con, sql = sigaa_sigra_unb_todos)
    con <- conectar()
    alunos_ativos_sigaa <- le_dados1(conexao = con, sql = sigaa_unb_ativos)
  }

  # recuperando o nome dos cursos
  arquivo_nome_curso_Rdata <-
    paste0(
      "arquivos/modelos/nome_cursos_",
      fonte_informacao,".Rdata"
    )
  load(arquivo_nome_curso_Rdata)
  
  for (i in 1:length(nomes_cursos)){
    
    # recuperando os modelos selecinados
    strDisciplina <- ''
    strDisciplina <-
      paste0(fonte_informacao, "_", str_to_lower(nomes_cursos[i]))
    # removendo espços em branco
    strDisciplina <- gsub(" ", "", strDisciplina)
    
    
    #dataframe que recebera a previsão dos alunos evadidos por modelo
    dfMatriculasGeral <- data.frame()
    
    # dataframe criado para receber os erros durante as itera??es nas litas dos modelos
    dfLog <- data.frame()
    
    # recuperando os modelos selecinados. Tenta abrir o arquivo se não der erro retorna TRUE.
    dfErro <- tryCatch({
      
      arquivo_Rdata <-
        paste0(
          "arquivos/modelos/modelos_treinados_",
          strDisciplina,
          "_",
          stringr::str_to_lower(paste(tipo_integralizacao, collapse = "_")),
          ".Rdata"
        )
      
      load(arquivo_Rdata)
      return = TRUE 
    },
    error = function(e) {
      print(paste("Erro: O Modelo ",strDisciplina, "não encontrado.", e))
    })
    
    # caso o log de erro exista, adiciona o dataframe de log e vança para o próximo
    if (!is_logical(dfErro)) {
      dfLog <- rbind(dfErro[1], dfLog)
      rm(dfErro)
      next
    }
    
  
  # percorre a lista de modelos
  for (i in 1:length(listaModelos)) {
    # se encontrar lista de modelos vazia avançar para o próximo modelo.
    if (length(listaModelos[[i]]) == 0){
      next
    }
    
    for (j in seq(2, length(listaModelos[[i]]), 7)) {
      
      modelo <- listaModelos[[i]][j]
      opcao <- as.character(listaModelos[[i]][j + 1])
      nome_curso <- as.character(listaModelos[[i]][j + 2])
      ano <- as.integer(listaModelos[[i]][j + 3])
      periodo <- as.integer(listaModelos[[i]][j + 4])
      desc_mode <- as.character(listaModelos[[i]][j + 5])
      
      # selecionando disciplinas por op??o e tipo integraliza??o.
      dfDisplinasOpcao <-
        selecionarDisplinasPorOpacao(todos_alunos,
                                     data.frame(opcao, nome_curso),
                                     tpDisciplina = tipo_integralizacao)
      
      # seleciona os alunos de uma opcao filtrados pelo coorte
      dfAlunosAtivos <-
        selecionarAlunosAtivosOpco(alunos_ativos_sigaa,
                                   tipo_integralizacao,
                                   opcao,
                                   nome_curso,
                                   ano,
                                   periodo)
      
      if (length(dfAlunosAtivos$matricula) >= 1) {
        dfdadosT  <-
          montarTabelaDisciplinas(dfAlunosAtivos, dfDisplinasOpcao)
        dfdadosT  <-
          inserirDisplinasCursadas(dfAlunosAtivos[, 1:2], dfdadosT)
        dfdadosT$situacao  <- NULL
        # convertendo a matricula em coluna
        dfdadosT$matricula <- row.names(dfdadosT)
        
        # total de alunos e disciplinas por coorte
        total_alunos <- length(dfdadosT[, 1])
        total_disciplinas <- length(dfdadosT) - 1
        
        print("___________________________________________________")
        
        print(paste("Opção: ", opcao))
        print(paste("Total de alunos: ", total_alunos))
        print(paste("Total de disciplinas: ", total_disciplinas))
        print(paste("Curso: ", opcao , nome_curso, ano, periodo))
        print(paste("Modelo: ", desc_mode))
        
        
        dfErro <- tryCatch({
          if (desc_mode == "C5") {
            previsoes <-
              predict(modelo, newdata = dfdadosT %>% select(-matricula))
            
            dfMatriculas <- rbind(dfdadosT)
            dfMatriculas$previsoes <-
              cbind(as.character(previsoes[[1]]))
            
            dfMatriculas_C5 <- dfMatriculas %>%
              filter(previsoes == "EVADIDO") %>%
              select(matricula, previsoes)
            
            if (length(dfMatriculas_C5$matricula) != 0) {
              dfMatriculas_C5$modelo <- desc_mode
              dfMatriculas_C5$opcao <-  opcao
              dfMatriculas_C5$nome_curso <-  nome_curso
              dfMatriculas_C5$ano_ingresso <-  ano
              dfMatriculas_C5$periodo_ingresso <-  periodo
              dfMatriculas_C5$total_alunos <- total_alunos
              dfMatriculasGeral <-
                rbind(dfMatriculas_C5, dfMatriculasGeral)
              #print(dfMatriculas_C5)
              # a limpeza desta vari?vel foi necess?ria, pois ela estava sendo retorna pela func?o trycach()
              rm(dfMatriculas_C5)
            }
            
          }
        },
        error = function(e) {
          #strErro <- paste("Erro F1_C5O ","na Op??o: ", opcao,e)
          print(paste("Erro F1_C5O ", "na Opção: ", opcao, e))
        })
        # caso o log de erro exista, adiciona no dataframe que ser? gravado
        if (!is.null(dfErro)) {
          dfLog <- rbind(dfErro[1], dfLog)
          rm(dfErro)
        }
        
        dfErro <- tryCatch({
          if (desc_mode == "RF") {
            previsoes_RF <-
              predict(modelo, data = dfdadosT %>% select(-matricula))
            
            dfMatriculas <- rbind(dfdadosT)
            dfMatriculas$previsoes <-
              cbind(as.character(previsoes_RF[[1]]$predictions))
            
            dfMatriculas_RF <- dfMatriculas %>%
              filter(previsoes == "EVADIDO") %>%
              select(matricula, previsoes)
            
            if (length(dfMatriculas_RF$matricula) != 0) {
              dfMatriculas_RF$modelo <- desc_mode
              dfMatriculas_RF$opcao <-  opcao
              dfMatriculas_RF$nome_curso <-  nome_curso
              dfMatriculas_RF$ano_ingresso <-  ano
              dfMatriculas_RF$periodo_ingresso <-  periodo
              dfMatriculas_RF$total_alunos <- total_alunos
              dfMatriculasGeral <-
                rbind(dfMatriculas_RF, dfMatriculasGeral)
              # a limpeza desta vari?vel foi necess?ria, pois ela estava sendo retorna pela func?o trycach()
              rm(dfMatriculas_RF)
            }
          }
        },
        error = function(e) {
          #strErro <- paste("Erro RF ","na Op??o: ", opcao,e)
          print(paste("Erro RF ", "na Opção: ", opcao, e))
        })
        
        # caso o log de erro exista, adiciona no dataframe que ser? gravado
        if (!is.null(dfErro)) {
          dfLog <- rbind(dfErro[1], dfLog)
          rm(dfErro)
        }
        
        dfErro <- tryCatch({
          if (desc_mode == "RPART") {
            previsoes_Rpart <-
              predict(modelo,
                      newdata = dfdadosT %>% select(-matricula),
                      type = 'class')
            
            dfMatriculas <- rbind(dfdadosT)
            dfMatriculas$previsoes <-
              cbind(as.character(previsoes_Rpart[[1]]))
            
            dfMatriculas_Rpart <- dfMatriculas %>%
              filter(previsoes == "EVADIDO") %>%
              select(matricula, previsoes)
            
            if (length(dfMatriculas_Rpart$matricula) != 0) {
              dfMatriculas_Rpart$modelo <- desc_mode
              dfMatriculas_Rpart$opcao <-  opcao
              dfMatriculas_Rpart$nome_curso <-  nome_curso
              dfMatriculas_Rpart$ano_ingresso <-  ano
              dfMatriculas_Rpart$periodo_ingresso <-  periodo
              dfMatriculas_Rpart$total_alunos <- total_alunos  
              dfMatriculasGeral <-
                rbind(dfMatriculas_Rpart, dfMatriculasGeral)
              # a limpeza desta vari?vel foi necess?ria, pois ela estava sendo retorna pela func?o trycach()
              rm(dfMatriculas_Rpart)
            }
          }
        },
        error = function(e) {
          #strErro <- paste("Erro RPART ","na Op??o: ", opcao,e)
          print(paste("Erro RPART ", "na Opção: ", opcao, e))
        })
        
        # caso o log de erro exista, adiciona no dataframe que ser? gravado
        if (!is.null(dfErro)) {
          dfLog <- rbind(dfErro[1], dfLog)
          rm(dfErro)
        }
        
        dfErro <- tryCatch({
          if (desc_mode == "RegLog") {
            probabilidades <-
              predict(modelo,
                      newdata = dfdadosT %>% select(-matricula),
                      type = 'response')
            previsoes_Reg_logistica <-
              ifelse(as.double(unlist(probabilidades)) > 0.5, "FORMADO", "EVADIDO")
            previsoes_Reg_logistica <-
              as.list(previsoes_Reg_logistica)
            
            dfMatriculas <- rbind(dfdadosT)
            dfMatriculas$previsoes <-
              cbind(as.character(previsoes_Reg_logistica))
            
            dfMatriculas_RegLog <- dfMatriculas %>%
              filter(previsoes == "EVADIDO") %>%
              select(matricula, previsoes)
            
            if (length(dfMatriculas_RegLog$matricula) != 0) {
              dfMatriculas_RegLog$modelo <- desc_mode
              dfMatriculas_RegLog$opcao <-  opcao
              dfMatriculas_RegLog$nome_curso <-  nome_curso
              dfMatriculas_RegLog$ano_ingresso <-  ano
              dfMatriculas_RegLog$periodo_ingresso <-  periodo
              dfMatriculas_RegLog$total_alunos <- total_alunos
              dfMatriculasGeral <-
                rbind(dfMatriculas_RegLog, dfMatriculasGeral)
              # a limpeza desta vari?vel foi necess?ria, pois ela estava sendo retorna pela func?o trycach()
              rm(dfMatriculas_RegLog)
            }
          }
        },
        error = function(e) {
          #strErro <- paste("Erro RegLog ","na Op??o: ", opcao,e)
          print(paste("Erro RegLog ", "na Opção: ", opcao, e))
        })
        
        # caso o log de erro exista, adiciona no dataframe que ser? gravado
        if (!is.null(dfErro)) {
          dfLog <- rbind(dfErro[1], dfLog)
          rm(dfErro)
        }
        
        dfErro <- tryCatch({
          if (desc_mode == "RN") {
            previsoes_RN <-
              h2o.predict(object = modelo[[1]], newdata = as.h2o(dfdadosT %>% select(-matricula)))
            
            previsoes_RN <- as.vector(previsoes_RN$predict)
            
            dfMatriculas <- rbind(dfdadosT)
            dfMatriculas$previsoes <-
              cbind(as.character(previsoes_RN))
            
            dfMatriculas_RN <- dfMatriculas %>%
              filter(previsoes == "EVADIDO") %>%
              select(matricula, previsoes)
            
            # condição que verifica se exite previs?o para algum aluno evadir.
            if (length(dfMatriculas_RN$matricula) != 0) {
              dfMatriculas_RN$modelo <- desc_mode
              dfMatriculas_RN$opcao <-  opcao
              dfMatriculas_RN$nome_curso <-  nome_curso
              dfMatriculas_RN$ano_ingresso <-  ano
              dfMatriculas_RN$periodo_ingresso <-  periodo
              dfMatriculas_RN$total_alunos <- total_alunos
              dfMatriculasGeral <-
                rbind(dfMatriculas_RN, dfMatriculasGeral)
              # a limpeza desta vari?vel foi necess?ria, pois ela estava sendo retorna pela func?o trycach()
              rm(dfMatriculas_RN)
            }
          }
        },
        error = function(e) {
          #strErro <- paste("Erro RN ","na Op??o: ", opcao,e)
          print(paste("Erro RN ", "na Opção: ", opcao, e))
        })
        
        # caso o log de erro exista, adiciona no dataframe que ser? gravado
        if (!is.null(dfErro)) {
          dfLog <- rbind(dfErro[1], dfLog)
          rm(dfErro)
        }
        
      } # fim if - Se exitem alunos ativos
      
      # fim da condição se a lista interna dos existe
      
    }# firm for 2
    
  } # fim for 1
  
  
  # escrevendo arquivo log
  if (length(dfLog) > 0) {
    names(dfLog) <- "Erro_log"
    log_csv <- paste0(
      "arquivos/logs/log_prev_",
      strDisciplina,
      "_",
      stringr::str_to_lower(paste(tipo_integralizacao, collapse = "_")),
      ".csv"
    )
    write.csv2(dfLog,
               file = log_csv,
               row.names = TRUE,
               fileEncoding = "UTF-16")
  }
  

  # escrevendo no formato csv o dataframe
  if (length(dfMatriculasGeral) > 0 ) {
    nomesColunas <-
      c(
        "matricula",
        "previsao",
        "modelo",
        "opcao",
        "curso",
        "ano_gresso",
        "periodo_ingresso",
        "total_alunos"
      )
    names(dfMatriculasGeral) <- nomesColunas
    arquivo_csv <-
      paste0(
        "arquivos/previsoes/previsao_evasao_",
        strDisciplina,"_",
        stringr::str_to_lower(paste(tipo_integralizacao, collapse = "_")),
        ".csv"
      )
    write.csv2(
      dfMatriculasGeral,
      file = arquivo_csv,
      row.names = TRUE,
      fileEncoding = "UTF-16"
    )
  }else{
    print("Não realizou previsão")
  }
  
  
  } # for recuperando os cursos

}

inicio <- Sys.time()  
realizar_previsao()
Sys.time() - inicio



