from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from customer.models import Customer, Commande, ProduitPanier
from shop.models import Produit, CategorieEtablissement, CategorieProduit, Etablissement
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

@override_settings(ALLOWED_HOSTS=['testserver', '127.0.0.1', 'localhost', '*'])
class ShopClientSecurityTests(TestCase):
    """Module 9: Tests de Sécurité Avancée (Shop & Client)"""

    def setUp(self):
        self.client = Client()
        
        # --- Fausse image pour éviter les erreurs ---
        image_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
        self.logo = SimpleUploadedFile("logo.gif", image_data, content_type="image/gif")

        # --- CONFIGURATION UTILISATEURS ---
        # User A (Le gentil) - AVEC PHOTO
        self.user_a = User.objects.create_user(username='user_a', password='password123')
        self.customer_a = Customer.objects.create(user=self.user_a, contact_1="01", photo=self.logo)
        
        # User B (La victime)
        self.user_b = User.objects.create_user(username='user_b', password='password123')
        self.customer_b = Customer.objects.create(user=self.user_b, contact_1="02", photo=self.logo)

        # --- CONFIGURATION PRODUITS ---
        cat = CategorieEtablissement.objects.create(nom="Tech")
        etab = Etablissement.objects.create(
            user=User.objects.create_user('v','p'), nom="Shop", categorie=cat, 
            nom_du_responsable="R", prenoms_duresponsable="P", contact_1="00", 
            logo=self.logo, couverture=self.logo
        )
        cat_prod = CategorieProduit.objects.create(nom="Ph", categorie=cat)
        
        
        self.produit = Produit.objects.create(
            nom="iPhone 15", prix=1000, etablissement=etab, categorie=cat_prod, 
            image=self.logo, slug="iphone-15"
        )

        
        self.commande_b = Commande.objects.create(
            customer=self.customer_b, 
            prix_total=5000, 
            transaction_id="TRANS_USER_B"
        )
        ProduitPanier.objects.create(commande=self.commande_b, produit=self.produit)

    def test_shop_search_injection(self):
        """TC-ADV-05: Tentative d'injection SQL/XSS dans la recherche Shop"""
        # Simulation d'une attaque XSS
        malicious_search = "<script>alert('HACK')</script>"
        
     
        url = reverse('shop') + f"?search={malicious_search}"
        
        # On doit être connecté
        self.client.force_login(self.user_a)
        response = self.client.get(url)
        
        
        self.assertEqual(response.status_code, 200)

    def test_client_idor_order_access(self):
        """TC-ADV-06: Tentative d'accès à la commande d'un autre client (IDOR)"""
        self.client.force_login(self.user_a)
        
        
        url = reverse('commande-detail', args=[self.commande_b.id])
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)

    def test_shop_pagination_limit(self):
        """TC-ADV-07: Test des limites de pagination (Page inexistante)"""
        self.client.force_login(self.user_a)
        
        # On demande la page 999999 des commandes
        url = reverse('commande') + "?page=999999"
        response = self.client.get(url)
        
        #
        self.assertEqual(response.status_code, 200)