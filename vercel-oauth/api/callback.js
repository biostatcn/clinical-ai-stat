// Decap CMS GitHub OAuth — Callback endpoint
// Exchanges code for token and returns to CMS via postMessage

export default async function handler(req, res) {
  const { code, state } = req.query;
  const clientId = process.env.OAUTH_CLIENT_ID;
  const clientSecret = process.env.OAUTH_CLIENT_SECRET;

  if (!code) return res.status(400).send('Missing code');

  // Exchange code for access token
  const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify({
      client_id: clientId,
      client_secret: clientSecret,
      code,
      state,
    }),
  });

  const data = await tokenResponse.json();
  const accessToken = data.access_token;

  if (!accessToken) {
    return res.status(400).send(`Token exchange failed: ${JSON.stringify(data)}`);
  }

  // Return HTML that sends token back to CMS via postMessage
  res.setHeader('Content-Type', 'text/html');
  res.status(200).send(`
    <html>
    <body>
    <script>
      (function() {
        function receiveMessage(message) {
          window.opener.postMessage(
            'authorization:${accessToken}:${JSON.stringify({ token: accessToken })}',
            message.origin
          );
          window.close();
        }
        window.addEventListener('message', receiveMessage, false);
        window.opener.postMessage('authorizing:${accessToken}', '*');
      })();
    </script>
    </body>
    </html>
  `);
}
