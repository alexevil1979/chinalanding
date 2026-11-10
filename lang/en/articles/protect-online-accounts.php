<?php
return [
    'title' => 'How to Protect Your Online Accounts',
    'seo_title' => 'How to Protect Online Accounts: Passwords, Verification, and Session Hygiene',
    'meta_description' => 'Focus on hub accounts such as email and password managers: unique strong passwords, two-factor authentication, OAuth review, and mail-forwarding checks to limit cascade damage after a takeover—email compromise often hits the most services.',
    'content_html' => <<<'HTML'
<p>Most digital life orbits a few hub accounts: email, Apple ID/Google account, a password manager, and banking apps. Losing one of them often cascades through password resets and card bindings faster than losing a phone.</p>
<h2>Map the hubs first</h2>
<p>List the email addresses and phone numbers that can reset other passwords and treat them as first-tier protection targets. Secondary accounts can share password-manager entries, but they must not share the same password.</p>
<h2>Passwords, 2FA, and sessions</h2>
<ul>
<li>A unique long password per site, maintained with a <a href="/articles/create-strong-passwords">strong-password</a> policy and a password manager.</li>
<li>Enable <a href="/articles/two-factor-authentication-guide">two-factor authentication</a> for email and payments, and store recovery codes offline.</li>
<li>Periodically review signed-in devices; revoke unfamiliar OAuth grants and long-idle sessions.</li>
</ul>
<h2>Third-party login and mail rules</h2>
<p>Signing into third parties with Google/WeChat effectively loans out control. Check for rules like “forward to another address” and “silently delete via filters”—common backdoors after account takeover.</p>
<p>Also read <a href="/articles/identify-phishing-attacks">how to spot phishing</a> and <a href="/articles/protect-digital-identity">protecting digital identity</a>.</p>
<h2>The password-reset chain</h2>
<p>Many sites send recovery to email or SMS. If an attacker only cracks a secondary forum but you reused the email password, they can click “Forgot password” all the way to banking portals. Using a unique password even on forums is a low-cost, high-leverage habit.</p>
<h2>Isolate a security email</h2>
<p>Register a dedicated mailbox for high-value accounts—not for newsletters or giveaways—to reduce exposure in breach dumps. Use that mailbox only for login and recovery, not for everyday mail.</p>
<h2>Evidence after a takeover</h2>
<p>Keep phishing message originals plus anomalous login IPs and timestamps; they help accelerate unlock appeals. Read <a href="/articles/prevent-personal-data-leaks">breach containment</a> for next actions.</p>
<h2>Aggregated login risk</h2>
<p>“Sign in with WeChat” binds identity to a super-app. Periodically revoke unused aggregated authorizations older than a year to shrink ghost sessions.</p>
<h2>Login-notification habits</h2>
<p>Enable remote-login email alerts, but do not click confirmation links inside the mail; open the official app to review activity so forged messages cannot hijack the flow.</p>
<h2>Secondary mailbox strategy</h2>
<p>Use a separate mailbox for shopping sites; keep the primary mailbox for banking and cloud. Then forum passwords in breach dumps cannot credential-stuff back into the hub.</p>
<p>When you get a subject like “Your account will be frozen,” open a new browser tab and type the bookmarked official domain instead of clicking the link.</p>
<h2>Number retirement and SIM recycling</h2>
<p>After a phone number is canceled and recycled by the carrier, the next owner may receive SMS codes for your old accounts. Before changing numbers, rebind every site and watch for a week so no service is left behind.</p>
<p>Lending a video subscription login to colleagues at term’s end effectively shares the same session. If their device has malware, your viewing history and card bindings are exposed together. Buy subscriptions separately or use official family sharing—do not hand over the master password.</p>
<p>Put a backup contact phone in the hub mailbox signature; if you become unreachable, family with a paper record can help unlock accounts more reliably than word of mouth.</p>
<p>After you finish the account inventory, a quarterly spot-check is enough—no need for daily anxiety.</p>
<p>Further reading: <a href="/articles/zero-trust-security">zero-trust thinking</a>.</p>
HTML,
    'faq_json' => '[{"q":"Do all websites need two-factor authentication?","a":"At least cover email, the password manager, cloud storage, and financial accounts; expand to the rest by sensitivity."},{"q":"Should I turn off all third-party logins?","a":"Not necessarily with a hard cut, but regularly review the authorization list and remove unused apps."},{"q":"What if I get a login alert that was not me?","a":"Change the password immediately, sign out all sessions, and check whether mail forwarding and recovery phone numbers were altered."}]',
];
