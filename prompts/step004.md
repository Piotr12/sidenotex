# Making a chrome extension.

This was done again in ChatGPT (o1-preview) to
start with. I am not sure if that was easier than 
Copilot Composer (???)

# Prompt

Hi, I need help with creating a simple Chrome extension.

It is called Sidenotex and serves as a tool for taking side notes on webpage. 

It operates with a simple backend that has two endpoints like on the sample below

1) Create a sidenote:

curl -X POST \
  http://localhost:8000/api/sidenotes/create/ \
  -H 'Authorization: Token REMOVED' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://example.com",
    "text": "This is a test sidenote from curl"
}'

2) List sidenotes for a page: 

curl -X GET \ 
  'http://localhost:8000/api/sidenotes/?url=https://example.com' \
  -H 'Authorization: Token REMOVED_AS_WELL!' 

It shall have two tabs: one for sidenotes (list and creation) and one for auth.

Lets start from the second one: authentication. 
It should allow for entering a token (and save it between chrome runs) and present a button to open the system homepage (https://sidenotex.com) for account creation.

The first one, on every page navigation should call the backend and list the extensions. below is how the reply json looks like: 

{"sidenotes": [{"text": "this is an example of a side note.", "created_at": "2024-11-14T17:29:06.224Z", "author__email": "piotr.nowacki@onet.pl"}, {"text": "another one", "created_at": "2024-11-14T17:29:22.482Z", "author__email": "piotr.nowacki@onet.pl"}]}%  

Guide me through the process of creating that extension, what files I need, what structure, how to test it. 

--- 

I would like it to display the saved token (when its saved)