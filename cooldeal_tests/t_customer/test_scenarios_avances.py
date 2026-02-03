from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from customer.models import Customer, Panier, ProduitPanier
from shop.models import Produit, CategorieEtablissement, CategorieProduit, Etablissement
import json
from django.urls import reverse

@override_settings(ALLOWED_HOSTS=['testserver', '127.0.0.1', 'localhost', '*'])
class AdvancedSecurityTests(TestCase):
    """Module 8: Tests de Cas Limites et Sécurité Avancée"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='hacker', password='password123')

    def test_signup_invalid_email_formats(self):
        """TC-ADV-01: Bombardement avec formats d'emails invalides"""
        bad_emails = [
            'pas-arobase.com', 
            'double@@gmail.com', 
            '@domaine-seul.com', 
            'espace dans@mail.com', 
            'sans-point@com'
        ]
        
        for email in bad_emails:
            data = {
                'username': f'user_{email.replace(" ","")}', # On nettoie le username
                'email': email, 
                'password': 'pw', 'passwordconf': 'pw',
                'nom': 'Test', 'prenoms': 'Test', 'phone': '00', 'adresse': 'Rue'
            }
            with open(__file__, 'rb') as fp:
                data['file'] = fp
                response = self.client.post(reverse('inscription'), data)
            
            # Le serveur doit répondre success=False pour CHAQUE email pourri
            self.assertFalse(response.json()['success'], f"L'email '{email}' aurait dû être rejeté !")

    def test_signup_empty_fields(self):
        """TC-ADV-02: Tentative d'inscription avec champs vides"""
        required_fields = ['username', 'email', 'password', 'nom', 'phone']
        
        for field in required_fields:
            data = {
                'username': 'valid', 'email': 'valid@test.com', 'password': 'pw', 
                'passwordconf': 'pw', 'nom': 'Nom', 'prenoms': 'Pre', 
                'phone': '01', 'adresse': 'Rue'
            }
            # On vide un champ à la fois
            data[field] = '' 
            
            with open(__file__, 'rb') as fp:
                data['file'] = fp
                response = self.client.post(reverse('inscription'), data)
            
            self.assertFalse(response.json()['success'], f"Le champ vide '{field}' n'a pas bloqué l'inscription !")

    def test_cart_negative_quantity(self):
        """TC-ADV-03: Protection contre les quantités négatives ou nulles"""
        # Configuration produit
        cat = CategorieEtablissement.objects.create(nom="C")
        etab = Etablissement.objects.create(
            user=self.user, nom="E", categorie=cat, 
            nom_du_responsable="X", prenoms_duresponsable="Y", contact_1="00"
        )
        cat_prod = CategorieProduit.objects.create(nom="S", categorie=cat)
        produit = Produit.objects.create(nom="P", prix=100, etablissement=etab, categorie=cat_prod)
        
        # On crée un panier vide spécifique pour ce test
        panier = Panier.objects.create()
        
        # Test quantité 0
        data_zero = {'panier': panier.id, 'produit': produit.id, 'quantite': 0}
        self.client.post(reverse('add_to_cart'), json.dumps(data_zero), content_type='application/json')
        
        # Test quantité négative
        data_neg = {'panier': panier.id, 'produit': produit.id, 'quantite': -5}
        self.client.post(reverse('add_to_cart'), json.dumps(data_neg), content_type='application/json')
        
        # Vérification : 
       
        count_items = ProduitPanier.objects.filter(panier=panier).count()
        self.assertEqual(count_items, 0, "Le panier ne devrait contenir aucun article !")

    def test_login_brute_force_simulation(self):
        """TC-ADV-04: Simulation d'attaques sur le login (Injections)"""
        bad_inputs = [
            "' OR '1'='1", 
            "<script>alert(1)</script>", 
            "admin --", 
            "DROP TABLE users;"
        ]
        
        for bad_input in bad_inputs:
            data = {'username': bad_input, 'password': 'password123'}
            response = self.client.post(reverse('post'), json.dumps(data), content_type='application/json')
            self.assertFalse(response.json()['success'], f"L'injection '{bad_input}' est passée !")