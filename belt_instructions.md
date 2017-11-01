# Belt Exam Instruction Updates

First I need a grading scheme to implement

| Error Description                                   | Point Deduction              |
|-----------------------------------------------------|------------------------------|
| route doesn't exist                                 | .5 or .25                    |
| can save but no validations                         | .25                          |
| missing validation message                          | .1 per message (caps to .25) |
| missing redirect                                    | .1                           |
| no welcome message                                  | .1                           |
| fails an assert contains                            | .25                          |
| missing links                                       | .1                           |
| logout: doesn't remove user from session            | .1                           |
| logout: doesn't redirect                            | .1                           |
| missing a "there are no quotes" etc. style message* | .25                          |

```
*need to have a way to check if something is moved from one table to another
```

# Option A Friends

## Routes:
You must use the following routes

| Verb | Route              | Description                                                                                            |
|------|--------------------|--------------------------------------------------------------------------------------------------------|
| Get  | "/"                | display a page containing the registration and login forms                                             |
| Post | "/register"        | allow the user to create a new account, redirects to "/" if errors or "/friends" if successful         |
| Post | "/login"           | allow the user to login to an existing account, redirects to "/" if errors or "/friends" if successful |
| Get  | "/logout"          | remove the user from session and redirect the user to "/"                                              |
| Get  | "/friends"         | welcome the user, contain a table of friends and a table of other users                                |
| Get  | "/user/6"          | show the profile of the user with an id=6                                                              |
| Post | "/user/6/friend"   | add the user with an id=6 to the logged in user's friends list                                         |
| Post | "/user/6/unfriend" | remove the user with an id=6 from the logged in user's friends list                                    |

## Form inputs and validation errors
You must use the following names in your form inputs and display the following validation errors

### Registration Form:

* name

   Name must be 3 characters or longer!

* alias

   Alias must be 3 characters or longer!

* email

   Email is required!<br>
   Invalid email!<br>
   Email already in use!	

* password

   Password must be 8 characters or longer!

* confirm_password

   Confirm Password must match Password!

* date_of_birth

   Date of Birth is required!<br>
   Date of Birth must be in the past!

### Login Form

* email

   Email is required!<br>
   Invalid email!<br>
   Email not found!

* password

   Password must be 8 characters or longer!<br>
   Incorrect Password!

# Option B Quotes

## Routes:
You must use the following routes

| Verb | Route                 | Description                                                                                            |
|------|-----------------------|--------------------------------------------------------------------------------------------------------|
| Get  | "/"                   | display a page containing the registration and login forms                                             |
| Post | "/register"           | allow the user to create a new account, redirects to "/" if errors or "/quotes" if successful          |
| Post | "/login"              | allow the user to login to an existing account, redirects to "/" if errors or "/quotes" if successful  |
| Get  | "/logout"             | remove the user from session and redirect the user to "/"                                              |
| Get  | "/quotes"             | welcome the user, should contain quoteable quotes, favorited quotes, and a quote form                  |
| Post | "/add_quote"          | allow the user to create a quote or display validation errors and redirect back to "/quotes"           |
| Get  | "/user/6"             | show the profile of the user with an id=6                                                              |
| Post | "/quote/6/favorite"   | add a quote to your favorites                                                                          |
| Post | "/quote/6/unfavorite" | remove a quote from your favorites                                                                     |


## Form inputs and validation errors
You must use the following names in your form inputs and display the following validation errors

### Registration Form:

* name

   Name must be 3 characters or longer!

* alias

   Alias must be 3 characters or longer!

* email

   Email is required!<br>
   Invalid email!<br>
   Email already in use!	

* password

   Password must be 8 characters or longer!

* confirm_password

   Confirm Password must match Password!

* date_of_birth

   Date of Birth is required!<br>
   Date of Birth must be in the past!

### Login Form

* email

   Email is required!<br>
   Invalid email!<br>
   Email not found!

* password

   Password must be 8 characters or longer!<br>
   Incorrect Password!

### Quote Form

* quoted_by

   Quoted By must be 3 characters or longer!

* message

   Message must be 10 characters or longer!

# Option C Travel Buddy

## Routes:
You must use the following routes

| Verb | Route                    | Description                                                                                             |
|------|--------------------------|---------------------------------------------------------------------------------------------------------|
| Get  | "/"                      | display a page containing the registration and login forms                                              |
| Post | "/register"              | allow the user to create a new account, redirects to "/" if errors or "/travels" if successful          |
| Post | "/login"                 | allow the user to login to an existing account, redirects to "/" if errors or "/travels" if successful  |
| Get  | "/logout"                | remove the user from session and redirect the user to "/"                                               |
| Get  | "/travels"               | welcome the user, contain a table of user's trips, and a table of all other trips                       |
| Get  | "/travels/add"           | show a form to create a new trip                                                                        |
| Post | "/add_trip"              | allow the user to create a trip or display validation errors and redirect back to "/travels/add"        |
| Get  | "/user/6"                | show the profile of the user with an id=6                                                               |
| Post | "/travels/destination/6" | show trip with the id=6                                                                                 |
| Post | "/travels/join/6"        | add the logged in user to the trip with id-6                                                            |

## Form inputs and validation errors
You must use the following names in your form inputs and display the following validation errors

### Registration Form:

* name

   Name must be 3 characters or longer!

* username

   Username must be 3 characters or longer!<br>
   Username already in use!

* password

   Password must be 8 characters or longer!

* confirm_password

   Confirm Password must match Password!

### Login Form

* username

   Username is required!<br>
   Email not found!

* password

   Password must be 8 characters or longer!<br>
   Incorrect Password!

### Add Trip Form

* destination
   
   Destination is required!

* description
   
   Description is required!

* start_date
   
   Start Date is required!<br>
   Start Date must be in the future!

* end_date

   End Date is required!<br>
   End Date must be in the future!<br>  
   End Date must be after Start Date!

# Option D Appointments

## Routes:
You must use the following routes

| Verb | Route                    | Description                                                                                                                         |
|------|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Get  | "/"                      | display a page containing the registration and login forms                                                                          |
| Post | "/register"              | allow the user to create a new account, redirects to "/" if errors or "/appointments"  if successful                                |
| Post | "/login"                 | allow the user to login to an existing account, redirects to "/" if errors or "/appointments"  if successful                        |
| Get  | "/logout"                | remove the user from session and redirect the user to "/"                                                                           |
| Get  | "/appointments"          | welcome the user, contain a table of the day's appointments, contain a table of the all other appointments, and an appointment form |
| Post | "/add_appointment"       | allow the user to create an appointment or display validation errors and redirect back to "/appointments"                           |
| Get  | "/appointments/6"        | show a form to edit the appointment with an id=6                                                                                    |
| Post | "/appointments/6/update" | allow the user to update the appointment with an id=6 or display validation errors and redirect back to "/appointments/6/update"    |
| Post | "/appointments/6/delete" | allow the user to delete the appointment with an id=6                                                                               |

## Form inputs and validation errors
You must use the following names in your form inputs and display the following validation errors

### Registration Form:

* name

   Name must be 3 characters or longer!

* username

   Username must be 3 characters or longer!<br>
   Username already in use!

* password

   Password must be 8 characters or longer!

* confirm_password

   Confirm Password must match Password!

* date_of_birth

   Date of Birth is required!<br>
   Date of Birth must be in the past!

### Login Form

* username

   Username is required!<br>
   Email not found!

* password

   Password must be 8 characters or longer!<br>
   Incorrect Password!

### Add Appointment Form

* date
   
   Date is required!<br>
   Date must be in the future!

* time
   
   Time is required!<br>
   Appointment with this date and time already exists!

* task

   Task is required!

### Edit Appointment Form	
	
* date
   
   Date is required!<br>
   Date must be in the future!

* time
   
   Time is required!<br>
   Appointment with this date and time already exists!

* task

   Task is required!

*status

# Option E Pokes

## Routes:
You must use the following routes

| Verb | Route       | Description                                                                                                                            |
|------|-------------|----------------------------------------------------------------------------------------------------------------------------------------|
| Get  | "/"         | display a page containing the registration and login forms                                                                             |
| Post | "/register" | allow the user to create a new account, redirects to "/" if errors or "/pokes" if successful                                           |
| Post | "/login"    | allow the user to login to an existing account, redirects to "/" if errors or "/pokes" if successful                                   |
| Get  | "/logout"   | remove the user from session and redirect the user to "/"                                                                              |
| Get  | "/pokes"    | welcome the user, contain a sorted list of the user's poke history, and a table of all users and their pokes and a button to poke them |
| Post | "/poke/6"   | let the logged in user poke the user with an id-6                                                                                      |

## Form inputs and validation errors
You must use the following names in your form inputs and display the following validation errors

### Registration Form:

* name

   Name must be 3 characters or longer!

* alias

   Alias must be 3 characters or longer!

* email

   Email is required!<br>
   Invalid email!<br>
   Email already in use!	

* password

   Password must be 8 characters or longer!

* confirm_password

   Confirm Password must match Password!

* date_of_birth

   Date of Birth is required!<br>
   Date of Birth must be in the past!

### Login Form

* email

   Email is required!<br>
   Invalid email!<br>
   Email not found!

* password

   Password must be 8 characters or longer!<br>
   Incorrect Password!

# Option F Wish List

## Routes:
You must use the following routes

| Verb | Route                  | Description                                                                                                                                        |
|------|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| Get  | "/"                    | display a page containing the registration and login forms                                                                                         |
| Post | "/register"            | allow the user to create a new account, redirects to "/" if errors or "/dashboard" if successful                                                   |
| Post | "/login"               | allow the user to login to an existing account, redirects to "/" if errors or "/dashboard" if successful                                           |
| Get  | "/logout"              | remove the user from session and redirect the user to "/"                                                                                          |
| Get  | "/dashboard"           | welcome the user, contain a table of user's wish list items, and a table of all other wishlist items                                               |
| Get  | "/wish_items/create"   | show a form to create a new wish list item                                                                                                         |
| Post | "/add_wish"            | allow the user to create a wish list item and redirect back to "/dashboard" or display validation errors and redirect back to "/wish_items/create" |
| Get  | "/wish_items/6"        | show wish list item with an id=6                                                                                                                   |
| Post | "/wish_items/6/add"    | add the wish item with an id=6 to the logged in user's to wish list                                                                                |
| Post | "/wish_items/6/remove" | allow the logged in user to remove the wish item with an id=6 from their wish list                                                                 |
| Post | "/wish_items/6/delete" | allow the user to delete an item with an id=6 if that user created it                                                                              |

## Form inputs and validation errors
You must use the following names in your form inputs and display the following validation errors

### Registration Form:

* name

   Name must be 3 characters or longer!

* username

   Username must be 3 characters or longer!<br>
   Username already in use!

* password

   Password must be 8 characters or longer!

* confirm_password

   Confirm Password must match Password!

* date_hired

   Hire Date is required!<br>
   Hire Date must be in the past!

### Login Form

* username

   Username is required!<br>
   Email not found!

* password

   Password must be 8 characters or longer!<br>
   Incorrect Password!

### Add wish list item Form

* product

   Product is required!<br>
   Product must be 3 characters or more!