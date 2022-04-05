import os
import shutil

os.system('mkdir pages_1') #création des dossiers qui cotniendront les différentes pages
os.system('mkdir pages_2')
os.system('mkdir pages_3')
parent = os.getcwd()
print('Directory : ' + parent)

foldernames = os.listdir()  #liste qui contient le nom de tous els dossiers -> correspond aux identifiants ARK
foldernames.remove('pages_1') #suppression des dossiers 'réceptacles' de la liste
foldernames.remove('pages_2')
foldernames.remove('pages_3')

for name in foldernames:
    if os.path.isdir(name): #si l'élément de la liste est un dossier, alors on se déplace dedans
        path = parent + '/' + name
        os.chdir(path)
        filenames = os.listdir()
        for file in filenames: #classification et renommage des fichiers en fonction de leur nature (page 1, 2 ou 3 du numéro de revue)
            if file == 'p1.jpg':
                os.rename(file, parent + '/pages_1/' + name + '_' + file)
            elif file == 'p2.jpg':
                os.rename(file, parent + '/pages_2/' + name + '_' + file)
            else:
                os.rename(file, parent + '/pages_3/' + name + '_' + file)
        print("ARK treated : " + name)
        os.chdir(parent) #on revient dans le dossier parent

print("Classification and renaming done.")