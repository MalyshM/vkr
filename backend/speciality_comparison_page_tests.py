import asyncio
import unittest
import aiohttp as aiohttp


class SpecialityComparisonTests(unittest.TestCase):
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

    def test_attendance_static_for_specialities_a(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'speciality1': '10.05.03 Информационная безопасность автоматизированных систем',
                  'speciality2': '01.03.03 Механика и математическое моделирование',
                  'lect': False}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_for_specialities", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["speciality"], str)
            self.assertIsInstance(item["arrival"], float)
            self.assertIsInstance(item["id"], int)
            self.assertIsNotNone(item["speciality"])
            self.assertIsNotNone(item["arrival"])
            self.assertIsNotNone(item["id"])

    def test_attendance_static_for_specialities_b(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'speciality1': '',
                  'speciality2': '',
                  'lect': False}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_for_specialities", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["speciality"], str)
            self.assertIsInstance(item["arrival"], float)
            self.assertIsInstance(item["id"], int)
            self.assertIsNotNone(item["speciality"])
            self.assertIsNotNone(item["arrival"])
            self.assertIsNotNone(item["id"])

    def test_attendance_static_for_specialities_false(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'speciality1': '01.03.03 Механика и математическое моделирование',
                  'lect': False}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_for_specialities", **params))
        self.assertEqual(response['status'], 422)

    def test_attendance_static_for_specialities_by_false_token(self):
        params = {'token': 'token',
                  'speciality1': '10.05.03 Информационная безопасность автоматизированных систем',
                  'speciality2': '01.03.03 Механика и математическое моделирование',
                  'lect': False}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_for_specialities", **params))
        self.assertEqual(response['status'], 401)

    def test_total_points_for_specialities_a(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'speciality1': '10.05.03 Информационная безопасность автоматизированных систем',
                  'speciality2': '01.03.03 Механика и математическое моделирование',
                  'lect': False}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/total_points_for_specialities", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["speciality"], str)
            self.assertIsInstance(float(item["total_points"]), float)
            self.assertFalse(math.isnan(float(item["total_points"])))
            self.assertIsInstance(item["id"], int)
            self.assertIsNotNone(item["speciality"])
            self.assertIsNotNone(item["total_points"])
            self.assertIsNotNone(item["id"])

    def test_total_points_for_specialities_b(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'speciality1': '',
                  'speciality2': '',
                  'lect': False}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/total_points_for_specialities", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["speciality"], str)
            self.assertIsInstance(item["total_points"], float)
            self.assertIsInstance(item["id"], int)
            self.assertIsNotNone(item["speciality"])
            self.assertIsNotNone(item["total_points"])
            self.assertIsNotNone(item["id"])

    def test_total_points_for_specialities_false(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'speciality1': '01.03.03 Механика и математическое моделирование',
                  'lect': False}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/total_points_for_specialities", **params))
        self.assertEqual(response['status'], 422)

    def test_total_points_for_specialities_by_false_token(self):
        params = {'token': 'token',
                  'speciality1': '10.05.03 Информационная безопасность автоматизированных систем',
                  'speciality2': '01.03.03 Механика и математическое моделирование',
                  'lect': False}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/total_points_for_specialities", **params))
        self.assertEqual(response['status'], 401)

    def test_attendance_static_stud_for_all_specialities(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'lect': False}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_stud_for_all_specialities", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["stud_speciality"], str)
            self.assertIsInstance(item["arrival"], float)
            self.assertIsInstance(item["studs_in_speciality"], int)
            self.assertIsNotNone(item["stud_speciality"])
            self.assertIsNotNone(item["arrival"])
            self.assertIsNotNone(item["studs_in_speciality"])

    def test_attendance_static_stud_for_all_specialities_false(self):
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
            self.get_request(url="/api/attendance_static_stud_for_all_specialities", **params))
        self.assertEqual(response['status'], 422)

    def test_attendance_static_stud_for_all_specialities_by_false_token(self):
        params = {'token': 'token',
                  'lect': False}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_stud_for_all_specialities", **params))
        self.assertEqual(response['status'], 401)

    def test_total_points_studs_for_all_specialities_by_true_token(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'lect': True}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/total_points_studs_for_all_specialities", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["stud_speciality"], str)
            self.assertIsInstance(item["avg_total_points"], float)
            self.assertIsInstance(item["studs_in_speciality"], int)
            self.assertIsNotNone(item["stud_speciality"])
            self.assertIsNotNone(item["avg_total_points"])
            self.assertIsNotNone(item["studs_in_speciality"])

    def test_total_points_studs_for_all_specialities_by_false_token(self):
        params = {'token': 'token',
                  'lect': True}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/total_points_studs_for_all_specialities", **params))
        self.assertEqual(response['status'], 401)

    def test_total_points_studs_for_all_specialities_false(self):
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
            self.get_request(url="/api/total_points_studs_for_all_specialities", **params))
        self.assertEqual(response['status'], 422)

    def test_attendance_static_total_points_studs_for_all_specialities_by_true_token(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'lect': True}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_total_points_studs_for_all_specialities", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["stud_speciality"], str)
            self.assertIsInstance(item["avg_total_points"], float)
            self.assertIsInstance(item["studs_in_speciality"], int)
            self.assertIsNotNone(item["stud_speciality"])
            self.assertIsNotNone(item["avg_total_points"])
            self.assertIsNotNone(item["studs_in_speciality"])

    def test_attendance_static_total_points_studs_for_all_specialities_by_false_token(self):
        params = {'token': 'token',
                  'lect': True}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_total_points_studs_for_all_specialities", **params))
        self.assertEqual(response['status'], 401)

    def test_attendance_static_total_points_studs_for_all_specialities_false(self):
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
            self.get_request(url="/api/attendance_static_total_points_studs_for_all_specialities", **params))
        self.assertEqual(response['status'], 422)

    def test_speciality_kr_total_points_attendance_dynamic(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_speciality_kr_total_points_attendance_dynamic2(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_speciality_kr_total_points_attendance_dynamic3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],
                'group_by_speciality': 'false',
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])
            self.assertIn(total_points['teacher_name'], "Павлова Елена Александровна, Плотоненко Юрий Анатольевич")

    def test_speciality_kr_total_points_attendance_dynamic4(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'true',
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_speciality_kr_total_points_attendance_dynamic5(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_speciality_kr_total_points_attendance_dynamic6(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])
            self.assertIn(total_points['teacher_name'], "Павлова Елена Александровна")

    def test_speciality_kr_total_points_attendance_dynamic_fail(self):
        data = {'token': 'token', 'group_by_speciality': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 401)

    def test_speciality_kr_total_points_attendance_dynamic_fail2(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token']}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 422)

    def test_speciality_kr_total_points_attendance_dynamic_fail3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false',
                'teacher_list': 'asd,asd'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 401)

    def test_speciality_kr_total_points_attendance_dynamic_fail4(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false',
                'teacher_list': 'Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIn(total_points['teacher_name'], 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич')

    def test_speciality_kr_attendance_dynamic(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_speciality_kr_attendance_dynamic2(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_speciality_kr_attendance_dynamic3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],
                'group_by_speciality': 'false',
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])
            self.assertIn(total_points['teacher_name'], "Павлова Елена Александровна, Плотоненко Юрий Анатольевич")

    def test_speciality_kr_attendance_dynamic4(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'true',
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_speciality_kr_attendance_dynamic5(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_speciality_kr_attendance_dynamic6(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])
            self.assertIn(total_points['teacher_name'], "Павлова Елена Александровна")

    def test_speciality_kr_attendance_dynamic_fail(self):
        data = {'token': 'token', 'group_by_speciality': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 401)

    def test_speciality_kr_attendance_dynamic_fail2(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token']}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 422)

    def test_speciality_kr_attendance_dynamic_fail3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false',
                'teacher_list': 'asd,asd'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 401)

    def test_speciality_kr_attendance_dynamic_fail4(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false',
                'teacher_list': 'Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIn(total_points['teacher_name'], 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич')

    def test_speciality_kr_total_points_dynamic(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])

    def speciality_kr_total_points_dynamic2(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])

    def test_speciality_kr_total_points_dynamic3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],
                'group_by_speciality': 'false',
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIn(total_points['teacher_name'], "Павлова Елена Александровна, Плотоненко Юрий Анатольевич")

    def test_speciality_kr_total_points_dynamic4(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'true',
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])

    def test_speciality_kr_total_points_dynamic5(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])

    def test_speciality_kr_total_points_dynamic6(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['stud_speciality'], str)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points['stud_speciality'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIn(total_points['teacher_name'], "Павлова Елена Александровна")

    def test_speciality_kr_total_points_dynamic_fail(self):
        data = {'token': 'token', 'group_by_speciality': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 401)

    def test_speciality_kr_total_points_dynamic_fail2(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token']}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 422)

    def test_speciality_kr_total_points_dynamic_fail3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false',
                'teacher_list': 'asd,asd'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 401)

    def test_speciality_kr_total_points_dynamic_fail4(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_speciality': 'false',
                'teacher_list': 'Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIn(total_points['teacher_name'], 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич')


if __name__ == '__main__':
    unittest.main()
