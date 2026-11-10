<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>Lookalike sites increasingly resemble the real ones: colors, logos, even the padlock are easy to copy. HTTPS only encrypts traffic between you and the domain in the address bar—it does not prove that domain belongs to the brand you think.</p>
<h2>The domain is the first evidence</h2>
<p>Watch for lookalike characters: Latin l vs digit 1, Cyrillic а vs Latin a. Do not click “Log in” from email; open bookmarks or the official app instead.</p>
<h2>Page behavior signals</h2>
<ul>
<li>Pop-ups that demand installing a browser extension or root certificate as soon as the page opens.</li>
<li>Requests for SMS codes, card CVV, or recovery phrases.</li>
<li>Countdown scare tactics: “Your account freezes in 30 minutes.”</li>
</ul>
<h2>Certificates and redirect chains</h2>
<p>The certificate subject should match the address bar; stop typing if you see a warning. Short links and QR codes can bypass visual checks—before paying, search the official store for the app.</p>
<p>For social-engineering angles, read <a href="/articles/identify-phishing-attacks">phishing recognition</a>; for the transport layer, read <a href="/articles/what-is-https">what HTTPS proves</a>.</p>
<h2>Supply-chain tampering</h2>
<p>When a legitimate site is compromised, the padlock can still show. Watch extension prompts, sudden update frames, and layouts that do not match the usual page.</p>
<h2>Search-engine ad slots</h2>
<p>Brand-term search ads often link to lookalike domains and sit above organic results. Check the URL before clicking—not just the brand words in the title.</p>
<h2>WebView shells</h2>
<p>Fraud apps embed a browser that loads a fake bank page; the address bar may be hidden. For high-sensitivity actions, stick to the official standalone app or bookmark entry—see <a href="/articles/protect-mobile-data">mobile protection</a>.</p>
<h2>Internationalized domain fraud</h2>
<p>Punycode lets Cyrillic letters look like Latin domains. Use the browser’s “show original” option and leave immediately if you see odd characters.</p>
<h2>Free SSL automation</h2>
<p>Let’s Encrypt lowers the HTTPS barrier—and lets scammers get certificates cheaply. Domain verification always comes before the padlock.</p>
<h2>Comment bait</h2>
<p>Suddenly, a normal forum fills with praise replies sharing the same download short link—often paving the way for malware packages. Avoid “crack / patch” sites; use official update channels.</p>
<p>Promo SMS short domains appear by the thousands during campaigns and are hard to tell apart at a glance; shopping is safer if you type the official site yourself.</p>
<h2>Web3 phishing</h2>
<p>Fake wallet connect pages mimic MetaMask pop-ups and push unlimited approvals. Connect DApps only from the extension’s own entry points; refuse floating “one-click connect” overlays.</p>
<p>“Your PC is infected—call this hotline” pop-ups are pure social engineering. Real systems do not use a full-screen browser page to demand a phone call; end the process and close the tab in Task Manager.</p>
<p>When a fake “system update” page asks you to download an .msi, compare against Microsoft cumulative patch numbers. Real OS updates go through Settings—not random domains.</p>
<p>Turn on “always show the full URL” in the address bar so shortened nickname domains cannot hide, and pasted-together lookalike subdomains become obvious.</p>
<p>Export and back up bookmarks regularly so a malicious extension cannot quietly rewrite entries.</p>
<p>If a strange page asks you to dial for help, hang up every time.</p>
HTML;
return [
  'title' => 'How to identify malicious websites',
  'seo_title' => 'How to identify malicious websites: domain, certificate, and language signals',
  'meta_description' => 'Spot spoofed and malicious sites via domain spelling, certificate subject, scare tactics, and install prompts—and remember the HTTPS padlock does not prove brand trust. When unsure, use the official app entry.',
  'content_html' => $content,
  'faq_json' => '[{"q":"Does a padlock mean it is the official site?","a":"No; anyone can get a certificate for their own domain—the padlock is not brand trust."},{"q":"Should I still visit if the browser warns of danger?","a":"Do not continue; it may be expired, mismatched, or tampered with by a man-in-the-middle."},{"q":"Are links inside PDF invoices trustworthy?","a":"Same risk as email links; verify the domain before entering credentials."}]',
];
