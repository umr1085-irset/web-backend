import os, csv, sys
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.apps import apps

from scilicium_django_react.users.models import User
from scilicium_django_react.ontologies.models import *


def updateOntoID(instance,oID,oLabel):
    """
        instance : instance of the ontology model
        oID : string (ontologyID)
        oLabel : string (ontologyLabel)
    """
    
    instance.ontologyID = oID
    instance.ontologyLabel = oLabel
    instance.save()
    print("Missing ontologyID added for " + oLabel)
    

def checkAndUpdateOntoID(instance,oID,oLabel):
    """
        instance : instance of the ontology model
        oID : string (ontologyID)
        oLabel : string (ontologyLabel)
    """
    ontoID = instance.ontologyID
    if ontoID == "" or ontoID == " " :
        instance.ontologyID = oID
        instance.ontologyLabel = oLabel
        instance.save()
        print("Missing ontologyID added for " + oLabel)
    else :
        print(oLabel + "is already present with ID " + oID)

def import_onto(dict_onto,user):
    """
        Import an ontological concep
        dict_loom : dictionary
        user : django user object
    """

    if dict_onto["model"] != "skip" :
        #on récupère le model de classe à partir de son libellé
        modelStr = dict_onto["model"]
        try : 
            className = apps.get_model("ontologies",dict_onto["model"])
            #on supprime la clé/valeur correspondante car ce n'est pas un attribut du model
            del dict_onto["model"]
            
            #si le displayLabel n'existe pas (tel quel ou en version lower uppercase), on créé le terme
            if not className.objects.filter(displayLabel__iexact = dict_onto['displayLabel']).exists()  : 
                if dict_onto["ontologyLabel"] == "" : 
                    dict_onto["ontologyLabel"] = dict_onto["displayLabel"]
                sp = className.objects.create(**dict_onto)
                sp.save()
                print("Onto object created for " + dict_onto['displayLabel'])


            #si le display label lower case existe ,  s'il y a un ONTO ID de transmis et s'il n'y en as pas sur l'existant, on l'ajoute
            elif className.objects.filter(displayLabel = dict_onto["displayLabel"].lower()).exists() and dict_onto["ontologyID"] != "" and dict_onto["displayLabel"] != "" :
                #update s'il n'y avait pas d'info sur l'ontoID auparavant
                sp = className.objects.get(displayLabel=dict_onto["displayLabel"].lower())
                checkAndUpdateOntoID(sp,dict_onto["ontologyID"],dict_onto["ontologyLabel"])

            #si le display label existe s'il y aun ONTO ID de transmis et qu'il n'y en as pas sur l'existant, on verifie s'il faut l'ajouter    
            elif className.objects.filter(displayLabel = dict_onto["displayLabel"]).exists() and dict_onto["ontologyID"] != "" and dict_onto["displayLabel"] != "":    
                sp = className.objects.get(displayLabel=dict_onto["displayLabel"]) 
                checkAndUpdateOntoID(sp,dict_onto["ontologyID"],dict_onto["ontologyLabel"])
            else : 
                print(dict_onto['displayLabel'] + " is already in  " + modelStr)
  
    
        except LookupError : 
            print("there is no model corresponding to" + modelStr)

    else :
        print("SKIP")



def import_data_from_list(infofile):

    admin_user = User.objects.filter(is_superuser=True)
    if not admin_user:
        self.stdout.write("No superuser, aborting")
    else :
        admin_user = admin_user[0]

    print(os.getcwd())
    with open(infofile, "r", encoding="utf-8-sig") as csvfile:
        #les entêtes du fichier csv correspondent aux attributs des models onto
        #par contre, les noms des modèles actuels ne correspondent pas à ceux qui devaient être implémentés
        #donc dictionnaire pour établir les correspondances
    
        csv_reader = csv.reader(csvfile, delimiter=";")
        headers = next(csv_reader)

        for row in csv_reader: 
            row_data = {key: value for key, value in zip(headers,row)}
            print("row in csv")
            print(row_data)

            dict_modelName = {"Species":"Species", "BiomaterialCollectedFrom":"Organ", "BiomaterialEntity":"Tissue", "DevelopmentStage": "DevStage", "Omics":"Omics", "Resolution":"Granularity", "Technology":"Sequencing","ExperimentalDesign":"ExperimentalProcess", "Modification":"Chemical"}
            dict_onto={}
            for key, value in row_data.items():
                if key=="model" :
                    if value in dict_modelName.keys():
                        value2 = dict_modelName[value]
                        dict_onto["model"] = value2
                    else :
                        dict_onto["model"] = "skip"
                else :
                    dict_onto[key] = value
            
            #print(dict_onto)
            import_onto(dict_onto, admin_user)



def launch_import(infofile):
    import_data_from_list(infofile)


class Command(BaseCommand):
    # Show this when the user types help
    help = "Load initial data about the ontology concepts (ontologyLabel, ontologyID, displayLabel, model)"


    def add_arguments(self, parser):
        #Positional arguments
        parser.add_argument('infofile', type=str, help="Filepath to the file containing the ontological concepts info")


    def handle(self, *args, **options):
        launch_import(options['infofile'])
        


