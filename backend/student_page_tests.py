import asyncio
import unittest
import aiohttp as aiohttp


class StudentPageTests(unittest.TestCase):
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
        params = {'id_stud': 144,
                  'id_team': 2}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/cum_sum_points_for_stud_for_team", **params))
        self.assertEqual(response['status'], 200)
        # todo: жалуется на mimetype

        for item in response['response_json']:
            self.assertIsInstance(item["name"], str)
            self.assertIsInstance(item["cum_sum"], float)
            self.assertIsInstance(item["counter"], int)
            self.assertIsInstance(item["isTest"], bool)
            self.assertIsNotNone(item["name"])
            self.assertIsNotNone(item["cum_sum"])
            self.assertIsNotNone(item["counter"])
            self.assertIsNotNone(item["isTest"])


    def test_attendance_dynamical_for_stud_for_team_true(self):
        params = {'id_stud': 144,
                  'id_team': 2}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_dynamical_for_stud_for_team", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["name"], str)
            self.assertIsInstance(item["dynamical_arrival"], float)
            self.assertIsNotNone(item["name"])
            self.assertIsNotNone(item["dynamical_arrival"])


    def test_attendance_dynamical_for_stud_for_team_false(self):
        params = {'id_stud': None,
                  'id_team': None}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_dynamical_for_stud_for_team", **params))
        self.assertEqual(response['status'], 422)


    def test_attendance_static_for_stud_for_team_true(self):
        params = {'id_stud': 144,
                  'id_team': 2}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_for_stud_for_team", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["name"], str)
            self.assertIsInstance(item["static_arrival"], float)
            self.assertIsNotNone(item["name"])
            self.assertIsNotNone(item["static_arrival"])

    def test_attendance_static_for_stud_for_team_false(self):
        params = {'id_stud': None,
                  'id_team': None}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_for_stud_for_team", **params))
        self.assertEqual(response['status'], 422)

    def test_all_in_one_for_stud_for_team(self):
        params = {'id_stud': 144,
                  'id_team': 2}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/all_in_one_for_stud_for_team", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["name"], str)
            self.assertIsInstance(item["static_arrival"], float)
            self.assertIsInstance(item["dynamical_arrival"], float)
            self.assertIsInstance(item["cum_sum"], float)
            self.assertIsInstance(item["counter"], int)
            self.assertIsInstance(item["isTest"], bool)
            self.assertIsNotNone(item["name"])
            self.assertIsNotNone(item["static_arrival"])
            self.assertIsNotNone(item["dynamical_arrival"])
            self.assertIsNotNone(item["cum_sum"])
            self.assertIsNotNone(item["counter"])
            self.assertIsNotNone(item["isTest"])

    def test_all_in_one_for_stud_for_team(self):
        params = {'id_stud': None,
                  'id_team': None}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/all_in_one_for_stud_for_team", **params))
        self.assertEqual(response['status'], 422)




if __name__ == '__main__':
    unittest.main()