<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>The debate about public Wi-Fi is not “can you use it,” but “what are you using it for.” On the same hotspot, checking a bus timetable and logging into online banking have completely different risk budgets.</p>
<h2>Where the threats come from</h2>
<p>Same-segment eavesdroppers, malicious portals, spoofed SSIDs, and certificates you install by mistake can all divert traffic from the expected path. HTTPS protects page content, but it cannot stop you from typing a password into a fake portal.</p>
<h2>Practical layering</h2>
<ol>
<li>Mark the network as public in the OS and turn off file sharing.</li>
<li>For low-sensitivity browsing, confirm TLS; for medium sensitivity, consider a <a href="/articles/what-is-vpn">VPN</a> and check for <a href="/articles/what-is-dns-leak">DNS leaks</a>.</li>
<li>For high sensitivity, switch to cellular—see the <a href="/articles/safe-public-network-use">public network usage guide</a>.</li>
</ol>
<h2>Do not trust appearances</h2>
<p>A polished café QR sticker may belong to an attacker. Only SSIDs printed on official paper instructions are worth typing in by hand.</p>
<p>Transport basics: <a href="/articles/what-is-https">HTTPS</a>.</p>
<h2>Laptop hotspot sharing</h2>
<p>When a laptop shares a phone hotspot, default password strength varies. If you enable sharing for a temporary meeting, turn it off afterward and set a random passphrase so passers-by cannot freeload and inspect traffic metadata.</p>
<h2>Hotel wired ports</h2>
<p>A wall RJ45 jack is not safer: same-floor VLAN broadcasts and ARP spoofing can still happen. Apply the same HTTPS and tunnel policy on wired links.</p>
<h2>Kill-switch verification</h2>
<p>If a tunnel client claims a kill switch, disconnect and test whether DNS and IP fall back to a bare connection. Configuration notes are in the <a href="/articles/what-is-dns-leak">DNS leak</a> article.</p>
<h2>Cross-border roaming misbinds</h2>
<p>Near borders, phones may auto-join open hotspots from another country’s carrier—both cost and security risks. Select the network manually and disable automatic data roaming.</p>
<h2>Session fixation</h2>
<p>Captive portals sometimes force an HTTP first hop before login. Watch whether the address bar upgrades to HTTPS immediately; otherwise do not enter a password.</p>
<h2>Live-stream upload windows</h2>
<p>Live streams expose audience reactions and location together; a hostile viewer can combine that with a Wi-Fi portal to gather more intelligence. Publishing a delayed replay is steadier.</p>
<p>When sharing a hotspot with companions, use the system guest network for isolation instead of handing out the main password.</p>
<h2>DNS over TLS during the portal phase</h2>
<p>Before captive-portal auth completes, system encrypted DNS may fail the handshake and fall back to plaintext. That is not a tunnel leak—it is an unauthenticated state; re-enable encryption after you are on the network.</p>
<p>Hotel cards printing “free Wi-Fi” and a fixed password often end up photographed from trash into social media. A conference photo with the password in the background is an open guest network—after check-in, ask for a personal account instead of a shared passphrase.</p>
<p>Public Wi-Fi checks promoted by anti-fraud apps are essentially online lookups. Grant network-info permission only; do not also open the contacts book.</p>
<p>A B&amp;B host’s chalkboard with the Wi-Fi password becomes a public post if it appears in an Instagram room shot. Erase the text or change the password before indoor photos.</p>
<p>Long-term café remote workers should use the shop’s official member account rather than borrowing temporary guest passwords.</p>
<p>Low battery is not a reason to lower your protection level.</p>
HTML;
return [
  'title' => 'Is public Wi-Fi safe?',
  'seo_title' => 'Is public Wi-Fi safe? Risk tiers and protection tips',
  'meta_description' => 'Side-channel sniffing, malicious captive portals, and fake hotspots on public Wi-Fi—combine HTTPS, trusted tunnels, and mobile data by sensitivity, and avoid high-risk banking on hotspots. A quick checklist before you connect while traveling.',
  'content_html' => $content,
  'faq_json' => '[{"q":"Is free airport Wi-Fi always monitored?","a":"Operators usually have a logging policy; that is not necessarily malice, but do not assume full privacy."},{"q":"Can MAC randomization anonymize you?","a":"It can reduce tracking, but after login account-layer identifiers still apply."},{"q":"Is it safe to keep browsing if the VPN drops?","a":"With a kill switch, traffic stops; otherwise you may bare-connect and leak the real IP and DNS."}]',
];
