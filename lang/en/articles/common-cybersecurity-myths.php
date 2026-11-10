<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>Security explainers are full of shortcuts that “sound right” yet fail against social engineering or bulk attacks. The eight myths below keep resurfacing in Chinese-language communities; each one is split into misconception—reality—mechanism—example—action so you can check your own devices and accounts instead of memorizing a slogan.</p>
<h2>1 Complex passwords do not solve everything</h2>
<h3>Common misconception</h3>
<p>The more complex the password, the better—other protections are optional.</p>
<h3>Reality</h3>
<p>Even a long passphrase cannot stop you from typing it into a fake page, and it cannot fix passwords reused after a dump. A compromised hub account can reset other services in a chain.</p>
<h3>Technical explanation</h3>
<p>Offline cracking speed depends on the hash algorithm and leak shape, but credential stuffing reuses plaintext pairs directly. NIST SP 800-63B stresses length, uniqueness, and breach response—not meaningless frequent rotation.</p>
<h3>Real-world example</h3>
<p>After a forum database leak, attackers tried the same email–password pair on mail and payment platforms—special characters in the password were irrelevant.</p>
<h3>What users should do</h3>
<p>Use unique long passphrases from a password manager for hub email and financial accounts, and enable <a href="/articles/two-factor-authentication-guide">two-factor authentication</a>; when you get a breach notice, prioritize sites that reused the password. Weaker sites can keep independent passwords—do not sacrifice manageability for “fancy” complexity.</p>
<h2>2 HTTPS does not mean a site is trustworthy</h2>
<h3>Common misconception</h3>
<p>A padlock in the address bar means it is the official site and not a fake.</p>
<h3>Reality</h3>
<p>TLS only protects confidentiality and integrity between you and the domain in front of you; it does not audit the operator’s identity or stop malicious scripts on the page.</p>
<h3>Technical explanation</h3>
<p>Any entity that controls a domain can obtain a public CA certificate. A valid certificate only means the link matches that domain—see <a href="/articles/what-is-https">HTTPS boundaries</a>.</p>
<h3>Real-world example</h3>
<p>Searching a brand term, an ad slot uses a lookalike domain with a valid certificate, yet the form sends credentials to the attacker’s server.</p>
<h3>What users should do</h3>
<p>Enter high-value logins from bookmarks or the official app; before paying, check domain spelling—do not judge by the padlock alone.</p>
<h2>3 A VPN is not absolute anonymity</h2>
<h3>Common misconception</h3>
<p>Turn on a VPN and nobody knows who you are or which sites you visited.</p>
<h3>Reality</h3>
<p>A tunnel changes path and exit IP; account cookies, device fingerprints, payment links, and metadata visible to the provider remain.</p>
<h3>Technical explanation</h3>
<p>A VPN encapsulates traffic at the IP layer; the operator decrypts and forwards at the exit. Timing, volume, and destination metadata may still be logged or inferred. If the client is malware-laced or replaced with a tampered build, the tunnel becomes an exfiltration channel rather than a shield. See <a href="/articles/what-is-vpn">how VPN works</a>.</p>
<h3>Real-world example</h3>
<p>A user enables a commercial VPN but still signs into the same Google account—ad and risk profiles stay highly continuous with the untunneled state.</p>
<h3>What users should do</h3>
<p>Write a threat model first: stopping path eavesdropping and stopping account correlation are different goals; separate browser profiles and review VPN jurisdiction and client provenance.</p>
<h2>4 Antivirus cannot stop every threat</h2>
<h3>Common misconception</h3>
<p>Installing a suite means you are immune.</p>
<h3>Reality</h3>
<p>Zero-days, fileless attacks, social engineering, and malicious extensions often bypass expected signature databases.</p>
<h3>Technical explanation</h3>
<p>Endpoint protection combines heuristics, behavior monitoring, and system integrity—but it cannot replace patch management and least privilege. CISA baseline practices list patching, backups, and least privilege together—not antivirus alone.</p>
<h3>Real-world example</h3>
<p>After a user allows “remote assistance,” an attacker operates the desktop and transfers money; antivirus never fires because the remote session is legitimate.</p>
<h3>What users should do</h3>
<p>Keep automatic system updates on; refuse unknown macros and installers from unclear sources; do not perform high-sensitivity actions on a machine that has already been asked for remote control.</p>
<h2>5 Private browsing does not hide you from the carrier</h2>
<h3>Common misconception</h3>
<p>An incognito window keeps the ISP and Wi-Fi operator from seeing what you visit.</p>
<h3>Reality</h3>
<p>Private mode mainly avoids keeping local history and some cookies; the link layer and recursive DNS still see connections and queries (unless you separately configure encrypted DNS and a tunnel).</p>
<h3>Technical explanation</h3>
<p>Private browsing does not encrypt metadata outside the IP payload; after you sign in, the server still records activity. Carriers and gateways still see which IPs you reach, when, and roughly how much traffic. See <a href="/articles/how-online-tracking-works">online tracking</a> and <a href="/articles/what-is-dns-leak">DNS paths</a>.</p>
<h3>Real-world example</h3>
<p>A café network admin sees news domains visited in an incognito session in gateway logs—incognito is irrelevant.</p>
<h3>What users should do</h3>
<p>Split sensitive browsing by scenario: no local traces ≠ link anonymity; when you need link protection, combine HTTPS with a trusted tunnel, and move high-sensitivity tasks to cellular.</p>
<h2>6 Two-factor authentication lowers risk but does not erase phishing</h2>
<h3>Common misconception</h3>
<p>With 2FA on, you cannot be tricked.</p>
<h3>Reality</h3>
<p>SMS and TOTP can still be relayed in real time on a phishing page; push-approval “fatigue clicking” can fool the user themselves.</p>
<h3>Technical explanation</h3>
<p>FIDO2/passkeys bind to the site origin and strongly resist relay phishing; classic OTP lacks that domain binding. OWASP authentication guidance stresses choosing factor strength by asset value.</p>
<h3>Real-world example</h3>
<p>A lookalike login page forwards the six-digit TOTP the user typed to the real site and hijacks the session.</p>
<h3>What users should do</h3>
<p>Prefer hardware keys or domain-verifiable WebAuthn for finance and email; for push logins, check location and app name item by item and reject unfamiliar approvals.</p>
<h2>7 Updates really matter</h2>
<h3>Common misconception</h3>
<p>People who “never get infected” can postpone updates indefinitely.</p>
<h3>Reality</h3>
<p>Public CVEs and in-the-wild exploits do not pick careful users; OS, browser, and firmware patches close known holes—they are not decoration.</p>
<h3>Technical explanation</h3>
<p>Attack chains often enter through outdated components, then move laterally to credentials and data. NIST and CISA repeatedly list timely patching among the lowest-cost defenses.</p>
<h3>Real-world example</h3>
<p>Unpatched router flaws stay on botnet scan lists for a long time—whether the owner “browses carefully” is irrelevant.</p>
<h3>What users should do</h3>
<p>Enable automatic security updates; put routers and NAS on the same patch cadence as phones; after major vulnerability news, check your own device models first. Retiring IoT firmware that is no longer maintained is more realistic than clinging to “I never click links.”</p>
<h2>8 Backup is not the same as sync</h2>
<h3>Common misconception</h3>
<p>Files in a cloud sync folder equal a backup.</p>
<h3>Reality</h3>
<p>Sync mirrors accidental deletes and ransomware encryption; true recoverability needs version history, offline copies, and periodic restore drills.</p>
<h3>Technical explanation</h3>
<p>Backup emphasizes point-in-time recoverability and immutable copies; sync emphasizes multi-device consistency. Ransomware encrypts plaintext files in online sync folders so the “backup” fails too. Version retention and object lock (WORM) are different cloud capabilities—read retention days before you buy.</p>
<h3>Real-world example</h3>
<p>A user deletes a project folder; cloud sync deletes it everywhere immediately; without version history it is gone.</p>
<h3>What users should do</h3>
<p>Apply 3-2-1 to critical data: at least one offline or immutable copy; periodically test restoring a small file; client-encrypt confidential material before upload.</p>
<p>These eight layers stack: transport encryption protects the link, account hardening protects identity, patches and backups protect availability. More account habits: <a href="/articles/protect-online-accounts">protecting online accounts</a> and <a href="/articles/identify-phishing-attacks">recognizing phishing</a>; for public networks, see <a href="/articles/public-wifi-safety">public Wi-Fi safety</a>.</p>
HTML;
return [
  'title' => 'Common cybersecurity myths',
  'seo_title' => 'Common cybersecurity myths: eight checkable facts',
  'meta_description' => 'Eight myths unpacked—complex passwords, HTTPS, VPN anonymity, antivirus silver bullets, private browsing, 2FA, system updates, and cloud sync as backup—each with misconception, mechanism, and a concrete check against your accounts and devices.',
  'content_html' => $content,
  'faq_json' => '[{"q":"Does the HTTPS padlock prove a site is the brand’s official site?","a":"No. The padlock only means a valid TLS session with the address-bar domain—not operator identity."},{"q":"Why still care about login accounts after enabling a VPN?","a":"A VPN mainly changes the network path; sites can still identify you via cookies and accounts."},{"q":"Is SMS two-factor authentication strong enough?","a":"Better than a single factor, but it can be relayed in real-time phishing; high-value accounts should upgrade toward FIDO2-class factors."},{"q":"Does a cloud sync folder count as a backup?","a":"Not a complete backup; deletes and ransomware propagate—you need versions and offline copies."}]',
];
