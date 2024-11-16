document.addEventListener('DOMContentLoaded', function () {
  // Tab elements
  const sidenotesTab = document.getElementById('sidenotesTab');
  const authTab = document.getElementById('authTab');
  const sidenotesContent = document.getElementById('sidenotesContent');
  const authContent = document.getElementById('authContent');


  function loadToken() {
    chrome.storage.sync.get(['token'], function (result) {
      const tokenInput = document.getElementById('tokenInput');
      tokenInput.value = result.token || '';
    });
  }

  // Switch to Sidenotes Tab
  sidenotesTab.addEventListener('click', function () {
    sidenotesContent.style.display = 'block';
    authContent.style.display = 'none';
  });

  // Switch to Auth Tab
  authTab.addEventListener('click', function () {
    authContent.style.display = 'block';
    sidenotesContent.style.display = 'none';
    loadToken(); // Load the saved token
  });

  // Handle Auth Form Submission
  const authForm = document.getElementById('authForm');
  authForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const token = document.getElementById('tokenInput').value;
    chrome.storage.sync.set({ token: token }, function () {
      alert('Token saved!');
    });
  });

  // Open Homepage Button
  const openHomepageButton = document.getElementById('openHomepage');
  openHomepageButton.addEventListener('click', function () {
    chrome.tabs.create({ url: 'https://sidenotex.com' });
  });

  // Handle Create Sidenote Form Submission
  const createSidenoteForm = document.getElementById('createSidenoteForm');
  createSidenoteForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const sidenoteText = document.getElementById('sidenoteText').value;
    createSidenote(sidenoteText);
  });

  // Load Sidenotes on Popup Open
  loadSidenotes();

  // Function to Load Sidenotes
  function loadSidenotes() {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const url = tabs[0].url;
      loadToken();
      chrome.storage.sync.get(['token'], function (result) {
        const token = result.token;
        if (!token) {
          alert('Please set your token in the Auth tab.');
          return;
        }
        fetch(`https://sidenotex.com/api/sidenotes/?url=${encodeURIComponent(url)}`, {
          method: 'GET',
          headers: {
            'Authorization': 'Token ' + token
          }
        })
          .then(response => response.json())
          .then(data => {
            displaySidenotes(data.sidenotes);
          })
          .catch(error => {
            console.error('Error fetching sidenotes:', error);
          });
      });
    });
  }

  // Function to Display Sidenotes
  function displaySidenotes(sidenotes) {
    const sidenotesList = document.getElementById('sidenotesList');
    sidenotesList.innerHTML = '';
    sidenotes.forEach(function (sidenote) {
      const div = document.createElement('div');
      div.className = 'sidenote';
      div.textContent = sidenote.text;
      sidenotesList.appendChild(div);
    });
  }

  // Function to Create a Sidenote
  function createSidenote(text) {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const url = tabs[0].url;
      chrome.storage.sync.get(['token'], function (result) {
        const token = result.token;
        if (!token) {
          alert('Please set your token in the Auth tab.');
          return;
        }
        fetch('https://sidenotex.com/api/sidenotes/create/', {
          method: 'POST',
          headers: {
            'Authorization': 'Token ' + token,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            url: url,
            text: text
          })
        })
          .then(response => response.json())
          .then(data => {
            alert('Sidenote created!');
            loadSidenotes();
          })
          .catch(error => {
            console.error('Error creating sidenote:', error);
          });
      });
    });
  }
});