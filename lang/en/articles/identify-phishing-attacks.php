<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>Phishing exploits your reaction speed more than a pure technical bug. An urgent email or a spoofed SMS aims to make you hand over credentials or a verification code before you verify.</p>
<h2>Channels and scripts</h2>
<p>Macro-laden email attachments, fake invoice PDFs, IM impersonating support, and “boss needs a payment” social engineering are all broad phishing. Business email compromise (BEC) may spoof lookalike domains of real organizations.</p>
<h2>Recognition anchors</h2>
<ul>
<li>Whether the From domain matches Reply-To.</li>
<li>Whether the hover URL matches the link text.</li>
<li>Whether the message asks for OTP, recovery codes, or remote-desktop access.</li>
</ul>
<h2>Response flow</h2>
<p>Do not click login links inside the email; use the official app instead. If you already entered a password, change it immediately and sign out other sessions. For payment-instruction changes, confirm on a second channel.</p>
<p>On the web: <a href="/articles/identify-malicious-websites">malicious websites</a>; for accounts: <a href="/articles/protect-online-accounts">online accounts</a> and <a href="/articles/two-factor-authentication-guide">2FA</a>.</p>
<h2>Deepfake voice</h2>
<p>AI-synthesized boss voices urging wire transfers already make the news. For large amounts, call back a known landline or confirm in person—do not transfer on instruction alone.</p>
<h2>Calendar-invite spam</h2>
<p>Auto-accepting meeting invites can plant phishing links in your calendar, where phone notifications are more visible than email. Turn off auto-add for unknown invites.</p>
<h2>Attachment macros and OneNote</h2>
<p>Attack chains embed scripts in notes to bypass mail gateways. Open unfamiliar attachments only in an isolated VM—or not at all.</p><h2>Gift-card scripts</h2><p>“Your boss wants Apple gift cards” is a classic BEC play. Real company purchasing does not ask for card numbers and PINs over instant messaging.</p><h2>QR codes in attachments</h2><p>QR codes inside PDFs bypass email link scanners. Before scanning with a phone, confirm the expected sender really issued that file.</p><h2>Recruiting phishing</h2><p>Fake recruiters asking for ID and bank details to “open a payroll account” are often money-laundering fronts. Legitimate processes collect documents only after background checks and through an encrypted onboarding portal.</p><p>For “tax authority” voice calls, hang up and dial the official hotline yourself—do not call back the number on caller ID.</p><h2>Courier “collect on delivery”</h2><p>SMS claiming a parcel needs a paid QR scan is often a phishing site. Check status in the official courier app; do not pay via unknown QR codes.</p><h2>Scholarship scams</h2><p>Prospective students get “Ministry of Education scholarship” links asking for bank cards—official-sounding details that do not check out. Compare against the education authority’s published lists; do not tap broadcast QR pushes.</p><p>University-mailbox “scholarship disbursement” phishing spikes at term start. Real funds go through school finance systems and never ask you to WeChat-scan a “processing fee.” Confirm by phone with the finance office first.</p><p>Real HR background-check firms call from landlines and provide a website verification path; they do not ask for ID over Telegram. Hang up on unknown IM claiming to be screening.</p><p>For voicemails about “courier refunds,” look up the tracking number in a separate official app. Do not let urgency push you to type a card number on a noisy subway.</p><p>When sending sensitive attachments from a work mailbox, use an encrypted portal link and verbally confirm a one-time passphrase by phone.</p><p>Treat curiosity kindly: one extra hover check is harmless.</p><p>If a fake “police” call claims you are laundering money, verify in person at the nearest station window.</p>
<p>Further reading: <a href="/articles/common-cybersecurity-myths">cybersecurity myths</a>.</p>
HTML;
return [
  'title' => 'How to recognize phishing attacks',
  'seo_title' => 'How to spot phishing: message patterns and response steps',
  'meta_description' => 'Phishing tactics in email and SMS, including fake payment instructions: never log in from links inside messages, confirm account or wire changes on a second channel, and never read verification codes aloud to callers—then verify the outcome once.',
  'content_html' => $content,
  'faq_json' => '[{"q":"Is a phishing email safe once it is in spam?","a":"You can still mis-click. Train yourself never to log into any service from the spam folder."},{"q":"Can 2FA stop phishing?","a":"FIDO2/passkeys reduce risk significantly; SMS codes can still be forwarded in real time."},{"q":"Why report phishing?","a":"It helps platforms block infrastructure and trains you to review the telltale signs."}]',
];
