from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import CategorieEtablissement, CategorieProduit, Etablissement, Produit
import datetime
import unittest

class ShopModelsTest(TestCase):

    def setUp(self):
        """Configuration initiale"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        self.cat_etab = CategorieEtablissement.objects.create(
            nom="High Tech",
            description="Vente de matériel informatique"
        )

       
        
        self.etablissement = Etablissement.objects.create(
            user=self.user,
            nom="Boutique Samuel",
            description="Meilleure boutique",
            categorie=self.cat_etab,
            email="samuel@test.com",
            adresse="Abidjan",
            pays="CI",
            contact_1="0102030405",
            nom_du_responsable="Kouame",      
            prenoms_duresponsable="Samuel"     
        )

        self.cat_produit = CategorieProduit.objects.create(
            nom="Ordinateurs",
            description="PC Portables",
            categorie=self.cat_etab
        )

    def test_categorie_slug_generation(self):
        """TC01: Vérifier slug automatique"""
        self.assertTrue(self.cat_etab.slug)
        self.assertIn("high-tech", self.cat_etab.slug)

    def test_etablissement_update_user_info(self):
        """TC02: Vérifier synchro User"""
       
        self.etablissement.nom_du_responsable = "Kouassi"
        self.etablissement.prenoms_duresponsable = "Jean"
        self.etablissement.save()
        
        # On recharge l'user pour vérifier la mise à jour
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Kouassi")
        self.assertEqual(self.user.first_name, "Jean")

    def test_produit_check_promotion_active(self):
        """TC03: Promo active"""
        today = datetime.date.today()
        produit = Produit.objects.create(
            nom="HP Victus",
            description="PC Gamer",
            prix=500000,
            etablissement=self.etablissement,
            categorie=self.cat_produit,
            date_debut_promo=today - datetime.timedelta(days=1),
            date_fin_promo=today + datetime.timedelta(days=5)
        )
        self.assertTrue(produit.check_promotion)

    def test_produit_check_promotion_expired(self):
        """TC04: Promo expirée"""
        today = datetime.date.today()
        produit = Produit.objects.create(
            nom="Vieux PC",
            description="PC Gamer",
            prix=500000,
            etablissement=self.etablissement,
            categorie=self.cat_produit,
            date_debut_promo=today - datetime.timedelta(days=10),
            date_fin_promo=today - datetime.timedelta(days=1)
        )
        self.assertFalse(produit.check_promotion)