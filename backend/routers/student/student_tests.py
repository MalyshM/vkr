import asyncio
import unittest
import aiohttp as aiohttp


class StudentTests(unittest.TestCase):
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

    def test_get_student_true(self):
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
        self.assertIsNotNone(data["speciality"])
        self.assertIsNotNone(data["id"])
        self.assertIsNotNone(data["email"])
        self.assertIsNotNone(data["date_of_add"])
        self.assertIsNotNone(data["name"])

    def test_get_student_false_a(self):
        params = {}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/get_student", **params))
        self.assertEqual(response['status'], 422)

    def test_get_student_false_b(self):
        params = {'id_stud': -1}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/get_student", **params))
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['headers']['content-type'], 'application/json')


if __name__ == '__main__':
    unittest.main()
