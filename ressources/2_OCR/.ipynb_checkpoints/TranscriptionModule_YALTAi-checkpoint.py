import csv
import os
import urllib3
import re
import codecs
import sys
import lxml.etree as ET
import pandas as pd
import shutil
import glob
from bs4 import BeautifulSoup as bs


def segmentation_YALTAi(folder_name, kraken_model=False):
    """
    Function allowing the segmentation of newspaper issues thanks to the YOLO model and the use of YALTAi that provides an adapter for Kraken to use YOLOv5 Object Detection routine.
    
    Parameters :
    
    folder_name = str, name of the folder where the issues are located.
    kraken_model = bool, allows to use or not the Kraken model for baselines corsicaFT_best.mlmodel.
    """
    issues = os.listdir(f"./{folder_name}/")
    
    for issue in issues:
        path = f"{folder_name}/{issue}/*.jpeg"
        if kraken_model is False:
            os.system(f"yaltai kraken --device cpu -I \"{path}\" --suffix \".xml\" segment --yolo runs/train/exp2/weights/best.pt")
        else:
            os.system(f"yaltai kraken --device cpu -I \"{path}\" --suffix \".xml\" segment --yolo runs/train/exp2/weights/best.pt -m corsicaFT_best.mlmodel")
            

def modif_fileName_element(folder_name):
    """
    Function that normalizes the <fileName> element of XML files produces by the segmentation/transcription to match the associated JPEG image.
    
    Parameter :
    
    folder_name = str, name of the folder where the issues are located.
    """
    issues = os.listdir(f"./{folder_name}/")
    
    for issue in issues:

        files = [f for f in os.listdir(f'./{folder_name}/{issue}') if f.endswith('xml')]

        for alto in files:
            if re.search(r"(page_\w+)", alto):
                ark = re.search(r"(page_\w+)", alto).group(1)

            content = []

            with open(f"./{folder_name}/{issue}/{alto}", "r") as file:
                content = file.readlines()

            content = "".join(content)
            bs_content = bs(content, "xml")

            result = bs_content.find("fileName")
            result.string = ark + ".jpeg"

            with open(f"./{folder_name}/{issue}/{alto}", "w") as file:
                file.write(str(bs_content))
            
            print(f"The file {alto} has been treated.")
                
def uzn_generator_from_alto(folder_name, id_name="block"):
    """
    Function that allows you to create UZN files from XML files obtained during segmentation with YALTAi. 
    
    Parameters :
    
    folder_name = str, name of the folder where the issues are located.
    id_name = str, start of the ID of the TextBlock element. Usefull to select the only elements we want.
    
    """
    issues = os.listdir(f"./{folder_name}/")
    
    for issue in issues:

        xml_files = [f for f in os.listdir(f'./{folder_name}/{issue}') if f.endswith('xml')]

        for xml in xml_files: #Pour chaque XML, le récupère les métadonnées relatives aux coordonnées de chaque TextBlock

            print(f'Name of the file : {xml}')

            if sys.stdout.encoding != 'UTF-8': # que j'implémente dans un fichier UZn nouvellement créé
                sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

            namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
                         'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                         'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#',
                         'alto-4': 'http://www.loc.gov/standards/alto/ns-v4#'}
            tree = ET.parse(f"./{folder_name}/{issue}/{xml}")
            xmlns = tree.getroot().tag.split('}')[0].strip('{')
            if xmlns in namespace.values():
                with open(f"./{folder_name}/{issue}/{xml}.uzn", "a+") as f:
                    all_ids =  []
                    
                    for line in tree.iterfind('.//{%s}TextBlock' % xmlns):
                        id_ref = line.attrib.get('ID')
                        #print(f"The ID of the block is : {id_ref}")
                        
                        if id_ref not in all_ids and line.attrib['ID'].startswith(id_name):
                            all_ids.append(id_ref)
                            text = line.attrib.get('HPOS') + ' ' + line.attrib.get('VPOS') + ' ' + line.attrib.get('WIDTH') + ' ' + line.attrib.get('HEIGHT') +  ' ' + line.attrib.get('ID') + '\n'
                            f.write(text)
                    
                    print(f'Number of regions : {len(all_ids)}')
                print(f"The UZN file from the {xml} has been created.")
            else:
                print('ERROR: Not a valid ALTO file (namespace declaration missing)')
    
    #Let's normalize the name of the UZN files
        uzn_files = [f for f in os.listdir(f'./{folder_name}/{issue}/') if f.endswith('.uzn')]
        
        for uzn in uzn_files:
            if re.search(r'(page_\w+)', uzn):
                name = re.search(r'(page_\w+)', uzn).group(1)
            os.rename(f"./{folder_name}/{issue}/{uzn}", f"./{folder_name}/{issue}/{name}.uzn")
    
def recognition_Tesseract(folder_name):
    """
    Function allowing character recognition using the Tesseract engine and following the UZN files obtained.
    
    Parameter :
    
    folder_name = str, name of the folder where the issues are located.
    """
    issues = os.listdir(f"./{folder_name}/")
    
    count = 0
    
    for issue in issues:
        
        uzn_files = [f for f in os.listdir(f'./{folder_name}/{issue}/') if f.endswith('.uzn')]
        uzn_files.sort()
        
        jpeg_files = [f for f in os.listdir(f'./{folder_name}/{issue}/') if f.endswith('.jpeg')]
        jpeg_files.sort()
        
        count += 1
        print(f"Issue being treated : {issue} <=====> {count}/{len(issues)}")
        
        for reco in range(len(jpeg_files)): 
            print(f'{jpeg_files[reco]} → {uzn_files[reco]}') # test de correspondance
            os.system(f'tesseract ./{folder_name}/{issue}/{jpeg_files[reco]} ./{folder_name}/{issue}/{uzn_files[reco]} --psm 4 -l fra+cos+ita')
            
def manuscript_concatenate(folder_name):
    """
    Function that collects the results of text recognition obtained in a single TXT file.
    
    Parameter :
    
    folder_name = str, name of the folder where the issues are located.
    """
    
    issues = os.listdir(f"./{folder_name}/")
    
    os.mkdir(f"./{folder_name}/MANUSCRIPTS")
    
    for issue in issues:
        txt_files = [f for f in os.listdir(f'./{folder_name}/{issue}/') if f.endswith('.txt')]
        txt_files.sort()
        
        with open(f"./{folder_name}/{issue}/{issue}.txt", 'w') as outfile:
            for txt in txt_files:
                with open(f"./{folder_name}/{issue}/{txt}") as infile:
                    outfile.write(infile.read())
        
        os.rename(f"./{folder_name}/{issue}/{issue}.txt", f"./{folder_name}/MANUSCRIPTS/{issue}.txt")