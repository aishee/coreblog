# coreblog
Blog build with python, custom css + bootstrap.

Blog using Django, bootstrap, aiworkcss.

**Fetures:**
- Articles, classification, columns add, delete, modify. Support tinymce rich text editor. Support article code highlighted .
- Implement user registration, login, change password, forgot to reset your password . By E-mail notification registered users, a user forgets a password-based mail (need to set up a mailbox in setting.py).
- Implement user avatar , users can upload an avatar, and then edit the picture size, and then save, avatars can exist locally, can also be automatically saved in seven cattle cloud (you need to set a good configuration in setting.py in seven cattle).
- Comments support , to achieve an independent review system.
- Home support display rotation , display the latest comments show the most popular articles.
- Home support the display of the tag cloud , has a very cool notes cloud.
- Has a dynamic loading of "all articles" section shows all article categories, you can display the number of articles or browse sorted by time.
- Have a timeline display of very cool "news" section, you can add a daily news in the background.
- Support mobile browsing on the mobile browser has been adjusted.

**Installation**
- Install virtualenv
- Clone repositories:
```
git clone https://github.com/aishee/coreblog
cd coreblog
```
- Install requirements:
```
pip install -r requirements.txt
```
- Custom configuration in file sec_blog/settings.py
- Initialize the database:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

- Run
```
python manage.py runserver
```
- Access to http://127.0.0.1:8000
