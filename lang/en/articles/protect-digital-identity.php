<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>A digital identity is a puzzle of credentials scattered across services: email, phone number, ID scans, social-security identifiers, and payment bindings. Attackers care more about “can we assemble enough material to reset a password” than about breaking every system at once.</p>
<h2>How public information is stitched together</h2>
<p>A birthday on a resume, Weibo check-ins, an old forum nickname, and a password from a breach dump are often enough for a targeted customer-support scam.</p>
<h2>Shrink the puzzle surface</h2>
<ul>
<li>Hide phone numbers and exact birthdays on social accounts; put a company switchboard on resumes instead of a private number.</li>
<li>Upload ID photos only through official channels, then delete temporary local copies.</li>
<li>Enable strong authentication on core email and payment accounts—see <a href="/articles/protect-online-accounts">account protection</a>.</li>
</ul>
<h2>Recovery channels matter just as much</h2>
<p>Backup email, SIM, and security-question answers that are easy to guess become a shortcut around two-factor authentication. Periodically rehearse “how do I unlock the password manager if I lose my phone.”</p>
<p>On the data side, read <a href="/articles/prevent-personal-data-leaks">leak prevention</a> and <a href="/articles/identify-phishing-attacks">anti-phishing</a>.</p>
<h2>Family impersonation risk</h2>
<p>When relatives photograph both sides of an ID to run an errand, storing those shots in chat albums spreads uncontrolled copies. Ask them to delete after the task, and wipe local thumbnails too.</p>
<h2>Second-hand account markets</h2>
<p>Buying real-name game or social accounts can trigger platform risk controls and even pull you into fraud chains. Complete real-name verification yourself—do not buy an “already verified” identity.</p>
<h2>Credit freezes</h2>
<p>Requesting a security freeze at a credit bureau can block fraudulent loans after identity theft. Processes differ by country; the point is knowing this buffer exists.</p>
<h2>Metadata leaks</h2>
<p>Boarding-pass photos contain names and PNRs that can be used to phish airline support. Mosaic barcodes and document numbers when posting travel photos.</p>
<h2>E-signature habits</h2>
<p>If the phone number bound to an e-contract platform changes without an update, someone else may inherit signing rights. Update the signing profile before you switch numbers.</p>
<h2>Traces from government services</h2>
<p>Screenshots of online government portals include case numbers; forwarding them to family chats spreads traceable identifiers. Mask what you must, then delete temporary images from chat.</p>
<p>Combinations of student IDs, employee numbers, and access-card IDs are enough to impersonate an insider calling an IT hotline—avoid casually reading numbers aloud in social-engineering scripts.</p>
<h2>Genealogy data</h2>
<p>Genetic testing and family-tree sites aggregate near-kin relationships that social engineers can use to infer birthdays and mothers’ names. Narrow visibility before uploading and turn off public matching.</p>
<p>Marathon bib photos show names that, with public results databases, can locate social accounts. Cover the number in finish-line selfies—same joy, less material for strangers to assemble.</p>
<p>If a screen share in class shows a household-register scan thumbnail, the whole room sees it. Close unrelated tabs before sharing and leave only the current courseware window.</p>
<p>Company names on invoices help with expense claims, but personal shopping nicknames should avoid real full-name initials—fewer correlation signals if purchase records hit a breach.</p>
<p>If FAQ answers printed on a poster are searchable, do not reuse them as website recovery answers.</p>
<p>Do not casually share annual physical-exam report photos in the family group chat.</p>
<p>If someone posing as support tells you to “stay on the line,” hang up and call the official number to verify identity.</p>
HTML;
return [
  'title' => 'How to protect your digital identity',
  'seo_title' => 'How to protect digital identity: reduce exposure and stop impersonation',
  'meta_description' => 'How email, phone numbers, and ID images become social-engineering material—plus reducing public exposure, securing recovery channels, and priority steps when someone registers in your name. Less public data raises the cost of abuse.',
  'content_html' => $content,
  'faq_json' => '[{"q":"What if real-name verification is unavoidable?","a":"Disclose the minimum fields; check screenshots for watermarks or terms beyond what you need."},{"q":"Do alter-ego nicknames help?","a":"They can lower cross-platform correlation, but a login email can still bind the profile back."},{"q":"Someone registered a service in my name?","a":"Gather evidence, ask the platform to freeze the account, and change the hub email password."}]',
];
