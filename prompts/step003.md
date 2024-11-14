# adding REST webservice to the app

Still in Cursor and using Claude3.5 sonnet.

I was picking the files of interest (most of the py files) vs going with full codebase.

I then asked for guidance how to test it via curl.

and made UI 1% less ugly ... this took longer than the rest. this still produced some unnecessary css but I ended in beter shape then I started.

# Prompt

I want to add the following REST services here:

+ list all sidenotes for an url, using logged user domain as a filter (i.e. get user from token, user domain from user, use this domain to filter what he/she can see)
+ create new sidenote (url,text as input)

nothing more (no deletion, no edits, no listing all sidenotes without an url provided)

They should authenticate using user token. 

-- 

How to test them with curl? 

--

Lovely, can you fix the dashboard.html edit form so the text and url fields are of same width? 

--- 
no, do not put all things together, edit form should be changed, css should go into the css (my_static/css/styles.css)

---
its not helping the textarea when redered has rows and cols values set (10 rows, 40 cols) 