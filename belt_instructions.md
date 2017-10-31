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
   Incorrect Password

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
   Incorrect Password

### Quote Form

* quote

   Quote must be 3 characters or longer!

* message

   Message must be 10 characters or longer!