# What happened 
I used that prompt and all went well - I ended up with an ugly app though. When I asked for improvement I asked for Tailwind but then decided to move to PureCSS, the initial output was not great so I asked for corrections. There were some but finally (not included in the prompt below) I gave up. 

The code that I have as part of step001 commit is all from o1-preview.

# Prompt

I want to create an app, need your help guiding me through the process.

It is called sidenotex and has two component: Django backend and Chrome Extension that talks with that backend over simple REST web service.What it does is a distributed website annotations service. User can create own annotations and see annotations of others, all in Chrome. 

This is Step001. We will start with authentication. Guide me, how to get it done. 

+ I want a landing page: centered text box to enter email and "start annotating" button below it. 
    + upon press, if user already exist then welcome email with token is sent to his account. if account is not there yet, token is randomized and sent. in both cases user is routed to account_created page where he is informed that account was created and token to log in awaits in his/her inbox.
+ On landing page there is also a login button that takes user to login screen. single entry field there to enter token
    + upon good token entry user is taken to a dashboard page.
+ Dashboard page works only for logged in user
    + for start there is a "welcome to sidenotex {email}" label and option to log out.

That is it. The User model should have email (string), token (string), created_at (string representation of a timestamp, seconds accuracy) and created_ip (IP that user was connecting from). 

Token should not be regenerated on second click for same email, just send existing one, do not modify the model entry. 

Advice step by step how to achieve this.

--

Thanks, can you improve the UI a bit, add Tailwind.

-- 

how about using purecss? 

--

nice, but lets not make the page use whole screen width, especially on the landing page it looks crazy, can you fix this? 