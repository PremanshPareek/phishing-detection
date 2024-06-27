browser.runtime.onMessage.addListener(async (message) => {
  if (message.action === 'checkContent') {
    const { username, email_message, url } = message.data;
    const response = await sendRequestToBackend(username, email_message, url);

    if (response.is_phishing) {
      if (message.type === 'email') {
        alert(`Phishing email detected!\n\nURL: ${url}`);
      } else if (message.type === 'url') {
        const warningUrl = browser.runtime.getURL("intermediatepage.html") + `?url=${encodeURIComponent(url)}`;
        browser.tabs.update({ url: warningUrl });
      }
    }
  }
});

async function sendRequestToBackend(username, emailMessage, url) {
  const apiUrl = 'https://your-backend-api-url'; // Replace with your actual backend API URL

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        email_message: emailMessage,
        url: url
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json();
    console.log('Backend Response:', responseData);

    return responseData;
  } catch (error) {
    console.error('Error sending request to backend:', error);
    return { error: true, message: 'Error sending request to backend' };
  }
}
