from django.test import TestCase
from django.contrib.auth.models import User
from customer.models import Customer, Panier, ProduitPanier, CodePromotionnel, PasswordResetToken
from shop.models import Produit, CategorieEtablissement, CategorieProduit, Etablissement
from django.utils import timezone
from datetime import timedelta

class CustomerModelsTest(TestCase):
    """Tests Unitaires - Module Customer (Logique Panier & Clients)"""

    def setUp(self):
        # 1. Création d'un User et Customer
        self.user = User.objects.create_user(username='client1', password='password123')
        self.customer = Customer.objects.create(
            user=self.user,
            adresse="Cocody",
            contact_1="0102030405"
        )

       
        self.cat_etab = CategorieEtablissement.objects.create(nom="Tech")
        
        
        self.etablissement = Etablissement.objects.create(
            user=User.objects.create_user(username='vendeur', password='pw'),
            nom="Vendeur Pro", 
            categorie=self.cat_etab, 
            email="vendeur@test.com", 
            adresse="Adjame", 
            contact_1="0000",
            nom_du_responsable="Directeur",   
            prenoms_duresponsable="Commercial" 
        )
        
        self.cat_prod = CategorieProduit.objects.create(nom="Phones", categorie=self.cat_etab)
        
        self.produit = Produit.objects.create(
            nom="iPhone", description="Tel", prix=1000, 
            etablissement=self.etablissement, categorie=self.cat_prod
        )

    def test_customer_str(self):
        """TC-CUST-01: Vérifier représentation string du Client"""
        self.assertEqual(str(self.customer), "client1")

    def test_panier_calcul_total(self):
        """TC-CUST-02: Vérifier le calcul du total du panier"""
        panier = Panier.objects.create(customer=self.customer)
        ProduitPanier.objects.create(produit=self.produit, panier=panier, quantite=2)
        self.assertEqual(panier.total, 2000)

    def test_panier_avec_coupon(self):
        """TC-CUST-03: Vérifier l'application d'un code promo"""
        panier = Panier.objects.create(customer=self.customer)
        ProduitPanier.objects.create(produit=self.produit, panier=panier, quantite=1)
        
        coupon = CodePromotionnel.objects.create(
            libelle="Promo Noel", etat=True, reduction=0.10, 
            code_promo="NOEL10", date_fin=timezone.now().date()
        )
        
        panier.coupon = coupon
        panier.save()
        self.assertEqual(panier.total_with_coupon, 900)

    def test_password_token_validity(self):
        """TC-CUST-04: Vérifier expiration du token (Sécurité)"""
        token = PasswordResetToken.objects.create(user=self.user, token="abc-123")
        self.assertTrue(token.is_valid())
        
        token.created_at = timezone.now() - timedelta(hours=2)
        token.save()
        self.assertFalse(token.is_valid())