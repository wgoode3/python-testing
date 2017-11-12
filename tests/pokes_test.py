# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from datetime import datetime, timedelta

# generate a future date to test date of birth validity
FUTURE_DATE = datetime.strftime(datetime.now() + timedelta(days=1), "%Y-%m-%d")

VALID_REGISTER = {
    "name": "Marisa",
    "alias": "Marisa",
    "email": "marisa@kirisame.com", 
    "password": "Test1234", 
    "confirm_password": "Test1234",
    "date_of_birth": "1990-01-01"
}

VALID_LOGIN = {
    "email": "reimu@hakureishrine.co.jp", 
    "password": "Test1234"
}

class BeltTest(TestCase):

    def setUp(self):
        self.client.post("/register", {
            "name": "Reimu",
            "alias": "Reimu",
            "email": "reimu@hakureishrine.co.jp", 
            "password": "Test1234", 
            "confirm_password": "Test1234",
            "date_of_birth": "1990-01-01"
        })

    def test_01_login_page_exists(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

    def test_02_login_with_no_email(self):
        res = self.client.post("/login", {  "email": "", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Email is required!")

    def test_03_login_with_invalid_email(self):
        res = self.client.post("/login", {  "email": "test.com", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Invalid email!")

    def test_04_login_with_non_existant_email(self):
        res = self.client.post("/login", {  "email": "example@example.com", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Email not found!")

    def test_05_login_with_short_password(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "aA1"}, follow=True)
        self.assertContains(res, "Password must be 8 characters or longer!")

    def test_06_login_with_incorrect_password(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test12345"}, follow=True)
        self.assertContains(res, "Incorrect Password!")

    def test_07_successful_login(self):
        res = self.client.post("/login", VALID_LOGIN, follow=True)
        self.assertContains(res, "Welcome, Reimu")

    def test_08_successful_login_redirects(self):
        res = self.client.post("/login", VALID_LOGIN, follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get("/pokes")
        self.assertContains(res, "Welcome, Reimu")

    def test_09_register_with_no_name(self):
        res = self.client.post("/register", { 
            "name": "",
            "alias": "Test",
            "email": "test@test.com", 
            "password": "Test1234", 
            "confirm_password": "Test1234",
            "date_of_birth": "1990-01-01"
        }, follow=True)
        self.assertContains(res, "Name must be 3 characters or longer!")

    def test_10_register_with_no_alias(self):
        res = self.client.post("/register", { 
            "name": "Test",
            "alias": "",
            "email": "test@test.com", 
            "password": "Test1234", 
            "confirm_password": "Test1234",
            "date_of_birth": "1990-01-01"
        }, follow=True)
        self.assertContains(res, "Alias must be 3 characters or longer!")

    def test_11_register_with_no_email(self):
        res = self.client.post("/register", { 
            "name": "Test",
            "alias": "Test",
            "email": "", 
            "password": "Test1234", 
            "confirm_password": "Test1234",
            "date_of_birth": "1990-01-01"
        }, follow=True)
        self.assertContains(res, "Email is required!")

    def test_12_register_with_invalid_email(self):
        res = self.client.post("/register", { 
            "name": "Test",
            "alias": "Test",
            "email": "test.com", 
            "password": "Test1234", 
            "confirm_password": "Test1234",
            "date_of_birth": "1990-01-01"
        }, follow=True)
        self.assertContains(res, "Invalid Email!")

    def test_13_register_with_existing_email(self):
        res = self.client.post("/register", { 
            "name": "Test",
            "alias": "Test",
            "email": "reimu@hakureishrine.co.jp", 
            "password": "Test1234", 
            "confirm_password": "Test1234",
            "date_of_birth": "1990-01-01"
        }, follow=True)
        self.assertContains(res, "Email already in use!")

    def test_14_register_with_short_password(self):
        res = self.client.post("/register", { 
            "name": "Test",
            "alias": "Test",
            "email": "test@test.com", 
            "password": "aA1", 
            "confirm_password": "Test1234",
            "date_of_birth": "1990-01-01"
        }, follow=True)
        self.assertContains(res, "Password must be 8 characters or longer!")

    def test_15_register_with_mismatched_password_and_confirm_password(self):
        res = self.client.post("/register", { 
            "name": "Test",
            "alias": "Test",
            "email": "test@test.com", 
            "password": "Test1234", 
            "confirm_password": "Test12345",
            "date_of_birth": "1990-01-01"
        }, follow=True)
        self.assertContains(res, "Confirm Password must match Password!")

    def test_16_register_with_no_date_of_birth(self):
        res = self.client.post("/register", { 
            "name": "Test",
            "alias": "Test",
            "email": "test@test.com", 
            "password": "Test1234", 
            "confirm_password": "Test1234",
            "date_of_birth": ""
        }, follow=True)
        self.assertContains(res, "Date of Birth is required!")

    def test_17_register_with_future_date_of_birth(self):
        res = self.client.post("/register", { 
            "name": "Test",
            "alias": "Test",
            "email": "test@test.com", 
            "password": "Test1234", 
            "confirm_password": "Test1234",
            "date_of_birth": FUTURE_DATE
        }, follow=True)
        self.assertContains(res, "Date of Birth must be in the past!")
        
    def test_18_successful_register(self):
        res = self.client.post("/register", VALID_REGISTER, follow=True)
        self.assertContains(res, "Welcome, Marisa")

    def test_19_successful_register_redirects(self):
        res = self.client.post("/register", VALID_REGISTER, follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get("/pokes")
        self.assertContains(res, "Welcome, Marisa")

    def test_20_poke_history_initializes_empty(self):
        res = self.client.get("/pokes")
        self.assertContains(res, "You have no pokes")
        self.assertContains(res, "0 people have poked you")

    def test_21_other_users_initializes_empty(self):
        res = self.client.get("/pokes")
        self.assertContains(res, "There are no other users")

    def test_22_new_user_can_see_other_user(self):
        res = self.client.post("/register", VALID_REGISTER, follow=True)
        self.assertNotContains(res, "There are no other users")
        self.assertContains(res, "Reimu")

    def test_23_new_user_can_see_poke_link(self):
        res = self.client.post("/register", VALID_REGISTER, follow=True)
        self.assertContains(res, "/poke/1")

    # this could match the csrf token as well so I'll add 11 pokes to make it less likely
    # If I do this a lot I should add this to the setUp
    def test_24_can_poke_user(self):
        self.client.post("/register", VALID_REGISTER)
        for _ in xrange(10):
            self.client.post("/poke/1")
        res = self.client.post("/poke/1", follow=True)
        self.assertContains(res, "11")

    def test_25_poked_user_sees_pokes(self):
        self.client.post("/register", VALID_REGISTER)
        for _ in xrange(12):
            self.client.post("/poke/1")
        res = self.client.post("/login", VALID_LOGIN, follow=True)
        self.assertContains(res, "1 people have poked you")
        self.assertNotContains(res, "You have no pokes")
        self.assertContains(res, "12")

    def test_26_poke_history_in_descending_order(self):
        self.client.post("/register", VALID_REGISTER)
        for _ in xrange(3):
            self.client.post("/poke/1")
        self.client.post("/register", {
            "name": "Momiji",
            "alias": "Momiji",
            "email": "momiji@gensokyo.co.jp", 
            "password": "Test1234", 
            "confirm_password": "Test1234",
            "date_of_birth": "1990-01-01"
        })
        for _ in xrange(5):
            self.client.post("/poke/1")
        res = self.client.post("/login", VALID_LOGIN, follow=True)
        marisa_index = str(res).find("Marisa")
        momiji_index = str(res).find("Momiji")
        # checks for both Marisa and Momiji in the response
        # and that Momiji appears before Marisa
        self.assertTrue(momiji_index > 0 and marisa_index > momiji_index)

    def test_27_logout(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Welcome, Reimu")
        res = self.client.get("/logout", follow=True)
        self.assertContains(res, "Welcome to Pokes")

    def test_28_logout_redirects(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=False)
        self.assertEqual(res.status_code, 302)

    def test_29_logout_clears_session(self):
        self.client.post("/login", {"email": "reimu@hakureishrine.co.jp", 
                                    "password": "Test1234"})
        self.client.get("/logout")
        res = self.client.get("/pokes")
        # print res.status_code
        self.assertEqual(res.status_code, 302)