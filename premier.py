import csv
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox

class AnalyseurReferencement:
    def __init__(self):
        self.url = ""
        self.mots_cles = []
        self.chemin_fichier_parasite = "parasite.csv"
        self.resultats = []

    def recuperer_html_depuis_url(self, url):
        try:
            reponse = requests.get(url)
            reponse.raise_for_status()
            return reponse.text
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération de HTML depuis {url}: {e}")
            return None

    def supprimer_balises_html(self, texte_html):
        soup = BeautifulSoup(texte_html, 'html.parser')
        return soup.get_text(separator=' ', strip=True)

    def extraire_valeurs_attribut(self, texte_html, balise, attribut):
        soup = BeautifulSoup(texte_html, 'html.parser')
        elements = soup.find_all(balise)
        return [element.get(attribut) for element in elements if element.get(attribut)]

    def compter_occurrences(self, texte):
        mots = texte.lower().split()
        occurrences = {}
        for mot in mots:
            if mot in occurrences:
                occurrences[mot] += 1
            else:
                occurrences[mot] = 1
        occurrences_triees = sorted(occurrences.items(), key=lambda item: item[1], reverse=True)
        return occurrences_triees

    def filtrer_mots_parasites(self, donnees, mots_parasites):
        mots_filtres = {}
        for mot, occurrences in donnees:
            if mot not in mots_parasites:
                mots_filtres[mot] = occurrences
        return mots_filtres

    def charger_mots_parasites(self):
        try:
            with open(self.chemin_fichier_parasite, newline='', encoding='utf-8') as csvfile:
                lecteur = csv.reader(csvfile)
                return [mot for ligne in lecteur for mot in ligne]
        except FileNotFoundError:
            print(f"Fichier parasite non trouvé : {self.chemin_fichier_parasite}")
            return []

    def mettre_a_jour_mots_cles_parasites(self, nouvelle_liste_mots_cles):
        try:
            with open(self.chemin_fichier_parasite, mode='a', newline='', encoding='utf-8') as csvfile:
                ecrivain = csv.writer(csvfile)
                ecrivain.writerow(nouvelle_liste_mots_cles)
            print("Liste des mots parasites mise à jour avec succès.")
        except IOError:
            print("Une erreur s'est produite lors de la mise à jour de la liste des mots parasites.")

    def extraire_nom_domaine(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    def trier_urls_par_domaine(self, nom_domaine, urls):
        urls_du_domaine = []
        urls_pas_du_domaine = []
        for url in urls:
            parsed_url = urlparse(url)
            domaine_url = parsed_url.netloc
            if domaine_url == nom_domaine:
                urls_du_domaine.append(url)
            else:
                urls_pas_du_domaine.append(url)
        return urls_du_domaine, urls_pas_du_domaine

    def auditer_page(self, url):
        texte_html = self.recuperer_html_depuis_url(url)

        if texte_html:
            soup = BeautifulSoup(texte_html, 'html.parser')

            valeurs_alt = self.extraire_valeurs_attribut(texte_html, 'img', 'alt')
            pourcentage_alt = (len(valeurs_alt) / len(soup.find_all('img'))) * 100 if soup.find_all('img') else 0

            texte_sans_html = self.supprimer_balises_html(texte_html)

            mots_parasites = self.charger_mots_parasites()

            occurrences_mots_cles = self.compter_occurrences(texte_sans_html)
            mots_cles_filtres = self.filtrer_mots_parasites(occurrences_mots_cles, mots_parasites)

            liens = self.extraire_valeurs_attribut(texte_html, 'a', 'href')

            domain_urls, non_domain_urls = self.trier_urls_par_domaine(self.extraire_nom_domaine(url), liens)

            top_mots_cles = dict(mots_cles_filtres)
            mots_cles_utilisateur_present = any(mot in self.mots_cles for mot, _ in top_mots_cles.items())
            mots_cles_utilisateur_parmi_top3 = any(mot in self.mots_cles for mot in list(top_mots_cles)[:3])

            resultat = {
                'url': url,
                'liens_sortants': len(non_domain_urls),
                'liens_internes': len(domain_urls),
                'pourcentage_alt_tags': pourcentage_alt,
                'occurrences_mots_cles_top': top_mots_cles,
                'mots_cles_utilisateur_present': mots_cles_utilisateur_present,
                'mots_cles_utilisateur_parmi_top3': mots_cles_utilisateur_parmi_top3
            }

            self.resultats.append(resultat)

class InterfaceUtilisateur:
    def __init__(self, analyseur):
        self.analyseur = analyseur
        self.root = tk.Tk()
        self.root.title("Analyseur de Référencement")

        self.creer_interface_principale()

    def creer_interface_principale(self):
        tk.Label(self.root, text="URL de la première page :").pack()
        self.entry_url = tk.Entry(self.root, width=50)
        self.entry_url.pack()

        tk.Label(self.root, text="Mots-clés (séparés par des virgules) :").pack()
        self.entry_mots_cles = tk.Entry(self.root, width=50)
        self.entry_mots_cles.pack()

        tk.Label(self.root, text="Mots-clés parasites à ajouter (séparés par des virgules) :").pack()
        self.entry_nouveaux_mots_parasites = tk.Entry(self.root, width=50)
        self.entry_nouveaux_mots_parasites.pack()

        ttk.Button(self.root, text="Analyser", command=self.analyser).pack()
        ttk.Button(self.root, text="Mettre à jour les mots-clés parasites", command=self.mettre_a_jour_mots_parasites).pack()

    def creer_interface_resultats(self):
        fenetre_resultats = tk.Toplevel(self.root)
        fenetre_resultats.title("Résultats de l'Analyse")

        tk.Label(fenetre_resultats, text="Résultats de l'analyse").pack()

        listbox_resultats = tk.Listbox(fenetre_resultats, width=100, height=20)
        listbox_resultats.pack()

        for resultat in self.analyseur.resultats:
            listbox_resultats.insert(tk.END, f"URL: {resultat['url']}")
            listbox_resultats.insert(tk.END, f"Liens Sortants: {resultat['liens_sortants']}")
            listbox_resultats.insert(tk.END, f"Liens Internes: {resultat['liens_internes']}")
            listbox_resultats.insert(tk.END, f"Pourcentage Balises Alt: {resultat['pourcentage_alt_tags']:.2f}%")
            listbox_resultats.insert(tk.END, f"Occurences Mots-Clés Top 3: {resultat['occurrences_mots_cles_top']}")
            listbox_resultats.insert(tk.END, f"Mots-Clés Utilisateur Présents: {'Oui' if resultat['mots_cles_utilisateur_present'] else 'Non'}")
            listbox_resultats.insert(tk.END, f"Mots-Clés Utilisateur Parmi Top 3: {'Oui' if resultat['mots_cles_utilisateur_parmi_top3'] else 'Non'}")
            listbox_resultats.insert(tk.END, "\n" + "-"*50 + "\n")

        ttk.Button(fenetre_resultats, text="Sauvegarder le rapport", command=self.sauvegarder_rapport).pack()

    def analyser(self):
        self.analyseur.url = self.entry_url.get()
        self.analyseur.mots_cles = [mot.strip() for mot in self.entry_mots_cles.get().split(",")]
        self.analyseur.resultats = []

        self.analyseur.auditer_page(self.analyseur.url)
        self.creer_interface_resultats()

    def sauvegarder_rapport(self):
        try:
            with open("referencement_report.csv", "a", newline='', encoding='utf-8') as csvfile:
                fieldnames = ['URL', 'Liens Sortants', 'Liens Internes', 'Pourcentage Balises Alt',
                              'Occurences Mots-Clés Top 3', 'Mots-Clés Utilisateur Présents',
                              'Mots-Clés Utilisateur Parmi Top 3']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')

                # Écrire chaque ligne de résultats
                for resultat in self.analyseur.resultats:
                    writer.writerow({
                        'URL': resultat['url'],
                        'Liens Sortants': resultat['liens_sortants'],
                        'Liens Internes': resultat['liens_internes'],
                        'Pourcentage Balises Alt': f"{resultat['pourcentage_alt_tags']:.2f}%",
                        'Occurences Mots-Clés Top 3': str(resultat['occurrences_mots_cles_top']),
                        'Mots-Clés Utilisateur Présents': 'Oui' if resultat['mots_cles_utilisateur_present'] else 'Non',
                        'Mots-Clés Utilisateur Parmi Top 3': 'Oui' if resultat[
                            'mots_cles_utilisateur_parmi_top3'] else 'Non',
                    })

            messagebox.showinfo("Rapport Sauvegardé", "Le rapport a été ajouté avec succès au fichier CSV.")
        except IOError:
            messagebox.showerror("Erreur", "Une erreur s'est produite lors de la sauvegarde du rapport.")

    def mettre_a_jour_mots_parasites(self):
        nouveaux_mots_parasites = [mot.strip() for mot in self.entry_nouveaux_mots_parasites.get().split(",")]
        if nouveaux_mots_parasites:
            self.analyseur.mettre_a_jour_mots_cles_parasites(nouveaux_mots_parasites)
            messagebox.showinfo("Mots-Clés Parasites Mis à Jour", "La liste des mots parasites a été mise à jour avec succès.")
        else:
            messagebox.showwarning("Aucun Mot-Clé Parasite", "Veuillez entrer des mots-clés parasites à ajouter.")

    def demarrer(self):
        self.root.mainloop()

if __name__ == "__main__":
    analyseur_referencement = AnalyseurReferencement()
    interface_utilisateur = InterfaceUtilisateur(analyseur_referencement)
    interface_utilisateur.demarrer()
