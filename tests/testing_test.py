from django.test import TestCase

class UserTest(TestCase):

	def setUp(self):
		self.client.post("/register", { "username": "reimu",
										"email": "reimu@hakureishrine.co.jp", 
										"password": "Test1234", 
										"confirm_password": "Test1234"})

	def test_login_screen_exists(self):
		res = self.client.get("/")
		self.assertContains(res, "Welcome to Messages")

	def test_register_with_errors(self):
		res = self.client.post("/register", {	"username": "", 
												"email": "", 
												"password": "", 
												"confirm_password": ""}, follow=True)
		self.assertContains(res, "Username is required!")
		self.assertContains(res, "Email is required!")
		self.assertContains(res, "Password is required!")
		self.assertContains(res, "Confirm password is required!")
		res = self.client.post("/register", {	"username": "a", 
												"email": "a", 
												"password": "a", 
												"confirm_password": "b"}, follow=True)
		self.assertContains(res, "Username must be 3 characters or more!")
		self.assertContains(res, "Invalid Email!")
		self.assertContains(res, "Password must contain at least 1 number and capitalization!")
		self.assertContains(res, "Password must match Confirm password!")

	def test_login_with_errors(self):
		res = self.client.post("/login", {	"email": "", 
											"password": ""}, follow=True)
		self.assertContains(res, "Email is required!")
		self.assertContains(res, "Password is required!")
		res = self.client.post("/login", {	"email": "a", 
											"password": "a"}, follow=True)
		self.assertContains(res, "Invalid Email!")
		self.assertContains(res, "Password must contain at least 1 number and capitalization!")
		res = self.client.post("/login", {	"email": "a@a.a", 
											"password": "Abcd1234"}, follow=True)
		self.assertContains(res, "Email not found!")
		res = self.client.post("/login", {	"email": "reimu@hakureishrine.co.jp", 
											"password": "Abcd1234"}, follow=True)
		self.assertContains(res, "Incorrect Password!")

	def test_successful_login(self):
		res = self.client.post("/login", {	"email": "reimu@hakureishrine.co.jp", 
											"password": "Test1234"}, follow=True)
		self.assertContains(res, "New Message")

	def test_successful_register(self):
		res = self.client.post("/register", { 	"username": "marisa",
												"email": "marisa@kirisame.co.jp", 
												"password": "Test1234", 
												"confirm_password": "Test1234"}, follow=True)
		self.assertContains(res, "New Message")
		self.assertContains(res, "reimu")