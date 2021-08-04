[![Board Status](https://dev.azure.com/Q17040301/cccbf8b9-4c8b-4968-997f-b1b13c1b6e94/b2cab589-c648-457b-acf0-55c467a7371d/_apis/work/boardbadge/71a2bf4f-c099-4d54-a0c0-168be6212f35)](https://dev.azure.com/Q17040301/cccbf8b9-4c8b-4968-997f-b1b13c1b6e94/_boards/board/t/b2cab589-c648-457b-acf0-55c467a7371d/Microsoft.RequirementCategory)
# log_retriever
Search/Retriever the logs from all server.

# Setup
Set up all the remote server with ssh key login
ssh-keygen -t rsa
ssh-copy-id user@target

# Development
$ export FLASK_APP=app.py (app.py is the default app, so it's not required to set this command.)
$ export FLASK_ENV=development

# run the server
$ python -m flask run

# Deployment with Apache wsgi
$ yum install python-flask
