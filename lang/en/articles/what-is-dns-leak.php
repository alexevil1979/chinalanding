<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>A DNS leak means: you already enabled a VPN or believed queries would take a trusted path, yet name resolution still goes through the local network, the carrier resolver, the router, or a browser-built-in resolver—exposing <strong>which domain names you asked for</strong> to an unintended observer. This is independent of whether page content uses HTTPS—intent leakage at the query stage stands on its own.</p>
<h2>Where DNS sits in the connection chain</h2>
<p>After you type <code>example.com</code>, the system or app queries a recursive resolver for A/AAAA records, then opens a TCP/TLS connection to that IP. The recursive resolver inherently sees the query name; if the query is unencrypted, the same LAN or upstream network may see it too. For the basics, see <a href="/articles/how-dns-servers-work">how DNS servers work</a>.</p>
<h2>Why VPN scenarios leak often</h2>
<p>A tunnel usually only guarantees that <strong>IP packets entering the tunnel</strong> follow the new path; DNS is a separate channel. Common causes: the client never pushed tunnel DNS; the OS still prefers the DHCP-supplied resolver; the browser alone enables DoH toward a provider unrelated to the VPN; split rules deliberately send some domains direct, but you did not realize that name is on the direct list. The difference between an accidental leak and <strong>intended split tunneling</strong> is whether behavior matches the policy you wrote—not the mere fact of “local resolution.”</p>
<h2>Split tunnel vs leak</h2>
<p>Enterprise VPNs often resolve intranet names locally and internet names through the tunnel—by design. A home user who wants “consistent privacy for all browsing” yet only encrypts HTTP while DNS still points at the carrier has a misconfiguration. When checking, look at IP egress, DNS egress, and the split table together—not only a client badge that says “connected.” Related: <a href="/articles/what-is-vpn">how VPN works</a>.</p>
<h2>What DoT and DoH mitigate</h2>
<p>DNS over TLS (RFC 7858) and DNS over HTTPS (RFC 8484) encrypt queries in transit, reducing path eavesdropping and tampering, and let clients pin a chosen resolution policy. They do <strong>not</strong> automatically hide queries inside the VPN tunnel: if browser DoH points at Cloudflare while web traffic exits a VPN, you may get an intentional or accidental mix of “IP in Germany, DNS in the US.” The resolver operator still sees the full query list. Mozilla’s docs describe Firefox DoH behavior and policy.</p>
<h2>How to detect</h2>
<ul>
<li>Before and after connecting the VPN, use a detection page you trust—or a script you control—to compare whether shown DNS and IP match your policy.</li>
<li>Retest after client upgrades, OS updates, or a new browser; a clean result is not permanent.</li>
<li>Check IPv6: if only IPv4 enters the tunnel while IPv6 stays direct, that is a bypass.</li>
<li>Confirm vendor options such as “tunnel DNS only” or “block LAN DNS” are on as intended.</li>
</ul>
<h2>Mitigation ideas</h2>
<ol>
<li>Set in-tunnel DNS in the VPN config and verify query egress matches the tunnel.</li>
<li>Unify encrypted DNS at the router or OS layer so apps do not each resolve differently.</li>
<li>Understand the split list: domains meant to go direct should not be reported as leaks.</li>
<li>For high-sensitivity scenarios, stack HTTPS and avoid account-critical actions on untrusted networks.</li>
</ol>
<h2>WebRTC and system resolver cache</h2>
<p>Some browsers in WebRTC scenarios may leak local interfaces or STUN probes—another “tunnel is up but a side channel remains” class of issue, alongside DNS leaks. System DNS cache and the <code>hosts</code> file can also make detection-page results disagree with a live packet capture—after changing config, restart the resolver service or clear the cache before retesting. If the split list matches by domain suffix, confirm wildcards are not sending traffic that should enter the tunnel into the direct resolver.</p>
<h2>What DNS encryption alone still cannot do</h2>
<p>DoH/DoT do not hide query content from your chosen resolver operator; they do not replace HTTPS for page bodies; and they do not stop a logged-in account from recording activity server-side. Traffic patterns, SNI (depending on protocol version and deployment), and IP addresses remain separate signals.</p>
<h2>What carriers and local gateways can see</h2>
<p>Unencrypted DNS outside the tunnel passes the home router and carrier recursion—often used for parental controls, malware-domain blocking, or compliance audits. Encrypted DNS moves “who can see the query name” to the resolver you chose; it does not make queries vanish from the planet. After switching VPN country, if you forget to sync DoH settings, a detection page may still show a resolution location that disagrees with the exit country—exactly why many users think “the VPN is broken.”</p>
<p>Suggested triage order: first confirm <a href="/articles/what-is-vpn">VPN</a> routing and kill switch, then encrypted DNS policy, then verify with an HTTPS site that the content layer is independently healthy.</p>
HTML;
return [
  'title' => 'What is a DNS leak?',
  'seo_title' => 'What is a DNS leak: causes, detection, and DoH/DoT limits',
  'meta_description' => 'Why DNS queries under a VPN may still use the local resolver, how to tell accidental leaks from intended split tunneling, and what DoH/DoT protect—and where they stop—for transport privacy and resolver policy consistency.',
  'content_html' => $content,
  'faq_json' => '[{"q":"Does using a VPN guarantee no DNS leak?","a":"Not necessarily. It depends on whether the client forces tunnel DNS and whether the OS or browser has another resolution path."},{"q":"Can encrypted DNS hide page content?","a":"No. It mainly protects the query channel; page content still relies on mechanisms such as HTTPS."},{"q":"Is local resolution under split tunneling a leak?","a":"If policy says the domain should go direct, local resolution may be expected; unexpected bypass is the leak."},{"q":"Can IPv6 cause a leak?","a":"If the tunnel ignores IPv6 while the system still goes direct over IPv6, expected paths may be bypassed—confirm dual-stack policy."}]',
];
