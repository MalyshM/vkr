import asyncio
import unittest
import aiohttp as aiohttp
from handlers import delete_test_user

asdasdasd
class UserTests(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:8090'
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
        self.loop.run_until_complete(delete_test_user())
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
            "isTeacher": False,
            "isCurator": False
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=user_data, url="/api/registration_standard"))
        self.assertEqual(response['status'], 409)
        self.assertIn("Пользователь с такими данными уже существует", response['response_text'])

    def test_z_get_user_by_false_token(self):
        # Test case for registration with conflicting user data
        response = self.loop.run_until_complete(
            self.post_request(token="token", url="/api/get_current_user_dev"))
        self.assertEqual(response['status'], 401)

    def test_z_get_user_by_true_token(self):
        # Test case for registration with conflicting user data
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        token = response['response_json']['access_token']
        response = self.loop.run_until_complete(
            self.post_request(token=token, url="/api/get_current_user_dev"))
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['response_json']["username"], "string")
        self.assertEqual(response['response_json']["isadmin"], True)
        self.assertEqual(response['response_json']["iscurator"], True)
        self.assertEqual(response['response_json']["email"], "string")
        self.assertEqual(response['response_json']["fio"], "string")
        self.assertEqual(response['response_json']["isteacher"], True)
        self.assertTrue(type(response['response_json']["date_of_add"]), str)
        self.assertEqual(len(response['response_json']), 9)

    def test_get_all_users(self):
        response = self.loop.run_until_complete(
            self.get_request(url='/api/get_all_users'))
        self.assertEqual(response['status'], 200)

        self.assertIsInstance(response['response_json'], list)

        for user in response['response_json']:
            self.assertIsInstance(user["id"], int)
            self.assertIsInstance(user["isadmin"], bool)
            self.assertIsInstance(user["iscurator"], bool)
            self.assertIsInstance(user["email"], str)
            self.assertIsInstance(user["fio"], str)
            self.assertIsInstance(user["username"], str)
            self.assertIsInstance(user["isteacher"], bool)
            self.assertIsInstance(user["date_of_add"], str)

            # Проверка на none
            self.assertIsNotNone(user["id"])
            self.assertIsNotNone(user["isadmin"])
            self.assertIsNotNone(user["iscurator"])
            self.assertIsNotNone(user["email"])
            self.assertIsNotNone(user["fio"])
            self.assertIsNotNone(user["username"])
            self.assertIsNotNone(user["isteacher"])
            self.assertIsNotNone(user["date_of_add"])

    def test_get_teams_for_user_by_true_token(self):

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
            self.get_request(url="/api/get_teams_for_user", **params))

        self.assertEqual(response['status'], 200)
        self.assertEqual(response['headers']['content-type'], 'application/json')

        self.assertIsInstance(response['response_json'], list)
        for team in response['response_json']:
            self.assertIsInstance(team["id"], int)
            self.assertIsInstance(team["name"], str)
            self.assertIsNotNone(team["id"])
            self.assertIsNotNone(team["name"])

    def test_get_teams_for_user_by_false_token(self):
        params = {'token': 'token'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/get_teams_for_user", **params))
        self.assertEqual(response['status'], 401)

    def test_get_student(self):
        params = {'id_stud': 2}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/get_student", **params))
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['headers']['content-type'], 'application/json')

        data = response['response_json'][0]
        self.assertIsInstance(data, dict)

        self.assertIsInstance(data["speciality"], str)
        self.assertIsInstance(data["id"], int)
        self.assertIsInstance(data["email"], str)
        self.assertIsInstance(data["date_of_add"], str)
        self.assertIsInstance(data["name"], str)
        # Проверка на none
        self.assertIsNotNone(data["speciality"])
        self.assertIsNotNone(data["id"])
        self.assertIsNotNone(data["email"])
        self.assertIsNotNone(data["date_of_add"])
        self.assertIsNotNone(data["name"])

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
