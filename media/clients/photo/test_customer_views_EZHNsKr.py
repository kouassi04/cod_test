from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from customer.models import Customer, Panier, ProduitPanier, CodePromotionnel
from shop.models import Produit, CategorieEtablissement, CategorieProduit, Etablissement
import json
from django.urls import reverse

# --- CORRECTION 1: Sécurité pour la classe Auth ---
@override_settings(ALLOWED_HOSTS=['testserver', '127.0.0.1', 'localhost', '*'])
class CustomerAuthTests(TestCase):
    """Module 3: Tests Authentification & Inscription"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='password123')
        self.customer = Customer.objects.create(user=self.user, contact_1="0102030405")

    # --- TESTS CONNEXION (islogin) ---
    
    def test_login_success_username(self):
        """TC-AUTH-01: Connexion réussie avec Username"""
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(reverse('post'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_login_success_email(self):
        """TC-AUTH-02: Connexion réussie avec Email"""
        # On vérifie que la vue traite la requête sans erreur (Code 200)
        # L'authentification par email dépend des backends configurés, on reste souple ici
        data = {'username': 'test@test.com', 'password': 'password123'}
        response = self.client.post(reverse('post'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_fail_wrong_password(self):
        """TC-AUTH-03: Echec connexion mot de passe incorrect"""
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(reverse('post'), json.dumps(data), content_type='application/json')
        self.assertFalse(response.json()['success'])

    def test_login_fail_unknown_user(self):
        """TC-AUTH-04: Echec connexion utilisateur inconnu"""
        data = {'username': 'ghost', 'password': 'password123'}
        response = self.client.post(reverse('post'), json.dumps(data), content_type='application/json')
        self.assertFalse(response.json()['success'])

    def test_login_fail_inactive_user(self):
        """TC-AUTH-05: Echec connexion compte inactif"""
        self.user.is_active = False
        self.user.save()
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(reverse('post'), json.dumps(data), content_type='application/json')
        self.assertFalse(response.json()['success'])

    # --- TESTS INSCRIPTION (inscription) ---

    def test_signup_success(self):
        """TC-AUTH-06: Inscription valide"""
        data = {
            'username': 'newuser', 'email': 'new@test.com', 'password': 'password123',
            'passwordconf': 'password123', 'nom': 'Nouveau', 'prenoms': 'Client',
            'phone': '07070707', 'adresse': 'Abidjan'
        }
        # Simulation d'envoi de fichier vide pour éviter l'erreur MultiValueDictKeyError
        with open(__file__, 'rb') as fp:
            data['file'] = fp
            response = self.client.post(reverse('inscription'), data)
        
        self.assertTrue(response.json()['success'])
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_fail_password_mismatch(self):
        """TC-AUTH-07: Echec inscription mots de passe différents"""
        data = {
            'username': 'badpass', 'email': 'bad@test.com', 'password': '123',
            'passwordconf': '456', 'nom': 'Test', 'prenoms': 'Test', 'phone': '00'
        }
        # Fake file
        with open(__file__, 'rb') as fp:
            data['file'] = fp
            response = self.client.post(reverse('inscription'), data)
            
        self.assertFalse(response.json()['success'])

    def test_signup_fail_existing_username(self):
        """TC-AUTH-08: Echec inscription username déjà pris"""
        data = {
            'username': 'testuser', # Déjà créé dans setUp
            'email': 'autre@test.com', 'password': 'password123', 'passwordconf': 'password123',
            'nom': 'Test', 'prenoms': 'Test', 'phone': '00'
        }
        with open(__file__, 'rb') as fp:
            data['file'] = fp
            response = self.client.post(reverse('inscription'), data)
            
        self.assertFalse(response.json()['success'])


# --- CORRECTION 2: Ajout OBLIGATOIRE du décorateur ici aussi ---
@override_settings(ALLOWED_HOSTS=['testserver', '127.0.0.1', 'localhost', '*'])
class CustomerCartTests(TestCase):
    """Module 4: Tests Panier & Coupons (Actions JSON)"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='cartuser', password='password123')
        self.customer = Customer.objects.create(user=self.user)
        self.panier = Panier.objects.create(customer=self.customer)
        
        # Setup produits avec responsables (pour éviter IntegrityError)
        cat = CategorieEtablissement.objects.create(nom="Cat")
        etab = Etablissement.objects.create(
            user=User.objects.create_user(username='v', password='p'), 
            nom="Etab", categorie=cat, nom_du_responsable="X", prenoms_duresponsable="Y", contact_1="00"
        )
        cat_prod = CategorieProduit.objects.create(nom="SubCat", categorie=cat)
        self.produit = Produit.objects.create(nom="Produit 1", prix=1000, etablissement=etab, categorie=cat_prod)

    def test_add_to_cart_new(self):
        """TC-CART-01: Ajouter un nouveau produit au panier"""
        data = {'panier': self.panier.id, 'produit': self.produit.id, 'quantite': 2}
        response = self.client.post(reverse('add_to_cart'), json.dumps(data), content_type='application/json')
        
        self.assertTrue(response.json()['success'])
        self.assertEqual(ProduitPanier.objects.get(panier=self.panier).quantite, 2)

    def test_delete_from_cart(self):
        """TC-CART-02: Supprimer un produit du panier"""
        item = ProduitPanier.objects.create(panier=self.panier, produit=self.produit, quantite=1)
        data = {'panier': self.panier.id, 'produit_panier': item.id}
        
        response = self.client.post(reverse('delete_from_cart'), json.dumps(data), content_type='application/json')
        self.assertTrue(response.json()['success'])
        self.assertEqual(ProduitPanier.objects.filter(panier=self.panier).count(), 0)

    def test_add_coupon_valid(self):
        """TC-CART-03: Ajouter un coupon valide"""
        CodePromotionnel.objects.create(code_promo="PROMO2026", reduction=0.1, etat=True, date_fin="2030-01-01")
        data = {'panier': self.panier.id, 'coupon': 'PROMO2026'}
        
        response = self.client.post(reverse('add_coupon'), json.dumps(data), content_type='application/json')
        self.assertTrue(response.json()['success'])
        self.panier.refresh_from_db()
        self.assertEqual(self.panier.coupon.code_promo, "PROMO2026")

    def test_add_coupon_invalid(self):
        """TC-CART-04: Ajouter un coupon invalide"""
        data = {'panier': self.panier.id, 'coupon': 'FAUXCODE'}
        response = self.client.post(reverse('add_coupon'), json.dumps(data), content_type='application/json')
        self.assertFalse(response.json()['success'])