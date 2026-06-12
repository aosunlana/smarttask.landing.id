# SmartTasker Indonesia — Developer Change Request Document (v2.0)

**Reference website (master template):** www.smarttasker.au
**Target domain:** smarttasker.id
**Objective:** Localised Indonesian replica of the Australian site — same layout, palette, typography, button styling, page structure, section order, responsiveness, branding. Replace Australian imagery/copy/references with Indonesian content.

## Quick change list (client's numbered requests)

1. Hero headline: replace "Get it done" with **"Never Pay A Stranger Again™"** (final wording may be updated by client). Replace subheading "Post your task big or small. Choose an expert and tick off that to do list" with:
   > Indonesia's trusted marketplace for local services.
   > Find, compare and hire local professionals with confidence.
2. Replace all "Download app" buttons with **"Join the waitlist"** buttons → opens a form (form to be provided; Brevo-backed).
3. Delete App Store and Google Play buttons. Just one blue **"Join the waitlist"** button.
4. Insert new section/page at position 1: **"Win a Honda Vario 125"** competition — picture of the bike + a man/woman, terms & conditions, Join the Waitlist button.
5. "Post any task big or small" section: use an image of an Indonesian worker.
6. "Start earning with lower fees" section: replace Isabella Thomson's photo with an Indonesian woman and name.
7. "Smart Secure Sorted" section: use an image of an Indonesian worker. **Delete the "Staged Milestone payment" line.**
8. "Start earning with lower fees" → change to **"Start earning with low fees"**; remove the "No subscriptions" line.
9. "Smart Secure Sorted" section: add new line: **"Get verified – Earn this trust badge and let customers know that you have been verified. Free Verification for the first 1000 taskers for 12 months"**
10. FAQ: client will provide updated answers to all questions (placeholder: keep questions, mark answers as TBD/keep existing until supplied).
11. Final "Download Now" button → **"Join the Waitlist"**.
12. Landing page must be **bilingual with a toggle switch** (English / Bahasa Indonesia).

**Links:** Contact button → mailto:support@smarttasker.id

## Language requirements

- Bilingual: English + Bahasa Indonesia
- Language selector visible in header
- Preference persists across pages (localStorage)
- Default: English

## Global CTA changes

Replace all "DOWNLOAD NOW" / "INSTALL APP" / "GET THE APP" → **JOIN WAITLIST**

## Section-by-section

| # | Section | Status | Notes |
|---|---------|--------|-------|
| — | Header | Minimal changes | Keep logo, nav structure, styling. Header CTA: JOIN WAITLIST. Add language toggle. |
| 1 | Hero | Modified | Keep layout. Indonesian imagery (homeowner/tasker/small business owner). Headline: Never Pay A Stranger Again™. Subheadline per above. CTA: JOIN WAITLIST. |
| 2 | Honda Vario Giveaway | NEW | Directly below hero (or page 1). Headline: WIN A HONDA VARIO. Sub: "Join SmartTasker before launch for your chance to win. Register as a customer or tasker." CTA: JOIN WAITLIST. Honda Vario image + Competition Terms link. |
| 3 | Post Your Task | Retain structure | Indonesian customer imagery, Indonesian copy. |
| 4 | Start Earning | Retain structure | Indonesian cleaner/electrician/handyman/gardener imagery. Add Founding Member messaging. Add: "Free Verification for the first 1000 taskers for 12 months". Title → "Start earning with low fees". Remove "No subscriptions" line. |
| 5 | Promote Your Business | Retain structure | Indonesian service provider imagery, localised copy. |
| 6 | Smart. Secure. Sorted. | Modified | Launch features only: Verified Taskers, Secure Escrow Payments, Reviews & Ratings, Compare Multiple Quotes, In-App Messaging, Transparent Hiring. Add "Get verified" trust-badge line (see #9). Do NOT mention: Milestone Payments, Customer Verification, unlaunched features. |
| 7 | Waitlist Registration | NEW | Above FAQ. Single dynamic form: user selects Customer / Tasker / Both. Captures customer regs, tasker regs, Honda Vario entries. Brevo integration. |
| 8 | FAQ | Modified | Keep layout. Combine Customer + Tasker FAQs into one section. Updated answers to be supplied. |
| 9 | Final CTA | Modified | DOWNLOAD NOW → JOIN WAITLIST. App store links → waitlist form. |
| 10 | Footer | Minimal changes | Update links. Required pages: Privacy Policy, Terms & Conditions, Honda Giveaway Terms, Contact Us. |

## Imagery requirements

- Replace ALL Australian imagery with Indonesian imagery: homeowners, families, tradespeople, cleaners, electricians, gardeners, small business owners.
- Avoid: tourist imagery, generic Bali tourism, beach clubs, surfing. Represent Indonesia as a whole.

## CRM (Brevo)

- Store: customer registrations, tasker registrations, Honda Vario entries, language preference, location, trade category.
- Tags: Prelaunch signup, Tasker, Verified Tasker, Customer, etc.
- ~12 automated emails to be migrated from Mailchimp (client has copies).

## Analytics

- Google Analytics, Meta Pixel, TikTok Pixel.
- Track: waitlist clicks, form starts, form submissions, Honda Vario entries.
- (IDs to be supplied by client — ship with placeholder snippets.)

## Pending from client

- [ ] Final hero headline confirmation
- [ ] Waitlist form fields / Brevo form details + API/account info
- [ ] Updated FAQ answers
- [ ] Honda Vario competition terms & conditions copy
- [ ] Analytics IDs (GA4, Meta Pixel, TikTok Pixel)
- [ ] Indonesian imagery (or approval to use placeholder stock imagery)
