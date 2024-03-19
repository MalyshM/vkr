import asyncio
import unittest
import aiohttp as aiohttp
from handlers import delete_test_user


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


    def test_cum_sum_points_for_stud_for_team(self):
        params = {'id_stud': 1,
                  'id_team': 1}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/cum_sum_points_for_stud_for_team", **params))
        self.assertEqual(response['status'], 200)

        for cum_sum in response['response_json']:
            self.assertIsInstance(cum_sum["name"], str)
            self.assertIsInstance(cum_sum["cum_sum"], int)
            self.assertIsInstance(cum_sum["counter"], int)
            self.assertIsInstance(cum_sum["isTest"], bool)

            # Проверка на none
            self.assertIsNotNone(cum_sum["name"])
            self.assertIsNotNone(cum_sum["cum_sum"])
            self.assertIsNotNone(cum_sum["counter"])
            self.assertIsNotNone(cum_sum["isTest"])


    def test_attendance_dynamical_for_stud_for_team(self):
        params = {'id_stud': 1,
                  'id_team': 1}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_dynamical_for_stud_for_team", **params))
        self.assertEqual(response['status'], 200)

        for dynamical_arrival in response['response_json']:
            self.assertIsInstance(dynamical_arrival["name"], str)
            self.assertIsInstance(dynamical_arrival["dynamical_arrival"], int)

            # Проверка на none
            self.assertIsNotNone(dynamical_arrival["name"])
            self.assertIsNotNone(dynamical_arrival["dynamical_arrival"])

    def test_attendance_static_for_stud_for_team(self):
        params = {'id_stud': 1,
                  'id_team': 1}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_for_stud_for_team", **params))
        self.assertEqual(response['status'], 200)

        for static_arrival in response['response_json']:
            self.assertIsInstance(static_arrival["name"], str)
            self.assertIsInstance(static_arrival["static_arrival"], float)

            # Проверка на none
            self.assertIsNotNone(static_arrival["name"])
            self.assertIsNotNone(static_arrival["static_arrival"])

    def test_all_in_one_for_stud_for_team(self):
        params = {'id_stud': 1,
                  'id_team': 1}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/all_in_one_for_stud_for_team", **params))
        self.assertEqual(response['status'], 200)

        for static_arrival in response['response_json']:
            self.assertIsInstance(static_arrival["name"], str)
            self.assertIsInstance(static_arrival["static_arrival"], float)

            # Проверка на none
            self.assertIsNotNone(static_arrival["name"])
            self.assertIsNotNone(static_arrival["static_arrival"])




if __name__ == '__main__':
    unittest.main()