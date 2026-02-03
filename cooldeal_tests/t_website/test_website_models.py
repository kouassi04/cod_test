from django.test import TestCase
from website.models import SiteInfo, Banniere, Appreciation, About, WhyChooseUs, Galerie, Horaire, Partenaire
import unittest

class WebsiteModelsTest(TestCase):
    """Tests Unitaires - Module Website"""

    def setUp(self):
        self.site_info = SiteInfo.objects.create(
            titre="CoolDeal CI",
            slogan="Le meilleur du e-commerce",
            description="Plateforme de vente en ligne",
            contact_1="+225 07070707",
            email="contact@cooldeal.ci",
            adresse="Abidjan",
            status=True
        )
        self.banniere = Banniere.objects.create(
            titre="Grande Promo", description=" -50% sur tout", status=True
        )
        self.about = About.objects.create(
            titre="Qui sommes nous", sous_titre="Notre histoire", description="...", status=True
        )
        self.why_us = WhyChooseUs.objects.create(
            titre="Service Rapide", description="Livraison 24h", icon="zmdi-favorite", status=True
        )

    def test_siteinfo_str(self):
        """TC201: Vérifier __str__"""
        self.assertEqual(str(self.site_info), "CoolDeal CI")

    def test_siteinfo_creation(self):
        """TC202: Vérifier création BDD"""
        saved_site = SiteInfo.objects.get(id=self.site_info.id)
        self.assertEqual(saved_site.email, "contact@cooldeal.ci")

    def test_banniere_defaults(self):
        """TC208: Vérifier valeurs par défaut"""
        banniere_inative = Banniere.objects.create(titre="Test Inactif", description="Desc")
        self.assertFalse(banniere_inative.status)

    def test_about_verbose_name(self):
        """TC216: Vérifier Meta"""
        verbose_name = About._meta.verbose_name
        self.assertEqual(verbose_name, "Session A propos")

    def test_why_choose_us_icon_choices(self):
        """TC218: Vérifier icône valide"""
        valid_icons = [choice[0] for choice in WhyChooseUs.ICON_CHOICES]
        self.assertIn(self.why_us.icon, valid_icons)

    def test_partenaire_creation(self):
        """TC224: Vérifier partenaire"""
        partenaire = Partenaire.objects.create(nom="Orange", description="Telecom")
        self.assertEqual(str(partenaire), "Orange")