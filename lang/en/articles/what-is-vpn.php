<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>A VPN (Virtual Private Network) creates an encrypted tunnel at the operating-system layer, encapsulates selected IP traffic toward a remote node, and lets that node fetch internet or internal resources on your behalf. It mainly changes the <strong>network path and egress appearance</strong>; it is not automatic anonymity and does not replace device- and account-level security.</p>
<h2>Where tunnel encapsulation happens</h2>
<p>Unlike a browser proxy that only affects one app, common VPN clients install a virtual NIC (TUN) or rewrite the system routing table so matching packets enter the tunnel. On-path observers typically see your UDP/TCP session to the VPN server but may not directly read every inner destination IP (volume, timing, and other side channels can still infer behavior). Cloudflare’s intro materials describe VPNs as a way to extend a trust boundary over an untrusted network—assuming you trust the tunnel endpoint.</p>
<h2>What encryption and integrity protect</h2>
<p>Modern protocols (WireGuard, IPsec, OpenVPN, TLS-based SSL VPN, and others) provide confidentiality and integrity for tunnel payloads, reducing path-tampering risk. NIST SP 800-77 systematically covers IPsec VPN deployment factors for enterprise reference. Emphasize: <strong>encryption starts after traffic enters the tunnel</strong>; if the endpoint already has a keylogger or malware, data may be read before encapsulation. Protocol details: <a href="/articles/what-is-wireguard">WireGuard</a>; layered concepts: <a href="/articles/network-traffic-encryption">network traffic encryption</a>.</p>
<h2>Why DNS is discussed with VPNs</h2>
<p>Domains must resolve before sites load. If the tunnel is up but the system still sends DNS queries to the local ISP resolver, you get the mismatch “egress IP changed, queries still local”—a DNS leak. Reliable setups pin in-tunnel DNS at the client or interface level and verify expected behavior after split routing. Topic: <a href="/articles/what-is-dns-leak">what is a DNS leak</a>.</p>
<h2>IP routing: full tunnel vs split</h2>
<p>After connect, the default route or an <code>AllowedIPs</code>-style prefix list decides which traffic enters the tunnel. <strong>Full tunnel</strong> sends nearly all internet traffic remotely; <strong>split tunneling</strong> encrypts only office prefixes or selected ranges while the rest uses the local gateway. Split is a policy choice, not a defect—but if you believe you are fully protected while actually going direct, the threat model breaks. The egress IP becomes the provider node address, so site risk engines see a different geography than without the tunnel.</p>
<h2>Metadata does not vanish with the tunnel</h2>
<p>Even with encrypted payloads, connection duration, byte counts, and handshake reconnect frequency between you and the VPN server may still be logged. A VPN does not erase browser cookies, account sessions, payment linkage, or device fingerprints; it shrinks exposure on the <strong>local network to tunnel ingress</strong> segment. EFF’s self-defense guides note any third-party tunnel operator can technically observe or record session features.</p>
<h2>Provider role and trust boundary</h2>
<p>A commercial VPN decrypts at egress and forwards connections to target servers for you. Log policy, jurisdiction, client signing and supply chain, and independent audits answer “whom you trust” better than “military-grade encryption” slogans. Self-hosting WireGuard on a VPS pulls trust back to you—and with it patching, ops, and incident response. Compare app-level paths in <a href="/articles/vpn-vs-proxy">VPN vs proxy</a>.</p>
<h2>Threat-model checklist</h2>
<ul>
<li><strong>Café Wi‑Fi eavesdropping:</strong> a trusted tunnel plus HTTPS usually raises the cost of passive sniffing.</li>
<li><strong>Hiding a residential IP only for scraping:</strong> may violate terms of service, and accounts can still bind activity to you.</li>
<li><strong>Password phishing:</strong> tunnels do not validate page authenticity; you still need domain checks and 2FA.</li>
<li><strong>Lost device:</strong> rely on full-disk encryption and a lock screen, not on a VPN.</li>
</ul>
<h2>Kill switches and dual-stack routing</h2>
<p>A kill switch blocks non-VPN egress when the tunnel drops unexpectedly, preventing the moment you “think you are still protected” while sites see your real IP. Implementations vary: some clients inject firewall rules; others rely on OS “VPN-only internet” policy. Full IPv4 tunnel with IPv6 still on the local gateway is another classic bypass; while connected, check default routes and DNS egress for both protocols.</p>
<h2>Common configuration pitfalls</h2>
<ul>
<li>No kill switch after disconnect—traffic silently returns to the default network.</li>
<li>IPv6 not tunneled while IPv4 is protected—creating a bypass.</li>
<li>Clients from unknown sources—supply-chain risk outweighs the protocol name.</li>
<li>Equating “new egress IP” with “the site cannot recognize me.”</li>
</ul>
<p>Enterprise remote access often adds multi-factor authentication and device compliance checks—identity-layer supplements that a tunnel protocol name alone cannot replace. For personal choice, first understand app-level proxy vs system-tunnel coverage, then decide whether a always-on tunnel is worth it.</p>
<p>Further reading: <a href="/articles/what-is-vless">VLESS protocol</a>.</p>
HTML;
return [
  'title' => 'What a VPN is and how it works',
  'seo_title' => 'What is a VPN: tunnels, encryption, DNS, and threat models',
  'meta_description' => 'How VPNs work through tunnel encapsulation, encryption and integrity, DNS paths, IP routing, and metadata boundaries—plus the provider’s role at egress decryption and where VPNs fit or fall short under common threat models.',
  'content_html' => $content,
  'faq_json' => '[{"q":"Does a VPN make me fully anonymous to websites?","a":"No. It mainly changes network path and egress IP; accounts, cookies, and fingerprints can still identify you."},{"q":"If I already use HTTPS, do I still need a VPN?","a":"It depends on the threat. HTTPS protects one site’s transport; a VPN changes the system-level path. Goals differ; they can stack."},{"q":"Are free VPNs always more dangerous?","a":"Not necessarily, but scrutinize business model, client provenance, and history; free is not automatically malicious, yet verifiable no-logs claims are rare."},{"q":"Can traffic leak after the tunnel drops?","a":"Without a kill switch or firewall rules, traffic may fall back to the local default route—test and verify."}]',
];
