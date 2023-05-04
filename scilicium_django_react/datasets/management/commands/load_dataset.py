import os, csv, sys, shutil
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File
from django.contrib.auth import get_user_model
from django.core.exceptions import *
from django.apps import apps

from scilicium_django_react.studies.models import Study, Contributor
from scilicium_django_react.datasets.models import *
from scilicium_django_react.users.models import User
from scilicium_django_react.ontologies.models import *


def get_ontoTerm(model,label):
    #les attributs sont différents des noms d'onto...
    dict_datasetAttr_model = {"tissue":"Tissue", "organ":"Organ", "species":"Species", "developmentStage": "DevStage", "omics":"Omics", "resolution":"Granularity", "technology":"Sequencing","experimentalDesign":"ExperimentalProcess", "molecule_applied":"Chemical", "biomaterialType":"BiomaterialType", "pathology":"Pathology"}
    #print(dict_datasetAttr_model[model])
    myModelStr = dict_datasetAttr_model[model]

    try : 
        className = apps.get_model("ontologies",myModelStr)
    except LookupError : 
        print("no model " + modelStr)

    else : 
        if className.objects.filter(displayLabel = label).exists() :
            print("onto term exists for " + label )
            onto_object = className.objects.filter(displayLabel = label).first()
        elif className.objects.filter(displayLabel = label.lower()).exists() : 
            print("onto terme lowercase exists for" + label)
            onto_object = className.objects.filter(displayLabel = label.lower()).first()
        else : 
            onto_object = create_ontoTerm(className,label)

        return onto_object


def create_ontoTerm(className,displayLabel):
    print("create onto term")
    dict_onto={}
    dict_onto["displayLabel"]=displayLabel
    dict_onto["ontologyLabel"]=displayLabel
    sp = className.objects.create(**dict_onto)
    sp.save()
    print(sp)
    return sp

def check_ontoLabels(dict_meta) : 
    keys_to_suppress = []
    dict_onto = {}

    for key,value in dict_meta.items() : 
        if "displayLabel" in key : 
            #le nom du model d'onto est stocke avant displayLabel
            model = key.split(".displayLabel")[0]
            #il peut y avoir plusieurs valeurs à ajouter, on fait un split sur la virgule
            if "," in value : 
                print("splitting " + value)
                value_list = value.split(",")
                onto_list = []
                for item in value_list : 
                    ontoTerm = get_ontoTerm(model,item)
                    onto_list.append(ontoTerm)
                dict_onto[model] = onto_list
            else :
                if value != "" : 
                    #print("single value")
                    ontoTerm = get_ontoTerm(model,value)
                    dict_onto[model] = [ontoTerm]
                    #print(ontoTerm)
    
            keys_to_suppress.append(key)

    return keys_to_suppress,dict_onto
            

def import_sop(dict_sop,user):
    
    keys_to_suppress, dict_onto = check_ontoLabels(dict_sop)

    #on supprime les anciennes clés par celle correspondant réellement àl'attribut
    for item in keys_to_suppress : 
        del dict_sop[item]

    sop=sopMeta.objects.create(**dict_sop)
    sop.save()

    for model,value in dict_onto.items() : 
        if model == "omics" : 
            sop.omics.add(*value)
        elif model == "resolution" : 
            sop.resolution.add(*value)
        elif model == "technology" : 
            sop.technology.add(*value)
        elif model == "experimentalDesign" : 
            sop.experimentalDesign.add(*value)
        elif model == "molecule_applied" : 
            sop.molecule_applied.add(*value)

    return sop.id

def import_bioMeta(dict_bioMeta,user):
    
    keys_to_suppress, dict_onto = check_ontoLabels(dict_bioMeta)
    #on supprime les anciennes clés par celle correspondant réellement àl'attribut
    for item in keys_to_suppress : 
        del dict_bioMeta[item]

    #l'attribut sex doit correspondre à un array
    if "sex" in dict_bioMeta.keys() : 
        value = dict_bioMeta["sex"]
        dict_bioMeta["sex"]=[value]

    #if "biomaterialType" in dict_bioMeta.keys() : 
        #value =  dict_bioMeta["biomaterialType"]
        #dans le model actuel, il ne peut y avoir qu'une seule valeur...
        #if "," in value : 
            #singleValue = value.split(",")[0]
            #dict_bioMeta["biomaterialType"] = singleValue.upper()
        #else :
            #dict_bioMeta["biomaterialType"] = value.upper()

    int_key_empty = []    
    for key, value in dict_bioMeta.items() :
        if key in ("age_start", "age_end") and value in (""," ") : 
            print(key)
            int_key_empty.append(key)
    for item in int_key_empty : 
        del dict_bioMeta[item]

    bio=biomaterialMeta.objects.create(**dict_bioMeta)
    bio.save()

    for model,value in dict_onto.items() : 
        if model == "species" : 
            bio.species.add(*value)
        elif model == "developmentStage" : 
            bio.developmentStage.add(*value)
        elif model == "tissue" : 
            bio.tissue.add(*value)
        elif model == "organ" : 
            bio.organ.add(*value)
        elif model == "pathology" : 
            bio.pathology.add(*value)
        elif model == "biomaterialType": 
            bio.biomaterialType.add(*value)
    
    return bio.id
    


def import_loom(dict_loom,user):
    """
        Import loom
        dict_loom : dictionary
        user : django user object
    """
    
    if not Loom.objects.filter(name = dict_loom['name']).exists():
        
        row = "genes"
        col = "cells"
        if "row_name" in dict_loom.keys() : 
            row = dict_loom["row_name"]
        if "col_name" in dict_loom.keys() : 
            col = dict_loom["col_name"]

        
        #on stocke les infos sur le fichier mais on sauve d'abord l'object sans cette info
        filename=dict_loom["file"]
        basename = os.path.basename(filename)
        lightfilename=dict_loom["light_file"]
        del dict_loom["file"]
        del dict_loom["light_file"]
        #adding temporary but compulsory value
        #loom = Loom(name = dict_loom["name"], rowEntity = ["Symbol"], colEntity = ["Age"], reductions = ["Umap"], classes = ["Age"], row_name = row, col_name = col, created_by = user)            
        loom = Loom(name = basename, rowEntity = ["Symbol"], colEntity = ["Age"], reductions = ["Umap"], classes = ["Age"], row_name = row, col_name = col, created_by = user)

        #loom = Loom.objects.create(**dict_loom)
        loom.save()
        #loom.created_by.add(user)
        print("Loom object created for " + filename)
        
        #une fois l'instance loom créé, on enregistre le fichier
        #loom_dir = "data_to_import/loom"
        if filename != "" :
            if not os.path.isfile(filename):
                loom.delete() # delete loom object from db
                raise Exception(f"Loom file doesn't exist: {filename}")

            filepath = filename # absolute path, path is name
            basename = os.path.basename(filename) # get file basename to store properly
            f = File(open(filepath,'rb'))
            loom.file.save(basename,f,save=False) # use basename and file connection f

            if lightfilename != "":
                if not os.path.isfile(lightfilename):
                    loom.delete()
                    raise Exception(f"Loom file doesn't exist: {lightfilename}")

                lightfilepath = lightfilename # absolute path, path is name
                lightbasename = os.path.basename(lightfilename) # get light file basename to store properly
                lf = File(open(lightfilepath,'rb'))
                loom.light_file.save(lightbasename,lf,save=False) # use basename and file connection lf

            loom.save()
            
            #destination = os.path.join(settings.MEDIA_ROOT,get_upload_path(loom,filename))
            #print(destination)
            #try :
                #shutil.copy(filepath,destination)
            #except OSError : 
                #print("could not copy file")
            #print("Loom created with file " + filename)

        return loom.id


    else :
        print("Loom already exists")
        try : 
            loom = Loom.objects.get(name = dict_loom['name'])
            return loom.id
        except MultipleObjectsReturned :  
            print("Can't associate loom name " + dict_loom['name'] + " to a single file")


def import_dataset(dict_dataset,admin_user,loomId,bioMetaId,sopId) :

        
    #ds=Dataset.objects.create(**dict_dataset)
    #ds.save()
    if loomId != "" :  
        loomObj = Loom.objects.get(id=loomId)
    else :
        loomObj = None
    bioMetaObj = biomaterialMeta.objects.get(id=bioMetaId)
    sopObj = sopMeta.objects.get(id=sopId)

    if "description" in dict_dataset and dict_dataset["description"] != "" :
        desc = dict_dataset["description"]
    else :
        desc = ""

    
    ds = Dataset(title = dict_dataset["title"], datasetId = "temp", description = desc, loom = loomObj, bioMeta = bioMetaObj, sop = sopObj, status = dict_dataset["status"].upper(), created_by = admin_user) 
    ds.save()


def import_data_from_list(infofile):


    admin_user = User.objects.filter(is_superuser=True)
    if not admin_user:
        self.stdout.write("No superuser, aborting")
    else :
        admin_user = admin_user[0]
    print("USER")
    print(admin_user)
    
    with open(infofile, "r", encoding="utf-8", errors="ignore") as csvfile :
        #les entêtes du fichier csv doit correspondre aux attributs de dataset, bioMeta, sop, loom
        # exemple pour un attr de Dataset : Dataset.title
        # exemple pour un attr de bioMeta : Dataset.bioMeta.tissue
        # exemple pour un attr Loom : Loom.file
    
        csv_reader = csv.reader(csvfile, delimiter=";")
        headers = next(csv_reader)

        for row in csv_reader: 
            row_data = {key: value for key, value in zip(headers,row)}
            #print("row in csv")
            print(row_data)
           
            if row_data["Loom.file"] == "" :
                print("skipping, no loom file to import")

            elif not Dataset.objects.filter(title=row_data["Dataset.title"]).exists() : 
                print("Creating dataset")
                loomName = row_data["Loom.file"].split(".loom")[0]
                bioMetaName = loomName + "_bioMeta"
                sopName = loomName + "_sopMeta"
                dict_loom={}
                dict_bioMeta = {}
                dict_sop = {}
                dict_dataset = {}
                for key, value in row_data.items():
                    if "Loom." in key : 
                        key2 = key.split("Loom.")[1]
                        print(key2)
                        dict_loom[key2] = value
                    elif "Dataset.bioMeta" in key : 
                        key2 = key.split("Dataset.bioMeta.")[1]
                        dict_bioMeta[key2] = value
                    elif "Dataset.sop" in key : 
                        key2 = key.split("Dataset.sop.")[1]
                        dict_sop[key2] = value
                    else :
                        if "Dataset." in key:
                            key2 = key.split("Dataset.")[1]
                            dict_dataset[key2] = value
                dict_loom["name"] = loomName
                #print(dict_loom)
                dict_bioMeta["name"] = bioMetaName
                #print(dict_bioMeta)
                dict_sop["name"] = sopName
                #print(dict_sop)
                #print(dict_dataset)
            


                loomId = import_loom(dict_loom, admin_user)
                bioMetaId = import_bioMeta(dict_bioMeta, admin_user)
                sopId = import_sop(dict_sop, admin_user)
                import_dataset(dict_dataset, admin_user, loomId, bioMetaId, sopId)
            else :
                print("Dataset already exists: " + row_data["Dataset.title"])


def launch_import(infofile):
    import_data_from_list(infofile)


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads csv to import dataset metadata (biometa,sopmeta) and associated loom file"


    def add_arguments(self, parser):
        #Positional arguments
        parser.add_argument('infofile', type=str, help="Filepath to the file containing the dataset info")

    def handle(self, *args, **options):
        launch_import(options['infofile'])
