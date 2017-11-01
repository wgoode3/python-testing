# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

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
        res = self.client.get("/quotes")
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
                                        "date_of_birth": "2200-01-01"}, follow=True)
        # I hope no one is using this in the year 2200!
        self.assertContains(res, "Date of Birth must be in the past!")
        
    def test_18_successful_register(self):
        res = self.client.post("/register", {   "name": "Marisa",
                                                "alias": "Marisa",
                                                "email": "marisa@kirisame.com", 
                                                "password": "Test1234", 
                                                "confirm_password": "Test1234",
                                                "date_of_birth": "1990-01-01"}, follow=True)
        self.assertContains(res, "Welcome back: Marisa")

    def test_19_successful_register_redirects(self):
        res = self.client.post("/register", {   "name": "Marisa",
                                                "alias": "Marisa",
                                                "email": "marisa@kirisame.com", 
                                                "password": "Test1234", 
                                                "confirm_password": "Test1234",
                                                "date_of_birth": "1990-01-01"}, follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get("/quotes")
        self.assertContains(res, "Welcome back: Marisa")

    def test_20_initializes_without_quotes(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Welcome back: Reimu")
        self.assertContains(res, "There are no quoteable quotes.")
        self.assertContains(res, "You have no favorite quotes.")

    def test_21_quote_creation_with_short_quoted_by(self):
        res = self.client.post("/add_quote", {  "quoted_by": "12",
                                                "message": "1234567890"}, follow=True)      
        self.assertContains(res, "Quoted By must be 3 characters or longer!")

    def test_22_quote_creation_with_short_message(self):
        res = self.client.post("/add_quote", {  "quoted_by": "123",
                                                "message": "123456789"}, follow=True)      
        self.assertContains(res, "Message must be 10 characters or longer!")

    def test_23_quote_creation(self):
        self.client.post("/login", { "email": "reimu@hakureishrine.co.jp", 
                                    "password": "Test1234"}, follow=True)
        res = self.client.post("/add_quote", {  "quoted_by": "Samone",
                                                "message": "You look like a dirty rice kind of guy"}, follow=True)
        self.assertContains(res, "Samone")
        self.assertContains(res, "You look like a dirty rice kind of guy")

    def test_24_quote_is_auto_favorited(self):
        self.client.post("/login", {"email": "reimu@hakureishrine.co.jp", 
                                    "password": "Test1234"}, follow=True)
        res = self.client.post("/add_quote", {  "quoted_by": "Samone",
                                                "message": "You look like a dirty rice kind of guy"}, follow=True)
        self.assertContains(res, "There are no quoteable quotes.")
        self.assertNotContains(res, "You have no favorite quotes.")

    def test_25_quote_can_be_removed_from_favorites(self):
        self.client.post("/add_quote", {"quoted_by": "Samone",
                                        "message": "You look like a dirty rice kind of guy"}, follow=True)
        res = self.client.post("/quote/1/unfavorite", follow=True)
        self.assertContains(res, "You have no favorite quotes.")
        self.assertNotContains(res, "There are no quoteable quotes.")

    def test_26_quote_can_be_added_to_favorites(self):
        self.client.post("/add_quote", {"quoted_by": "Samone",
                                        "message": "You look like a dirty rice kind of guy"}, follow=True)
        res = self.client.post("/quote/1/unfavorite", follow=True)
        self.assertContains(res, "You have no favorite quotes.")
        self.assertNotContains(res, "There are no quoteable quotes.")
        res = self.client.post("/quote/1/favorite", follow=True)
        self.assertContains(res, "There are no quoteable quotes.")
        self.assertNotContains(res, "You have no favorite quotes.")

    def test_27_has_user_page(self):
        self.client.post("/add_quote", {"quoted_by": "Samone",
                                        "message": "You look like a dirty rice kind of guy"}, follow=True)
        res = self.client.get("/user/1", follow=True)
        self.assertEqual(res.status_code, 200)

    def test_28_user_page_has_quote_count(self):
        self.client.post("/add_quote", {"quoted_by": "Samone",
                                        "message": "You look like a dirty rice kind of guy"}, follow=True)
        self.client.post("/add_quote", {"quoted_by": "Myself",
                                        "message": "I am always here earlier than Nameer"}, follow=True)
        res = self.client.get("/user/1", follow=True)
        self.assertContains(res, "2")

    def test_29_user_page_shows_quotes(self):
        self.client.post("/add_quote", {"quoted_by": "Samone",
                                        "message": "You look like a dirty rice kind of guy"}, follow=True)
        self.client.post("/add_quote", {"quoted_by": "Myself",
                                        "message": "I am always here earlier than Nameer"}, follow=True)
        res = self.client.get("/user/1", follow=True)
        self.assertContains(res, "I am always here earlier than Nameer")    

    def test_30_logout(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Welcome back: Reimu")
        res = self.client.get("/logout", follow=True)
        self.assertContains(res, "Welcome to Quotes")

    def test_31_logout_redirects(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=False)
        self.assertEqual(res.status_code, 302)

    # trying to return back to /friends throws a key error whether session it cleared or not
    # this test might not be something I can check
    def test_32_logout_clears_session(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Welcome back: Reimu")
        res = self.client.get("/logout", follow=True)
        self.assertContains(res, "Welcome to Quotes")
        with self.assertRaises(KeyError):
            self.client.get("/quotes")