<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>End-to-end encryption (E2EE) means content is encrypted on the sender’s device and decrypted only on the recipient’s device; by design the messaging provider cannot obtain plaintext. Cloudflare distinguishes this from “encryption in transit only,” where TLS often terminates at a server that then sees plaintext. E2EE addresses <strong>server-side reading of content</strong>, not invisibility that “communication never happened.”</p>
<h2>Key differences from HTTPS/TLS</h2>
<p>On an HTTPS site, TLS protects the browser-to-server path; the server must decrypt HTTP to render pages, index search, or fight spam. Instant messaging, some mail, and file-sync products keep long-term key material on user devices and forward ciphertext. In practice you often see <strong>two layers</strong>: an E2EE message body still delivered over TLS to the server. Understanding the layers prevents treating a “locked webpage” as “the carrier cannot read the chat.” See <a href="/articles/what-is-https">HTTPS</a> and <a href="/articles/network-traffic-encryption">network traffic encryption</a>.</p>
<h2>Keys, identity, and verification</h2>
<p>Mature E2EE designs offer security codes or fingerprint comparison to detect man-in-the-middle key substitution. Multi-device login must safely distribute or derive session keys on new devices; remote logout and key rotation after device loss decide whether “end-to-end” still holds the moment you lose a phone. NIST cryptography materials stress key lifecycle management as much as algorithm choice.</p>
<h2>What metadata still leaks</h2>
<p>Even when bodies are unreadable, operators often still hold account identifiers, who talks to whom, timestamps, message length or frequency, and device type. Traffic analysis can still draw social graphs for well-resourced adversaries. E2EE does not erase observation of “who speaks with whom”; it removes <strong>what was said</strong> from the operator’s view (when implemented correctly and without backdoors).</p>
<h2>Endpoints and human factors</h2>
<p>Screen photography, coerced unlocks, endpoint malware, and backups to non-E2EE cloud storage open leak paths outside the crypto. If the peer’s device is compromised, plaintext you send them can still be read. EFF’s “communicating with others” guidance reminds us cryptography assumes honest, uncompromised endpoints.</p>
<h2>Backup and multi-device traps</h2>
<p>Many products offer “cloud chat backup” for phone swaps. If the backup is not also end-to-end encrypted—or if backup keys are vendor-hosted—then <strong>history</strong> may become plaintext on servers. Before buying, read the white paper: is E2EE default, do backup keys live only on your devices, and does turning E2EE off break features?</p>
<h2>How to read product claims</h2>
<ul>
<li>Default on or optional? Can you tell when it is off?</li>
<li>Do groups, calls, and files share the same encryption model?</li>
<li>Is there an independent audit or an open-source client with reproducible builds?</li>
<li>How long is metadata retained, and can it be compelled by law enforcement?</li>
</ul>
<p>Evaluation dimensions appear in <a href="/articles/choose-privacy-tools">how to choose privacy tools</a>.</p>
<h2>Lawful access and product architecture</h2>
<p>National laws may require providers to assist with metadata or specific content disclosure; E2EE architecture (client-side encryption, key escrow) decides whether a request is technically feasible. Public materials from Signal, WhatsApp, and others discuss this to varying degrees—read transparency reports rather than “unbreakable” ads alone.</p>
<h2>Do groups and calls share the same model?</h2>
<p>Group key rotation and voice/video key-agreement paths may not upgrade in lockstep with text. If release notes say “chat E2EE” but omit group voice, ask support for a technical note. Federated interop also expands the trust anchor to third-party servers and widens security-code check scope.</p>
<h2>Forwarded screenshots and notification previews</h2>
<p>Once a message decrypts on-device, notification previews, recent-task thumbnails, and chat screenshots in cloud photo albums punch E2EE into the physical world. Disabling sensitive-thread previews and blacklisting screen sharing matter as much as enabling E2EE. If a work phone forces MDM backups, confirm the backup chain still matches your personal confidentiality expectations.</p>
<h2>Attacks E2EE does not directly stop</h2>
<p>Phishing for codes, fake support asking for recovery codes, passwords typed on fake login pages—these happen outside the E2EE channel. Account hardening still depends on strong passwords, two-factor authentication, and anti-phishing habits.</p>
<p>After this article, record chat and web browsing threats separately: messaging apps against E2EE white papers, site logins against HTTPS and domain checks—avoid covering every scenario with one tool name.</p>
HTML;
return [
  'title' => 'What is end-to-end encryption',
  'seo_title' => 'What is end-to-end encryption: differences from TLS and limits',
  'meta_description' => 'How end-to-end encryption keeps providers from reading message bodies, how that differs from TLS protecting only transit, and residual risks from metadata, compromised endpoints, multi-device sync, and cloud backup channels.',
  'content_html' => $content,
  'faq_json' => '[{"q":"With E2EE, does the operator see nothing at all?","a":"They usually still process metadata and account data; the exact scope depends on the product and applicable law—read official security docs."},{"q":"Why verify security codes?","a":"To detect man-in-the-middle key substitution, especially on first contact or after a contact’s key changes."},{"q":"Does E2EE prevent phishing?","a":"No. Phishing happens in the browser or through social deceit; verify entry points and domains."},{"q":"Is E2EE still effective with cloud backup on?","a":"Only if the backup is also end-to-end encrypted; vendor-hosted backup keys change the threat model."}]',
];
