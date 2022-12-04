import requests
from bs4 import BeautifulSoup
import csv
import datetime

# un lien 404 valide pour vérifier la méthode('https://httpbin.org/status/404') 
# un lien 401 valide pour vérifier la méthode('https://httpbin.org/basic-auth/user/pass') 

class crawler:
    def initialisation(self, url):
        self.url = url
        self.links = []
        self.links_with_error_404 = []
        self.links_with_authentication_401 = []
        self.links_scanned = []

    def valideUrl(self,sub_url:str)->bool:
        """
        Permet de vérifier si l'url est conforme
        """
        if sub_url not in self.links and sub_url != "#" and sub_url.startswith(self.url):
            return True
        else :
            return False


    def getPage(self) -> requests.models.Response:
        """
            Obtenir une page web avec un code html
        """
        page = requests.get(self.url)
        return page


    def getLinks(self):
        """
            Analyse la page HTML et récupère les liens trouvés.
            Remplit la liste LINKS de l'objet de la classe.
        """
        # Scanne la page et teste si l'URL est valide
        bs = BeautifulSoup(self.getPage().content, "html.parser")
        web_links = bs.select('a')
        actual_web_links = [web_link['href'] for web_link in web_links]
        for elt in actual_web_links :
            if self.valideUrl(elt) :
                self.links.append(elt)
        return

    def exportInCsvFile(self, liste_a_exporter:list):
        """
        Crée un fichier CSV dans le répertoire courant avec l'heure UTC de création. Horodate en GMT.
        """
        print("fichier CSV crée.")
        with open("links.csv", 'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Liste horodatée GMT du %s" % datetime.datetime.utcnow()])
            for i in range(0, len(liste_a_exporter)):
                writer.writerow([liste_a_exporter[i]])

        return

    def filterLinks404(self):
        """
            Remplit la liste links_with_error_404 à partir de la liste LINKS avec tous les liens renvoyant le code 404.
        """
        for i in range(0,len(self.links)):
            try:
                response = requests.get(self.links[i])
                if response.status_code == 404:
                    self.links_with_error_404.append(self.links[i])
            except :
                print("Exception Error")
        print("Vous avez %d lien(s) 404." %len(self.links_with_error_404))

        return

    def filterAuthenticate401(self):
        """
        Remplit la liste links_with_authentication_401 à partir de la liste LINKS en ne mettant que les URL
        demandant une authentification.
        """
        for i in range(0, len(self.links)):
            try:
                authi = requests.get(self.links[i], auth=("",""))
                if authi.status_code == 401:
                    self.links_with_authentication_401.append(self.links[i])
            except:
                print("Exception Error : lien %s" %(self.links[i]))
        print("Vous avez %d lien(s) avec authentification." %len(self.links_with_authentication_401))
        return

    def retrieveAbsoluteAllLinks(self):
        self.retrieveLinks() 
        self.links_scanned.append(self.url)
        indice_initial = 0
        indice_final = len(self.links)-1
        print("L'indice initial est %d, le final est %d" %(indice_initial,indice_final))


        while len(self.links) != len(self.links_scanned):
            print("Nbr de liens total : %d. Nbr de liens scannés : %d." %(len(self.links), len(self.links_scanned)))
            for i in range(indice_initial,indice_final):
                try:
                    print("Scan du lien %d. Liens totaux = %d" %(i,len(self.links)))
                    page = requests.get(self.links[i])
                    bs = BeautifulSoup(page.content, "html.parser")
                    web_links = bs.select('a')
                    actual_web_links = [web_link['href'] for web_link in web_links]
                    for elt in actual_web_links:
                        if self.isValidUrl(elt):
                            self.links.append(elt)
                    self.links_scanned.append(self.links[i])
                    indice = i+1
                except:
                    print("Le lien %s ne peut être lu." %self.links[i])
                    self.links_scanned.append(self.links[i])
                    indice = i+1
            indice_initial = indice
            indice_final = len(self.links)-1
        print("Scan de %s terminé. %d liens trouvés au total. %d liens scannés." %(self.url, len(self.links), len(self.links_scanned)))
        return


