<?php
return [
    'title' => 'What Is an IP Address',
    'seo_title' => 'What Is an IP Address: Public, Private, and Privacy Tools',
    'meta_description' => 'Explain how IPv4 and IPv6 addresses route packets, distinguish public egress from private LAN addresses, and clarify what IP means in site logs and risk systems versus DNS queries and account identifiers.',
    'content_html' => <<<'HTML'
<p>An IP address is a network-layer identifier used to address and deliver packets. Without it, a server cannot send a response back to your device. In everyday talk, “IP” usually means the <strong>public egress address</strong>—the one in website logs—not the private number your phone holds on bedroom Wi‑Fi.</p>
<h2>IPv4, IPv6, and formats</h2>
<p>IPv4 is often written as four dotted groups (for example 203.0.113.5, RFC 791); address exhaustion drove longer hexadecimal IPv6 notation. Most home broadband runs dual stack; which protocol connects first depends on the app, OS, and network configuration. Cloudflare intro materials compare IP to a mailing address to explain routing, but an IP changes with the network and is not a lifelong identity number.</p>
<h2>Public vs private addresses</h2>
<p>RFC 1918 private ranges such as 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16 are valid only inside a LAN. Routers use NAT so many internal devices share one public egress. An e-commerce backend therefore often sees the “whole household” IP and cannot map it to a specific lamp. Enterprise lines may have fixed public IPs; home broadband is usually dynamically assigned by the ISP—rebooting the ONT may change the number.</p>
<h2>What IP can and cannot tell you</h2>
<p>GeoIP databases often give city- or carrier-level location; error and lag are common, so IP alone is not enough for legal positioning. Risk systems treat IP as one signal: unusual geography, data-center IPs, and bulk logins that clash with history raise scores. But IP itself <strong>does not carry</strong> your real name and does not mean the device is already compromised—attackers still need open services, vulnerabilities, or credentials.</p>
<h2>Division of labor with DNS and HTTP logs</h2>
<p>When you visit a site, servers usually log source IP, time, request path, and user agent; DNS queries happen before the connection and give the resolver a domain list. The three complement each other: changing IP does not erase DNS records, nor account cookies. See <a href="/articles/how-dns-servers-work">how DNS works</a> and <a href="/articles/what-is-dns-leak">DNS leaks</a>.</p>
<h2>How privacy tools change IP appearance</h2>
<p>A <a href="/articles/what-is-vpn">VPN</a> or proxy makes remote servers see the tunnel egress IP instead of your home broadband address. That can change some geo risk results but cannot stop a logged-in account from linking behavior. Multi-hop schemes such as Tor further hide the origin at higher cost to performance and availability, and endpoint or human risks remain. Application proxies and system tunnels have different trust boundaries—clarify coverage before choosing.</p>
<h2>Dynamic IP, CGNAT, and “someone else’s baggage”</h2>
<p>Carrier-grade NAT (CGNAT) lets many households share few public IPs; bad history on an IP can hurt neighbors’ captcha pass rates. After a dynamic lease renews and the number changes, “foreign login” alerts may be false—understanding the mechanism reduces panic, while you should still verify unauthorized sessions.</p>
<h2>Do not fetishize hiding IP</h2>
<h2>Anycast, CDN, and log retention</h2>
<p>Large sites often sit behind CDN anycast ingress; banning a single IP often affects only an edge node, not the whole site. How long websites retain source-IP logs varies by product and law: some aggregate after weeks, others archive for risk long-term. As a visitor you cannot control retention—you can only reduce linkable identity clues on high-risk sites.</p>
<h2>Do not fetishize hiding IP</h2>
<p>Public forum posts, game voice chat, and P2P downloads can expose the IP in use; that is unrelated to whether HTTPS is used. Reducing linkage relies on account isolation, minimizing public information, and correct transport encryption—not superstition that “hiding IP equals invisibility.”</p>
<h2>Threat intelligence and false blocks</h2>
<p>Data-center IPs, known proxy ranges, and addresses once used by botnets enter shared threat intel. You may only face harder captchas because a neighbor abused the IP; changing egress is not always the cure. When politely appealing to a provider, attach a timeline and account reputation—better than repeatedly registering throwaways.</p>
<h2>NAT and port mapping</h2>
<p>With source NAT on a home gateway, outsiders see only the shared egress and cannot tell whether the living-room TV or study PC initiated the connection. Enabling UPnP or manual port maps exposes specific internal services on the public side; logs still show the egress IP, but the port hints which service sits behind it. Closing unnecessary maps reduces scan hits more than frequently changing IP.</p>
HTML,
    'faq_json' => '[{"q":"If someone knows my IP, can they control my computer?","a":"Not from IP alone. They usually also need open ports, unpatched vulnerabilities, or weak credentials."},{"q":"Does IPv6 give every device a global address?","a":"It depends on routing and firewall configuration; most homes still isolate the LAN with router prefixes."},{"q":"Why is the city on IP lookup sites inaccurate?","a":"Common. Databases lag; treat them as a rough reference only."},{"q":"After enabling a VPN, can sites still see other identifiers?","a":"Yes. Cookies, accounts, browser fingerprints, and more may still identify you."}]',
];
