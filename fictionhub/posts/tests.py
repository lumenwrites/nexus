from django.test import TestCase

from profiles.models import User
from .models import Post
from challenges.models import Prompt

class BasicTest(TestCase):
    def setUp(self):
        Prompt.objects.create(prompt="one")

    def test_post(self):
        """Animals that can speak are correctly identified"""
        prompt = Prompt.objects.get(slug="one")
        self.assertEqual(prompt.prompt, 'one')
        
