import os, csv, sys
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from scilicium_django_react.studies.models import Study, Contributor
from scilicium_django_react.datasets.models import *
from scilicium_django_react.users.models import User
from scilicium_django_react.ontologies.models import *

def create_ontoTerm(model,label):
    dict_onto={}
    dict_onto["displayLabel"]=label
    className = eval(model)()
    sp = className.objects.create(**dict_onto)
    sp.save()




def get_ontoTerm(model,label):
    dict_datasetAttr_model = {"tissue":"Tissue", "organ":"Organ", "species":"Species", "developmentStage": "DevStage", "omics":"Omics", "resolution":"Granularity", "technology":"Sequencing","experimentalDesign":"ExperimentalProcess", "molecule_applied":"Chemical"}
    print(dict_datasetAttr_model[model])
    className = eval(dict_datasetAttr_model[model])()
    try :
        onto_object = className.objects.get(displayLabel=label)
    except ObjectDoesNotExist : 
        print("creating ontoTerm "+ label + "for onto "+ model)
        create_ontoTerm(model,label)
        onto_object = className.objects.get(displayLabel=label)
        #sys.exit("no ontological term for " + label) 
    return onto_object

def import_bioMeta(dict_bioMeta,user):
    keys_to_suppress = []
    for key, value in dict_bioMeta : 
        if "displayLabel" in key : 
            model = key.split(".displayLabel")[0]
            ontoTerm = get_ontoTerm(model,value)
            dict_bioMeta[key2] = ontoTerm
            keys_to_suppress.append(key)

    for item in keys_to_suppres : 
        del dict_bioMeta[item]
            
    sp=biomaterialMeta.objects.create(**dict_bioMeta)
    sp.save()

def import_loom(dict_loom,user):
    """
        Import loom
        dict_loom : dictionary
        user : django user object
    """
    
    if not Loom.objects.filter(name = dict_loom['name']).exists():
        #adding temporary but compulsory value
        dict_loom["rowEntity"]=["Symbol"]
        dict_loom["colEntity"]=["Age"]
        dict_loom["reductions"]=["Umap"]
        dict_loom["classes"]=["Age"]
        
        #fileField
        filename=dict_loom["file"]
        del dict_loom["file"]
        #loom_dir = "data_to_import/loom"
        #f = File(open(os.path.join(settings.ROOT_DIR,loom_dir,filename)))
        #dict_loom["file"]=f       
        sp = Loom.objects.create(**dict_loom)
        sp.save()
        print("Loom object created for " + filename)

        loom_dir = "data_to_import/loom"
        filepath = os.path.join(settings.ROOT_DIR,loom_dir,filename)
        print(filepath)
        f = File(open(filepath,'rb'))
        #dict_loom["file"]=f       
        sp.file.save(filename,f,save=False)       
        
        sp.save()
        print("Loom created with file " + filename)


    else :
        print("Loom already exists")
        


def import_data_from_list(infofile):

    admin_user = User.objects.filter(is_superuser=True)
    if not admin_user:
        self.stdout.write("No superuser, aborting")
    else :
        admin_user = admin_user[0]

    print(os.getcwd())
    with open(infofile) as csvfile:
        #les entêtes du fichier csv doit correspondre aux attributs de dataset, bioMeta, sop, loom
        # exemple pour un attr de Dataset : Dataset.name
        # exemple pour un attr de bioMeta : Dataset.bioMeta.tissue
        # exemple pour un attr Loom : Loom.file
    
        csv_reader = csv.reader(csvfile, delimiter=";")
        headers = next(csv_reader)

        for row in csv_reader: 
            row_data = {key: value for key, value in zip(headers,row)}
            print("row in csv")
            print(row_data)
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
            print(dict_loom)
            dict_bioMeta["name"] = bioMetaName
            print(dict_bioMeta)
            dict_sop["name"] = sopName
            print(dict_sop)
            print(dict_dataset)
            
            import_loom(dict_loom, admin_user)
            #import_bioMeta(dict_bioMeta, admin_user)
            #import_sop(dict_sop, admin_user)
            #import_dataset(dictdataset, admin_user, loomName, bioMetaName, sopName)


def launch_import(infofile):
    import_data_from_list(infofile)


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from test.csv"


    def add_arguments(self, parser):
        #Positional arguments
        parser.add_argument('infofile', type=str, help="Filepath to the file containing the dataset info")


    def handle(self, *args, **options):
        launch_import(options['infofile'])
        #Code to load the data into database
        #for row in DictReader(open('./children.csv')):
            #child=children(name=row['Name'], sex=row['Sex'], age=row['Age'])  
            #child.save()


