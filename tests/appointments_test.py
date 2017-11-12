# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from datetime import datetime, timedelta

DATE1 = datetime.strftime(datetime.now(), "%Y-%m-%d")
DATE2 = datetime.strftime(datetime.now() - timedelta(days=2), "%Y-%m-%d")
DATE3 = datetime.strftime(datetime.now() + timedelta(days=2), "%Y-%m-%d")
TIME1 = datetime.strftime(datetime.now() + timedelta(minutes=2), "%H:%M")
TIME2 = datetime.strftime(datetime.now() + timedelta(minutes=3), "%H:%M")

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
        self.assertContains(res, "Hello, Reimu!")

    def test_08_successful_login_redirects(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get("/appointments")
        self.assertContains(res, "Hello, Reimu!")

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
                                        "date_of_birth": DATE3}, follow=True)
        self.assertContains(res, "Date of Birth must be in the past!")
        
    def test_18_successful_register(self):
        res = self.client.post("/register", { "name": "Marisa",
                                        "alias": "Marisa",
                                        "email": "marisa@kirisame.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=True)
        self.assertContains(res, "Hello, Marisa!")

    def test_19_successful_register_redirects(self):
        res = self.client.post("/register", { "name": "Marisa",
                                        "alias": "Marisa",
                                        "email": "marisa@kirisame.com", 
                                        "password": "Test1234", 
                                        "confirm_password": "Test1234",
                                        "date_of_birth": "1990-01-01"}, follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get("/appointments")
        self.assertContains(res, "Hello, Marisa!")

    def test_20_tasks_initialize_empty(self):
        res = self.client.get("/appointments")
        self.assertContains(res, "You have no appointments today.")
        self.assertContains(res, "You have no other appointments.")

    def test_21_add_appointment_without_task(self):
        res = self.client.post("/add_appointment", {    "task": "",
                                                        "date": DATE1,
                                                        "time": TIME1}, follow=True)
        self.assertContains(res, "Task is required!")

    def test_22_add_appointment_without_date(self):
        res = self.client.post("/add_appointment", {    "task": "Lunch with Marisa",
                                                        "date": "",
                                                        "time": TIME1}, follow=True)
        self.assertContains(res, "Date is required!")

    def test_23_add_appointment_without_time(self):
        res = self.client.post("/add_appointment", {    "task": "Lunch with Marisa",
                                                        "date": DATE1,
                                                        "time": ""}, follow=True)
        self.assertContains(res, "Time is required!")

    def test_24_add_appointment_with_date_in_past(self):
        res = self.client.post("/add_appointment", {    "task": "Lunch with Marisa",
                                                        "date": DATE2,
                                                        "time": TIME1}, follow=True)
        self.assertContains(res, "Date must be in the future!")

    # capitalization of messages can throw an error, maybe I should use .lower() ?

    def test_25_add_appointment_successfully_for_today(self):
        res = self.client.post("/add_appointment", {    "task": "Lunch with Marisa",
                                                        "date": DATE1,
                                                        "time": TIME1}, follow=True)
        self.assertNotContains(res, "You have no appointments today.")
        self.assertContains(res, "You have no other appointments.")
        self.assertContains(res, "Lunch with Marisa")

    def test_26_add_appointment_successfully_for_another_day(self):
        res = self.client.post("/add_appointment", {    "task": "Lunch with Marisa",
                                                        "date": DATE3,
                                                        "time": TIME1}, follow=True)
        self.assertContains(res, "You have no appointments today.")
        self.assertNotContains(res, "You have no other appointments.")
        self.assertContains(res, "Lunch with Marisa")

    def test_27_add_appointment_with_existing_date_and_time(self):
        res = self.client.post("/add_appointment", {    "task": "Lunch with Marisa",
                                                        "date": DATE1,
                                                        "time": TIME1}, follow=True)
        res = self.client.post("/add_appointment", {    "task": "Something else",
                                                        "date": DATE1,
                                                        "time": TIME1}, follow=True)
        self.assertContains(res, "Appointment with this date and time already exists!")

    def test_28_presence_of_edit_link(self):
        res = self.client.post("/add_appointment", {    "task": "Lunch with Marisa",
                                                        "date": DATE1,
                                                        "time": TIME1}, follow=True)
        self.assertContains(res, "/appointments/1")

    def test_29_edit_page_exists(self):
        self.client.post("/add_appointment", {  "task": "Lunch with Marisa",
                                                "date": DATE1,
                                                "time": TIME1})
        res = self.client.get("/appointments/1", follow=True)
        self.assertEqual(res.status_code, 200)

    def test_30_edit_page_contains_task(self):
        self.client.post("/add_appointment", {  "task": "Lunch with Marisa",
                                                "date": DATE1,
                                                "time": TIME1})
        res = self.client.get("/appointments/1", follow=True)
        self.assertContains(res, "Lunch with Marisa")

    # I can't possibly check for every date/time format that may be in the form
    # unless we make some additional requirements to use input type="date" && type="time" 

    # def test_30_test_edit_page_contains_date(self):
    #     self.client.post("/add_appointment", {  "task": "Lunch with Marisa",
    #                                             "date": DATE1,
    #                                             "time": TIME1})
    #     res = self.client.get("/appointments/1", follow=True)
    #     self.assertContains(res, "Lunch with Marisa")

    # def test_30_test_edit_page_contains_time(self):
    #     self.client.post("/add_appointment", {  "task": "Lunch with Marisa",
    #                                             "date": DATE1,
    #                                             "time": TIME1})
    #     res = self.client.get("/appointments/1", follow=True)
    #     self.assertContains(res, "Lunch with Marisa")

    def test_31_edit_appointment_task_required(self):
        self.client.post("/add_appointment", {  "task": "Lunch with Marisa",
                                                "date": DATE1,
                                                "time": TIME1})
        res = self.client.post("/appointments/1/update", {  "task": "",
                                                            "date": DATE1,
                                                            "time": TIME1,
                                                            "status": "Pending"}, follow=True)
        self.assertContains(res, "Task is required!")

    def test_32_edit_appointment_date_required(self):
        self.client.post("/add_appointment", {  "task": "Lunch with Marisa",
                                                "date": DATE1,
                                                "time": TIME1})
        res = self.client.post("/appointments/1/update", {  "task": "Lunch with Marisa",
                                                            "date": "",
                                                            "time": TIME1,
                                                            "status": "Pending"}, follow=True)
        self.assertContains(res, "Date is required!")

    def test_33_edit_appointment_time_required(self):
        self.client.post("/add_appointment", {  "task": "Lunch with Marisa",
                                                "date": DATE1,
                                                "time": TIME1})
        res = self.client.post("/appointments/1/update", {  "task": "Lunch with Marisa",
                                                            "date": DATE1,
                                                            "time": "",
                                                            "status": "Pending"}, follow=True)
        self.assertContains(res, "Time is required!")

    def test_34_edit_appointment_with_date_in_past(self):
        self.client.post("/add_appointment", {  "task": "Lunch with Marisa",
                                                "date": DATE1,
                                                "time": TIME1})
        res = self.client.post("/appointments/1/update", {  "task": "Lunch with Marisa",
                                                            "date": DATE2,
                                                            "time": TIME1,
                                                            "status": "Pending"}, follow=True)
        self.assertContains(res, "Date must be in the future!")

    def test_35_edit_appointment_with_existing_time_and_date(self):
        self.client.post("/add_appointment", {  "task": "Lunch with Marisa",
                                                "date": DATE1,
                                                "time": TIME1})
        self.client.post("/add_appointment", {  "task": "Tea with Remilia",
                                                "date": DATE1,
                                                "time": TIME2})
        res = self.client.post("/appointments/1/update", {  "task": "Lunch with Marisa",
                                                            "date": DATE1,
                                                            "time": TIME2,
                                                            "status": "Pending"}, follow=True)
        self.assertContains(res, "Appointment with this date and time already exists!")

    def test_36_edit_appointment_successfully(self):
        self.client.post("/add_appointment", {  "task": "Lunch with Marisa",
                                                "date": DATE1,
                                                "time": TIME1})
        res = self.client.post("/appointments/1/update", {  "task": "Lunch with Sanae",
                                                            "date": DATE1,
                                                            "time": TIME1,
                                                            "status": "Done"}, follow=True)
        self.assertContains(res, "Lunch with Sanae")
    
    def test_37_edit_appointment_status_to_done_removes_edit_link(self):
        self.client.post("/add_appointment", {  "task": "Lunch with Marisa",
                                                "date": DATE1,
                                                "time": TIME1})
        res = self.client.post("/appointments/1/update", {  "task": "Lunch with Sanae",
                                                            "date": DATE1,
                                                            "time": TIME1,
                                                            "status": "Done"}, follow=True)
        self.assertNotContains(res, "/appointments/1")

    def test_38_can_delete_appointment(self):
        res = self.client.post("/add_appointment", {    "task": "Lunch with Marisa",
                                                        "date": DATE1,
                                                        "time": TIME1}, follow=True)
        self.assertContains(res, "Lunch with Marisa")
        self.assertNotContains(res, "You have no appointments today.")
        res = self.client.post("/appointments/1/delete", follow=True)
        self.assertNotContains(res, "Lunch with Marisa")
        self.assertContains(res, "You have no appointments today.")

    def test_39_logout(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Hello, Reimu")
        res = self.client.get("/logout", follow=True)
        self.assertContains(res, "Welcome to Appointments")

    def test_40_logout_redirects(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=False)
        self.assertEqual(res.status_code, 302)

    # for some reason this time it passes the logout test, weird
    # this test might not be something I can check
    def test_41_logout_clears_session(self):
        res = self.client.post("/login", {  "email": "reimu@hakureishrine.co.jp", 
                                            "password": "Test1234"}, follow=True)
        self.assertContains(res, "Hello, Reimu")
        res = self.client.get("/logout", follow=True)
        self.assertContains(res, "Welcome to Appointments")
        res = self.client.get("/appointments")
        self.assertEqual(res.status_code, 302)