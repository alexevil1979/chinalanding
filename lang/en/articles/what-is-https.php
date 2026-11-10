<?php
return [
    'title' => 'What HTTPS Is and What It Does',
    'seo_title' => 'What HTTPS Is: TLS, Certificates, and What It Cannot Prove',
    'meta_description' => 'Explain how the TLS handshake and certificate-chain validation in HTTPS protect confidentiality and integrity in transit, clarify what the lock icon and domain match mean, and note that HTTPS neither proves operator honesty nor hides DNS queries.',
    'content_html' => <<<'HTML'
<p>HTTPS is HTTP running over TLS (Transport Layer Security): the browser and server complete a handshake and certificate validation, then encrypt page, form, and API data. MDN summarizes it as the secure version of HTTP; the core benefit is <strong>protecting against path eavesdropping and tampering</strong>, and—when validation succeeds—confirming you are talking to the domain bound in the certificate.</p>
<h2>What the TLS handshake does</h2>
<p>A typical flow: the client advertises supported protocol versions and cipher suites; the server presents a certificate chain; the client checks that the chain leads to a trusted root and that the certificate domain matches the address bar; both sides negotiate a symmetric session key and encrypt subsequent data with AEAD (or similar). TLS 1.3 (RFC 8446) shortens handshake round trips and removes many insecure options. NIST SP 800-52 continuously updates guidance on how government systems should configure TLS.</p>
<h2>What a certificate proves</h2>
<p>A public CA certificate means some entity controlled the SAN/CN domains listed and passed domain validation. Success means <strong>the encrypted channel leads to that domain</strong>—not that “this domain must be your bank.” A phishing site that controls a lookalike domain can also obtain a valid certificate. The OWASP transport cheat sheet stresses: TLS is a confidentiality and integrity control, not a business trust seal.</p>
<h2>Treat certificate warnings seriously</h2>
<p>Name mismatch, incomplete chain, expiry, or MitM replacement triggers a browser block or warning. Continuing then means voluntarily accepting an unknown certificate; passwords and payment data may flow to an attacker. Enterprise networks that deploy a private CA require employee devices to explicitly trust that root—a different trust model from public PKIX. Lookalike sites often copy visuals while changing one character in the domain; check the address bar first.</p>
<h2>What HTTPS protects and does not</h2>
<ul>
<li><strong>Protects:</strong> path adversaries struggle to read or alter HTTP content and most cookies (when attributes such as <code>Secure</code> are set correctly).</li>
<li><strong>Does not protect:</strong> plaintext handling, logs, and lawful requests on the server; data you type yourself into a fake site.</li>
<li><strong>Does not replace:</strong> endpoint malware, social phishing, or weak passwords.</li>
<li><strong>Does not hide:</strong> DNS query records, the source IP the server sees, visit times, and URL paths (in server logs).</li>
</ul>
<h2>Relation to VPN and E2EE</h2>
<p>HTTPS protects the <strong>browser-to-website</strong> hop; a VPN encapsulates <strong>system-level IP traffic</strong> to the tunnel endpoint; end-to-end encryption keeps the server from reading message bodies. They can stack but have different boundaries. Layered explanation: <a href="/articles/network-traffic-encryption">network traffic encryption</a>.</p>
<h2>Mixed content and HSTS</h2>
<p>An HTTPS page that loads HTTP subresources may trigger mixed-content blocking or weaken protection. An HSTS response header tells browsers to use only HTTPS for the site within a period, reducing sslstrip-style downgrade risk—but a bad deploy can lock you into a broken config, so validate on a test domain first. HTTP/2 and HTTP/3 multiplex connections over TLS, cutting handshakes—especially helpful on lossy mobile networks.</p>
<h2>OCSP and Certificate Transparency</h2>
<p>Browsers rely on revocation status and Certificate Transparency logs to spot anomalous issuance. Everyday users need not query CT by hand, but should know: <strong>a valid certificate</strong> answers the cryptographic path and domain binding—not who the site operator is. After an enterprise transparent proxy installs a root CA on a managed device, the lock icon still appears, yet decryption may occur at the company gateway—keeping work laptops and personal banking on separate devices is a safer split.</p>
<h2>Use on public networks</h2>
<p>On untrusted Wi‑Fi, HTTPS is the floor for browsing and login; still verify the domain and watch for captive-portal certificate forgeries. DNS path issues: <a href="/articles/what-is-dns-leak">DNS leaks</a>; for system-level path hardening, understand the added role of a <a href="/articles/what-is-vpn">VPN</a>.</p>
<h2>Cookies and security attributes</h2>
<p>Sites can set <code>Secure</code>, <code>HttpOnly</code>, and <code>SameSite</code> on cookies to reduce hijack or cross-site abuse outside HTTPS. Servers issue these flags; browsers enforce them—users cannot compensate for missing config by “feeling safe.” Once a login session exists, the server may still log activity by policy; that does not contradict TLS.</p>
HTML,
    'faq_json' => '[{"q":"Does the address-bar lock mean this is definitely the official site?","a":"No. The lock means a valid TLS session with the current domain—not brand ownership or a fraud-free page."},{"q":"Can I browse daily with a self-signed certificate?","a":"Only in explicitly trusted intranet or test environments; public sites should use a trusted CA, otherwise you should see a warning."},{"q":"Does HTTPS make websites slower?","a":"On modern hardware with HTTP/2 and HTTP/3 the overhead is small; security gains usually far outweigh latency cost."},{"q":"With HTTPS, do I still need to care about DNS?","a":"Yes. TLS does not encrypt DNS queries; the resolution path remains a separate exposure surface."}]',
];
