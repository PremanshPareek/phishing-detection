document.addEventListener('DOMContentLoaded', function() {
  const urlParams = new URLSearchParams(window.location.search);
  const url = urlParams.get('url');
  document.getElementById('url').textContent = url;

  document.getElementById('continueButton').addEventListener('click', function() {
    window.location.href = url;
  });

  document.getElementById('goBackButton').addEventListener('click', function() {
    window.history.back();
  });
});
