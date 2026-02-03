from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Produit, CategorieEtablissement, CategorieProduit, Etablissement
from django.core.files.uploadedfile import SimpleUploadedFile

@override_settings(ALLOWED_HOSTS=['testserver', '127.0.0.1', 'localhost', '*'])
class ShopViewsTest(TestCase):
    """Tests d'Intégration - Module Shop (Vues et URLs)"""

    def setUp(self):
        self.client = Client()
        
        # Fausse image pour éviter les erreurs 404/500
        image_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
        self.logo_test = SimpleUploadedFile("logo.gif", image_data, content_type="image/gif")

        self.user = User.objects.create_user(username='samuel_dev', password='password123')
        self.cat_etab = CategorieEtablissement.objects.create(nom="Mode", slug="mode")
        
        self.etablissement = Etablissement.objects.create(
            user=self.user, nom="Sam Shop", categorie=self.cat_etab, 
            email="sam@shop.com", adresse="Babi", contact_1="010101",
            nom_du_responsable="Admin", prenoms_duresponsable="Test",
            logo=self.logo_test, couverture=self.logo_test
        )
        
        self.cat_prod = CategorieProduit.objects.create(nom="Chaussures", categorie=self.cat_etab)
        
        self.produit = Produit.objects.create(
            nom="Nike Air", description="Super", prix=50000, 
            etablissement=self.etablissement, categorie=self.cat_prod,
            slug="nike-air", image=self.logo_test
        )

    def test_view_shop_home(self):
        """TC-VIEW-01: La page boutique s'affiche et contient le produit"""
        url = reverse('shop') 
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, "Nike Air") 

    def test_view_product_detail(self):
        """TC-VIEW-02: La page détail produit s'affiche et contient le prix"""
        url = reverse('product_detail', args=[self.produit.slug])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
       
        self.assertContains(response, "50000")

    def test_dashboard_security_redirect(self):
        """TC-VIEW-03: Dashboard inaccessible sans connexion"""
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) 

    def test_dashboard_access_logged_in(self):
        """TC-VIEW-04: Dashboard accessible une fois connecté"""
        self.client.login(username='samuel_dev', password='password123')
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sam Shop")