# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from datetime import datetime, timedelta

FUTURE_DATE = datetime.strftime(datetime.now() + timedelta(days=1), "%Y-%m-%d")

REIMU_REGISTER = {
    "name": "Reimu",
    "alias": "Reimu",
    "email": "reimu@hakureishrine.co.jp", 
    "password": "Test1234", 
    "confirm_password": "Test1234",
    "date_of_birth": "1990-01-01"
}

MARISA_REGISTER = {
    "name": "Marisa",
    "alias": "Marisa",
    "email": "marisa@kirisame.com", 
    "password": "Test1234", 
    "confirm_password": "Test1234",
    "date_of_birth": "1990-01-01"
}

REIMU_LOGIN = {
    "email": "reimu@hakureishrine.co.jp", 
    "password": "Test1234"
}

class BeltTest(TestCase):

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
        self.client.post("/register", REIMU_REGISTER)
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test12345"}, follow=True)
        self.assertContains(res, "Incorrect Password!")

    def test_07_successful_login(self):
        self.client.post("/register", REIMU_REGISTER)
        res = self.client.post("/login", REIMU_LOGIN, follow=True)
        self.assertContains(res, "Hello, Reimu")

    def test_08_successful_login_redirects(self):
        self.client.post("/register", REIMU_REGISTER)
        res = self.client.post("/login", REIMU_LOGIN)
        self.assertEqual(res.status_code, 302)
        res = self.client.get("/dashboard")
        self.assertContains(res, "Hello, Reimu")

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
        self.client.post("/register", REIMU_REGISTER)
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
        res = self.client.post("/register", MARISA_REGISTER, follow=True)
        self.assertContains(res, "Hello, Marisa")

    def test_19_successful_register_redirects(self):
        res = self.client.post("/register", MARISA_REGISTER)
        self.assertEqual(res.status_code, 302)
        res = self.client.get("/dashboard")
        self.assertContains(res, "Hello, Marisa")

    def test_20_logout(self):
        res = self.client.post("/register", REIMU_REGISTER, follow=True)
        self.assertContains(res, "Hello, Reimu")
        res = self.client.get("/logout", follow=True)
        self.assertContains(res, "Welcome to Wish List")

    def test_21_logout_redirects(self):
        self.client.post("/register", REIMU_REGISTER)
        res = self.client.get("/logout")
        self.assertEqual(res.status_code, 302)

    # for some reason this time it passes the logout test, weird
    # this test might not be something I can check
    def test_22_logout_clears_session(self):
        res = self.client.post("/register", REIMU_REGISTER, follow=True)
        self.assertContains(res, "Hello, Reimu")
        res = self.client.get("/logout", follow=True)
        self.assertContains(res, "Welcome to Wish List")
        res = self.client.get("/dashboard")
        self.assertEqual(res.status_code, 302)

    def test_23_your_wish_list_initializes_empty(self):
        res = self.client.post("/register", REIMU_REGISTER, follow=True)
        self.assertContains(res, "You have no items in your wishlist.")

    def test_24_others_wish_list_initializes_empty(self):
        res = self.client.post("/register", REIMU_REGISTER, follow=True)
        self.assertContains(res, "There are no other wish items.")

    def test_25_page_to_create_new_wish_exists(self):
        self.client.post("/register", REIMU_REGISTER)
        res = self.client.get("/wish_items/create", follow=True)
        self.assertEqual(res.status_code, 200)

    def test_26_create_new_wish_without_product(self):
        self.client.post("/register", REIMU_REGISTER)
        res = self.client.post("/add_wish", {"product": ""}, follow=True)
        self.assertContains(res, "Product is required!")

    def test_27_create_new_wish_with_too_short_product(self):
        self.client.post("/register", REIMU_REGISTER)
        res = self.client.post("/add_wish", {"product": "CD"}, follow=True)
        self.assertContains(res, "Product must be 3 characters or more!")

    def test_28_successfully_create_new_wish(self):
        self.client.post("/register", REIMU_REGISTER)
        res = self.client.post("/add_wish", {"product": "broom"}, follow=True)
        self.assertContains(res, "broom")

    def test_29_create_new_wish_adds_wish_to_users_wish_list(self):
        self.client.post("/register", REIMU_REGISTER)
        res = self.client.post("/add_wish", {"product": "broom"}, follow=True)
        self.assertNotContains(res, "You have no items in your wishlist.")
        self.assertContains(res, "There are no other wish items.")

    def test_30_other_user_does_not_wish_for_item(self):
        self.client.post("/register", REIMU_REGISTER)
        self.client.post("/add_wish", {"product": "broom"})
        res = self.client.post("/register", MARISA_REGISTER, follow=True)
        self.assertContains(res, "You have no items in your wishlist.")
        self.assertNotContains(res, "There are no other wish items.")

    def test_31_add_item_to_wishlist_link_exists(self):
        self.client.post("/register", REIMU_REGISTER)
        self.client.post("/add_wish", {"product": "broom"})
        res = self.client.post("/register", MARISA_REGISTER, follow=True)
        self.assertContains(res, "wish_items/1/add")

    def test_32_add_item_to_wishlist(self):
        self.client.post("/register", REIMU_REGISTER)
        self.client.post("/add_wish", {"product": "broom"})
        self.client.post("/register", MARISA_REGISTER)
        res = self.client.post("/wish_items/1/add", follow=True)
        self.assertNotContains(res, "You have no items in your wishlist.")
        self.assertContains(res, "There are no other wish items.")

    def test_33_remove_item_from_wishlist_link_exists(self):
        self.client.post("/register", REIMU_REGISTER)
        self.client.post("/add_wish", {"product": "broom"})
        self.client.post("/register", MARISA_REGISTER)
        res = self.client.post("/wish_items/1/add", follow=True)
        self.assertContains(res, "wish_items/1/remove")

    def test_34_remove_item_from_wishlist(self):
        self.client.post("/register", REIMU_REGISTER)
        self.client.post("/add_wish", {"product": "broom"})
        self.client.post("/register", MARISA_REGISTER)
        self.client.post("/wish_items/1/add")
        res = self.client.post("/wish_items/1/remove", follow=True)
        self.assertContains(res, "You have no items in your wishlist.")
        self.assertNotContains(res, "There are no other wish items.")

    def test_34_remove_item_from_wishlist_does_not_remove_for_others(self):
        self.client.post("/register", REIMU_REGISTER)
        self.client.post("/add_wish", {"product": "broom"})
        self.client.post("/register", MARISA_REGISTER)
        self.client.post("/wish_items/1/add")
        self.client.post("/wish_items/1/remove")
        res = self.client.post("/login", REIMU_LOGIN, follow=True)
        self.assertNotContains(res, "You have no items in your wishlist.")
        self.assertContains(res, "There are no other wish items.")

    def test_36_delete_item_from_wishlist_link_exists(self):
        self.client.post("/register", REIMU_REGISTER)
        res = self.client.post("/add_wish", {"product": "broom"}, follow=True)
        self.assertContains(res, "wish_items/1/delete")
        self.assertNotContains(res, "wish_items/1/remove")

    def test_37_delete_item_from_wishlist_deletes_item(self):
        self.client.post("/register", REIMU_REGISTER)
        self.client.post("/add_wish", {"product": "broom"})
        res = self.client.post("/wish_items/1/delete", follow=True)
        self.assertContains(res, "You have no items in your wishlist.")
        self.assertContains(res, "There are no other wish items.")

    def test_38_item_page_exists(self):
        self.client.post("/register", REIMU_REGISTER)
        self.client.post("/add_wish", {"product": "broom"})
        res = self.client.get("/wish_items/1", follow=True)
        self.assertEqual(res.status_code, 200)

    def test_39_item_page_has_product_name(self):
        self.client.post("/register", REIMU_REGISTER)
        self.client.post("/add_wish", {"product": "broom"})
        res = self.client.get("/wish_items/1", follow=True)
        self.assertContains(res, "broom")

    def test_40_item_page_has_wishing_users_names(self):
        self.client.post("/register", REIMU_REGISTER)
        self.client.post("/add_wish", {"product": "broom"})
        self.client.post("/register", MARISA_REGISTER)
        self.client.post("/wish_items/1/add")
        res = self.client.get("/wish_items/1", follow=True)
        self.assertContains(res, "Reimu")
        self.assertContains(res, "Marisa")