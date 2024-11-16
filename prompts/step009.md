# step 009

Improving the UI of Chrome Extension.

## prompt

Have a look at the backend_site.css attached. Currently its not used. Its from the website this extension corresponds with. the website uses PlainCSS but here I want to have no external libraries. Please update the UI of the extension so it 

+ looks more modern, clear, readable and estetic
+ use color scheme that relates to the backend website of it. 

---

Do make the buttons color look like my primary blue color, make the token entry text a textarea instead, one with up to three rows and occupying 100% of the width.

---
add a check token button on auth page, it should try to check sidenotes for https://example.com and based on reply know if access is right or not, show it via some visual (make the button red?)

---
the url should be encoded before its sent to the backend, use similar function

function encodeSearchUrl(event) {
        const urlInput = document.getElementById('search-url');
        urlInput.value = encodeURIComponent(urlInput.value);
    }

--
add a tiny header above both tabs, font color set to blue color of mine, left aligned, "sidenotex"

--

how to get the whole body have a tiny little margin? 

--

<header class="logo">sidenotex</header> should be clickable and open https://sidenotex.com in a new tab.

--

that logo text on top should be centered. 

--

while sidenotes are being loaded there should be a text "loading" shown in their place, if there are no there should be a "no sidenotes yet" text, and if sidenotes are there they should be listed same way as now.

--

rather than an alert on successfull sidenote creation the button should turn green for a moment then back to normal. if there is an issue, red and back to normal.

--

the number of sidenotes displayed should be limited to 5, if there is 6th returned from the API it should not be presented but instead a link "see more" should be shown. it should navigate user to url of the following format:

https://sidenotex.com/url-sidenotes/?url=https%253A%252F%252Fwww.example.com

(this is for https://www.example.com url, its encoded).
