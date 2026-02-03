from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from customer.models import Customer, Panier, ProduitPanier
from shop.models import Produit, CategorieEtablissement, CategorieProduit, Etablissement
import json
from django.urls import reverse

@override_settings(ALLOWED_HOSTS=['testserver', '127.0.0.1', 'localhost', '*'])
class CartUpdateTests(TestCase):
    """Module 14: Tests Mise à jour Panier (Quantités)"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('u', 'p')
        self.customer = Customer.objects.create(user=self.user)
        self.panier = Panier.objects.create(customer=self.customer)
        
        cat = CategorieEtablissement.objects.create(nom="C")
        etab = Etablissement.objects.create(user=User.objects.create_user('v','p'), nom="E", categorie=cat, nom_du_responsable="X", prenoms_duresponsable="Y", contact_1="00")
        cat_prod = CategorieProduit.objects.create(nom="S", categorie=cat)
        self.produit = Produit.objects.create(nom="P", prix=100, etablissement=etab, categorie=cat_prod)
        
        # Ajout initial
        self.pp = ProduitPanier.objects.create(panier=self.panier, produit=self.produit, quantite=1)

    def test_update_cart_increase(self):
        """TC-CART-UPD-01: Augmenter quantité"""
        data = {'panier': self.panier.id, 'produit': self.produit.id, 'quantite': 5}
        self.client.post(reverse('update_cart'), json.dumps(data), content_type='application/json')
        self.pp.refresh_from_db()
        self.assertEqual(self.pp.quantite, 5)

    def test_update_cart_zero(self):
        """TC-CART-UPD-02: Mettre quantité à 0 (Devrait supprimer ou rester 0)"""
        # Ta vue update_cart actuelle ne gère pas la suppression si 0, elle met juste 0.
        # C'est un comportement à tester.
        data = {'panier': self.panier.id, 'produit': self.produit.id, 'quantite': 0}
        self.client.post(reverse('update_cart'), json.dumps(data), content_type='application/json')
        self.pp.refresh_from_db()
        self.assertEqual(self.pp.quantite, 0)