# step010

With most of the work done I am playing with UI.

# prompt

I realized that the

<p class="domain-info">
        Your sidenotes are shared with others in <strong>{{ user_domain }}</strong> domain
    </p>

piece fits the header better. move it there. (to base.html, filled when user is logged and domain is known)

---
I wanted to improve the below piece, but made it worse. I want three links and then below them a small text aligned right (your sidenotes...)

<div class="nav-right">
                {% if request.session.user_id %}
                    <a href="{% url 'dashboard' %}" class="nav-link">Dashboard</a>
                    <a href="{% url 'url_sidenotes' %}" class="nav-link">Search</a>
                    <a href="{% url 'logout' %}" class="nav-link">Logout</a>
                    <br>
                    your sidenotes are shared with others in <span class="domain-info">{{ user_domain }}</span> domain
                {% endif %}
                <img src="{% static 'icon.png' %}" alt="sidenotex icon" class="nav-icon">
            </div>

---
its still bad lets move it to footer, above the copyright notice please.
-- 
if user is logged in, he/she should be moved to dashboard from the landing page.
-- 
in the navigation bar add a About link it should take users to about page and on that page details about the app should be presented. Remember that the main interface to this app is Chrome Extension (put a fake link for now). Create the about page. Be polite, deatiled but not to elaborate.

--

This page does not look well, make it look like terms page, reuse the styles where possible instead of current duplication. 

--
my styles file is a bit obese, can you trim it, refactor, in a way that it is shorter, no repeats there?

--
I want this list to not include the bulletpoints (as I have my own 1,2, and 1+2 ... but do not make it numbered list!
---

see how my landing_page looks, I am currently saving user email in the database, can I avoid it and instead have some md5 of it or something else? (I will still need to send the email but I do not want to store it) ... need to handle user coming back again and reregistgering. 

---
there are still references to email here in models.py, can you fix that as well? 

---
now the domain got empty, I still want to store the domain of the user, just not the email (this should be replaced with hash)

---

my app screen is in static files, called screen.png, find a place for it on the about page. 

---

