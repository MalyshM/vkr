import asyncio
import unittest
import aiohttp as aiohttp

class GroupComparisonPageTests(unittest.TestCase):
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

    def test_attendance_static_stud_for_teams(self):
        data = {'id_team1': 2, 'id_team2': 2}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_stud_for_teams", **data))
        self.assertEqual(response['status'], 200)
        for attendance_stud in response['response_json']:
            self.assertIsInstance(attendance_stud['name'], str)
            self.assertIsInstance(attendance_stud['id'], int)
            self.assertIsInstance(attendance_stud['team_name'], str)
            self.assertIsInstance(attendance_stud['arrival'], float)
            self.assertIsInstance(attendance_stud['team_id'], int)
            self.assertIsNotNone(attendance_stud['name'])
            self.assertIsNotNone(attendance_stud['id'])
            self.assertIsNotNone(attendance_stud['team_name'])
            self.assertIsNotNone(attendance_stud['arrival'])
            self.assertIsNotNone(attendance_stud['team_id'])

    def test_attendance_static_stud_for_teams_fail(self):
        data = {'id_team1': -1, 'id_team2': 2}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_stud_for_teams", **data))
        self.assertEqual(response['status'], 200)

    def test_attendance_static_stud_for_teams_fail_2(self):
        data = {'id_team1': 2, 'id_team2': -1}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_stud_for_teams", **data))
        self.assertEqual(response['status'], 200)

    def test_attendance_static_stud_for_teams_fail_3(self):
        data = {'id_team1': -1, 'id_team2': -1}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_stud_for_teams", **data))
        self.assertEqual(response['status'], 200)

    def test_total_points_stud_for_teams(self):
        data = {'id_team1': 2, 'id_team2': 2}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/total_points_stud_for_teams", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['name'], str)
            self.assertIsInstance(total_points['id'], int)
            self.assertIsInstance(total_points['team_name'], str)
            self.assertIsInstance(total_points['total_points'], float)
            self.assertIsInstance(total_points['team_id'], int)
            self.assertIsNotNone(total_points['name'])
            self.assertIsNotNone(total_points['id'])
            self.assertIsNotNone(total_points['team_name'])
            self.assertIsNotNone(total_points['total_points'])
            self.assertIsNotNone(total_points['team_id'])

    def test_total_points_stud_for_teams_fail_1(self):
        data = {'id_team1': -1, 'id_team2': 2}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/total_points_stud_for_teams", **data))
        self.assertEqual(response['status'], 200)

    def test_total_points_stud_for_teams_fail_2(self):
        data = {'id_team1': 2, 'id_team2': -1}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/total_points_stud_for_teams", **data))
        self.assertEqual(response['status'], 200)

    def test_total_points_stud_for_teams_fail_3(self):
        data = {'id_team1': -1, 'id_team2': -1}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/total_points_stud_for_teams", **data))
        self.assertEqual(response['status'], 200)

    def test_attendance_static_stud_for_all_teams(self):
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
            self.get_request(url="/api/attendance_static_stud_for_all_teams", **data))
        self.assertEqual(response['status'], 200)
        for attendance_stud in response['response_json']:
            self.assertIsInstance(attendance_stud['team_name'], str)
            self.assertIsInstance(attendance_stud['arrival'], float)
            self.assertIsInstance(attendance_stud['team_id'], int)
            self.assertIsInstance(attendance_stud['teacher_id'], int)
            self.assertIsInstance(attendance_stud['teacher_name'], str)
            self.assertIsNotNone(attendance_stud['team_name'])
            self.assertIsNotNone(attendance_stud['arrival'])
            self.assertIsNotNone(attendance_stud['team_id'])
            self.assertIsNotNone(attendance_stud['teacher_id'])
            self.assertIsNotNone(attendance_stud['teacher_name'])

    def test_attendance_static_stud_for_all_teams_fail(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': 'token'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_static_stud_for_all_teams", **data))
        self.assertEqual(response['status'], 401)

    def test_total_points_studs_for_all_teams(self):
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
            self.get_request(url="/api/total_points_studs_for_all_teams", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['team_name'], str)
            self.assertIsInstance(total_points['avg_total_points'], float)
            self.assertIsInstance(total_points['team_id'], int)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsNotNone(total_points['team_name'])
            self.assertIsNotNone(total_points['avg_total_points'])
            self.assertIsNotNone(total_points['team_id'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])

    def test_total_points_studs_for_all_teams_fail(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': 'token'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/total_points_studs_for_all_teams", **data))
        self.assertEqual(response['status'], 401)

    def test_team_kr_total_points_attendance_dynamic(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_team_kr_total_points_attendance_dynamic2(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points["team_name"], str)
            self.assertIsInstance(total_points["team_id"], int)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['team_name'])
            self.assertIsNotNone(total_points['team_id'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_team_kr_total_points_attendance_dynamic3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],
                'group_by_teacher': 'false', 'teacher_list':'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points["team_name"], str)
            self.assertIsInstance(total_points["team_id"], int)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['team_name'])
            self.assertIsNotNone(total_points['team_id'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_team_kr_total_points_attendance_dynamic4(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'true',
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_team_kr_total_points_attendance_dynamic5(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_team_kr_total_points_attendance_dynamic6(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points["team_name"], str)
            self.assertIsInstance(total_points["team_id"], int)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsInstance(total_points['Посещаемость_средняя'], float)
            self.assertIsNotNone(total_points['team_name'])
            self.assertIsNotNone(total_points['team_id'])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])
            self.assertIsNotNone(total_points['Посещаемость_средняя'])

    def test_team_kr_total_points_attendance_dynamic_fail(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': 'token', 'group_by_teacher': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 401)

    def test_team_kr_total_points_attendance_dynamic_fail2(self):
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
            self.get_request(url="/api/team_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 422)

    def test_team_kr_total_points_attendance_dynamic_fail3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],'group_by_teacher': 'true',
                'teacher_list': 'asd,asd'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 401)

    def test_team_kr_total_points_attendance_dynamic_fail4(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],'group_by_teacher': 'false',
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)

    def test_team_kr_total_points_dynamic(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])

    def test_team_kr_total_points_dynamic2(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points["team_name"], str)
            self.assertIsInstance(total_points["team_id"], int)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points["team_name"])
            self.assertIsNotNone(total_points["team_id"])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])

    def test_team_kr_total_points_dynamic3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],
                'group_by_teacher': 'false', 'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points["team_name"], str)
            self.assertIsInstance(total_points["team_id"], int)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points["team_name"])
            self.assertIsNotNone(total_points["team_id"])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])

    def test_team_kr_total_points_dynamic4(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],
                'group_by_teacher': 'true', 'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])

    def test_team_kr_total_points_dynamic5(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])

    def test_team_kr_total_points_dynamic6(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for total_points in response['response_json']:
            self.assertIsInstance(total_points["team_name"], str)
            self.assertIsInstance(total_points["team_id"], int)
            self.assertIsInstance(total_points['teacher_id'], int)
            self.assertIsInstance(total_points['teacher_name'], str)
            self.assertIsInstance(total_points['Успеваемость_средняя'], float)
            self.assertIsNotNone(total_points["team_name"])
            self.assertIsNotNone(total_points["team_id"])
            self.assertIsNotNone(total_points['teacher_id'])
            self.assertIsNotNone(total_points['teacher_name'])
            self.assertIsNotNone(total_points['Успеваемость_средняя'])

    def test_team_kr_total_points_dynamic_fail(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': 'token', 'group_by_teacher': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 401)

    def test_team_kr_total_points_dynamic_fail2(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 422)

    def test_team_kr_total_points_dynamic_fail3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],'group_by_teacher': 'false',
                'teacher_list': 'asd.asd'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)

    def test_team_kr_total_points_dynamic_fail4(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],
                'group_by_teacher': 'false', 'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_total_points_dynamic", **data))
        self.assertEqual(response['status'], 200)

    def test_team_kr_attendance_dynamic(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for attendance_dynamic in response['response_json']:
            self.assertIsInstance(attendance_dynamic['teacher_id'], int)
            self.assertIsInstance(attendance_dynamic['teacher_name'], str)
            self.assertIsInstance(attendance_dynamic['Посещаемость_средняя'], float)
            self.assertIsNotNone(attendance_dynamic['teacher_id'])
            self.assertIsNotNone(attendance_dynamic['teacher_name'])
            self.assertIsNotNone(attendance_dynamic['Посещаемость_средняя'])

    def test_team_kr_attendance_dynamic2(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for attendance_dynamic in response['response_json']:
            self.assertIsInstance(attendance_dynamic["team_name"], str)
            self.assertIsInstance(attendance_dynamic["team_id"], int)
            self.assertIsInstance(attendance_dynamic['teacher_id'], int)
            self.assertIsInstance(attendance_dynamic['teacher_name'], str)
            self.assertIsInstance(attendance_dynamic['Посещаемость_средняя'], float)
            self.assertIsNotNone(attendance_dynamic["team_name"])
            self.assertIsNotNone(attendance_dynamic["team_id"])
            self.assertIsNotNone(attendance_dynamic['teacher_id'])
            self.assertIsNotNone(attendance_dynamic['teacher_name'])
            self.assertIsNotNone(attendance_dynamic['Посещаемость_средняя'])

    def test_team_kr_attendance_dynamic3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],
                'group_by_teacher': 'false', 'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for attendance_dynamic in response['response_json']:
            self.assertIsInstance(attendance_dynamic["team_name"], str)
            self.assertIsInstance(attendance_dynamic["team_id"], int)
            self.assertIsInstance(attendance_dynamic['teacher_id'], int)
            self.assertIsInstance(attendance_dynamic['teacher_name'], str)
            self.assertIsInstance(attendance_dynamic['Посещаемость_средняя'], float)
            self.assertIsNotNone(attendance_dynamic["team_name"])
            self.assertIsNotNone(attendance_dynamic["team_id"])
            self.assertIsNotNone(attendance_dynamic['teacher_id'])
            self.assertIsNotNone(attendance_dynamic['teacher_name'])
            self.assertIsNotNone(attendance_dynamic['Посещаемость_средняя'])

    def test_team_kr_attendance_dynamic4(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'true',
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for attendance_dynamic in response['response_json']:
            self.assertIsInstance(attendance_dynamic['teacher_id'], int)
            self.assertIsInstance(attendance_dynamic['teacher_name'], str)
            self.assertIsInstance(attendance_dynamic['Посещаемость_средняя'], float)
            self.assertIsNotNone(attendance_dynamic['teacher_id'])
            self.assertIsNotNone(attendance_dynamic['teacher_name'])
            self.assertIsNotNone(attendance_dynamic['Посещаемость_средняя'])

    def test_team_kr_attendance_dynamic5(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for attendance_dynamic in response['response_json']:
            self.assertIsInstance(attendance_dynamic['teacher_id'], int)
            self.assertIsInstance(attendance_dynamic['teacher_name'], str)
            self.assertIsInstance(attendance_dynamic['Посещаемость_средняя'], float)
            self.assertIsNotNone(attendance_dynamic['teacher_id'])
            self.assertIsNotNone(attendance_dynamic['teacher_name'])
            self.assertIsNotNone(attendance_dynamic['Посещаемость_средняя'])

    def test_team_kr_attendance_dynamic6(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'false'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)
        for attendance_dynamic in response['response_json']:
            self.assertIsInstance(attendance_dynamic["team_name"], str)
            self.assertIsInstance(attendance_dynamic["team_id"], int)
            self.assertIsInstance(attendance_dynamic['teacher_id'], int)
            self.assertIsInstance(attendance_dynamic['teacher_name'], str)
            self.assertIsInstance(attendance_dynamic['Посещаемость_средняя'], float)
            self.assertIsNotNone(attendance_dynamic["team_name"])
            self.assertIsNotNone(attendance_dynamic["team_id"])
            self.assertIsNotNone(attendance_dynamic['teacher_id'])
            self.assertIsNotNone(attendance_dynamic['teacher_name'])
            self.assertIsNotNone(attendance_dynamic['Посещаемость_средняя'])

    def test_team_kr_attendance_dynamic_fail(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': 'token', 'group_by_teacher': 'true'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 401)

    def test_team_kr_attendance_dynamic_fail2(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 422)

    def test_team_kr_attendance_dynamic_fail3(self):
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'],'group_by_teacher': 'false',
                'teacher_list': 'asd.asd'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 405)

    def test_team_kr_attendance_dynamic_fail4(self):
        login_data = {
            "FIO": "Павлова Елена Александровна",
            "username": "Павлова Елена Александровна",
            "password": "Павлова Елена Александровна",
            "email": "Павлова Елена Александровна"
        }
        response = self.loop.run_until_complete(
            self.post_request(user_data_to_json=login_data, url="/api/login_standard"))
        data = {'token': response['response_json']['access_token'], 'group_by_teacher': 'false',
                'teacher_list': 'Павлова Елена Александровна,Плотоненко Юрий Анатольевич'}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/team_kr_attendance_dynamic", **data))
        self.assertEqual(response['status'], 200)

if __name__ == '__main__':
    unittest.main()
