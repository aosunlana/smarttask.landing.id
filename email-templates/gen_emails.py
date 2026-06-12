import pathlib, re

base_dir = pathlib.Path('C:/Users/osunl/source/repos/smarttask-landing-page/email-templates')
src_text = (base_dir / 'Invite Your Friends email.html').read_text(encoding='utf-8')

# ── helpers ──────────────────────────────────────────────────────────────────

def shared_transforms(html):
    """Apply all transforms that are the same in both EN and ID versions."""

    # 1. Remove Mailchimp conditional wrappers (keep the inner span)
    html = re.sub(r'<!--\*\|IF:MC_PREVIEW_TEXT\|\*-->\s*', '', html)
    html = re.sub(r'\s*<!--\*\|END:IF\|\*-->', '', html)
    # Strip the <!--[if !gte mso 9]><!----> and <!--<![endif]--> wrappers around preview span
    html = html.replace('<!--[if !gte mso 9]><!---->', '')
    html = html.replace('<!--<![endif]-->', '')

    # 2. Logo: replace mcusercontent src, fix alt
    html = re.sub(
        r'alt=""\s+src="https://mcusercontent\.com/[^"]+"',
        'alt="SmartTasker Indonesia" src="https://smarttasker.id/assets/images/logo.png"',
        html
    )

    # 3. Brevo merge tags
    html = html.replace('*|FNAME|*', '{{ contact.FULLNAME }}')
    html = html.replace('*|EMAIL|*', '{{ contact.EMAIL }}')
    html = html.replace('*|UNSUB|*', '{{ unsubscribe }}')
    html = html.replace('*|UPDATE_PROFILE|*', '{{ update_profile }}')
    html = html.replace('*|ARCHIVE|*', '{{ mirror }}')

    # 4. Remove social-icons block
    #    The block is a standalone <tr> containing the mceClusterLayout table
    html = re.sub(
        r'<tr><td[^>]+background-color:#ffffff[^>]+padding-top:0[^>]+padding-bottom:40px[^>]+mceLayoutContainer[^>]+>.*?</tbody></table></td></tr></tbody></table></td></tr></tbody></table>',
        '',
        html,
        flags=re.DOTALL
    )

    # 5. Remove <script> tag before </body>
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)

    # 6. Remove remaining Mailchimp conditional tags
    html = re.sub(r'\*\|IFNOT:ARCHIVE_PAGE\|\*', '', html)
    html = re.sub(r'\*\|END:IF\|\*', '', html)
    html = re.sub(r'\*\|IF:[^|]*\|\*', '', html)

    # 7. Button href (both the standard anchor and the VML fallback use & not &amp;)
    html = html.replace(
        'href="https://smarttasker.au/invite-your-friends/?email=*|EMAIL|*&autoDetect=1&autoTrigger=1"',
        'href="https://smarttasker.id/"'
    )
    # also handle post-FNAME-substitution version (should not appear but be safe)
    html = html.replace(
        'href="https://smarttasker.au/invite-your-friends/?email={{ contact.EMAIL }}&autoDetect=1&autoTrigger=1"',
        'href="https://smarttasker.id/"'
    )
    # any remaining AU URLs
    html = html.replace('http://smarttasker.au', 'https://smarttasker.id/')
    html = html.replace('https://smarttasker.au', 'https://smarttasker.id/')

    # 8. Footer: replace the entire copyright/address block with a regex
    html = re.sub(
        r'<p style="line-height: 125%;"><em><span style="font-size: 11px">Copyright \(C\).*?Want to change how you receive these emails\?</span></p>',
        '__FOOTER_COPYRIGHT__',
        html,
        flags=re.DOTALL
    )

    # 9. Footer preference/unsub links (already converted from *|UPDATE_PROFILE|* above)
    # (no-op — already handled by Brevo tag conversion)

    return html


def insert_giveaway_image(html, alt_text):
    """Insert the Honda giveaway image block between the intro paragraph and the button."""
    image_tr = (
        '<tr><td style="padding-top:0;padding-bottom:16px;padding-right:0;padding-left:0" valign="top">'
        '<table width="100%" style="border:0;border-collapse:separate"><tbody><tr>'
        '<td style="padding-left:50px;padding-right:50px;padding-top:0;padding-bottom:0" class="mceTextBlockContainer">'
        f'<img src="https://smarttasker.id/assets/images/honda-giveaway.jpg" width="560" height="auto" '
        f'style="width:100%;max-width:560px;height:auto;display:block;margin:0 auto;" '
        f'alt="{alt_text}" role="presentation"/>'
        '</td></tr></tbody></table></td></tr>'
    )
    # The button row starts with padding-top:12px;padding-bottom:12px;padding-right:24px;padding-left:24px
    # and contains mceBlockContainer align="center" and mceButtonContainer
    button_row_start = (
        '<tr><td style="padding-top:12px;padding-bottom:12px;padding-right:24px;padding-left:24px" '
        'class="mceBlockContainer" align="center" valign="top">'
        '<table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" '
        'data-block-id="50" class="mceButtonContainer">'
    )
    if button_row_start in html:
        html = html.replace(button_row_start, image_tr + button_row_start)
    return html


# ── ENGLISH VERSION ───────────────────────────────────────────────────────────

en = shared_transforms(src_text)

# Title
en = en.replace(
    '*|MC:SUBJECT|*',
    'Invite Your Friends - Honda Vario 160 Giveaway | SmartTasker Indonesia'
)

# Preview text (the span's content)
en = en.replace(
    '*|MC_PREVIEW_TEXT|*',
    'SmartTasker is coming to Indonesia — share with friends and family so they can join the waitlist and enter the Honda Vario 160 giveaway too!'
)

# Greeting (FNAME already converted to {{ contact.FULLNAME }} in shared_transforms)
en = en.replace(
    '<h2 style="line-height: 150%; text-align: left;" class="last-child">Hey {{ contact.FULLNAME }}!</h2>',
    '<h2 style="line-height: 150%; text-align: left;" class="last-child">Hey {{ contact.FULLNAME }}!</h2>'
)

# Main body paragraph (block 11) — note \xa0 before <strong>
old_body = (
    '<p style="text-align: left;" class="last-child">Be sure to participate in this months\xa0'
    '<strong>$500 SmartTasker Credits Giveaway</strong>!<br/><br/>'
    "Every month in the run up to our launch, we're giving away $500 SmartTasker Credits each to the TOP 3 PEOPLE who help spread the word about SmartTasker.<br/><br/>"
    'Simply invite your friends and be in to win - the more friends you invite, the more chances you have of winning!<br/><br/>'
    'Click the button below to get your unique share URL and start spreading the word:</p>'
)
new_body_en = (
    '<p style="text-align: left;" class="last-child">'
    'SmartTasker is coming to Indonesia soon — and we are so excited you are already on the waitlist!<br/><br/>'
    'Everyone who joins the waitlist before we launch is automatically entered into our '
    '<strong>Honda Vario 160 giveaway</strong>. '
    'Know friends or family who would love to get things done around the home, or earn extra income as a Tasker?<br/><br/>'
    'Send them to <a href="https://smarttasker.id/#waitlist" target="_blank">smarttasker.id</a> '
    'so they can grab their spot on the waitlist — and their own giveaway entry too.<br/><br/>'
    'Click the button below to share the link:</p>'
)
en = en.replace(old_body, new_body_en)

# Insert giveaway image
en = insert_giveaway_image(en, 'Honda Vario 160 Giveaway — SmartTasker Indonesia')

# Button text (standard anchor label)
en = en.replace('>Invite your friends</a>', '>Share smarttasker.id</a>')

# VML center text
en = re.sub(
    r'(\n)(Invite your friends)(\n</center>)',
    r'\1Share smarttasker.id\3',
    en
)

# Closing paragraph (block 53) — note \xa0 and emoji
old_closing = (
    '<p style="text-align: left;" class="last-child">'
    'If you win, the $500 will be credited to your SmartTasker account and can be used like real CASH to either pay for jobs or offset Tasker fees.\xa0'
    '<br/><br/>Grab your unique referral Link via the button above and start sharing with friends via email, text message, or social media! Your unique share URL will track each referral!\xa0'
    '<br/><br/>Start sharing! \U0001f64c \U0001f604<br/><br/>'
    '<em>Brianna, Customer Success Team | SmartTasker Pty Ltd</em></p>'
)
new_closing_en = (
    '<p style="text-align: left;" class="last-child">'
    'The easiest way to share is via <strong>WhatsApp</strong> — just drop the link into your group chats or send it directly to a contact. '
    'You can also share via text message, email, or your favourite social media platform.<br/><br/>'
    'Every new person who signs up gets their own waitlist spot and their own entry into the Honda Vario 160 giveaway. '
    'Help us build the biggest community possible before we launch!<br/><br/>'
    '<em>The SmartTasker Indonesia Team</em></p>'
)
en = en.replace(old_closing, new_closing_en)

# Support paragraph (block 45) — note curly apostrophes ’
old_support = (
    '<p class="last-child">If you have any questions about our upcoming launch, the SmartTasker App or our $500 SmartTasker Credits Giveaway, '
    'we’d love to hear from you. Email us at '
    '<a href="mailto:hello@smarttasker.au" target="_blank">hello@smarttasker.au</a>'
    ' and we’ll be back in touch as soon as we can.</p>'
)
new_support_en = (
    '<p class="last-child">If you have any questions about our upcoming launch or the Honda Vario 160 giveaway, '
    'we would love to hear from you. Email us at '
    '<a href="mailto:support@smarttasker.id" target="_blank">support@smarttasker.id</a>'
    ' and we will get back to you as soon as we can.</p>'
)
en = en.replace(old_support, new_support_en)

# Footer copyright block (the placeholder was set in shared_transforms)
en = en.replace(
    '__FOOTER_COPYRIGHT__',
    '<p style="line-height: 125%;"><em><span style="font-size: 11px">Copyright (C) 2026 SmartTasker Indonesia. All rights reserved.</span></em></p>'
    '<p style="line-height: 125%;"><span style="font-size: 11px">You are receiving this email because you joined the SmartTasker Indonesia waitlist at smarttasker.id.<br/><br/>'
    'Want to change how you receive these emails?</span></p>'
)

out_en = base_dir / 'invite-friends-en.html'
out_en.write_text(en, encoding='utf-8')
print('EN written:', len(en), 'bytes')


# ── BAHASA INDONESIA VERSION ──────────────────────────────────────────────────

id_html = shared_transforms(src_text)

# Title
id_html = id_html.replace(
    '*|MC:SUBJECT|*',
    'Ajak Teman-Temanmu — Giveaway Honda Vario 160 | SmartTasker Indonesia'
)

# Preview text
id_html = id_html.replace(
    '*|MC_PREVIEW_TEXT|*',
    'SmartTasker segera hadir di Indonesia — bagikan kepada teman dan keluarga agar mereka bisa daftar waitlist dan ikut giveaway Honda Vario 160 juga!'
)

# Greeting
id_html = id_html.replace(
    '<h2 style="line-height: 150%; text-align: left;" class="last-child">Hey {{ contact.FULLNAME }}!</h2>',
    '<h2 style="line-height: 150%; text-align: left;" class="last-child">Halo {{ contact.FULLNAME }}!</h2>'
)

# Main body paragraph
new_body_id = (
    '<p style="text-align: left;" class="last-child">'
    'SmartTasker segera hadir di Indonesia — dan kami sangat senang Anda sudah bergabung dengan waitlist kami!<br/><br/>'
    'Setiap orang yang mendaftar ke waitlist sebelum peluncuran otomatis mendapatkan kesempatan memenangkan '
    '<strong>Honda Vario 160</strong> dalam giveaway kami. '
    'Punya teman atau keluarga yang butuh bantuan pekerjaan sehari-hari, atau ingin menambah penghasilan sebagai Tasker?<br/><br/>'
    'Kirimkan mereka ke <a href="https://smarttasker.id/#waitlist" target="_blank">smarttasker.id</a> '
    'agar mereka bisa mendaftarkan diri ke waitlist — dan ikut serta dalam giveaway juga.<br/><br/>'
    'Klik tombol di bawah ini untuk berbagi tautannya:</p>'
)
id_html = id_html.replace(old_body, new_body_id)

# Insert giveaway image
id_html = insert_giveaway_image(id_html, 'Giveaway Honda Vario 160 — SmartTasker Indonesia')

# Button text
id_html = id_html.replace('>Invite your friends</a>', '>Bagikan smarttasker.id</a>')

# VML center text
id_html = re.sub(
    r'(\n)(Invite your friends)(\n</center>)',
    r'\1Bagikan smarttasker.id\3',
    id_html
)

# Closing paragraph
new_closing_id = (
    '<p style="text-align: left;" class="last-child">'
    'Cara termudah untuk berbagi adalah melalui <strong>WhatsApp</strong> — cukup kirimkan tautannya ke grup chat atau langsung ke kontak Anda. '
    'Anda juga bisa berbagi melalui SMS, email, atau platform media sosial favorit Anda.<br/><br/>'
    'Setiap orang baru yang mendaftar mendapatkan tempat di waitlist dan kesempatan sendiri untuk memenangkan Honda Vario 160. '
    'Mari bersama-sama membangun komunitas yang besar sebelum peluncuran!<br/><br/>'
    '<em>Tim SmartTasker Indonesia</em></p>'
)
id_html = id_html.replace(old_closing, new_closing_id)

# Support paragraph
new_support_id = (
    '<p class="last-child">Jika Anda memiliki pertanyaan tentang peluncuran kami atau giveaway Honda Vario 160, '
    'kami dengan senang hati akan membantu. Kirim email ke '
    '<a href="mailto:support@smarttasker.id" target="_blank">support@smarttasker.id</a>'
    ' dan kami akan segera menghubungi Anda kembali.</p>'
)
id_html = id_html.replace(old_support, new_support_id)

# Support heading
id_html = id_html.replace(
    '<h3 style="line-height: 125%;" class="last-child"><strong>Need support?</strong></h3>',
    '<h3 style="line-height: 125%;" class="last-child"><strong>Butuh bantuan?</strong></h3>'
)

# Footer copyright block
id_html = id_html.replace(
    '__FOOTER_COPYRIGHT__',
    '<p style="line-height: 125%;"><em><span style="font-size: 11px">Copyright (C) 2026 SmartTasker Indonesia. Semua hak dilindungi.</span></em></p>'
    '<p style="line-height: 125%;"><span style="font-size: 11px">Anda menerima email ini karena telah mendaftar ke waitlist SmartTasker Indonesia di smarttasker.id.<br/><br/>'
    'Ingin mengubah preferensi email Anda?</span></p>'
)

# Footer link labels in ID
id_html = id_html.replace(
    '<span style="font-size: 11px">You can </span>'
    '<a href="{{ update_profile }}"><span style="font-size: 11px">update your preferences</span></a>'
    '<span style="font-size: 11px"> or </span>'
    '<a href="{{ unsubscribe }}"><span style="font-size: 11px">unsubscribe</span></a>',
    '<span style="font-size: 11px">Anda bisa </span>'
    '<a href="{{ update_profile }}"><span style="font-size: 11px">memperbarui preferensi</span></a>'
    '<span style="font-size: 11px"> atau </span>'
    '<a href="{{ unsubscribe }}"><span style="font-size: 11px">berhenti berlangganan</span></a>'
)
id_html = id_html.replace(
    '<a href="{{ mirror }}"><span style="font-size: 11px">View in browser</span></a>',
    '<a href="{{ mirror }}"><span style="font-size: 11px">Lihat di browser</span></a>'
)

out_id = base_dir / 'invite-friends-id.html'
out_id.write_text(id_html, encoding='utf-8')
print('ID written:', len(id_html), 'bytes')


# ── VERIFICATION ─────────────────────────────────────────────────────────────

print('\n--- Verification ---')
for fname, html in [('EN', en), ('ID', id_html)]:
    issues = []
    if 'mcusercontent.com' in html: issues.append('mcusercontent still present')
    if 'smarttasker.au' in html: issues.append('smarttasker.au still present')
    if 'Pty Ltd' in html: issues.append('Pty Ltd still present')
    if 'Brianna' in html: issues.append('Brianna still present')
    if '$500 SmartTasker Credits' in html: issues.append('$500 credits still present')
    if 'hello@smarttasker.au' in html: issues.append('old support email still present')
    if 'mceSocialIcon' in html: issues.append('social icons still present')
    if '<script' in html: issues.append('script tag still present')
    if '*|' in html: issues.append('Mailchimp tags still present')
    if 'support@smarttasker.id' not in html: issues.append('new support email missing')
    if 'honda-giveaway.jpg' not in html: issues.append('giveaway image missing')
    if '{{ contact.FULLNAME }}' not in html: issues.append('FULLNAME tag missing')
    if '{{ unsubscribe }}' not in html: issues.append('unsubscribe tag missing')
    if '{{ update_profile }}' not in html: issues.append('update_profile tag missing')
    if '{{ mirror }}' not in html: issues.append('mirror tag missing')
    if '#ddf770' not in html: issues.append('#ddf770 band missing')
    if 'v:roundrect' not in html: issues.append('VML button missing')
    if 'smarttasker.id/assets/images/logo.png' not in html: issues.append('logo missing')
    if '2026' not in html: issues.append('copyright year missing')
    if issues:
        print(f'{fname} ISSUES: {issues}')
    else:
        print(f'{fname}: all checks passed')
