import asyncio
import unittest
import aiohttp as aiohttp


class UserTests(unittest.TestCase):
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




if __name__ == '__main__':
    unittest.main()