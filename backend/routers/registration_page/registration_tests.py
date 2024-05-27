import asyncio
import unittest
import aiohttp as aiohttp


class RegistrationTests(unittest.TestCase):
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

    def test_a_registration_standard_a_success(self):
        self.loop.run_until_complete(self.get_request(url="/api/delete_test_user"))
        user_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string",
            "isAdmin": True,
            "isTeacher": True,
            "isCurator": True
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=user_data, url="/api/registration_standard"))
        self.assertEqual(response['status'], 200)
        self.assertIn("access_token", response['response_json'])
        self.assertEqual(response['response_json']["token_type"], "bearer")

    def test_registration_standard_z_conflict(self):
        # Test case for registration with conflicting user data
        user_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string",
            "isAdmin": True,
            "isTeacher": True,
            "isCurator": True
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=user_data, url="/api/registration_standard"))
        self.assertEqual(response['status'], 409)
        self.assertIn("Пользователь с такими данными уже существует", response['response_text'])

    def test_login_standard_success(self):
        # Test case for successful login
        user_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=user_data, url="/api/login_standard"))
        self.assertEqual(response['status'], 200)
        self.assertIn("access_token", response['response_json'])
        self.assertEqual(response['response_json']["token_type"], "bearer")

    def test_login_standard_invalid_user(self):
        # Test case for login with invalid user data
        user_data = {
            "FIO": "invalid",
            "username": "invalid",
            "password": "invalid",
            "email": "invalid"
        }

        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=user_data, url="/api/login_standard"))
        self.assertEqual(response['status'], 409)
        self.assertIn("Нельзя войти в несуществующий аккаунт/Неправильно введены данные", response['response_text'])


if __name__ == '__main__':
    unittest.main()
