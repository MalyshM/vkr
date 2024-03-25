import asyncio
import unittest
import aiohttp as aiohttp

class MainPageTests(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:8090'
        self.loop = asyncio.get_event_loop()

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

    def test_attendance_per_stud_for_team(self):
        data = {'id_team': 2}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_per_stud_for_team", **data))
        self.assertEqual(response['status'], 200)
        for stud_data in response['response_json']:
            self.assertIsInstance(stud_data['stud_name'], str)
            self.assertIsInstance(stud_data['stud_id'], int)
            self.assertIsInstance(stud_data['Посещаемость'], float)
            self.assertIsNotNone(stud_data['stud_name'])
            self.assertIsNotNone(stud_data['stud_id'])
            self.assertIsNotNone(stud_data['Посещаемость'])

    def test_attendance_per_stud_for_team_fail(self):
        data = {'id_team': -1}
        response = self.loop.run_until_complete(
            self.get_request(url="/api/attendance_per_stud_for_team", **data))
        self.assertEqual(response['status'], 200)

    def test_total_points_attendance_per_stud_for_team(self):
        data = {'id_team': 2}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/total_points_attendance_per_stud_for_team', **data))
        self.assertEqual(response['status'], 200)
        for stud_attendance in response['response_json']:
            self.assertIsInstance(stud_attendance['stud_name'], str)
            self.assertIsInstance(stud_attendance['stud_id'], int)
            self.assertIsInstance(stud_attendance['Посещаемость'], float)
            self.assertIsInstance(stud_attendance['Успеваемость'], float)
            self.assertIsInstance(stud_attendance['Посещаемость_средняя'], float)
            self.assertIsInstance(stud_attendance['Успеваемость_средняя'], float)
            self.assertIsNotNone(stud_attendance['stud_name'])
            self.assertIsNotNone(stud_attendance['stud_id'])
            self.assertIsNotNone(stud_attendance['Посещаемость'])
            self.assertIsNotNone(stud_attendance['Успеваемость'])
            self.assertIsNotNone(stud_attendance['Посещаемость_средняя'])
            self.assertIsNotNone(stud_attendance['Успеваемость_средняя'])

    def test_total_points_attendance_per_stud_for_team_fail(self):
        data = {'id_team': -1}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/total_points_attendance_per_stud_for_team', **data))
        self.assertEqual(response['status'], 200)

    def test_total_points_per_stud_for_team(self):
        data = {'id_team': 2}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/total_points_per_stud_for_team', **data))
        self.assertEqual(response['status'], 200)
        for stud_attendance in response['response_json']:
            self.assertIsInstance(stud_attendance['stud_name'], str)
            self.assertIsInstance(stud_attendance['stud_id'], int)
            self.assertIsInstance(stud_attendance['Успеваемость'], float)
            self.assertIsNotNone(stud_attendance['stud_name'])
            self.assertIsNotNone(stud_attendance['stud_id'])
            self.assertIsNotNone(stud_attendance['Успеваемость'])

    def test_total_points_per_stud_for_team_fail(self):
        data = {'id_team': -1}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/total_points_per_stud_for_team', **data))
        self.assertEqual(response['status'], 200)

    def test_total_marks_for_team(self):
        data = {'id_team': 2}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/total_marks_for_team', **data))
        self.assertEqual(response['status'], 200)
        for mark in response['response_json']:
            self.assertIsInstance(mark['mark'], str)
            self.assertIsInstance(mark['percent'], float)
            self.assertIsInstance(mark['avg_total_points'], float)
            self.assertIsNotNone(mark['mark'])
            self.assertIsNotNone(mark['percent'])
            self.assertIsNotNone(mark['avg_total_points'])
            if (mark['avg_total_points'] > 90):
                expected_mark = 'отл.'
            elif (mark['avg_total_points'] > 75):
                expected_mark = 'хор.'
            elif (mark['avg_total_points'] > 61):
                expected_mark = 'удовл.'
            else:
                expected_mark = 'неудовл.'
            self.assertEqual(mark['mark'], expected_mark)

    def test_total_marks_for_team_fail(self):
        data = {'id_team': -1}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/total_marks_for_team', **data))
        self.assertEqual(response['status'], 200)

    def test_attendance_num_for_stud_for_team(self):
        data = {'id_team': 2}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/attendance_num_for_stud_for_team', **data))
        self.assertEqual(response['status'], 200)
        for attendance in response['response_json']:
            self.assertIsInstance(attendance['name'], str)
            self.assertIsInstance(attendance['id'], int)
            self.assertIsInstance(attendance['Посещаемость'], int)
            self.assertIsNotNone(attendance['name'])
            self.assertIsNotNone(attendance['id'])
            self.assertIsNotNone(attendance['Посещаемость'])

    def test_attendance_num_for_stud_for_team_fail(self):
        data = {'id_team': -1}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/attendance_num_for_stud_for_team', **data))
        self.assertEqual(response['status'], 200)

    def test_attendance_num_for_stud_for_team_stat_table_team(self):
        data = {'id_team': 2, "name_of_lesson": "Организация функций30"}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/attendance_num_for_stud_for_team_stat_table', **data))
        self.assertEqual(response['status'], 200)
        for attendance in response['response_json']:
            self.assertIsInstance(attendance['stud_name'], str)
            self.assertIsInstance(attendance['id'], int)
            self.assertIsInstance(attendance['Успеваемость'], float)
            self.assertIsInstance(attendance['Посещаемость'], float)
            self.assertIsNotNone(attendance['stud_name'])
            self.assertIsNotNone(attendance['id'])
            self.assertIsNotNone(attendance['Успеваемость'])
            self.assertIsNotNone(attendance['Посещаемость'])

    def test_attendance_num_for_stud_for_team_stat_table_fail(self):
        data = {'id_team': -1}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/attendance_num_for_stud_for_team_stat_table', **data))
        self.assertEqual(response['status'], 200)

    def test_attendance_num_for_stud_for_team_stat_table_fail(self):
        data = {'id_team': -1}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/attendance_num_for_stud_for_team_stat_table', **data))
        self.assertEqual(response['status'], 422)

    def test_attendance_num_for_stud_for_team_stat_table_fail_2(self):
        data = {'id_team': 2}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/attendance_num_for_stud_for_team_stat_table', **data))
        self.assertEqual(response['status'], 422)

    def test_attendance_num_for_stud_for_team_stat_table_fail_3(self):
        data = {'id_team': 'name_of_lesson'}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/attendance_num_for_stud_for_team_stat_table', **data))
        self.assertEqual(response['status'], 422)

    def test_attendance_num_for_stud_for_team_stat_table_fail_4(self):
        data = {'id_team': 'asd'}
        response = self.loop.run_until_complete(
            self.get_request(url='/api/attendance_num_for_stud_for_team_stat_table', **data))
        self.assertEqual(response['status'], 422)
