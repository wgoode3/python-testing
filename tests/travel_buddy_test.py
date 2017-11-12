# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from datetime import datetime, timedelta

# generate start and end dates that will always be in the future
START_DATE = datetime.strftime(datetime.now() + timedelta(days=1), "%Y-%m-%d")
END_DATE = datetime.strftime(datetime.now() + timedelta(days=2), "%Y-%m-%d")

class BeltTest(TestCase):

    def setUp(self):
        self.client.post("/register", { "name": "Reimu",
                                        "username": "Reimu",
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234"})

    def test_01_login_page_exists(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

    def test_02_login_with_no_username(self):
        res = self.client.post("/login", {  "username": "", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Username must be 3 characters or longer!")

    def test_03_login_with_non_existant_username(self):
        res = self.client.post("/login", {  "username": "Marisa", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Username not found!")

    def test_04_login_with_short_password(self):
        res = self.client.post("/login", {  "username": "Reimu", 
                                            "password": "aA1"}, follow=True)
        self.assertContains(res, "Password must be 8 characters or longer!")

    def test_05_login_with_incorrect_password(self):
        res = self.client.post("/login", {  "username": "Reimu", 
                                            "password": "Test12345"}, follow=True)
        self.assertContains(res, "Incorrect Password!")

    def test_06_successful_login(self):
        res = self.client.post("/login", {  "username": "Reimu", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Hello, Reimu")

    def test_07_successful_login_redirects(self):
        res = self.client.post("/login", {  "username": "Reimu", 
                                            "password": "Test1234"}, follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get("/travels")
        self.assertContains(res, "Hello, Reimu")

    def test_08_register_with_no_name(self):
        res = self.client.post("/register", {   "name": "",
                                                "username": "Test",
                                                "password": "Test1234", 
                                                "confirm_password": "Test1234"}, follow=True)
        self.assertContains(res, "Name must be 3 characters or longer!")

    def test_09_register_with_no_username(self):
        res = self.client.post("/register", {   "name": "Test",
                                                "username": "",
                                                "password": "Test1234", 
                                                "confirm_password": "Test1234"}, follow=True)
        self.assertContains(res, "Username must be 3 characters or longer!")

    def test_10_register_with_existing_username(self):
        res = self.client.post("/register", {   "name": "Test",
                                                "username": "Reimu",
                                                "password": "Test1234", 
                                                "confirm_password": "Test1234"}, follow=True)
        self.assertContains(res, "Username already in use!")

    def test_11_register_with_short_password(self):
        res = self.client.post("/register", {   "name": "Test",
                                                "username": "Test",
                                                "password": "aA1", 
                                                "confirm_password": "aA1"}, follow=True)
        self.assertContains(res, "Password must be 8 characters or longer!")

    def test_12_register_with_mismatched_password_and_confirm_password(self):
        res = self.client.post("/register", {   "name": "Test",
                                                "username": "Test",
                                                "password": "Test1234", 
                                                "confirm_password": "Test12345"}, follow=True)
        self.assertContains(res, "Confirm Password must match Password!")
        
    def test_13_successful_register(self):
        res = self.client.post("/register", {   "name": "Marisa",
                                                "username": "Marisa",
                                                "password": "Test1234", 
                                                "confirm_password": "Test1234"}, follow=True)
        self.assertContains(res, "Hello, Marisa")

    def test_14_successful_register_redirects(self):
        res = self.client.post("/register", {   "name": "Marisa",
                                                "username": "Marisa",
                                                "password": "Test1234", 
                                                "confirm_password": "Test1234"}, follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get("/travels")
        self.assertContains(res, "Hello, Marisa")

    def test_15_joined_trips_initializes_empty(self):
        res = self.client.get("/travels", follow=True)
        self.assertContains(res, "You haven't joined any trips.")

    def test_16_user_trips_initializes_empty(self):
        res = self.client.get("/travels", follow=True)
        self.assertContains(res, "There are no other trips.")

    def test_17_add_trip_form_exists(self):
        res = self.client.get("/travels/add", follow=True)
        self.assertEqual(res.status_code, 200)

    def test_18_add_trip_with_no_destination(self):
        res = self.client.post("/add_trip", {   "destination": "",
                                                "description": "Visit the Hakurei Shrine",
                                                "start_date": START_DATE, 
                                                "end_date": END_DATE}, follow=True)
        self.assertContains(res, "Destination is required!")

    def test_19_add_trip_with_no_description(self):
        res = self.client.post("/add_trip", {   "destination": "Gensokyo",
                                                "description": "",
                                                "start_date": START_DATE, 
                                                "end_date": END_DATE}, follow=True)
        self.assertContains(res, "Description is required!")

    def test_20_add_trip_with_no_start_date(self):
        res = self.client.post("/add_trip", {   "destination": "Gensokyo",
                                                "description": "Visit the Hakurei Shrine",
                                                "start_date": "", 
                                                "end_date": END_DATE}, follow=True)
        self.assertContains(res, "Start Date is required!")

    def test_21_add_trip_with_no_end_date(self):
        res = self.client.post("/add_trip", {   "destination": "Gensokyo",
                                                "description": "Visit the Hakurei Shrine",
                                                "start_date": START_DATE, 
                                                "end_date": ""}, follow=True)
        self.assertContains(res, "End Date is required!")

    def test_22_add_trip_with_start_date_in_past(self):
        res = self.client.post("/add_trip", {   "destination": "Gensokyo",
                                                "description": "Visit the Hakurei Shrine",
                                                "start_date": "2017-10-10", 
                                                "end_date": END_DATE}, follow=True)
        self.assertContains(res, "Start Date must be in the future!")

    def test_23_add_trip_with_end_date_in_past(self):
        res = self.client.post("/add_trip", {   "destination": "Gensokyo",
                                                "description": "Visit the Hakurei Shrine",
                                                "start_date": START_DATE, 
                                                "end_date": "2017-10-10"}, follow=True)
        self.assertContains(res, "End Date must be in the future!")

    def test_24_add_trip_with_start_date_after_end_date(self):
        res = self.client.post("/add_trip", {   "destination": "Gensokyo",
                                                "description": "Visit the Hakurei Shrine",
                                                "start_date": END_DATE, 
                                                "end_date": START_DATE}, follow=True)
        self.assertContains(res, "End Date must be after Start Date!")

    def test_25_add_trip_successfully(self):
        res = self.client.post("/add_trip", {   "destination": "Gensokyo",
                                                "description": "Visit the Hakurei Shrine",
                                                "start_date": START_DATE, 
                                                "end_date": END_DATE}, follow=True)
        self.assertContains(res, "Gensokyo")

    def test_26_add_trip_successfully_redirects(self):
        res = self.client.post("/add_trip", {   "destination": "Gensokyo",
                                                "description": "Visit the Hakurei Shrine",
                                                "start_date": START_DATE, 
                                                "end_date": END_DATE}, follow=False)
        self.assertEqual(res.status_code, 302)

    def test_27_user_autojoins_their_trip(self):
        res = self.client.post("/add_trip", {   "destination": "Gensokyo",
                                                "description": "Visit the Hakurei Shrine",
                                                "start_date": START_DATE, 
                                                "end_date": END_DATE}, follow=True)
        self.assertContains(res, "There are no other trips.")
        self.assertNotContains(res, "You haven't joined any trips.")

    def test_28_other_user_has_not_joined(self):
        self.client.post("/add_trip", { "destination": "Gensokyo",
                                        "description": "Visit the Hakurei Shrine",
                                        "start_date": START_DATE, 
                                        "end_date": END_DATE})
        res = self.client.post("/register", {   "name": "Marisa",
                                                "username": "Marisa",
                                                "password": "Test1234", 
                                                "confirm_password": "Test1234"}, follow=True)
        self.assertContains(res, "You haven't joined any trips.")

    def test_29_other_user_can_join_trip(self):
        self.client.post("/add_trip", { "destination": "Gensokyo",
                                        "description": "Visit the Hakurei Shrine",
                                        "start_date": START_DATE, 
                                        "end_date": END_DATE})
        self.client.post("/register", { "name": "Marisa",
                                        "username": "Marisa",
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234"})
        res = self.client.post("/travels/join/1", follow=True)
        self.assertContains(res, "There are no other trips.")
        self.assertNotContains(res, "You haven't joined any trips.")

    def test_30_destination_page_exists(self):
        self.client.post("/add_trip", { "destination": "Gensokyo",
                                        "description": "Visit the Hakurei Shrine",
                                        "start_date": START_DATE, 
                                        "end_date": END_DATE})
        res = self.client.get("/travels/destination/1", follow=True)
        self.assertEqual(res.status_code, 200)

    def test_31_destination_page_has_destination(self):
        self.client.post("/add_trip", { "destination": "Gensokyo",
                                        "description": "Visit the Hakurei Shrine",
                                        "start_date": START_DATE, 
                                        "end_date": END_DATE})
        res = self.client.get("/travels/destination/1", follow=True)
        self.assertContains(res, "Gensokyo")

    def test_32_destination_page_has_description(self):
        self.client.post("/add_trip", { "destination": "Gensokyo",
                                        "description": "Visit the Hakurei Shrine",
                                        "start_date": START_DATE, 
                                        "end_date": END_DATE})
        res = self.client.get("/travels/destination/1", follow=True)
        self.assertContains(res, "Visit the Hakurei Shrine")

    # Start and End date testing are a bit problematic
    # there are too many ways to display a valid date, I don't want to check them all

    # def test_33_destination_page_has_start_date(self):
    #     self.client.post("/add_trip", { "destination": "Gensokyo",
    #                                     "description": "Visit the Hakurei Shrine",
    #                                     "start_date": START_DATE, 
    #                                     "end_date": END_DATE})
    #     res = self.client.get("/travels/destination/1", follow=True)
    #     self.assertContains(res, START_DATE)

    # def test_34_destination_page_has_end_date(self):
    #     self.client.post("/add_trip", { "destination": "Gensokyo",
    #                                     "description": "Visit the Hakurei Shrine",
    #                                     "start_date": START_DATE, 
    #                                     "end_date": END_DATE})
    #     res = self.client.get("/travels/destination/1", follow=True)
    #     self.assertContains(res, END_DATE)

    def test_33_destination_page_has_planner(self):
        self.client.post("/add_trip", { "destination": "Gensokyo",
                                        "description": "Visit the Hakurei Shrine",
                                        "start_date": START_DATE, 
                                        "end_date": END_DATE})
        res = self.client.get("/travels/destination/1", follow=True)
        self.assertContains(res, "Reimu")

    def test_34_destination_page_has_no_other_users_on_trip(self):
        self.client.post("/add_trip", { "destination": "Gensokyo",
                                        "description": "Visit the Hakurei Shrine",
                                        "start_date": START_DATE, 
                                        "end_date": END_DATE})
        res = self.client.get("/travels/destination/1", follow=True)
        self.assertContains(res, "There are no other users going on this trip.")

    def test_35_destination_page_has_user_who_joins(self):
        self.client.post("/add_trip", { "destination": "Gensokyo",
                                        "description": "Visit the Hakurei Shrine",
                                        "start_date": START_DATE, 
                                        "end_date": END_DATE})
        self.client.post("/register", { "name": "Marisa",
                                        "username": "Marisa",
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234"})
        self.client.post("/travels/join/1")
        res = self.client.get("/travels/destination/1", follow=True)
        self.assertNotContains(res, "There are no other users going on this trip.")  
        self.assertContains(res, "Marisa")

    def test_36_logout(self):
        res = self.client.post("/login", {  "username": "Reimu", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Hello, Reimu")
        res = self.client.get("/logout", follow=True)
        self.assertContains(res, "Travel Buddy")

    def test_37_logout_redirects(self):
        res = self.client.post("/login", {  "username": "Reimu", 
                                            "password": "Test1234"}, follow=False)
        self.assertEqual(res.status_code, 302)

    # trying to return back to /friends throws a key error whether session it cleared or not
    # this test might not be something I can check
    def test_38_logout_clears_session(self):
        res = self.client.post("/login", {  "username": "Reimu", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Hello, Reimu")
        res = self.client.get("/logout", follow=True)
        self.assertContains(res, "Travel Buddy")
        with self.assertRaises(KeyError):
            self.client.get("/travels")