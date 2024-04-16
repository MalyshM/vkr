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
            self.assertIsInstance(item["total_points"] * 1.0, float) # чтобы привести к флоуту (нечисловое значение энивей не приведётся)te
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

    def test_speciality_kr_total_points_attendance_dynamic_group_true_token_adm(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'group_by_speciality': True,
                  'teacher_list': ''}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["stud_speciality"], str)
            self.assertIsInstance(item["teacher_id"], int)
            self.assertIsInstance(item["teacher_name"], str)
            self.assertIsInstance(item["Успеваемость_средняя"], float)
            self.assertIsInstance(item["Посещаемость_средняя"], float)
            self.assertIsNotNone(item["stud_speciality"])
            self.assertIsNotNone(item["teacher_id"])
            self.assertIsNotNone(item["teacher_name"])
            self.assertIsNotNone(item["Успеваемость_средняя"])
            self.assertIsNotNone(item["Посещаемость_средняя"])


    def test_speciality_kr_total_points_attendance_dynamic_group_false_token_adm(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'group_by_speciality': False,
                  'teacher_list': ''}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["stud_speciality"], str)
            self.assertIsInstance(item["teacher_id"], int)
            self.assertIsInstance(item["teacher_name"], str)
            self.assertIsInstance(item["Успеваемость_средняя"], float)
            self.assertIsInstance(item["Посещаемость_средняя"], float)
            self.assertIsNotNone(item["stud_speciality"])
            self.assertIsNotNone(item["teacher_id"])
            self.assertIsNotNone(item["teacher_name"])
            self.assertIsNotNone(item["Успеваемость_средняя"])
            self.assertIsNotNone(item["Посещаемость_средняя"])

    def test_speciality_kr_total_points_attendance_dynamic_group_true_token_teach(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'group_by_speciality': True,
                  'teacher_list': ''}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["stud_speciality"], str)
            self.assertIsInstance(item["teacher_id"], int)
            self.assertIsInstance(item["teacher_name"], str)
            self.assertIsInstance(item["Успеваемость_средняя"], float)
            self.assertIsInstance(item["Посещаемость_средняя"], float)
            self.assertIsNotNone(item["stud_speciality"])
            self.assertIsNotNone(item["teacher_id"])
            self.assertIsNotNone(item["teacher_name"])
            self.assertIsNotNone(item["Успеваемость_средняя"])
            self.assertIsNotNone(item["Посещаемость_средняя"])

    def test_speciality_kr_total_points_attendance_dynamic_group_false_token_teach(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'group_by_speciality': False,
                  'teacher_list': ''}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["stud_speciality"], str)
            self.assertIsInstance(item["teacher_id"], int)
            self.assertIsInstance(item["teacher_name"], str)
            self.assertIsInstance(item["Успеваемость_средняя"], float)
            self.assertIsInstance(item["Посещаемость_средняя"], float)
            self.assertIsNotNone(item["stud_speciality"])
            self.assertIsNotNone(item["teacher_id"])
            self.assertIsNotNone(item["teacher_name"])
            self.assertIsNotNone(item["Успеваемость_средняя"])
            self.assertIsNotNone(item["Посещаемость_средняя"])

    def test_speciality_kr_total_points_attendance_dynamic(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))

        params = {'token': response['response_json']['access_token'],
                  'group_by_speciality': False,
                  'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **params))
        self.assertEqual(response['status'], 200)

        for item in response['response_json']:
            self.assertIsInstance(item["stud_speciality"], str)
            self.assertIsInstance(item["teacher_id"], int)
            self.assertIsInstance(item["teacher_name"], str)
            self.assertIsInstance(item["Успеваемость_средняя"], float)
            self.assertIsInstance(item["Посещаемость_средняя"], float)
            self.assertIsNotNone(item["stud_speciality"])
            self.assertIsNotNone(item["teacher_id"])
            self.assertIsNotNone(item["teacher_name"])
            self.assertIsNotNone(item["Успеваемость_средняя"])
            self.assertIsNotNone(item["Посещаемость_средняя"])

    def test_speciality_kr_total_points_attendance_dynamic_by_false_token(self):
        params = {'token': 'token',
                  'group_by_speciality': True,
                  'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **params))
        self.assertEqual(response['status'], 401)

    def test_speciality_kr_total_points_attendance_dynamic_false_a(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))


        params = {'token': response['response_json']['access_token'],
                  'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **params))
        self.assertEqual(response['status'], 422)

    def test_speciality_kr_total_points_attendance_dynamic_false_b(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))


        params = {'token': response['response_json']['access_token'],
                  'group_by_speciality': False,
                  'teacher_list': 'asd,asd'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **params))
        self.assertEqual(response['status'], 200)

    def test_speciality_kr_total_points_attendance_dynamic_false_c(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))


        params = {'token': response['response_json']['access_token'],
                  'group_by_speciality': False,
                  'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/speciality_kr_total_points_attendance_dynamic", **params))
        self.assertEqual(response['status'], 200)





if __name__ == '__main__':
    unittest.main()