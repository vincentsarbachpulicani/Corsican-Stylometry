# Début du script

require("stringi")

setwd("~/dev/projet_R/textes")
dossier = dir()

clean_text = function(document){
  texte = readLines(document, encoding = 'utf-8')
  texte = stri_trans_nfc(texte)
  texte = tolower(texte)
  length(texte)
  texte = gsub("s'ell'","si ellu ",texte, fixed=TRUE)
  texte = gsub("s’ell’","si ellu ",texte,fixed = TRUE)
  texte = gsub("’"," ",texte,fixed=TRUE)
  texte = gsub("'"," ",texte,fixed=TRUE)
  texte = gsub("."," ",texte,fixed=TRUE)
  texte = gsub(","," ",texte,fixed=TRUE)
  texte = gsub("!"," ",texte,fixed=TRUE)
  texte = gsub("?"," ",texte,fixed=TRUE)
  texte = gsub("("," ",texte,fixed=TRUE)
  texte = gsub(")"," ",texte,fixed=TRUE)
  texte = gsub("-"," ",texte,fixed=TRUE)
  texte = gsub("é","e",texte,fixed=TRUE)
  texte = gsub("è","e",texte,fixed=TRUE)
  texte = gsub("ê","e",texte,fixed=TRUE)
  texte = gsub("à","a",texte,fixed=TRUE)
  texte = gsub("ù","u",texte,fixed=TRUE)
  texte = gsub("â","a",texte,fixed=TRUE)
  texte = gsub("ò","o",texte,fixed=TRUE)
  texte = gsub("ô","o",texte,fixed=TRUE)
  texte = gsub("î","i",texte,fixed=TRUE)
  texte = gsub("ì","i",texte,fixed=TRUE)
  texte = gsub(":"," ",texte,fixed=TRUE)
  return(texte)
}

txt1 = clean_text("almanaccu_1932.txt")
txt1
txt2 = clean_text("a-nostra-santa-fede.txt")
txt2
txt3 = clean_text("pontenovu.txt")
txt3
