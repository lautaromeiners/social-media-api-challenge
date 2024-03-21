# Social Media API Challenge
Designs and implement a Django API for a social media platform that allows users to create posts, follow other users, and comment on posts.

The API should includes the following models:
  * User: Represents a user on the platform. Include fields for username, email, password, and followers/following relationships.
  * Post: Represents a user's post. Include fields for the author (foreign key to User model), content, and timestamps (date created).
  * Comment: Represents a comment on a post. Include fields for the author (foreign key to User model), post (foreign key to Post model), and content.
    
And implements the following endpoints:
  * GET /api/users/: Retrieve a list of all users.
  * GET /api/users/{id}/: Retrieve details of a specific user. Including number of total posts, number of total comments, followers and following.
  * POST /api/users/{id}/follow/{id}/: Set first id user as follower of second id user.
  * POST /api/users/{id}/unfollow/{id}/: Set first id user to unfollow second id user.
  * POST /api/users/create/: Create a new user.
  * GET /api/posts/: Retrieve a list of all posts ordered from newest to oldest from all users, with pagination and filters. Implemented filters are: author_id, from_date, to_date.
  * GET /api/posts/{id}/: Retrieve details of a specific post with it's last three comments included and the information of it's creator.
  * POST /api/posts/: Create a new post.
  * GET /api/posts/{id}/comments/: Retrieve all comments for a specific post.
  * POST /api/posts/{id}/comments/: Add a new comment to a post.

# Installation Instructions

After cloning the repository the first step for installation is creating a virtual environment.

```
python3.8 -m venv venv
```

And activate it

```
source venv/bin/activate
```

Once we've got the virtual environment activated we have to install the required dependencies. For this project I'm using pip, so the command to run is

```
pip install -r requirements.txt
```

With the dependencies installed, what's left to do is run migrations.

```
python manage.py migrate
```

With this step done we are ready to run our server.

```
python manage.py runserver
```

Or we can run the tests to make sure that everything works correctly

```
python manage.py test
```

# API Usage

After we have our API installed we can go ahead and start using it. Below I will leave some cURL commands to test the API.

As I implemented Token based authentication the first thing we need to do is to create a User and grab that token that we will use in subsequent calls to the API.

```
curl -X POST \
  http://localhost:8000/api/users/create/ \
  -H 'Content-Type: application/json'   -d '{"username": "test", "email": "test@example.com", "password": "secretpassword"}'
```

Of course you can use whatever username, email and password you want. So once we get the token we will paste it in the header on subsequent API calls. All the other endpoints require authentication.

Here's a complete list of cURL commands for the previously stated supported endpoints.

```
curl -X GET \
  http://localhost:8000/api/users/ \
  -H 'Authorization: Token {token}'

curl -X GET \
  http://localhost:8000/api/users/{id}/ \
  -H 'Authorization: Token {token}'

curl -X POST \
  http://localhost:8000/api/users/{id}/follow/{id}/ \
  -H 'Authorization: Token {token}'
  
curl -X POST \
  http://localhost:8000/api/users/{id}/unfollow/{id}/ \
  -H 'Authorization: Token {token}'

curl http://localhost:8000/api/posts/ \
  -G \
  -H "Authorization: Token {token}"

curl http://localhost:8000/api/posts/?author_id={id} \
  -G \
  -H "Authorization: Token {token}"
  
curl http://localhost:8000/api/posts/?from_date={from_date YYYY-MM-DD format}\
  -G \
  -H "Authorization: Token {token}"

curl http://localhost:8000/api/posts/?to_date={to_date YYYY-MM-DD format} \
  -G \
  -H "Authorization: Token {token}"
 
curl http://localhost:8000/api/posts/{id}/ \
  -H "Authorization: Token {token}"

curl http://localhost:8000/api/posts/{id}/comments/ \
  -X POST \
  -H "Authorization: Token {token}" \
  -H "Content-Type: application/json" \
  -d '{"content": "This is a new comment"}'
  
curl http://localhost:8000/api/posts/{id}/comments/ \
  -G \
  -H "Authorization: Token {token}"
  
curl http://localhost:8000/api/posts/ \
  -X POST \
  -H "Authorization: Token {token}" \
  -H "Content-Type: application/json" \
  -d '{"content": "This is a new post content"}'
```

# Code Quality

Code is formatted with Black, DRF Generic Views are heavily used to provide clear and readable code. The application has unit tests covering what I believe is most of the application logic. Django's app structure is used to separate concerns from Users and Posts/Comments, ensuring reusability.

# Optimizations

Select related and prefetch are both used to ensure we don't incur unnecessary costs (of multiple queries, facing the N+1 problem). I provided different serializers in some endpoints (of the same model) to avoid fetching unnecesary data. Operations such as Counting are done on the DB to ensure good performance.

# Challenges Faced

Although the built-in User model in Django is great and an instrumental part of the framework, there are some tricky spots when customizing it (mainly configuring it and using it with DRF). I even run into an [issue](https://github.com/encode/django-rest-framework/issues/9300) when using the latest version of DRF that as of 2024-03-21 is still open. Luckily it was easily solved by downgrading to DRF version 3.14.0 (that is freezed in the requirements now).
