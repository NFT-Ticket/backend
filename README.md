# NFT Django Backend API

### Folder Structure

Look at the tree below to understand where to put `.env` file and `ssl` folder

<!-- prettier-ignore-start -->

. (backend) \
├── README.md  \
├── Server/  \
├── manage.py  \
├── nft_backend/  \
├── requirements.txt  \
├── ssl/ \
├── venv/ \
└── .env 

<!-- prettier-ignore-end -->

### Install Virtual Environment

To make sure the dependencies are same across all copies, we use a virtual environment to install them. The commands are perscibed with a UNIX based terminal in mind (bash/zsh). Some commands might differ for DOS based OS like Windows.

1. Create a virtual env named `venv` by using: `python3 venv venv`
2. Activate the virtual env using: `source venv/bin/activate`

### Install Dependencies

The dependencies are listed out in `requirements.txt` which can be installed with `pip3 install -r requirements.txt`

### Run Server

The server runs by default at `port 8000` using `python3 manage.py runserver` or using `python3 manage.py runserver <port>` at a specified port

### List out Dependencies

If you make any changes to the files and install some dependencies, list them out in `requirement.txt` file using the command `pip3 freeze > requirements.txt`

## REST API Design

#### Admin Routes

`GET /admin` is for Django Admin page

#### Utility Routes

Helper routes to be used to show warnings during signup
`GET /api/username` returns a list of all usernames in db
`GET /api/email` returns a list of all emails in db

#### User Routes

`GET /api/user` lists all users \
`POST /api/user` adds new user to the db \
`GET /api/user/<email_id>` returns the user with `<email_id>` \
`PUT /api/user/<email_id>` modifies the user with `<email_id>`
`DELETE /api/user/<email_id>` deletes the user with `<email_id>`

#### Other Routes

Not fully tested yet. check `server/views.py` and `server/urls.py`
