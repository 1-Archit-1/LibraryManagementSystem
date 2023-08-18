
A django rest framework based web api's application .

## Dependencies
This project relies mainly on Django. Mainly:
  - Python 3.8+
  - Django 3+ or 4+
  - Django Rest Framework


  - Required features for a library management system 
  - Proper [JWT][1] based authentication should be implemented in each protected web api endpoint
  - Ensure an user can only perform actions using apis which are allowed to the role assigned to that user

### Scenario
The are two roles in the system; `LIBRARIAN` and `MEMBER`

### As a User
  - I can signup either as `LIBRARIAN` and `MEMBER` using username and password
  - I can login using username/password and get JWT access token

#### As a Librarian
  - I can add, update, and remove Books from the system
  - I can add, update, view, and remove Member from the system
  
#### As a Member
  - I can view, borrow, and return available Books
  - Once a book is borrowed, its status will change to `BORROWED`
  - Once a book is returned, its status will change to `AVAILABLE`
  - I can delete my own account
