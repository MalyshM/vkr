import asyncio
import unittest
import aiohttp as aiohttp


class UtilTests(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://moais-dashboard.ru:8082'
        self.loop = asyncio.get_event_loop()

    async def post_request(self, url: str, user_data_to_json: dict | None = None, token: str | None = None) -> dict:
        async with aiohttp.ClientSession(trust_env=True) as session:
            if token is None:
                res = await session.post(self.base_url + url, json=user_data_to_json)
            else:
                res = await session.post(self.base_url + url + f"?token={token}")
            return {'status': res.status, 'response_json': await res.json(), 'response_text': await res.text(),
                    'headers': res.headers}

    async def get_request(self, url: str, **params) -> dict:
        async with aiohttp.ClientSession(trust_env=True) as session:
            temp_str = '?'
            for key, value in params.items():
                temp_str += key + '=' + str(value) + '&'
            if temp_str[-1] == '&': temp_str = temp_str[:-1]
            if len(temp_str) == 1: temp_str = ''
            res = await session.get(self.base_url + url + temp_str)
            return {'status': res.status, 'response_json': await res.json(), 'response_text': await res.text(),
                    'headers': res.headers}

    def test_get_all_specialities_by_true_token(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        params = {'token': response['response_json']['access_token']}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/get_all_specialities", **params))
        self.assertEqual(response['status'], 200)

        for speciality in response['response_json']:
            self.assertIsInstance(speciality["speciality"], str)
            self.assertIsNotNone(speciality["speciality"])

    def test_get_all_specialities_by_false_token(self):
        params = {'token': 'token'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/get_all_specialities", **params))
        self.assertEqual(response['status'], 401)

    def test_get_all_kr(self):
        response = self.loop.run_until_complete(
            self.get_request(url='/api/get_all_kr'))
        self.assertEqual(response['status'], 200)

        for kr in response['response_json']:
            self.assertIsInstance(kr["name"], str)
            self.assertIsNotNone(kr["name"])

    def test_get_all_teachers_unique_by_true_token(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        params = {'token': response['response_json']['access_token']}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/get_all_teachers_unique", **params))
        self.assertEqual(response['status'], 200)

        for teacher in response['response_json']:
            self.assertIsInstance(teacher["id"], int)
            self.assertIsInstance(teacher["name"], str)
            self.assertIsNotNone(teacher["id"])
            self.assertIsNotNone(teacher["name"])

    def test_get_all_teachers_unique_by_false_token(self):
        params = {'token': 'token'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/get_all_teachers_unique", **params))
        self.assertEqual(response['status'], 401)

    def test_get_all_teachers_by_true_token(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        params = {'token': response['response_json']['access_token']}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/get_all_teachers", **params))
        self.assertEqual(response['status'], 200)

        for teacher in response['response_json']:
            self.assertIsInstance(teacher["id"], int)
            self.assertIsInstance(teacher["name"], str)
            self.assertIsNotNone(teacher["id"])
            self.assertIsNotNone(teacher["name"])

    def test_get_all_teachers_by_false_token(self):
        params = {'token': 'token'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/get_all_teachers", **params))
        self.assertEqual(response['status'], 401)


if __name__ == '__main__':
    unittest.main()
