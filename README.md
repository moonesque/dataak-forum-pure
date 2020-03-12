# Harvesting Project
This projects implements the required task in Python 3, using ```request-html``` library.
## Setup
To setup the project, navigate to the root and create a virtual environment.
```
python3 -m venv venv
source venv/bin/actiavte
```
Install the dependencies, using pip:
```
pip install -r requirments.txt
```
Create a MySQL database:
```
CREATE database dataak_forum_pure CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use dataak_forum_pure;
```
Navigate to the project directory and edit the models.py file.
```
cd dataak_forum_pure
vim models.py
```
Modify the ```CONNECTION_STRING``` to match your MySQL credentials.
## Usage
To run the crawler and store the data in the MySQL database:
```
python3 main.py
```
You should now be able to query the database and get the desired result.
 The ```mysqldump``` of the database is included in the root of the project.

The following queries answer question #4 on the given task:

* Users with the most posts:
```
select name, count(name) as number_of_posts from posts inner join authors on posts.author_id = authors.id group by name order by number_of_posts desc
```
* Number of all posts in the whole forum:
```
select count(*) as posts from posts;
```
* Forums with the most active users:
```
select forum_name, count(name) as active_users from (select forum_name, name from forums inner join threads on forums.id = threads.forum_id inner join posts on threads.id = posts.thread_id inner join authors on authors.id = posts.author_id group by forum_name, name) as subq group by forum_name order by active_users desc;
```
* Threads with the most active users:
```
select thread, count(name) as active_users from (select thread, name from forums inner join threads on forums.id = threads.forum_id inner join posts on threads.id = posts.thread_id inner join authors on authors.id = posts.author_id group by thread, name) as subq group by thread order by active_users desc;
```
* Forums with no posts:
```
 select forum_name from (select forum_name, posts.id from forums left join threads on forums.id = threads.forum_id left join posts on threads.id = posts.thread_id) as subq where id is NULL;
```
