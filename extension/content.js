function isEmailPage() {
    const hostname = window.location.hostname;
    return hostname.includes('mail.google.com') || hostname.includes('outlook.live.com') || hostname.includes('mail.yahoo.com');
  }
  
  function extractEmailContent() {
    const hostname = window.location.hostname;
    let emailContentElement;
    
    if (hostname.includes('mail.google.com')) {
      emailContentElement = document.querySelector('.ii.gt');
    } else if (hostname.includes('outlook.live.com')) {
      emailContentElement = document.querySelector('.rpHighlightAllClass'); // Adjust selector for Outlook
    } else if (hostname.includes('mail.yahoo.com')) {
      emailContentElement = document.querySelector('.message-body'); // Adjust selector for Yahoo Mail
    }
  
    if (emailContentElement) {
      const emailContent = emailContentElement.innerText;
      const emailUrl = window.location.href;
      const username = 'user@example.com'; // Replace with actual logic to get the username
      sendContentToBackend('email', username, emailContent, emailUrl);
    }
  }
  
  function sendContentToBackend(type, username, emailMessage, url) {
    browser.runtime.sendMessage({
      action: 'checkContent',
      type: type,
      data: {
        username: username,
        email_message: emailMessage,
        url: url
      }
    });
  }
  
  function checkUrl(url) {
    // Perform URL analysis if needed
    if (url.includes("facebook.com")) { // Example condition
      const username = 'user@example.com'; // Replace with actual logic to get the username
      sendContentToBackend('url', username, '', url);
    }
  }
  
  // Monitor the page for changes indicating an email is opened
  if (isEmailPage()) {
    const observer = new MutationObserver(extractEmailContent);
    observer.observe(document.body, { childList: true, subtree: true });
  
    // Initially check for opened email
    extractEmailContent();
  } else {
    // Perform URL analysis if it's not an email page
    checkUrl(window.location.href);
  }
  