# Nettoyage des textes

library(stringi)
library(ggplot2)

setwd("~/dev/projet_R/")


clean_text = function(document){  # création d'une fonction pour nettoyer le texte de l'accentuation, de la casse et de la ponctuation afin d'isoler les MFW (most frequent words)
  texte = readLines(document, encoding = 'utf-8')
  texte = stri_trans_nfc(texte) # avec le package stringi, permet de normaliser en unicode l'encodage des textes (l'export eScriptorium de ces textes n'était pas normalisé)
  texte = tolower(texte)
  texte = gsub("’","'",texte,fixed=TRUE)
  texte = gsub("s'ell'","si ellu ",texte, fixed=TRUE)
  texte = gsub("s'ellu","si ellu ",texte,fixed = TRUE)
  texte = gsub("cum'è","cume hè",texte,fixed=TRUE)
  texte = gsub("s'hè","si hè",texte,fixed=TRUE)
  texte = gsub("quant'è","quantu hè",texte,fixed=TRUE)
  texte = gsub("quest'","questu hè",texte,fixed=TRUE)
  texte = gsub("d'","di ",texte,fixed=TRUE)
  texte = gsub("n'","ne ",texte,fixed=TRUE)
  texte = gsub("é","è",texte,fixed=TRUE) # l'accent aigu n'existe pas en langue corse, il s'agit surement d'un erreur de l'auteur ou de transcription
  texte = gsub("ô", "ò", texte, fixed=TRUE)
  texte = gsub(" è "," hè ",texte,fixed=TRUE)
  texte = gsub(" l "," lu ",texte,fixed=TRUE)
  texte = gsub(" s "," si ",texte,fixed=TRUE)
  texte = gsub(" ch "," chì ",texte,fixed=TRUE)
  texte = gsub("\""," ",texte,fixed=TRUE)
  texte = gsub("\\d|\\.|,|\\?|!|(|)|-|–|—|»|«|\\|", "", texte)
  texte = gsub("'|:|;| |  ", " ", texte)
  return(texte)
}

import <- function(folder){
  cwd <- getwd()
  files <- dir(folder)
  pathfiles = file.path(cwd,folder,files)
  corpus <- lapply(pathfiles,clean_text)
  return(c(corpus))
}

old_txt = import("old_texts/")
new_txt = import("new_texts/")

names_old = dir(path="~/dev/projet_R/old_texts/")
names_new = dir(path="~/dev/projet_R/new_texts/")

# Mise en évidence des caractéristiques des textes

car_old_txt = sum(nchar(old_txt))
car_old_txt

car_new_txt = sum(nchar(new_txt))
car_new_txt

car_txt = c(car_old_txt, car_new_txt)
corpus_names = c("Old texts", "New texts")


df_txt = data.frame(Corpus=corpus_names, Nb.Caractères = car_txt)
df_txt


split_old = unlist(strsplit(unlist(old_txt)," "))
word_old = length(split_old)

split_new = unlist(strsplit(unlist(new_txt)," "))
word_new = length(split_new)


word_txt = c(word_old,word_new)
rate_car_words = car_txt / word_txt

df_txt = data.frame(df_txt, Nb.Mots = word_txt,Caractères.par.mots = rate_car_words)

# Calculs de fréquences et premières visualisations

frequency = function(split_txt){
  unified_txt = paste(split_txt, collapse = " ")
  unified_txt = gsub("  ", " ",unified_txt,fixed=TRUE)
  unified_txt = gsub(" l "," lu ",unified_txt,fixed=TRUE) # Problèmes de lemmatisation
  unified_txt = gsub(" cum "," cume ",unified_txt,fixed=TRUE)
  split_txt = unlist(strsplit(unified_txt," "))
  freq_words_txt = summary(factor(split_txt))[1:15]
  total_words = length(split_txt)
  df = data.frame(MFW = names(freq_words_txt),Frequency = freq_words_txt,Rate = freq_words_txt/total_words*100)
}

df_old_mfw = frequency(split_old)
df_old_mfw

df_new_mfw = frequency(split_new)
df_new_mfw

barplot_old = ggplot(data=df_old_mfw, aes(x = MFW, y = Frequency, fill = MFW)) + geom_col()
barplot_old
barplot_new = ggplot(data=df_new_mfw, aes(x = MFW, y = Frequency, fill = MFW)) + geom_col()
barplot_new

# Réduction de dimension

word_frequency = function(text, text_research=""){
  word_list = unlist(strsplit(text," "))
  word_index = (word_list==text_research)
  words_total = length(word_list)
  rate = sum(word_index)/words_total
  return(rate)
}

matrix_freq = function(textes, freq_corpus){
  freq_mat=matrix(0, nrow = length(textes), ncol = length(freq_corpus[,1]))
  for (j in 1:length(textes)) {
    print(j)
    for (i in 1:length(freq_corpus[,1])) {
      freq_mat[j,i] = word_frequency(textes[[j]],freq_corpus$MFW[i])
    }
  }
  return(freq_mat)
}


old_words_15 = df_old_mfw[1:15,]
old_words_15
mat_old15 = matrix_freq(old_txt, old_words_15)
rownames(mat_old15) = names_old
colnames(mat_old15) = old_words_15[,1]
mat_old15


new_words_15 = df_new_mfw[1:15,]
new_words_15
mat_new15 = matrix_freq(new_txt, new_words_15)
rownames(mat_new15) = names_new
colnames(mat_new15) = new_words_15[,1]
mat_new15

# Visualisation des données réduites

hm_old = heatmap(mat_old15)
hm_new = heatmap(mat_new15)
