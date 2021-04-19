# simple-blockchain
just playing with blockchain, trying understand how it works

the flask project can be run on same machine in two terminals

flask run

For second run uncomment
#FLASK_RUN_PORT=5001
in .flaskenv - so the first instance will be run on default port 5000 but the second on 5001

HTTP POST requests body examples
================

/transactions/add
=========

{
	"sender": "d5a153157fa047a586a3ae146700124c",
	"recipient": "recipient-address",
	"total": 5
}

/nodes/register
==================

{
	"nodes": ["http://localhost:5001"]
}


GET requests: Conent-Type application/json
