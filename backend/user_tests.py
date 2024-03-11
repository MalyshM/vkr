import unittest
from fastapi.testclient import TestClient

from handlers import delete_test_user
from main import get_application

import math


class UserTests(unittest.TestCase):
    def setUp(self):
        self.app = get_application()
        self.client = TestClient(self.app)

    def test_a_registration_standard_a_success(self):
        # Test case for successful registration
        user_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string",
            "isAdmin": True,
            "isTeacher": True,
            "isCurator": True
        }

        response = self.client.post("/api/registration_standard", json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertEqual(response.json()["token_type"], "bearer")

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

        response = self.client.post("/api/registration_standard", json=user_data)
        self.assertEqual(response.status_code, 409)
        self.assertIn("Пользователь с такими данными уже существует", response.text)

    def test_z_get_user_by_false_token(self):
        # Test case for registration with conflicting user data
        response = self.client.post("/api/get_current_user_dev?token=token")
        self.assertEqual(response.status_code, 401)

    def test_z_get_user_by_true_token(self):
        # Test case for registration with conflicting user data
        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.client.post("/api/login_standard", json=login_data)
        token = response.json()['access_token']
        response = self.client.post(f"/api/get_current_user_dev?token={token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "string")
        self.assertEqual(response.json()["isadmin"], True)
        self.assertEqual(response.json()["iscurator"], True)
        self.assertEqual(response.json()["email"], "string")
        self.assertEqual(response.json()["fio"], "string")
        self.assertEqual(response.json()["isteacher"], True)
        self.assertTrue(type(response.json()["date_of_add"]), str)
        self.assertEqual(len(response.json()), 9)

    def test_get_all_users(self):
        response = self.client.get('/api/get_all_users')

        self.assertEqual(response.status_code, 200)

        self.assertIsInstance(response.json(), list)

        for user in response.json():
            self.assertEqual(type(user["id"]), int)
            self.assertEqual(type(user["isadmin"]), bool)
            self.assertEqual(type(user["iscurator"]), bool)
            self.assertEqual(type(user["email"]), str)
            self.assertEqual(type(user["fio"]), str)
            self.assertEqual(type(user["username"]), str)
            self.assertEqual(type(user["isteacher"]), bool)
            self.assertEqual(type(user["date_of_add"]), str)

            # Проверка на НаНы
            self.assertFalse(math.isnan(user["id"]))
            self.assertFalse(math.isnan(user["isadmin"]))
            self.assertFalse(math.isnan(user["iscurator"]))
            self.assertFalse(math.isnan(user["email"]))
            self.assertFalse(math.isnan(user["fio"]))
            self.assertFalse(math.isnan(user["username"]))
            self.assertFalse(math.isnan(user["isteacher"]))
            self.assertFalse(math.isnan(user["date_of_add"]))

    def test_get_teams_for_user_by_true_token(self):

        login_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }
        response = self.client.post("/api/login_standard", json=login_data)
        token = response.json()['access_token']

        response = self.client.get(f"/api/get_teams_for_user?token={token}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')

        self.assertIsInstance(response.json(), list)
        for team in response.json():
            self.assertEqual(type(team["id"]), int)
            self.assertEqual(type(team["name"]), str)

            self.assertFalse(math.isnan(response.json()["id"]))
            self.assertFalse(math.isnan(response.json()["name"]))

    def test_get_teams_for_user_by_false_token(self):
        response = self.client.get(f"/api/get_teams_for_user?token=token")
        self.assertEqual(response.status_code, 409)


    def test_get_student(self):
        student_id = 2
        response = self.client.get(f'/api/get_student?id_stud={student_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')

        data = response.json()
        self.assertIsInstance(data, dict)

        self.assertEqual(type(response.json()["speciality"]), str)
        self.assertEqual(type(response.json()["id"]), int)
        self.assertEqual(type(response.json()["email"]), str)
        self.assertEqual(type(response.json()["date_of_add"]), str)
        self.assertEqual(type(response.json()["name"]), str)

        # Проверка на НаНы
        self.assertFalse(math.isnan(response.json()["speciality"]))
        self.assertFalse(math.isnan(response.json()["id"]))
        self.assertFalse(math.isnan(response.json()["email"]))
        self.assertFalse(math.isnan(response.json()["date_of_add"]))
        self.assertFalse(math.isnan(response.json()["name"]))


    def test_login_standard_success(self):
        # Test case for successful login
        user_data = {
            "FIO": "string",
            "username": "string",
            "password": "string",
            "email": "string"
        }

        response = self.client.post("/api/login_standard", json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertEqual(response.json()["token_type"], "bearer")

    def test_login_standard_invalid_user(self):
        # Test case for login with invalid user data
        user_data = {
            "FIO": "invalid",
            "username": "invalid",
            "password": "invalid",
            "email": "invalid"
        }

        response = self.client.post("/api/login_standard", json=user_data)
        self.assertEqual(response.status_code, 409)
        self.assertIn("Нельзя войти в несуществующий аккаунт/Неправильно введены данные", response.text)

if __name__ == '__main__':
    # Create a TestSuite and add the desired tests in the desired order
    print(delete_test_user())
    unittest.main()
