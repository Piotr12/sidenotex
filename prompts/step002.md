# finishing the backend in Cursor

I switched to Cursor (Claude 3.5 sonnet) to modify the code further. 

There was a series of actions.
+ extend a user Model
+ create an annotation Model 

# Prompts 

Each with own smaller commit

## Step002.1

Extend my model please - I need a user_domain field into User table, extracted from the email. 
--
I want to show this domain in the dashboard view 

## Step002.2

lets add one more model. It is called Sidenote and contains the following fields:
+ URL => an URL string (if you can check if for being a
+ Text => a long description users will be adding)
+ Author => a foreign key to the user table
+ Domain => string, user domain (duplicate, for easier selection of annotations by domain)