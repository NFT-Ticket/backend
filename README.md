# NFT Django Backend API

<img src="static/nft_logo.png">

### Introduction to NFTicket

NFTicket is a plaform to purchase and store tickets securely on your phone. It improves upon the old ticket vendor model by implementing blockchain technology for the security and accessibility of your tickets. Our users spend less time managing their tickets and more time enjoying their events!

### Video recording showing App features in iPhone

Since Apple's appstore policy prevents us from publishing our app to the appstore, we made a video recording to show the key features of the app running in a build mode. Andriod users should be able to download the app by downloading the Expo Go app and scanning the QR code provided in the link in the google sheet.

[![NFT ios App demo](https://img.youtube.com/vi/bd4xmAp97L4/0.jpg)](https://www.youtube.com/watch?v=bd4xmAp97L4 "NFT ios App demo")

### For Android Users

1. Download the Expo go app from playstore
   https://play.google.com/store/apps/details?id=host.exp.exponent&hl=en_US&gl=US
2. Scan the QR code below:
   <img src="static/expo.png">
3. Create account, copy Wallet Address and then reload the account from the Test Net Faucet by visiting https://bank.testnet.algorand.network/
4. use the app; buy and sell tickets

### System Architecture

<img src="static/system_architecture.png">

### Folder Structure

Look at the tree below to understand where to put `.env` file and `ssl` folder

<!-- prettier-ignore-start -->

. (backend) \
├── Procfile \
├── README.md \
├── algorand/ \
├── encryptor/ \
├── firebase_auth/ \
├── ipfs/ \
├── manage.py \
├── nft_backend/ \
├── requirements.txt \
├── server/ \
├── ssl/ \
├── static/ \
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

### NOTE:

While sending the request, be careful not to miss the trailing (ending) slash `/` sign. \
For Django, `/api/user` is different from `/api/user/`. Django will try to redirect the former request to the latter request. \
While this may work for some request methods like `GET`, methods like `PUT`, `DELETE`, and `POST` might not receive the payload after redirection.

#### Admin Routes

`GET /admin` is for Django Admin page

#### Utility Routes

Helper routes to be used to show warnings during signup \
`GET /api/username/` returns a JSON object with list of all usernames in db \
`GET /api/email/` returns a JSON object with list of all emails in db

#### User Routes

`GET /api/user/` lists all users \
`POST /api/user/` adds new user to the db \
`GET /api/user/<email_id>/` returns the user with `<email_id>` \
`PUT /api/user/<email_id>/` modifies the user with `<email_id>` \
`DELETE /api/user/<email_id>/` deletes the user with `<email_id>` \

`GET /api/user/ticket/<email_id>/` returns the list of tickets owned by the user \
`GET /api/user/balance/<email_id>/` returns the balance of user in micro ALGOs \
`GET /api/user/nft/<email_id>/` returns the list of all nfts owned by the user \
`GET /api/user/transaction/<email_id>/` returns the list of transactions where tickets are sold by user with email_id

#### Event Routes

`GET /api/event/` lists all events in the future. This will omit all past events \
`GET /api/event/ticket/<event_id>/` returns a list of secondary tickets on sale for the event. \
`POST /api/event/` adds new new event to the db. Params required: `vendor<email>, ticket_quantity<int>, title<str>, description<str>, images:List[str], street_address<str>, city<str>, zipcode<int>, date, time`\
`GET /api/event/<event_id>/` returns the event with `<event_id>` \
`PUT /api/event/<event_id>/` modifies the event with `<event_id>` \
`GET /api/event/search/?query=<url_encoded_query_string>` search the database for events where either of title, description, street_address, or city matches the query string. The match is done using django's `__icontains` module that uses SQL LIKE `%query%` to search for text that might be a match.

#### Ticket Routes

`GET /api/ticket/<ticket_id>/` returns the ticket owned by user after purchase. \

`POST /api/ticket/` with params: `event_id` and `buyer<email_id>` as body makes an atomic transaction where ALGOS are transferred to the seller and NFT is transferred to the user atomically. If either of the transactions fail, the whole transaction fails. If the transactions are successful, a ticket is issued for the buyer. \

`PUT /api/ticket/<ticket_id>/` with modified ticket as the body changes the ticket object in the db. Use this when a user wants to sell their ticket and adjust price to the ticket for sale. \

`PATCH /api/ticket/<ticket_id>/` with params: `buyer<email_id>` as body makes an atomic transaction where ALGOS are transferred to the owner of `<ticket_id>` and NFT is transferred to `buyer<email_id>`. If the atomic transfer is successful, the Ticket database is changed where the owner is changed from seller to new buyer and the `on_sale` property is set to False.
