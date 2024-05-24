import asyncio
import unittest
import aiohttp as aiohttp


class TeamTests(unittest.TestCase):
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

    def test_get_teams_for_user_wo_lect_by_true_token(self):
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
            self.get_request(url="/api/get_teams_for_user_without_lect", **params))

        self.assertEqual(response['status'], 200)
        self.assertEqual(response['headers']['content-type'], 'application/json')

        self.assertIsInstance(response['response_json'], list)
        for team in response['response_json']:
            self.assertIsInstance(team["id"], int)
            self.assertIsInstance(team["name"], str)
            self.assertIsNotNone(team["id"])
            self.assertIsNotNone(team["name"])

    def test_get_teams_for_user_wo_lect_by_false_token(self):
        params = {'token': 'token'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/get_teams_for_user_without_lect", **params))
        self.assertEqual(response['status'], 401)


if __name__ == '__main__':
    unittest.main()
