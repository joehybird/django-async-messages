from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.utils.encoding import force_text

from async_messages import (AsyncMessageException, get_messages, message_user,
                            message_users, messages)


class MiddlewareTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('david', "django-async@test.com", 'password')
        self.userB = User.objects.create_user('johnathan', "django-async@test.com", 'password')

        self.client = Client()
        self.client.login(username='david', password='password')

        self.clientB = Client()
        self.clientB.login(username='johnathan', password='password')

    def test_message_appears_for_user(self):
        message_user(self.user, "Hello david")
        message_user(self.userB, "Hello john")

        response = self.client.get('/')
        self.assertEqual(
            ['Hello david'],
            [force_text(m) for m in response.context['messages']]
        )

        response = self.clientB.get('/')
        self.assertEqual(
            ['Hello john'],
            [force_text(m) for m in response.context['messages']]
        )

    def test_message_appears_all_users(self):
        message_users(User.objects.all(), "Hello")

        response = self.client.get('/')
        self.assertEqual(
            ['Hello'],
            [force_text(m) for m in response.context['messages']]
        )

        response = self.clientB.get('/')
        self.assertEqual(
            ['Hello'],
            [force_text(m) for m in response.context['messages']]
        )

    def test_message_queue(self):
        message_user(self.user, "First Message")
        message_user(self.user, "Second Message")

        response = self.client.get('/')
        self.assertEqual(
            ['First Message', 'Second Message'],
            [force_text(m) for m in response.context['messages']]
        )

    def test_message_queue_empty(self):
        response = self.client.get('/')
        self.assertEqual([], [force_text(m) for m in response.context['messages']])

class AnonynousUserTests(TestCase):
    def test_anonymous(self):
        client = Client()
        response = client.get('/')
        msgs = list(response.context['messages'])
        self.assertEqual(0, len((msgs)))

    def test_anonymous_message(self):
        client = Client()
        user = auth.get_user(client)

        with self.assertRaises(AsyncMessageException) as e:
            message_user(user, "Second Message")

        self.assertEqual(force_text(e.exception),
                         'Anonymous users cannot send messages.')

    def test_get_messages_anonymous(self):
        client = Client()
        user = auth.get_user(client)

        self.assertIsNone(user.id)
        self.assertIsNone(get_messages(user))

    @override_settings(MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
        'async_messages.middleware.AsyncMiddleware'
    ])
    def test_no_session(self):
        client = Client()
        response = client.get('/')
        self.assertEqual([], [force_text(m) for m in response.context['messages']])


class TestMessagesApi(TestCase):
    def setUp(self):
        username, password = 'david', 'password'
        self.user = User.objects.create_user(username, "django-async@test.com", password)
        self.client = Client()
        self.client.login(username=username, password=password)

    def assertMessageOk(self, level):
        response = self.client.get('/')
        msgs = list(response.context['messages'])
        self.assertEqual(1, len((msgs)))
        self.assertEqual('Hello', force_text((msgs)[0]))

    def test_info(self):
        messages.info(self.user, "Hello")
        self.assertMessageOk(constants.INFO)

    def test_success(self):
        messages.success(self.user, "Hello")
        self.assertMessageOk(constants.SUCCESS)

    def test_warning(self):
        messages.warning(self.user, "Hello")
        self.assertMessageOk(constants.WARNING)

    def test_error(self):
        messages.error(self.user, "Hello")
        self.assertMessageOk(constants.ERROR)

    def test_debug(self):
        messages.debug(self.user, "Hello")
        # 0 messages because by default django.contrib.messages ignore DEBUG
        # messages (this can be changed using set_level)
        response = self.client.get('/')
        msgs = list(response.context['messages'])
        self.assertEqual(0, len((msgs)))
