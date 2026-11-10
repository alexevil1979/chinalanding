<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>In modern threat models a strong password means “long enough, unique per site, and stored safely.” A complex but reused eight-character password has almost no defense against breach dumps.</p>
<h2>Length beats fancy composition</h2>
<p>Current NIST guidance emphasizes length and usability over mandatory periodic rotation without cause. A random string of 16+ characters or a passphrase of 4–5 random words usually beats a short password stuffed with special symbols.</p>
<h2>What a password manager does</h2>
<p>It generates, autofills, and encrypts entries; you only need one strong master password plus its 2FA. Never screenshot the vault or email the database in cleartext.</p>
<h2>After a breach</h2>
<p>When one site is breached, changing only that password is not enough—check whether the same password was reused elsewhere. A compromised hub email should trigger a full rotation.</p>
<p>Next: <a href="/articles/two-factor-authentication-guide">two-factor authentication</a>, <a href="/articles/protect-online-accounts">account protection</a>, and <a href="/articles/identify-phishing-attacks">watching for phishing that asks for the master password</a>.</p>
<h2>Memorable passphrases</h2>
<p>Random word strings with digit separators balance length and typing speed. Avoid famous quotes and song lyrics—corpus attacks already include popular lines.</p>
<h2>Security-question traps</h2>
<p>“Mother’s maiden name” is often searchable on social media. For site security questions, store random strings in the password manager instead of truthful answers.</p>
<h2>Enterprise SSO</h2>
<p>Company single sign-on feeds downstream apps; you still need the strongest factors on the SSO primary account. One breach can take the whole line down.</p><h2>Keyboard layout</h2><p>Rare symbols are easy to mistype across devices. Passphrases built from common-layout words reduce mobile friction.</p><h2>Hardware token backups</h2><p>Keep two physical U2F keys in different places; losing one should not lock you out entirely.</p><h2>Hash-breach timelines</h2><p>Site dumps sometimes surface years later while you still trust an “old” password. Treat hub accounts as if they may already appear in unknown breach sets—even if you have not rotated in years.</p><p>Password managers with breach monitoring (Have I Been Pwned–style) help you rotate on a schedule.</p><h2>Built-in browser suggestions</h2><p>Chrome and Safari random-password features are convenient but ecosystem-locked. Decide whether you accept that lock-in before migrating to a standalone manager.</p><h2>IME cloud sync</h2><p>Mobile input methods that sync personal dictionaries to the cloud may send account fragments to a server. For sensitive logins, switch to a temporary offline keyboard.</p><p>Old policies that force a change every three months push people to increment a trailing digit. Even after policy reform, attackers still predict that pattern. Prefer manager-generated random strings and rotate only when a site is breached.</p><p>A shared “project password” in a team doc means every ex-member still holds a root key until removed. Use invite-based accounts and separate password entries instead.</p><p>A sticky note with the master password on the keyboard is often seen by cleaning staff first. Put credentials in the manager; paper should only hold non-master emergency contact numbers.</p><p>Forgetting the master password locks the vault—rehearse recovery at least once.</p><p>Before exporting the vault, confirm nobody is shoulder-surfing.</p>
<p>Further reading: <a href="/articles/common-cybersecurity-myths">common security myths</a>.</p>
HTML;
return [
  'title' => 'How to create strong passwords',
  'seo_title' => 'How to create strong passwords: length, uniqueness, and managers',
  'meta_description' => 'Why length and per-site uniqueness matter, how password managers generate and store entries, and how to prioritize hub accounts like email after a breach hit—reused short passwords are the most common failure; verify the outcome once.',
  'content_html' => $content,
  'faq_json' => '[{"q":"Is writing passwords in a notebook OK?","a":"Acceptable if physical access is controlled and it is not stored with the computer; a password manager is still preferable."},{"q":"Must I change passwords every three months?","a":"Forced rotation without breach evidence often produces weaker passwords; focus on uniqueness and length."},{"q":"Do biometrics replace passwords?","a":"They mostly unlock a local vault; remote accounts still need independent credentials."}]',
];
