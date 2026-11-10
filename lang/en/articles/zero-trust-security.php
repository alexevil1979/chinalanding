<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>Zero Trust is not another firewall SKU alias; it is a set of architecture principles: whether traffic comes from the corporate campus or home broadband, <strong>never trust by default</strong>—every access should be re-evaluated from identity, device posture, and context. NIST SP 800-207 defines continuous verification, least privilege, and assume breach. For individual readers, the point is translating slogans into daily habits—not buying an entire product line.</p>
<h2>Old assumptions it breaks</h2>
<p>Traditional models often treat “intranet = safe zone”: connect a VPN and browse the whole network laterally. After remote work and cloud SaaS, an attacker who steals a laptop session can move inside. Zero Trust instead asks: does this user, this device, and today’s risk signals justify access to <strong>this one</strong> resource? CISA’s Zero Trust maturity model describes enterprise stages; individuals can borrow the “identity / device / network” triad to organize home setup.</p>
<h2>Core practices (in plain language)</h2>
<ul>
<li><strong>Continuous verification:</strong> reconfirm before sensitive actions—not a single morning login that stays open all day.</li>
<li><strong>Least privilege:</strong> cloud links default to non-public; collaborative docs limited to named editors; IoT cameras must not reach NAS shares.</li>
<li><strong>Micro-segmentation:</strong> guest Wi‑Fi, smart appliances, and work PCs on separate SSIDs or VLANs so one compromise does not take everything.</li>
<li><strong>Context:</strong> when a new device signs into email, old devices should get an alert and a one-tap sign-out.</li>
</ul>
<h2>Personal examples</h2>
<p>At home: put IoT on an isolated router segment, change default passwords, and close WAN-side admin pages. For accounts: strongest 2FA on email and payments; unique passwords for ordinary forums. For sharing: contractor design links expire in seven days—not “anyone with the link can edit forever.” On public networks: use cellular for high-sensitivity work; a <a href="/articles/what-is-vpn">VPN</a> hardens the path layer but does not replace identity checks.</p>
<h2>What it is not</h2>
<p>Zero Trust does not mean MFA on every page refresh—it puts strong verification on high-value assets. Nor does sticking a “Zero Trust” label on an old VPN equal a completed migration; unclear policy only multiplies pop-ups without reducing over-privilege. Cloudflare Learning Center overviews stress principles over any single product.</p>
<h2>Relation to encryption layers</h2>
<p>Transport encryption (<a href="/articles/network-traffic-encryption">traffic encryption</a>, <a href="/articles/what-is-https">HTTPS</a>) protects the link; Zero Trust governs <strong>who may access which resource above that link</strong>. They complement each other. Before buying gateway products, make sure you can restate the policy in everyday language—marketing labels are not a shield that lets you skip password hygiene.</p>
<h2>Civilian conditional access</h2>
<p>Enterprise “conditional access” translates to: open the payroll spreadsheet only from a locked laptop whose patches are no more than 30 days old; if the phone is lost, remote-wipe the work profile. Individuals can approximate with separate browser profiles, distinct OS user accounts, and drive permissions limited to specific emails—without a full IAM platform. The core remains default-deny of excess rights.</p>
<h2>Continuous verification is not harassment</h2>
<p>Equating every refresh with a prompt to “continuous verification” makes households abandon the practice. More practical: keep financial sheets, will scans, and seed-phrase photos in separate accounts and devices; trigger second confirmation when opening them, while the news browser stays low-friction. Timing how many clicks a cold email-password reset takes is a simple yardstick for whether Zero Trust actually landed.</p>
<p>NIST documents use enterprise vocabulary, but “assume breach” also fits individuals: if a laptop is lost somewhere in the past, assume cloud share links may still be found—so default private and short-lived links are a home-executable Zero Trust version.</p>
<h2>Three small starting points</h2>
<ol>
<li>Turn off “anyone can edit / discover” defaults in cloud drives and collaboration tools.</li>
<li>Split accounts or browser profiles by purpose so one breach does not hit every service.</li>
<li>Quarterly, inventory signed-in devices and OAuth grants; revoke unknowns.</li>
</ol>
<h2>Lightweight practice for small teams</h2>
<p>A three-to-five-person studio need not buy a full SASE stack. Agree that finance sheets are email-restricted, revoke all external links on the day someone leaves, and keep company laptops full-disk encrypted with a five-minute auto-lock. If the identity provider already offers conditional access, separate personal Gmail from workday Microsoft login profiles to reduce session bleed. Zero Trust is iterative—not a one-shot “go-live complete.”</p>
HTML;
return [
  'title' => 'What is a Zero Trust security architecture',
  'seo_title' => 'What is Zero Trust security: principles individuals can apply',
  'meta_description' => 'A non-vendor view of Zero Trust’s “never trust by default, always verify” assumption, with least privilege, device posture checks, and network segmentation you can apply to home routers, cloud drives, and collaboration accounts.',
  'content_html' => $content,
  'faq_json' => '[{"q":"Is Zero Trust only for large enterprises?","a":"The idea scales down to segmented Wi‑Fi, expiring links, and device inventories; small setups can still practice the core assumptions."},{"q":"Does installing a Zero Trust client make me safe?","a":"The client is only an enforcement point; unclear policy and permissions still cause oversharing or wrong grants."},{"q":"Does Zero Trust conflict with firewalls?","a":"They complement each other. Firewalls filter boundary traffic; Zero Trust emphasizes identity and per-access decisions."},{"q":"How does it coexist with the old VPN model?","a":"A VPN can remain one access channel, but connecting should no longer mean undifferentiated access to the whole network."}]',
];
