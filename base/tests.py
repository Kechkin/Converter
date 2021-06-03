import base64
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "convert.settings")
django.setup()
from django.test import TestCase, Client


class SimpleTest(TestCase):
    def test_get_index(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(bytes('tester:dark5550505', 'utf8')).decode('utf8'),
        }
        c = Client()
        c.login(username='tester', password='dark5550505')
        response = c.get('/', **auth_headers)
        return self.assertEqual(response.status_code, 200)

    def test_get_index2(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(bytes('nickolas:glasstaken123', 'utf8')).decode('utf8')
        }
        c = Client()
        c.login(username='nickolas', password='glasstaken123')
        response = c.get('/', **auth_headers)
        return self.assertEqual(response.status_code, 200)

    def test_post_add(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(bytes('nickolas:glasstaken123', 'utf8')).decode('utf8')
        }
        c = Client()
        c.login(username='nickolas', password='glasstaken123')
        response = c.post('/add/', **auth_headers)
        return self.assertEqual(response.status_code, 200)

    #
    def test_post_search(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(bytes('tester:dark5550505', 'utf8')).decode('utf8')
        }
        c = Client()
        c.login(username='tester', password='dark5550505')
        response = c.post('/search/', **auth_headers)
        return self.assertEqual(response.status_code, 200)

    def test_post_login(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(bytes('nickolas:glasstaken123', 'utf8')).decode('utf8')
        }
        c = Client()
        c.login(username='nickolas', password='glasstaken123')
        response = c.post('/login/', {'username': 'nickolas', 'password': 'glasstaken123'}, **auth_headers)
        return self.assertEqual(response.status_code, 302)
