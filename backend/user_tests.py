import unittest
from fastapi.testclient import TestClient

from handlers import delete_test_user
from main import get_application


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
            self.assertIn("id", user)
            self.assertIn("isadmin", user)
            self.assertIn("iscurator", user)
            self.assertIn("email", user)
            self.assertIn("fio", user)
            self.assertIn("username", user)
            self.assertIn("isteacher", user)
            self.assertIn("date_of_add", user)


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
            self.assertIn("id", team)
            self.assertIn("name", team)

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

        self.assertTrue(type(response.json()["speciality"]), str)
        self.assertTrue(type(response.json()["id"]), int)
        self.assertTrue(type(response.json()["email"]), str)
        self.assertTrue(type(response.json()["date_of_add"]), str)
        self.assertTrue(type(response.json()["name"]), str)


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
