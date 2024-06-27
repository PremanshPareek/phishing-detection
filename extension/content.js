async function checkEmailContent(emailContent) {
  const response = await fetch('http://localhost:5000/check-email', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email: emailContent })
  });
  const data = await response.json();
  return data.is_phishing;
}

function parseEmail() {
  // Assuming email content is within a specific HTML structure
  const emailContent = document.querySelector('.email-body').innerText;
  checkEmailContent(emailContent).then(isPhishing => {
    if (isPhishing) {
      alert('Warning: This email contains a phishing attempt!');
    }
  });
}

browser.runtime.onMessage.addListener((message) => {
  if (message.action === 'checkEmail') {
    parseEmail();
  }
});
