// Decap CMS GitHub OAuth — Begin endpoint
// Redirects user to GitHub for authorization

export default async function handler(req, res) {
  const clientId = process.env.OAUTH_CLIENT_ID;
  if (!clientId) {
    return res.status(500).send('OAUTH_CLIENT_ID not configured');
  }

  const redirectUri = `${process.env.VERCEL_URL || req.headers.host}/api/callback`;

  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: `https://${redirectUri}`,
    scope: 'repo',
    state: req.query.state || Math.random().toString(36).slice(2),
  });

  res.writeHead(302, { Location: `https://github.com/login/oauth/authorize?${params}` });
  res.end();
}
