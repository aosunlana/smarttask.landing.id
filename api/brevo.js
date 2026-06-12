/**
 * SmartTasker Indonesia — Brevo proxy (Vercel serverless function)
 * =================================================================
 * Same job as brevo-proxy/worker.js but Vercel-native: deploys automatically
 * with the site (any file in /api/ becomes an endpoint at /api/<name>).
 *
 * Setup:
 *   1. In the Vercel dashboard → Project → Settings → Environment Variables:
 *      add BREVO_API_KEY = <the Brevo API key>   (all environments)
 *   2. In js/brevo-config.js set:  PROXY_URL: '/api/brevo'
 *      (same-origin — no CORS configuration needed)
 */

const ALLOWED_ATTRS = ['FULLNAME', 'WHATSAPP', 'LOCATION', 'ROLE', 'TRADE_CATEGORY', 'LANGUAGE', 'GIVEAWAY_ENTRY'];

function sanitizeAttributes(attrs) {
  const out = {};
  for (const key of ALLOWED_ATTRS) {
    if (typeof attrs[key] === 'string' && attrs[key].length <= 500) {
      out[key] = attrs[key];
    }
  }
  return out;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  if (!process.env.BREVO_API_KEY) {
    return res.status(500).json({ error: 'BREVO_API_KEY env var not configured in Vercel' });
  }

  const payload = req.body || {};
  if (!payload.email || typeof payload.email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.email)) {
    return res.status(400).json({ error: 'Valid email required' });
  }

  const body = {
    email: payload.email,
    updateEnabled: true,
    listIds: Array.isArray(payload.listIds) ? payload.listIds.filter(n => Number.isInteger(n) && n > 0) : [],
    attributes: sanitizeAttributes(payload.attributes || {}),
  };

  const brevoRes = await fetch('https://api.brevo.com/v3/contacts', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'api-key': process.env.BREVO_API_KEY,
    },
    body: JSON.stringify(body),
  });

  if (brevoRes.ok) {
    return res.status(200).json({ success: true });
  }
  const err = await brevoRes.json().catch(() => ({}));
  if (err.code === 'duplicate_parameter') {
    return res.status(200).json({ success: true, duplicate: true });
  }
  console.error('Brevo error', brevoRes.status, err);
  return res.status(502).json({ error: 'Brevo rejected the submission' });
}
