from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from shop.models import Produit, CategorieEtablissement, CategorieProduit, Etablissement
from customer.models import Commande, ProduitPanier, Customer
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime

@override_settings(ALLOWED_HOSTS=['testserver', '127.0.0.1', 'localhost', '*'])
class ShopFiltersTests(TestCase):
    """Module 16: Tests des Filtres de Recherche (Commandes & Produits)"""

    def setUp(self):
        self.client = Client()
        self.img = SimpleUploadedFile("test.jpg", b"img", content_type="image/jpeg")
        
        # Vendeur
        self.vendeur = User.objects.create_user('vendeur', 'pass')
        self.cat_etab = CategorieEtablissement.objects.create(nom="Tech")
        self.etab = Etablissement.objects.create(
            user=self.vendeur, nom="Shop", categorie=self.cat_etab, 
            logo=self.img, couverture=self.img, email="v@t.com", 
            nom_du_responsable="R", prenoms_duresponsable="P", contact_1="01"
        )
        
        # Produit
        self.cat_prod = CategorieProduit.objects.create(nom="PC", categorie=self.cat_etab)
        self.produit = Produit.objects.create(
            nom="MacBook", prix=1000, etablissement=self.etab, 
            categorie=self.cat_prod, image=self.img
        )

        # Clients et Commandes
        self.client1 = User.objects.create_user('client1', 'pass', first_name="Jean")
        self.cust1 = Customer.objects.create(user=self.client1, contact_1="01")
        
        # Commande 1 : Payée
        self.cmd1 = Commande.objects.create(customer=self.cust1, prix_total=1000, status=True) # Payée
        ProduitPanier.objects.create(commande=self.cmd1, produit=self.produit, quantite=1)

        # Commande 2 : Non Payée (Attente)
        self.cmd2 = Commande.objects.create(customer=self.cust1, prix_total=1000, status=False) # Attente
        ProduitPanier.objects.create(commande=self.cmd2, produit=self.produit, quantite=1)

    def test_filter_commandes_status_payee(self):
        """TC-FILT-01: Filtrer commandes par statut 'payée'"""
        self.client.force_login(self.vendeur)
        response = self.client.get(reverse('commande-reçu') + "?status=payée")
        self.assertEqual(response.status_code, 200)
        # On vérifie dans le contexte
        if response.context:
            commandes = response.context['commandes']
            self.assertIn(self.cmd1, commandes)
            self.assertNotIn(self.cmd2, commandes)

    def test_filter_commandes_status_attente(self):
        """TC-FILT-02: Filtrer commandes par statut 'attente'"""
        self.client.force_login(self.vendeur)
        response = self.client.get(reverse('commande-reçu') + "?status=attente")
        self.assertEqual(response.status_code, 200)
        
        if response.context:
            commandes = response.context['commandes']
            self.assertIn(self.cmd2, commandes)
            self.assertNotIn(self.cmd1, commandes)

    def test_filter_commandes_client_name(self):
        """TC-FILT-03: Filtrer commandes par nom client"""
        self.client.force_login(self.vendeur)
        response = self.client.get(reverse('commande-reçu') + "?client=Jean")
        self.assertEqual(response.status_code, 200)
        
        if response.context:
            commandes = response.context['commandes']
            self.assertEqual(len(commandes), 2) # Jean a fait 2 commandes

    def test_filter_commandes_produit_name(self):
        """TC-FILT-04: Filtrer commandes par nom produit"""
        self.client.force_login(self.vendeur)
        response = self.client.get(reverse('commande-reçu') + "?produit=MacBook")
        self.assertEqual(response.status_code, 200)
        
        if response.context:
            commandes = response.context['commandes']
            self.assertGreaterEqual(len(commandes), 1)

    def test_filter_commandes_date(self):
        """TC-FILT-05: Filtrer commandes par date (Aujourd'hui)"""
        today = datetime.now().strftime('%Y-%m-%d')
        self.client.force_login(self.vendeur)
        response = self.client.get(reverse('commande-reçu') + f"?date_min={today}")
        self.assertEqual(response.status_code, 200)
        
        if response.context:
            commandes = response.context['commandes']
            self.assertGreaterEqual(len(commandes), 1)