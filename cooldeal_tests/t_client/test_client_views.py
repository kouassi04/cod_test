from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from customer.models import Customer
from django.core.files.uploadedfile import SimpleUploadedFile

@override_settings(ALLOWED_HOSTS=['testserver', '127.0.0.1', 'localhost', '*'])
class ClientProfileTests(TestCase):
    """Module 7: Tests Espace Client (Profil & Sécurité)"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='cl', password='pw')
        
        # - Création d'une fausse photo 
        image_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
        self.photo = SimpleUploadedFile("avatar.gif", image_data, content_type="image/gif")

        self.customer = Customer.objects.create(
            user=self.user, 
            contact_1="0101",
            photo=self.photo 
        )

    def test_profil_access_logged_in(self):
        """TC-CLI-01: Accès profil connecté"""
        self.client.login(username='cl', password='pw')
        response = self.client.get(reverse('profil'))
        self.assertEqual(response.status_code, 200)

    def test_profil_access_anonymous(self):
        """TC-CLI-02: Accès profil anonyme (Redirection)"""
        response = self.client.get(reverse('profil'))
        self.assertEqual(response.status_code, 302)

    def test_commande_page_access(self):
        """TC-CLI-03: Accès page commandes"""
        self.client.login(username='cl', password='pw')
        response = self.client.get(reverse('commande'))
        self.assertEqual(response.status_code, 200)