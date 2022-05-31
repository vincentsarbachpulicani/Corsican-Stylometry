
library(tidyverse) # manipulation
library(stm) # modélisation
library(stminsights) # interface graphique
library(NLP)
library(tm) # pour les stopwords

getwd()


brut_df <- read.csv("output_output_good_data.csv")

df_art = subset(brut_df, Type == 'article', select = c("Titre", "Auteur", "Type", "Langue", "Texte"))
df_poe = subset(brut_df, Type == 'poesie', select = c("Titre", "Auteur", "Type", "Langue", "Texte"))

df_cos <- subset(brut_df, Langue == 'cos', select = c("Titre", "Auteur", "Type", "Langue", "Texte"))
df_fra <- subset(brut_df, Langue == 'fra', select = c("Titre", "Auteur", "Type", "Langue", "Texte"))
df_ita <- subset(brut_df, Langue == 'ita', select = c("Titre", "Auteur", "Type", "Langue", "Texte"))




function_topmod_fra <- function(df){
  propre <- textProcessor(df$Texte,
                        metadata = df,
                        language = "fr",
                        stem = F) # nettoyage de base
  
  out <- prepDocuments(propre$documents, 
                     propre$vocab, 
                     propre$meta, 
                     lower.thresh = 2) # élimination de mots rares
  
  fit <- stm(documents = out$documents,
           vocab = out$vocab,
           K = 5, # nombre souhaité de topics
           data = out$meta, # métadonnées
           #prevalence = ~Auteur, # métadonnées prises en compte
           max.em.its = 1000, # nombre maximal d'itérations
           init.type = "Spectral", # algorithme déterministe et efficace
           verbose = FALSE)
  
  plot(fit, type = "summary")
  labelTopics(fit, n = 5)

  
  Content <- stm(out$documents, out$vocab, K = 10,
                 #prevalence =~ Auteur, content =~ Auteur,
                 max.em.its = 1000, data = out$meta, init.type = "Spectral")
  
  plot(Content, type = "summary")
  labelTopics(Content)
}

function_topmod_ita <- function(df){
  propre <- textProcessor(df$Texte,
                          metadata = df,
                          language = "it",
                          stem = F) # nettoyage de base
  
  out <- prepDocuments(propre$documents, 
                       propre$vocab, 
                       propre$meta, 
                       lower.thresh = 2) # élimination de mots rares
  
  fit <- stm(documents = out$documents,
             vocab = out$vocab,
             K = 5, # nombre souhaité de topics
             data = out$meta, # métadonnées
             prevalence = ~Auteur, # métadonnées prises en compte
             max.em.its = 1000, # nombre maximal d'itérations
             init.type = "Spectral", # algorithme déterministe et efficace
             verbose = FALSE)
  
  plot(fit, type = "summary")
  labelTopics(fit, n = 5)
  
  
  Content <- stm(out$documents, out$vocab, K = 10,
                 #prevalence =~ Auteur, content =~ Auteur,
                 max.em.its = 1000, data = out$meta, init.type = "Spectral")
  
  plot(Content, type = "summary")
  labelTopics(Content)
}

test_fra = function_topmod_fra(df_fra)
test_ita = function_topmod_ita(df_ita)
test_cos = function_topmod_ita(df_cos)

test_art = function_topmod_fra(df_art)
test_art = function_topmod_ita(df_art)

test_poe = function_topmod_fra(df_poe)
test_poe = function_topmod_ita(df_poe)


save.image("modelling_memoire_2.rda")

run_stminsights()


