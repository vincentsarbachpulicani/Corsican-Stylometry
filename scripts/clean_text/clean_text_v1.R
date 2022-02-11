# Nettoyage des textes

library(stringi)
library(ggplot2)

setwd("~/dev/memoire/stylometrie-local/scripts/clean_text/test/")
dossier = dir() # Permet d'avoir accès au fichiers présents dans le dossier "textes", fichiers que nous utliserons

clean_text = function(document){  # création d'une fonction pour nettoyer le texte de l'accentuation, de la casse et de la ponctuation afin d'isoler les MFW (most frequent words)
  texte = readLines(document, encoding = 'utf-8')
  texte = stri_trans_nfc(texte) # avec le package stringi, permet de normaliser en unicode l'encodage des textes (l'export eScriptorium de ces textes n'était pas normalisé)
  texte = tolower(texte)
  length(texte)
  texte = gsub("’","'",texte,fixed=TRUE)
  texte = gsub("s'ell'|s'ellu","si ellu ",texte, fixed=TRUE)
  texte = gsub("s'ellu","si ellu ",texte,fixed = TRUE)
  texte = gsub("cum'è","cume è",texte,fixed=TRUE)
  texte = gsub("s'hè","si he",texte,fixed=TRUE)
  texte = gsub("quant'è","quantu he",texte,fixed=TRUE)
  texte = gsub("quest'","questu he",texte,fixed=TRUE)
  texte = gsub("d'","di ",texte,fixed=TRUE)
  texte = gsub("n'","ne ",texte,fixed=TRUE)
  texte = gsub("'"," ",texte,fixed=TRUE)
  texte = gsub("\""," ",texte,fixed=TRUE)
  texte = gsub(".","",texte,fixed=TRUE)
  texte = gsub(",","",texte,fixed=TRUE)
  texte = gsub("!","",texte,fixed=TRUE)
  texte = gsub("?","",texte,fixed=TRUE)
  texte = gsub("(","",texte,fixed=TRUE)
  texte = gsub(")","",texte,fixed=TRUE)
  texte = gsub("-","",texte,fixed=TRUE)
  texte = gsub("é","e",texte,fixed=TRUE)
  texte = gsub(" è "," he ",texte,fixed=TRUE)
  texte = gsub("hè","he",texte,fixed=TRUE)
  texte = gsub("ê","e",texte,fixed=TRUE)
  texte = gsub("è","e",texte,fixed=TRUE)
  texte = gsub("à","a",texte,fixed=TRUE)
  texte = gsub("ù","u",texte,fixed=TRUE)
  texte = gsub("â","a",texte,fixed=TRUE)
  texte = gsub("ò","o",texte,fixed=TRUE)
  texte = gsub("ô","o",texte,fixed=TRUE)
  texte = gsub("î","i",texte,fixed=TRUE)
  texte = gsub("ì","i",texte,fixed=TRUE)
  texte = gsub(":"," ",texte,fixed=TRUE)
  texte = gsub("–", "", texte,fixed=TRUE)
  texte = gsub(";"," ",texte,fixed=TRUE)
  texte = gsub("  "," ",texte,fixed=TRUE)
  texte = gsub("   "," ",texte,fixed=TRUE)
  texte = gsub(" l "," lu ",texte,fixed=TRUE)
  texte = gsub(" s "," si ",texte,fixed=TRUE)
  texte = gsub("—","",texte,fixed=TRUE)
  texte = gsub(" ch "," chi ",texte,fixed=TRUE)
  return(texte)
}

txt1 = clean_text("document.txt")

# Étape de la création d'un tableau dataframe

# On commence par calculer le nombre de caracrères de chacun des textes
cartxt1 = sum(nchar(txt1))
cartxt = c(cartxt1)
cartxt

# On crée la dataframe avec les deux premières colonnes : le nom de textes puis le nombre de caractères
df_txt = data.frame("Textes"=dossier,"Nb Caractères"=cartxt)
df_txt

# On calcule maintenant les occurences de mots
splittxt1 = unlist(strsplit(txt1," "))
wordtxt1 = length(splittxt1)
wordtxt = c(wordtxt1)

df_txt = data.frame(df_txt, "Nb Mots"=wordtxt)
df_txt

# Calcule d'un indice du nombre moyen de caractères par mots -> pas obligatoire, expliquer pourquoi
indice_mots_car = cartxt / wordtxt
indice_mots_car

df_txt = data.frame(df_txt, "Pourcentage caratères/mots"=indice_mots_car)
df_txt

# Les occurences de mots

split_txt = c(splittxt1)
unified_txt = paste(split_txt, collapse = " ")
unified_txt = gsub("  ", " ",unified_txt,fixed=TRUE)
unified_txt = gsub(" l "," lu ",unified_txt,fixed=TRUE)
unified_txt = gsub(" cum "," cume ",unified_txt,fixed=TRUE)
split_txt = unlist(strsplit(unified_txt," "))
freq_mots_txt = summary(factor(split_txt))
freq_mots_txt = freq_mots_txt[1:15]
freq_mots_txt


df_freq_mots = data.frame(mfw=names(freq_mots_txt),frequence=freq_mots_txt)
df_freq_mots
# write.csv(df_freq_mots,"/home/vsp/dev/projet_R/new-data.csv")

# Graphiques

graph1 = ggplot(data=df_freq_mots, aes(x=mfw, y=frequence)) + geom_bar(stat="identity")
graph1
