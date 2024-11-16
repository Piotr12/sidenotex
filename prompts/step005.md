# adding email sending

This was a NIGHTMARE!! (not really GenAI/LLM related, seems that setting an SMTP server in 2024 is not that easy thanks to all the SPAM that is all around. I gave up.) 

First, Getting sendmail installed was going well until I got stuck with docker image builds. Tried to troubleshoot for a moment but moved to postfix after a quarter of no progress. Postfix install went well and all seem to build just fine. 

But then there was an 500 Server error upon sending email.
 
Upon sorting this one (root user should run postfix was the fix) I ended with nondelivered emails.

And DNS records edits.

And I gave up and instead went the "hosted service way"

# prompt

5+ prompts for sendmail install that had issues, the only thing they managed to get well was settings.py (reused below)

---

Do add a postfix install to this Dockerfile so I can send emails (like configured in settings.py). The domain this will be hosted at is sidenotex.com (in case its of any importance). 

--- 

I have my code failing with a server error 500 after the print(f"Sending email to {email} with token {user.token}") line. what is wrong? 

(its running in a Docker container where postfix should be installed) 

maybe we can start with some more debugging? 

---

I am getting Connection refused. 

--- 

Great, the code is not failing any more. Email Success is sent, I will remove the extra debugging code. You mentioned something about some DNS entries to be added to ensure my mail has more chance to be sent well. What to do exactly?

--- 

even after doing all that stuff my emails are still not delivered. I removed all the postfix stuff from Dockerfile. Do update my settings.py to use a hosted service. My outgoing server is pro?.mail.ovh.net, it uses STARTTLS security and is hosted on port 587.

---

Great, how to pass a local (where I build the image) env variable as EMAIL_HOST_PASSWORD thats baked into the image and available at runtime (I accept the security downsides of that)

---

(...)

# ... 

there was more but it was a lot of running in circles, mainly due to not providing the right context to Cursor (Kamal -> Docker -> bin/app script -> Django). The end state is a curious way Claude managed to get it done. Leaving it as is. 

finally, I fixed manually the endpoints in the chrome extension to test things ... seems it all works (?)