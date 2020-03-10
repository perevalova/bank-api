from django.test import TestCase
from django.contrib.auth import  get_user_model


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='useremail@email.com',
            password='testpassword123'
        )
        self.assertEqual(user.email, 'useremail@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            email='superuseremail@email.com',
            password='testpassword123'
        )
        self.assertEqual(user.email, 'superuseremail@email.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
