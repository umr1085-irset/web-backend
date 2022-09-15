import os, csv, sys, json, requests
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File
from django.contrib.auth import get_user_model
from django.core.exceptions import *
from django.apps import apps

from scilicium_django_react.studies.models import *
from scilicium_django_react.datasets.models import *
from scilicium_django_react.users.models import User



def checkPMCforAbstract(pmcid) : 
    abstract = ""
    #urlConvert = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v&.0/?ids="+pmid+"&format=json"
    #response_API = requests.get(urlConvert)
    #data = response_API.txt
    #parse_json = json.loads(data)
    #pmcid = parse_json["records"]["pmcid"]

    urlPMC = "https://www.ebi.ac.uk/biostudies/files/S-E"+pmcid+"/S-E"+pmcid+".json"
    response_PMC=requests.get(urlPMC)
    data_PMC = response_PMC.txt
    jsonp = json.loads(data_PMC)
    attributes = jsonp["section"]["attributes"]
    for item in attributes : 
        if item["name"] == "Abstract" : 
            abstract = item["value"]
    return abstract


def createPubmedArticleOLD(pmid) : 

    url = "https://www.ebi.ac.uk/eropepmc/webservices/rest/article/MED/"+pmid+"?resultType=core&format=json"
    response_API = requests.get(url)
    data = response_API.text
    parse_json = json.loads(data)
    info = parse_json["result"]
    authors = info["authorList"]
    journalinfo = info["journalInfo"]
    volume = journalinfo["volume"]
    date = datetime.datetime(journalinfo["yearOfPublication"],journalinfo["printPublicationDate"].split("-")[1],journalinfo["printPublicationDate"].split("-")[2],00,00,00)
    journal = journalinfo["journal"]["medlineAbbreviation"]
    doid = info["doi"]
      
    print(authors)
    

def createPubmedArticle(pmid) : 
    print("pubmed ID " + pmid) 
    if Article.objects.filter(pmid = pmid).exists() : 
        article = Article.objects.get(pmid = pmid)
    else :

        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id="+pmid+"&retmode=json"
        response_API = requests.get(url)
        data = response_API.text
        parse_json = json.loads(data)
        #print(parse_json)
        info = parse_json["result"][pmid]
        authors = info["authors"]
        title  = info["title"]
        volume = info["volume"]
        if volume == "" : 
            volInt = 0
        else : 
            volInt = int(volume)
        journal = info["fulljournalname"] 
        dateStr = info["sortpubdate"]
        dateArr = dateStr.split(" ")[0].split("/")
        #print(dateArr)
        date = datetime(int(dateArr[0]),int(dateArr[1]),int(dateArr[2]),0,0,0)
        date_ok = make_aware(date)
        doid = info["elocationid"]
        ids = info["articleids"]
        #print(ids)
        doid = ""
        pmc = ""
        for item in ids : 
            print(item)
            if item["idtype"] == "doi" :
                doid = item["value"]
            elif item["idtype"] == "pmc" : 
                pmc = item["value"]
    
        abstract = ""
        if pmc != "" :
            print("PMC ID " + pmc)
            abstract = checkPMCforAbstract(pmc)

        article = Article(title=title,pmid=pmid,doid=doid,pmc=pmc,abstract=abstract,journal=journal,volume=volInt,releaseDate=date_ok)
        article.save()
        
            

        authorlist=[]
        for author in authors :
            if Author.objects.filter(fullName = author["name"]).exists() : 
                print("Author " + author["name"] + "already exists")
                a = Author.objects.filter(fullName = author["name"]).first()
                authorlist.append(a)
            else : 
                a=Author(fullName=author["name"])
                a.save()
                authorlist.append(a)

        for authorObj in authorlist : 
            article.author.add(authorObj)

    return article


def listBySource(idList) :
    print("List by source")
    print(idList)
    pubmedList = []
    biorxivList = []
    for item in idList : 
        if "pubmed:" in item :
            print(item)
            idpub = item.split(":")[1]
            print(idpub)
            pubmedList.append(idpub)
            print("pubmed article to fetch")
        elif "pmid:" in item : 
            pubmedList.append(item.split(":")[1])
            print("pubmed article to fech")
        elif biorxiv in item : 
            biorxivList.append(item.split(":")[1])
    print(pubmedList)
    return pubmedList, biorxivList

def add_datasets(study, datasetInfo) : 
    datasets=[]
    if datasetInfo != "" :
        if "," in datasetInfo :
            datasets = datasetInfo.split(",")
        else : 
            datasets.append(datasetInfo)

    for dsName in datasets : 
        if Dataset.objects.filter(title = dsName).exists() :
            dsObj = Dataset.objects.filter(title = dsName).first()
            study.dataset_of.add(dsObj)
            print(dsName + " added to study")
        else : 
            print(dsName + " could not be found")

def  import_data_from_list(infofile):

    admin_user = User.objects.filter(is_superuser=True)
    if not admin_user:
        self.stdout.write("No superuser, aborting")
    else :
        admin_user = admin_user[0]

    print(os.getcwd())
    with open(infofile) as csvfile:
        #les entêtes du fichier csv doit correspondre aux attributs d'une study en base sur le modèle Study.title, etc
        csv_reader = csv.reader(csvfile, delimiter=";")
        headers = next(csv_reader)

        for row in csv_reader: 
            row_data = {key: value for key, value in zip(headers,row)}
            print("row in csv")
            print(row_data)
            #On regarde d'abord s'il y a des ifnos concernant l'article
            articleID = row_data["Study.article"]
            print("article ID " + articleID)
            pubmedList = []
            biorxivList = []
            if "," in articleID :
                print("list of ids")
                articleList = articleID.split(",")
                pubmedList, biorxivList = listBySource(articleList)
            elif articleID != "" : 
                print("single article ID")
                articleL = []
                articleL.append(articleID)
                pubmedList, biorxivList = listBySource(articleL)

            artObjList = [] 
            for pmid in pubmedList :
                print(pmid + "in pubmedList")
                artObjList.append(createPubmedArticle(pmid))
            
            description = ""
            #par defaut, on regarde s'il y a une desc associé à l'article
            if len(artObjList) > 0 : 
                description = getattr(artObjList[0], "abstract")
            #si la description est donnée dans le fichier, c'est cette description que l'on prend
            if row_data["Study.description"] != "" : 
                description = row_data["Study.description"]
             
            #creation de la study (pour le moment, on ne gère pas la collection)
            if not Study.objects.filter(title = row_data["Study.title"]).exists() :
                study = Study(title=row_data["Study.title"],studyId="temp",description=description,status=row_data["Study.status"].upper(), dataCurators=row_data["Study.dataCurators"], externalID=row_data["Study.externalID"], created_by = admin_user)
                study.save()

                for article in artObjList : 
                    study.article.add(article)
            
                viewer = row_data["Study.viewer"]
                viewerObj = Viewer.objects.get(name = viewer)
                study.viewer.add(viewerObj)
            
                if len(artObjList) > 0 : 
                    contributors = artObjList[0].author.all()
                    for contrib in contributors: 
                        if Contributor.objects.filter(name=getattr(contrib, "fullName")).exists() :
                            contribObj = Contributor.objects.filter(name=getattr(contrib, "fullName")).first()
                            study.contributor.add(contribObj)
                        else : 
                            contribObj=Contributor(name=getattr(contrib,"fullName"), email="unknown@gmail.com")
                            contribObj.save()
                            study.contributor.add(contribObj)
                

                #adding datasets 
                add_datasets(study, row_data["Study.relatedDataset"])

                print(row_data["Study.title"] + " imported")

                #TO DO : associate study to dataset
            else : 
                print(row_data["Study.title"] + " already in database. Checking datasets")
                study = Study.objects.get(title = row_data["Study.title"])
                add_datasets(study, row_data["Study.relatedDataset"])

            

def launch_import(infofile):
    import_data_from_list(infofile)


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from study.csv"


    def add_arguments(self, parser):
        #Positional arguments
        parser.add_argument('infofile', type=str, help="Filepath to the file containing the study info")


    def handle(self, *args, **options):
        launch_import(options['infofile'])
        #Code to load the data into database
        #for row in DictReader(open('./children.csv')):
            #child=children(name=row['Name'], sex=row['Sex'], age=row['Age'])  
            #child.save()


