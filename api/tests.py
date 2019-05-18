from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient

import json


class UserTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.validUserDict = {
            "email": "test@yopmail.com",
            "password": "1234",
            "username": "test",
            "first_name": "Tester",
            "last_name": "Mc Toaster",
            "wallet": {"balance": 10}
        }
        self.invalidUserDict = {
            "password": "1234",
            "username": "test",
            "first_name": "Tester",
            "last_name": "Mc Toaster"
        }

    # CREATE TWO USERS, AUTHENTICATE ONE
    def create_users_and_authenticate(self):
        user1dict = self.validUserDict.copy()
        user2dict = self.validUserDict.copy()
        user2dict.update({'email': 'test2@yopmail.com', 'username': 'test2'})

        # CREATE TWO USERS
        self.client.post(reverse('api:user'), data=user1dict, format='json')
        self.client.post(reverse('api:user'), data=user2dict, format='json')

        credentials = {
            'email': self.validUserDict['email'],
            'password': self.validUserDict['password'],
        }
        token = self.client.post(reverse('token_obtain_pair'), data=credentials)
        self.client.credentials(HTTP_AUTHORIZATION='{} {}'.format('Bearer', token.data.get('access')))

    def test_user_creation(self):
        response = self.client.post(reverse('api:user'), data=self.validUserDict, format='json')
        self.assertEqual(response.status_code, 200, response.content)

        response = self.client.post(reverse('api:user'), data=self.invalidUserDict)
        self.assertEqual(response.status_code, 400)

    def test_unauthorized_and_authentication(self):
        # CREATE A USER
        response = self.client.post(reverse('api:user'), data=self.validUserDict, format='json')
        result = json.loads(response.content.decode('utf-8'))
        user_id = result.get('id')

        response = self.client.get('/api/users/' + str(user_id))
        self.assertEqual(response.status_code, 401)

        credentials = {
            'email': self.validUserDict['email'],
            'password': self.validUserDict['password'],
        }

        # AUTHENTICATE
        token = self.client.post(reverse('token_obtain_pair'), data=credentials)
        self.client.credentials(HTTP_AUTHORIZATION='{} {}'.format('Bearer', token.data.get('access')))

        # GET INFO AGAIN BUT AUTHENTICATED
        response = self.client.get('/api/users/' + str(user_id))
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get('wallet').get('balance'), 10)

    def test_forbidden_get_details(self):
        self.create_users_and_authenticate()

        # GET DETAILS FROM USER 2
        response = self.client.get('/api/users/2')
        self.assertEqual(response.status_code, 403)

    def test_get_details(self):
        self.create_users_and_authenticate()

        response = self.client.get('/api/users/1')
        self.assertEqual(response.status_code, 200)

    def test_forbidden_transfer(self):
        self.create_users_and_authenticate()

        # TRANSFER FROM USER 2 WALLET
        response = self.client.post('/api/users/2/transfer', data={'to_user': 1, 'amount': 10})
        self.assertEqual(response.status_code, 403)

        # TRANSFER TO SELF
        response = self.client.post('/api/users/1/transfer', data={'to_user': 1, 'amount': 10})
        self.assertEqual(response.status_code, 400)

    def test_transfer(self):
        self.create_users_and_authenticate()

        # TRANSFER FROM USER 1 WALLET
        response = self.client.post('/api/users/1/transfer', data={'to_user': 2, 'amount': 10})
        self.assertEqual(response.status_code, 200)

        # CHECK MY WALLET
        response = self.client.get('/api/users/1')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get('wallet').get('balance'), 0)
