# Back-End Capstone - Game Night Database

## Project Description

This is a database for users to store information about their boardgames, loan them out or borrow others, and schedule events , like a game night, for others to attend.

## Features

### User

- Login with email and password
- Add and edit their address
- Create and Edit boardgame records they own
- View boardgame records, including ones owned by other users, and associated ratings and categories,
- Create and edit events they are hosting
- View other events posted
- View and edit their own information
- Loan and borrow boardgames

### Admin

- All capabilities of Users
- View all address records
- Edit details for any boardgame record
- Create and edit categories and ratings
- View all Users, and specific User information
- Activate and Deactivate Users

### Super Admin

- All capabilities of Users and Admins
- Edit a Users address
- Delete any record or User

## Installation

1. Clone repository

2. Install Dependencies

3. Environment Setup

## Tables

### Auth

| Route   | Method | Role Access | Route Function              |
| ------- | ------ | ----------- | --------------------------- |
| /login  | POST   |             | add auth_token on login     |
| /logout | DELETE |             | delete auth_token on logout |

### Users

| Route            | Method | Role Access   | Route Function                                                                                                     |
| ---------------- | ------ | ------------- | ------------------------------------------------------------------------------------------------------------------ |
| /user            | POST   | Admin , Super | Create a User. Admins can create basic users. Super Admins can create Admins.                                      |
| /users           | GET    | Admin         | View all Users. Admin+ required.                                                                                   |
| /users/active    | GET    | Admin         | View all Active Users. Admin+ required.                                                                            |
| /user/profile    | GET    | Owner , User  | Allows a User to view their own information.                                                                       |
| /user/<user_id>  | GET    | Admin , User  | View a specific User record. Users can see name and email. Admins can see additional information.                  |
| /user/<user_id>  | PUT    | Owner , Super | Update information on a User’s record. Users can update their own record. Super Admins can update any User record. |
| /user/activation | PUT    | Admin         | Activate or deactivate a user account. Admin+ required                                                             |
| /user/delete     | DELETE | Super         | Deactivate a User. Super Admin required.                                                                           |

### Addresses

| Route                 | Method | Role Access   | Route Function                                                                                            |
| --------------------- | ------ | ------------- | --------------------------------------------------------------------------------------------------------- |
| /address              | POST   | User          | Create a new address record. Adds address to user if user’s address is null.                              |
| /addresses            | GET    | Admin         | View all address records. Admin+ required                                                                 |
| /address/<address_id> | GET    | User          | View an address record.                                                                                   |
| /address/<address_id> | PUT    | Owner , Super | Update an address record. Super Admins can update any user’s address. Users can update their own address. |
| /address/delete       | DELETE | Super         | Delete an address record. Super Admin required                                                            |

### Events

| Route             | Method | Role Access   | Route Function                                        |
| ----------------- | ------ | ------------- | ----------------------------------------------------- |
| /event            | POST   | User          | Create an Event record.                               |
| /events           | GET    | User          | View all Events                                       |
| /event/<date>     | GET    | User          | View all listed Events happening on a specific date.  |
| /event/<event_id> | GET    | User          | View an Event by specific id.                         |
| /event/<event_id> | PUT    | Admin , Owner | Update an Event. Host or Admin+ required              |
| /event/delete     | DELETE | Super         | Remove an Event record. Host or Super Admin required. |

### Categories

| Route                   | Method | Role Access | Route Function                                           |
| ----------------------- | ------ | ----------- | -------------------------------------------------------- |
| /category               | POST   | Admin       | Create a New Category record. Admin+ required            |
| /categories             | GET    | User        | View list of Categories and their associated Board Games |
| /category/<category_id> | GET    | User        | View a category by specific id                           |
| /category/<category_id> | PUT    | Admin       | Update a Category record by id. Admin+ required          |
| /category/delete        | DELETE | Super       | Delete a Category Record. Super Admin required.          |

### BGG Ratings

| Route                  | Method | Role Access | Route Function                                     |
| ---------------------- | ------ | ----------- | -------------------------------------------------- |
| /rating                | POST   | Admin       | Create a Rating Record for a game. Admin+ required |
| /ratings               | GET    | User        | View all Rating records.                           |
| /rating/game/<game_id> | GET    | User        | View a Rating for specific game by the game id.    |
| /rating/<rating_id>    | GET    | User        | View a specific Rating by Id.                      |
| /rating/<rating_id>    | PUT    | Admin       | Update a Rating record by id. Admin+ required.     |
| /rating/delete         | DELETE | Super       | Delete a Rating record. Super Admin required.      |

### Board Games

| Route                             | Method | Role Access   | Route Function                                                                                  |
| --------------------------------- | ------ | ------------- | ----------------------------------------------------------------------------------------------- |
| /boardgame                        | POST   | User          | Create a new Board Game record.                                                                 |
| /boardgames                       | GET    | User          | View listed Board Games                                                                         |
| /boardgame/age/<age_range>        | GET    | User          | View listed Board Games by age. Cannot view games with an age range higher than user’s age.     |
| /boardgame/players/<player_count> | GET    | User          | View listed Board Games by player count.                                                        |
| /boardgame/owner/<user_id>        | GET    | User          | View Board Games an owned by a User.                                                            |
| /boardgame/<boardgame_id>         | GET    | User          | View a Board Game record.                                                                       |
| /boardgame/<boardgame_id>         | PUT    | Admin , Owner | Update a Board Game record. Admins can update any record. Users can only update games they own. |
| /boardgame/delete                 | DELETE | Super         | Delete a Board Game record. Super Admin required.                                               |

### Game Loans

| Route                          | Method | Role Access   | Route Function                                                                                                                                        |
| ------------------------------ | ------ | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| /gameloan                      | POST   | Admin , Owner | Create a Game Loan record. Updates borrowed game’s availability field to False. Boardgame owner or Admin+ required.                                   |
| /gameloans                     | GET    | Admin         | View all loan records. Admin+ required.                                                                                                               |
| /gameloans/<borrower_id>       | GET    | Admin , Owner | Allows specific user to view all games they are borrowing. Allows an Admin to view all Loan records a specific user has. Borrower or Admin+ required. |
| /gameloans/boardgame/<game_id> | GET    | Admin , Owner | View Loan record for a specific game. Game owner or Admin+ required.                                                                                  |
| /gameloan/<loan_id>            | GET    | Admin , Owner | View a Loan record by specific id. Game Owner, Borrower, or Admin+ required.                                                                          |
| /gameloan/<loan_id>            | PUT    | Admin , Owner | Update a Loan record. Game Owner or Admin+ required. Updating the date_returned field updates the borrowed game’s availability field to True          |
| /gameloan/return/<loan_id>     | PUT    | Admin , Owner | Sets the date_returned field, and updates the borrowed game’s available field to True. BoardGame owner or admin+ required.                            |
| /gameloan/delete               | DELETE | Super         | Remove a loan record. Super Admin required.                                                                                                           |

### Example Data

## What I learned ths Semester

The thing that stood out the most from what I learned would be Schemas. They were something intimidating at first. After a little experimention though, and a few builds I got the hang of them. I like that you can control what information a model sends through the use of multiple schemas. And that they take advantive of inheritance.

I also learned that consistency goes a long way. This semester was jam packed with additional responsabilities outside of this course. Having to juggle school, work, My Story Matters, health issues, and kids really leaves you with little time for anything, especially homework. However, I found that I could still get these big projects done when consistently following the schedule I layed out for myself. I just kept making babysteps and then all of a sudden we're here at the end.

## Favorite Part of Class

It's hard for me to pick favorites. I really enjoyed going through the SQL Queries with SQLZoo, and building databases like the Jedi Academy Training and the Fellowship database. Working in python again was great too. I think my favorite part of this though is walking away with the ability to build my own database and backend. I can go make my own apps now. I can take an idea and turn it into something and see it through start to finish.
