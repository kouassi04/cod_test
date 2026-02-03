from django.test import TestCase
from shop.models import Produit
from datetime import date, timedelta

class ShopLogicTests(TestCase):
    """Module 11: Tests Unitaires Logique Métier (Promotions)"""

    def setUp(self):
        self.today = date.today()

    def test_promo_active_date_range(self):
        """TC-LOGIC-01: Promo active (Date début < Auj < Date fin)"""
        p = Produit(date_debut_promo=self.today - timedelta(days=1), date_fin_promo=self.today + timedelta(days=1))
        self.assertTrue(p.check_promotion)

    def test_promo_active_today_start(self):
        """TC-LOGIC-02: Promo commence aujourd'hui"""
        p = Produit(date_debut_promo=self.today, date_fin_promo=self.today + timedelta(days=1))
        self.assertTrue(p.check_promotion)

    def test_promo_active_today_end(self):
        """TC-LOGIC-03: Promo finit aujourd'hui"""
        p = Produit(date_debut_promo=self.today - timedelta(days=1), date_fin_promo=self.today)
        self.assertTrue(p.check_promotion)

    def test_promo_inactive_future(self):
        """TC-LOGIC-04: Promo pas encore commencée"""
        p = Produit(date_debut_promo=self.today + timedelta(days=5), date_fin_promo=self.today + timedelta(days=10))
        self.assertFalse(p.check_promotion)

    def test_promo_inactive_past(self):
        """TC-LOGIC-05: Promo terminée"""
        p = Produit(date_debut_promo=self.today - timedelta(days=10), date_fin_promo=self.today - timedelta(days=5))
        self.assertFalse(p.check_promotion)

    def test_promo_no_dates(self):
        """TC-LOGIC-06: Pas de dates définies"""
        p = Produit()
        self.assertFalse(p.check_promotion)

    def test_promo_only_start_date(self):
        """TC-LOGIC-07: Seulement date début (Indéfini = False dans ta logique)"""
        p = Produit(date_debut_promo=self.today - timedelta(days=1))
        self.assertFalse(p.check_promotion) # Car ton code vérifie 'if self.date_fin_promo'

    def test_slug_generation_on_save(self):
        """TC-LOGIC-08: Génération automatique du slug à la sauvegarde"""
        # Note: Test unitaire pur sans BDD complète si possible, mais save() requiert BDD
        # On mockera si besoin, ici on teste juste la logique string
        pass # Déjà couvert dans test_models.py, mais bon rappel