# Brevo Proxy — Setup Guide

The waitlist form sends submissions to Brevo **through this proxy** so the
Brevo API key is never exposed in the website's JavaScript (front-end code is
publicly readable; a leaked key gives full access to the contact base).

## One-time Brevo account setup (when you have access)

1. **Create contact attributes** — Brevo dashboard → Contacts → Settings →
   Contact attributes. Add these (all type **Text**):
   `FULLNAME`, `WHATSAPP_NUMBER`, `LOCATION`, `ROLE`, `TRADE_CATEGORY`, `LANGUAGE`,
   `GIVEAWAY_ENTRY`
   ⚠️ Do **not** name it `WHATSAPP` — that is a Brevo *reserved identifier* and the
   submission fails with `404 document_not_found / "Contact does not exist"`.
2. **Create lists — one per "tag"** — Contacts → Lists (folder `SmartTasker_Indonesia`):
   - `PreLaunch_SmartTasker_Lead_Signup` — ID **4** (master: every form submission) ✅ created
   - `PreLaunch_SmartTasker_Lead_Signup_En` — used the site in English → English email automations ✅ created
   - `PreLaunch_SmartTasker_Lead_Signup_Id` — used the site in Bahasa Indonesia → Indonesian email automations ✅ created
   Optional later: `Customer`, `Tasker`, `Honda_Vario_Entry` (the ROLE /
   GIVEAWAY_ENTRY attributes cover this for now).
   Note each list's numeric ID and fill it into `js/brevo-config.js`.

   **Email-by-language:** the form sends each contact to the master list AND
   the list matching the language they used on the site. In Brevo, create two
   automations ("contact added to list" trigger): one on
   `PreLaunch_SmartTasker_Lead_Signup_En` sending the English templates, one on
   `PreLaunch_SmartTasker_Lead_Signup_Id` sending the Indonesian ones
   (templates in `email-templates/`). The contact's `LANGUAGE`
   attribute (`en`/`id`) is also stored as a fallback for segment-based sends.
3. **Get an API key** — Settings (top-right) → SMTP & API → API Keys →
   Generate a new key.

> **"Tags":** Brevo has no Mailchimp-style tags — a Brevo **list** plays that
> role. A Mailchimp tag like `Registered_User` becomes a list named
> `Registered_User`; "tagging" a contact = adding them to that list. Campaigns,
> segments, and automations all target lists directly.

## Deploy the proxy (Cloudflare Workers, free)

```
npm i -g wrangler
wrangler login
cd brevo-proxy
wrangler deploy worker.js --name smarttasker-brevo
wrangler secret put BREVO_API_KEY     # paste the API key when prompted
```

The deploy prints a URL like `https://smarttasker-brevo.<account>.workers.dev`.

## Wire the site

Edit `js/brevo-config.js`:

```js
PROXY_URL: 'https://smarttasker-brevo.<account>.workers.dev',
LIST_IDS: { prelaunch: 2, customer: 3, tasker: 4, giveaway: 5 },   // your real list IDs
```

Done. Submissions now upsert contacts into Brevo (re-submitting the same email
updates the contact instead of erroring).

## Before launch

- In `worker.js`, change `ALLOWED_ORIGIN` from `'*'` to `'https://smarttasker.id'`.
- Confirm `DEV_DIRECT_API_KEY` in `js/brevo-config.js` is empty.

## Alternative hosts

The same logic ports trivially to Netlify Functions / Vercel if the site is
hosted there — ask the developer to adapt `worker.js` (it's ~80 lines).
