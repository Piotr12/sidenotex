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
  const submitButton = createSidenoteForm.querySelector('button[type="submit"]');

  createSidenoteForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const sidenoteText = document.getElementById('sidenoteText').value;
    submitButton.disabled = true;
    createSidenote(sidenoteText);
  });

  // Load Sidenotes on Popup Open
  loadSidenotes();

  // Function to Load Sidenotes
  function loadSidenotes() {
    const sidenotesList = document.getElementById('sidenotesList');
    sidenotesList.innerHTML = '<div class="empty-state">Loading...</div>';
    
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const url = encodeURIComponent(tabs[0].url);
      loadToken();
      chrome.storage.sync.get(['token'], function (result) {
        const token = result.token;
        if (!token) {
          alert('Please set your token in the Auth tab.');
          return;
        }
        fetch(`https://sidenotex.com/api/sidenotes/?url=${url}`, {
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
            const errorDiv = document.createElement('div');
            errorDiv.className = 'empty-state';
            errorDiv.textContent = 'Error loading sidenotes';
            sidenotesList.innerHTML = '';
            sidenotesList.appendChild(errorDiv);
          });
      });
    });
  }

  // Function to Display Sidenotes
  function displaySidenotes(sidenotes) {
    const sidenotesList = document.getElementById('sidenotesList');
    sidenotesList.innerHTML = '';
    
    if (!sidenotes || sidenotes.length === 0) {
      const emptyDiv = document.createElement('div');
      emptyDiv.className = 'empty-state';
      emptyDiv.textContent = 'No sidenotes yet';
      sidenotesList.appendChild(emptyDiv);
      return;
    }

    // Display only first 5 sidenotes
    const displayedSidenotes = sidenotes.slice(0, 5);
    displayedSidenotes.forEach(function (sidenote) {
      const div = document.createElement('div');
      div.className = 'sidenote';
      div.textContent = sidenote.text;
      sidenotesList.appendChild(div);
    });

    // Add "see more" link if there are more than 5 sidenotes
    if (sidenotes.length > 5) {
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const currentUrl = encodeURIComponent(encodeURIComponent(tabs[0].url));
        const seeMoreLink = document.createElement('a');
        seeMoreLink.href = '#';
        seeMoreLink.className = 'create-account-link';
        seeMoreLink.textContent = 'See more';
        seeMoreLink.addEventListener('click', function(e) {
          e.preventDefault();
          chrome.tabs.create({ url: `https://sidenotex.com/url-sidenotes/?url=${currentUrl}` });
        });
        sidenotesList.appendChild(seeMoreLink);
      });
    }
  }

  // Function to Create a Sidenote
  function createSidenote(text) {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const url = tabs[0].url;
      chrome.storage.sync.get(['token'], function (result) {
        const token = result.token;
        if (!token) {
          alert('Please set your token in the Auth tab.');
          submitButton.disabled = false;
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
            submitButton.classList.remove('button-error');
            submitButton.classList.add('button-success');
            submitButton.textContent = 'Created!';
            document.getElementById('sidenoteText').value = '';
            
            setTimeout(() => {
              submitButton.classList.remove('button-success');
              submitButton.disabled = false;
              submitButton.textContent = 'Create Sidenote';
            }, 2000);
            
            loadSidenotes();
          })
          .catch(error => {
            console.error('Error creating sidenote:', error);
            submitButton.classList.add('button-error');
            submitButton.textContent = 'Error!';
            
            setTimeout(() => {
              submitButton.classList.remove('button-error');
              submitButton.disabled = false;
              submitButton.textContent = 'Create Sidenote';
            }, 2000);
          });
      });
    });
  }

  // Add this after your existing event listeners
  const checkTokenButton = document.getElementById('checkToken');
  checkTokenButton.addEventListener('click', function() {
    const token = document.getElementById('tokenInput').value;
    if (!token) {
      alert('Please enter a token first');
      return;
    }

    const testUrl = encodeURIComponent('https://example.com');
    checkTokenButton.disabled = true;
    fetch(`https://sidenotex.com/api/sidenotes/?url=${testUrl}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Token ' + token
      }
    })
      .then(response => {
        checkTokenButton.disabled = false;
        if (response.ok) {
          checkTokenButton.classList.remove('button-error', 'secondary-button');
          checkTokenButton.classList.add('button-success');
          checkTokenButton.textContent = 'Token Valid';
        } else {
          checkTokenButton.classList.remove('button-success', 'secondary-button');
          checkTokenButton.classList.add('button-error');
          checkTokenButton.textContent = 'Invalid Token';
        }
        
        setTimeout(() => {
          checkTokenButton.classList.remove('button-error', 'button-success');
          checkTokenButton.classList.add('secondary-button');
          checkTokenButton.textContent = 'Check Token';
        }, 2000);
      })
      .catch(error => {
        checkTokenButton.disabled = false;
        checkTokenButton.classList.remove('button-success', 'secondary-button');
        checkTokenButton.classList.add('button-error');
        checkTokenButton.textContent = 'Error';
        
        setTimeout(() => {
          checkTokenButton.classList.remove('button-error');
          checkTokenButton.classList.add('secondary-button');
          checkTokenButton.textContent = 'Check Token';
        }, 2000);
      });
  });

  document.querySelector('.logo').addEventListener('click', function(e) {
    e.preventDefault();
    chrome.tabs.create({ url: 'https://sidenotex.com' });
  });
});