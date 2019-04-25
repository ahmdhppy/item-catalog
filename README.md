

# Item Catalogue Project


 ## Project  Description:

Item Catalogue is a Udacity Full Stack Nanodegree Project. 
This project uses data storage to create a RESTFUL web app. 
The features of this project are as follows:
- Categories: Multilayered list of categories
- Items: Items that fall under the categories
- Users Functionality which includes the following
    - Creation of users through sign up; either through manual creation or Google Account Sign In/Sign Up (Authentication Process). Along with standard login functionality
    - Users gaining privileges to create items and then further edit the items they have created
        - Created items are public which means they can be viewed (can be read) by non-users
- Endpoint API: Prints item data in JSON. Readable by both machine and humans. This allows other applications/software to access or extract information easily from this web app. 
    


## Project contents

Within the download you'll find the following files:

```
Item-Catalog/
├── config
│   ├── __init__.py
│   ├── config.py
├── forms
│   ├── __init__.py
│   ├── forms.py
├── models
│   ├── __init__.py
│   ├── models.py
├── routes
│   ├── __init__.py
│   ├── routes.py
├── static
│   ├── css
│   │   └── bootstrap.css
│   ├── fonts
│   │   ├── glyphicons-halflings-regular.eot
│   │   ├── glyphicons-halflings-regular.svg
│   │   ├── glyphicons-halflings-regular.ttf
│   │   ├── glyphicons-halflings-regular.woff
│   │   └── glyphicons-halflings-regular.woff2
│   ├── signin.css
│   └── styles.css
├── templates
│   ├── deleteitem.html
|   ├── edititem.html
|   ├── header.html
|   ├── home.html
|   ├── item.html
|   ├── main.html
|   ├── newitem.html
|   ├── signin.html
|   └── signup.html
├── app.py
├── create_db.py
├── insert_data.py
├── config.conf
├── requirements.txt
├── README.md
```
## Requirements

-   Python 2.7 https://www.python.org/
-   Postgresql https://www.postgresql.org/
-   Python packages ``` Flask flask_bootstrap flask_sqlalchemy flask_googlelogin sqlalchemy_utils passlib flask_wtf psycopg2``` 

## Installation

1.  Install required packages ```apt install postgresql  python2.7 python-pip postgresql-server-dev-all -y```


    


## Steps to run this project
1.  Visit [Google Credentials](https://console.developers.google.com/apis/credentials) then create OAuth client ID by type your information and add this URI `http://localhost:5000/oauth2callback` in Authorised redirect URIs.

2.  Open terminal and navigate to the folder that you saved.

3.  Install python packages ```pip2 install -r requirements.txt``` 

4.  There is a file called `config.conf` edit it to your cofigurarion and save. 

5. Create a database: ```python2.7 create_db.py -c <path of config file>```

6. Insert demo cateogries: ```python2.7 insert_data.py -c <path of config file>```
    
7. Run the application: ```python2.7 app.py -c <path of config file>```
    
8. Finally Access and test your application by visiting  [http://localhost:5000](http://localhost:5000/).

   
    

## JSON Endpoints
http://localhost:5000/categories/json
- Return categories information

```/categories/json/<int:categ_id>```
http://localhost:5000/categories/json/35
- Return category information

http://localhost:5000/items/json
- Return items information

```/items/json/<int:item_id_id>```
http://localhost:5000/items/json/35
- Return item information



 ## Licence

The MIT License ([MIT](https://choosealicense.com/licenses/mit/#))
Copyright © 2019 Ahmad Baniata
