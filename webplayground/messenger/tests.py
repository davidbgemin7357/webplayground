from django.core.checks import messages
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Thread, Message

# Create your tests here.
class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', None, 'test1234')
        self.user2 = User.objects.create_user('user2', None, 'test1234')
        self.user3 = User.objects.create_user('user3', None, 'test1234')

        self.thread = Thread.objects.create()

    # añadir usuarios al hilo
    def test_add_users_to_thread(self):
        # agregando usuarios
        self.thread.users.add(self.user1, self.user2)
        # comprobación si dos valores son equivalentes   2 usuarios dentro del hilo
        self.assertEqual(len(self.thread.users.all()), 2)

    # test que recupere un hilo a partir de sus usuarios existentes:
    def test_filter_thread_by_users(self):
        self.thread.users.add(self.user1, self.user2)
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(self.thread, threads[0])

    # comprobar que no existe un hilo cuando los usuarios no forman parte de él:
    def test_filter_non_existent_thread(self):
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(len(threads), 0)

    
    # comprobar si los mensajes han sido añadidos al hilo
    def test_add_messages_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content='Muy buenas')
        message2 = Message.objects.create(user=self.user2, content='Hola')
        self.thread.messages.add(message1, message2)
        self.assertEqual(len(self.thread.messages.all()), 2)

        for message in self.thread.messages.all():
            print("({}): {}".format(message.user, message.content))


    # refactorización:
    # pruba para comprobar si un 3er usuario puede inyectar mensaje al hilo
    # este test fallará porque el hilo solo debe recibir mensajes de dos usuarios que forman parte de este hilo, no de usuarios ajenos al hilo. Por ello lo que se va a hacer es una modificación del modelo
    def test_add_message_from_user_not_in_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content='Muy buenas')
        message2 = Message.objects.create(user=self.user2, content='Hola')
        message3 = Message.objects.create(user=self.user3, content='soy un espía')
        self.thread.messages.add(message1, message2, message3)
        self.assertEqual(len(self.thread.messages.all()), 2)

    # find y find or create
    def test_find_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find(self.user1, self.user2)
        self.assertEqual(self.thread, thread)

    def test_find_or_create_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find_or_create(self.user1, self.user2)
        self.assertEqual(self.thread, thread)

        thread = Thread.objects.find_or_create(self.user1, self.user3)
        self.assertIsNotNone(self.thread, thread)