<?php
return [
    'title' => 'Why Data Encryption Matters',
    'seo_title' => 'Why Data Encryption Matters: In Transit, at Rest, and Keys',
    'meta_description' => 'Distinguish transport encryption, disk encryption at rest, and end-to-end encryption by threat scenario; poor key and recovery handling can nullify strong-looking protection. Practice backup and recovery, then verify the result.',
    'content_html' => <<<'HTML'
<p>Encryption turns readable information into a form only key holders can restore. It is neither magic nor a cure-all: different scenarios need different mixes of transport encryption, encryption at rest, and end-to-end encryption.</p>
<h2>Three problems, three answers</h2>
<p>Eavesdropping in transit is mitigated by TLS/HTTPS; device loss or discarded drives are protected by disk and backup encryption; if you want cloud providers unable to read chat content, you need <a href="/articles/what-is-end-to-end-encryption">end-to-end encryption</a>.</p>
<h2>Keys and recovery matter equally</h2>
<p>Losing the key equals losing the data. Password-manager master passwords, BitLocker recovery keys, and 2FA backup codes deserve secure storage points—like photocopies of a deed—not only a memo on the same phone.</p>
<h2>Correcting misconceptions</h2>
<ul>
<li>“The company can recover my email” means it is not end-to-end; separate compliance from privacy.</li>
<li>Full-disk encryption does not stop phishing; malware reads plaintext before encryption.</li>
<li>Aging algorithms (such as short-key RSA) should be retired as systems upgrade.</li>
</ul>
<p>Transport-layer detail: <a href="/articles/network-traffic-encryption">network traffic encryption</a> and <a href="/articles/what-is-https">HTTPS basics</a>.</p>
<h2>The three-copy backup rule</h2>
<p>One local encrypted copy, one offline medium, and one cloud copy are different recovery paths. Encrypting without sync still hurts when the drive dies; syncing without encryption becomes risk when cloud policy changes.</p>
<h2>Exporting chat history</h2>
<p>Exporting to cleartext CSV breaks the previous E2EE protection boundary. Encrypt export files separately and delete temporary copies before sharing.</p>
<h2>Law and enterprise compliance</h2>
<p>Companies can decrypt work email; employees should not put personal health and similar topics in non-E2EE enterprise tools. Individuals control their own key material.</p>
<h2>Hardware security modules</h2>
<p>TPM or a secure enclave binds disk keys to the boot chain. Before selling a used motherboard, revoke platform keys at the firmware layer.</p>
<h2>Email delivery encryption</h2>
<p>Standard SMTP usually has no end-to-end protection; encrypt sensitive attachments separately before sending—do not assume “Sent” means confidential.</p>
<h2>Legal and regulatory requests</h2>
<p>Cloud vendors that encrypt data at rest may still decrypt and hand it over under legal process. Sensitive projects should use client-side encryption with self-controlled keys—and accept that this always conflicts with convenience.</p>
<p>After printing confidential contracts, a shredder matters as much as digital wipe; paper is an often-overlooked offline leak path.</p>
<h2>Ransomware and backups</h2>
<p>Ransomware encrypts cleartext backups sitting in online sync folders. Under the 3-2-1 rule, at least one offline immutable backup lets encryption serve recovery instead of becoming a single point of failure.</p>
<p>Photojournalists who hand camera cards straight to a print shop are handing over unencrypted data at rest. Archive high-value material encrypted on a laptop first, then send selects—more proactive than regretting cloud previews later.</p>
<p>Open-source project private keys on an unencrypted laptop collapse the signing trust chain if a CI image is exfiltrated. Keep developer hardware keys separately.</p>
<p>Mixing Time Machine and cloud drive into one backup lets ransomware take everything. Pull the offline drive once a week so encrypted disks are truly recoverable.</p>
HTML,
    'faq_json' => '[{"q":"Is built-in cloud-drive encryption enough?","a":"It depends on the threat model; to keep cloud operators from reading content you need client-side encryption or E2EE messaging."},{"q":"BitLocker vs VeraCrypt?","a":"The former integrates deeply with Windows; the latter is cross-platform but requires you to manage boot configuration more carefully."},{"q":"Does encryption slow performance?","a":"With modern hardware acceleration most users notice nothing; large files on old devices may be slightly slower."}]',
];
