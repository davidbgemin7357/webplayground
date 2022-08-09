from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User

# Create your tests here.
class ProfileTestCase(TestCase):
    # necesariamente se tiene que usar estos dos métodos; setUp y el otro test_loquesevaAprobar en este caso si el perfil existe
    def setUp(self):
        User.objects.create_user('test', 'test@test.com', 'test1234')

    def test_profile_exists(self):
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertEqual(exists, True)