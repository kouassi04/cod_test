from django.test import TestCase, Client, override_settings
from django.urls import reverse
from contact.models import Contact, NewsLetter
import json

@override_settings(ALLOWED_HOSTS=['testserver', '127.0.0.1', 'localhost', '*'])
class ContactTests(TestCase):
    """Module 6: Tests Formulaires Contact & Newsletter"""

    def setUp(self):
        self.client = Client()

    def test_contact_post_success(self):
        """TC-CONT-01: Envoi message contact valide"""
        data = {
            'email': 'client@test.com', 'nom': 'Jean', 
            'sujet': 'Question', 'messages': 'Bonjour aidez-moi'
        }
        
        response = self.client.post(reverse('post_contact'), json.dumps(data), content_type='application/json')
        self.assertTrue(response.json()['success'])
        self.assertTrue(Contact.objects.filter(email='client@test.com').exists())

    def test_contact_post_invalid_email(self):
        """TC-CONT-02: Rejet email invalide"""
      
        data = {'email': 'pas-un-email', 'nom': 'Jean', 'sujet': 'Sujet', 'messages': 'Msg'}
        response = self.client.post(reverse('post_contact'), json.dumps(data), content_type='application/json')
        self.assertFalse(response.json()['success'])

    def test_contact_post_missing_fields(self):
        """TC-CONT-03: Rejet champs manquants"""
        data = {'email': 'test@test.com', 'nom': '', 'sujet': '', 'messages': ''} 
        response = self.client.post(reverse('post_contact'), json.dumps(data), content_type='application/json')
        self.assertFalse(response.json()['success'])

    def test_newsletter_success(self):
        """TC-CONT-04: Inscription Newsletter valide"""
        data = {'email': 'news@test.com'}
        response = self.client.post(reverse('post_newsletter'), json.dumps(data), content_type='application/json')
        
        
        self.assertTrue(response.json()['success'])
        
        