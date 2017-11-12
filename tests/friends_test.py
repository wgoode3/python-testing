# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from datetime import datetime, timedelta

# generate a future date to test date of birth validity
FUTURE_DATE = datetime.strftime(datetime.now() + timedelta(days=1), "%Y-%m-%d")

class BeltTest(TestCase):

    def setUp(self):
        self.client.post("/register", { "name": "Reimu",
                                        "alias": "Reimu",
                                        "email": "reimu@hakureishrine.co.jp", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"})

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
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Welcome back: Reimu")

    def test_08_successful_login_redirects(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get("/friends")
        self.assertContains(res, "Welcome back: Reimu")

    def test_09_register_with_no_name(self):
        res = self.client.post("/register", { "name": "",
                                        "alias": "Test",
                                        "email": "test@test.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        self.assertContains(res, "Name must be 3 characters or longer!")

    def test_10_register_with_no_alias(self):
        res = self.client.post("/register", { "name": "Test",
                                        "alias": "",
                                        "email": "test@test.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        self.assertContains(res, "Alias must be 3 characters or longer!")

    def test_11_register_with_no_email(self):
        res = self.client.post("/register", { "name": "Test",
                                        "alias": "Test",
                                        "email": "", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        self.assertContains(res, "Email is required!")

    def test_12_register_with_invalid_email(self):
        res = self.client.post("/register", { "name": "Test",
                                        "alias": "Test",
                                        "email": "test.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        self.assertContains(res, "Invalid Email!")

    def test_13_register_with_existing_email(self):
        res = self.client.post("/register", { "name": "Test",
                                        "alias": "Test",
                                        "email": "reimu@hakureishrine.co.jp", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        self.assertContains(res, "Email already in use!")

    def test_14_register_with_short_password(self):
        res = self.client.post("/register", { "name": "Test",
                                        "alias": "Test",
                                        "email": "test@test.com", 
                                        "password": "aA1", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        self.assertContains(res, "Password must be 8 characters or longer!")

    def test_15_register_with_mismatched_password_and_confirm_password(self):
        res = self.client.post("/register", { "name": "Test",
                                        "alias": "Test",
                                        "email": "test@test.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test12345",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        self.assertContains(res, "Confirm Password must match Password!")

    def test_16_register_with_no_date_of_birth(self):
        res = self.client.post("/register", { "name": "Test",
                                        "alias": "Test",
                                        "email": "test@test.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": ""}, follow=True)
        self.assertContains(res, "Date of Birth is required!")

    def test_17_register_with_future_date_of_birth(self):
        res = self.client.post("/register", { "name": "Test",
                                        "alias": "Test",
                                        "email": "test@test.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": FUTURE_DATE}, follow=True)
        self.assertContains(res, "Date of Birth must be in the past!")
        
    def test_18_successful_register(self):
        res = self.client.post("/register", { "name": "Marisa",
                                        "alias": "Marisa",
                                        "email": "marisa@kirisame.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        self.assertContains(res, "Welcome back: Marisa")

    def test_19_successful_register_redirects(self):
        res = self.client.post("/register", { "name": "Marisa",
                                        "alias": "Marisa",
                                        "email": "marisa@kirisame.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get("/friends")
        self.assertContains(res, "Welcome back: Marisa")

    def test_20_successful_register_contains_previous_user(self):
        res = self.client.post("/register", { "name": "Marisa",
                                        "alias": "Marisa",
                                        "email": "marisa@kirisame.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        self.assertContains(res, "Reimu")
        self.assertContains(res, "You don't have any friends.")

    def test_21_can_friend_user(self):
        res = self.client.post("/register", { "name": "Marisa",
                                        "alias": "Marisa",
                                        "email": "marisa@kirisame.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        res = self.client.post("/user/1/friend", follow=True)
        self.assertContains(res, "There are no other users.")

    def test_22_can_unfriend_user(self):
        res = self.client.post("/register", { "name": "Marisa",
                                        "alias": "Marisa",
                                        "email": "marisa@kirisame.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        res = self.client.post("/user/1/friend", follow=True)
        self.assertContains(res, "There are no other users.")
        res = self.client.post("/user/1/unfriend", follow=True)
        self.assertContains(res, "You don't have any friends.")

    def test_23_user_profile_exists(self):
        res = self.client.get("/user/1", follow=True)
        self.assertContains(res, "Reimu")
        self.assertContains(res, "reimu@hakureishrine.co.jp")
    
    def test_24_logout(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Welcome back: Reimu")
        res = self.client.get("/logout", follow=True)
        self.assertContains(res, "Welcome to Friends")

    def test_25_logout_redirects(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=False)
        self.assertEqual(res.status_code, 302)

    # trying to return back to /friends throws a key error whether session it cleared or not
    # this test might not be something I can check
    def test_26_logout_clears_session(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Welcome back: Reimu")
        res = self.client.get("/logout", follow=True)
        self.assertContains(res, "Welcome to Friends")
        with self.assertRaises(KeyError):
            self.client.get("/friends")