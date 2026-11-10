<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>Airport, mall, and conference Wi‑Fi get you online fast but rarely pledge loyalty to your data. Treat public networks as pipes that carry traffic without vouching for identity—and the mindset clears up.</p>
<h2>Three steps before you connect</h2>
<p>Match the SSID to the on-site signage, disable auto-join for open hotspots, and set the laptop network type to Public. Do not rush into online banking before system patches are applied.</p>
<h2>Tier actions by sensitivity while connected</h2>
<ul>
<li><strong>Low sensitivity:</strong> news, maps—watch for <a href="/articles/what-is-https">HTTPS</a> and that the lock matches the correct domain.</li>
<li><strong>Medium sensitivity:</strong> email, social—avoid entering passwords on captive portals that are unrelated to getting online.</li>
<li><strong>High sensitivity:</strong> payments, password changes, uploading ID documents—switch to cellular data when you can.</li>
</ul>
<h2>Cleanup after you leave</h2>
<p>Disconnect and “forget” the network; check whether a configuration profile or intercept certificate was installed. If you see unusual login alerts, follow the <a href="/articles/protect-online-accounts">account protection</a> playbook.</p>
<p>Also see <a href="/articles/public-wifi-safety">public Wi‑Fi risks in depth</a> and <a href="/articles/what-is-vpn">VPN boundaries</a>.</p>
<h2>Trade shows and event venues</h2>
<p>Large events often offer free Wi‑Fi that harvests audience profiles. Booth QR logins may bind OpenID grants to unknown apps; prefer a disposable email or refuse non-essential authorizations.</p>
<h2>Power banks and USB ports</h2>
<p>Public USB charging ports may enable data pins and push configuration profiles. Bring your own wall charger or a USB data blocker to avoid “charge that syncs.”</p>
<h2>Regular café regulars</h2>
<p>Even a legitimate café hotspot can be mimicked by a same-name fake nearby. On first connect, note how the password is presented, and save the correct SSID as a manual profile rather than forever auto-joining.</p><h2>Train and in-flight LANs</h2><p>Closed vehicle and aircraft LANs are still untrusted. Watch a movie, but do not reset email passwords mid-flight—handle high-sensitivity tasks after landing.</p><h2>Metered billing traps</h2><p>Per-minute airport Wi‑Fi rushes you into payment pages—exactly the social-engineering window. Buying a data pack is often wiser.</p><h2>Shared coworking desks</h2><p>Places like WeWork often put many companies on one VLAN. Printer-driver bugs have historically spread laterally; before printing sensitive contracts, confirm the queue has no other jobs.</p><p>Locking with Win+L when you leave the desk is basic etiquette; shoulder surfing beats Wi‑Fi side channels more often than people expect.</p><h2>Video-call backgrounds</h2><p>On public networks, vendors may dial down transport-security options to save bitrate. For contract discussions, prefer wired or cellular and verify the meeting link is under your company’s domain.</p><p>Library lab PCs may still run outdated systems; autorun risks from USB coexist with Wi‑Fi risks. Use them only for read-only database lookups—never enter credentials that can reset your email.</p><p>International roaming data is expensive, but a single carrier account chain is shorter. Briefly enabling roaming to finish bank tasks can beat an unknown hotspot.</p><p>For business file handoffs, prefer an enterprise-drive link with expiry over hotspot peer transfer. Close sharing after the file lands so the folder is not left open during later review.</p><p>The same sensitivity tiers apply to short business trips.</p>
HTML;
return [
  'title' => 'How to use public networks safely',
  'seo_title' => 'How to use public networks safely: a tiered playbook',
  'meta_description' => 'Practical habits for airports, malls, and similar spaces: verify hotspot names before connecting, tier actions by sensitivity while online, and after leaving check certificates and sessions—ready to reuse on business travel; verify the outcome once.',
  'content_html' => $content,
  'faq_json' => '[{"q":"Is registering a phone number on a Wi‑Fi portal risky?","a":"It may be used for marketing or profile linking; give only the minimum and avoid reusing important phone numbers."},{"q":"Does seeing HTTPS mean I can pay on public Wi‑Fi?","a":"HTTPS protects transport but does not prove the hotspot itself is trustworthy; for large amounts, prefer cellular."},{"q":"How do I detect an installed certificate after leaving?","a":"Inspect newly added root certificates in the system trust store and remove any that are unfamiliar and unexplained."}]',
];
