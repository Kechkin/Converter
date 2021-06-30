import base64
import json
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
        response = c.get('/', **auth_headers)
        return self.assertEqual(response.status_code, 200)

    def test_get_index2(self):
        c = Client()
        c.login(username='nickolas', password='glasstaken123')
        response = c.get('/')
        return self.assertEqual(response.status_code, 200)

    def test_post_add(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(bytes('nickolas:glasstaken123', 'utf8')).decode('utf8')
        }
        c = Client()
        response = c.post('/add/', **auth_headers)
        return self.assertEqual(response.status_code, 200)

    def test_post_search(self):
        c = Client()
        c.login(username='tester', password='dark5550505')
        response = c.post('/search/', {"currency": "USD"})
        return self.assertEqual(response.status_code, 200)

    def test_post_login(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(bytes('nickolas:glasstaken123', 'utf8')).decode('utf8')
        }
        c = Client()
        c.login(username='nickolas', password='glasstaken123')
        response = c.post('/login/', {'username': 'nickolas', 'password': 'glasstaken123'}, **auth_headers)
        return self.assertEqual(response.status_code, 302)

    def test_api_add(self):
        c = Client()
        data = {
            "currency": "USD",
            "value": 56.7,
        }
        c.login(username='nickolas', password='glasstaken123')
        response = c.post('/api/add/', json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        return self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'Data': {'currency': 'USD', 'value': '56.7'}}
        )

    def test_api_search(self):
        c = Client()
        data = {
            "currency": "USD",
            "time": "2021-05-27 12:22",
        }
        c.login(username='nickolas', password='glasstaken123')
        response = c.post('/api/search/', json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        return self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': {'currency': 'USD',
                      'time': '2021-05-27T11:48:49.340',
                      'value': '555.00'}}
        )

    def test_api_convert(self):
        c = Client()
        data = {
            "currency": "EURO",
            "currency2": "USD",
            "time": "2021-05-27 12:22",
            "money": 55
        }
        c.login(username='nickolas', password='glasstaken123')
        response = c.post('/api/convert/', json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        return self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': {'currency': 'EURO', 'result': '11.40', 'time': '2021-05-27 12:22'}}
        )
