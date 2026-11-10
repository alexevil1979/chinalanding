<?php
return [
    'title' => 'How DNS Servers Work',
    'seo_title' => 'How DNS Servers Work: Resolution Path and Encrypted DNS',
    'meta_description' => 'Explain how DNS maps domains to IPs via recursive queries and caching; encrypted DNS protects the transport path, while the resolver operator may still see query names—configure once at the home router to avoid gaps.',
    'content_html' => <<<'HTML'
<p>Before the browser finishes loading a page, a domain name must be translated into an IP address. DNS is like a phone book: you ask “where is example.com,” the resolver records that question, and returns an answer. The process is independent of whether the page itself uses HTTPS.</p>
<h2>The recursive resolution path</h2>
<p>Clients usually send queries to a recursive resolver (router, ISP, or public DNS). If the recursive resolver has no local cache, it walks the hierarchy—root, TLD, then authoritative servers—until it assembles the record.</p>
<h2>Record types and TTL</h2>
<ul>
<li><code>A</code>/<code>AAAA</code> point to an IP; <code>CNAME</code> creates an alias.</li>
<li>TTL controls how long answers stay cached; a long TTL slows failover, a short TTL increases query volume.</li>
</ul>
<h2>Encryption and the privacy boundary</h2>
<p>DoH/DoT protect queries against eavesdropping and tampering on the wire, but the resolver operator can still see which names you asked for. Understand this together with <a href="/articles/what-is-dns-leak">DNS leaks</a> and <a href="/articles/what-is-ip-address">IP addresses</a>.</p>
<p>When troubleshooting, cross-check <a href="/articles/check-network-security">home network checks</a> for hijacked resolution.</p>
<h2>Caching and poisoning</h2>
<p>Recursive resolvers cache answers. If an attacker poisons a record within the TTL and briefly points a bank domain at a fake IP, users who typed the correct URL can still be redirected. Encrypted DNS plus HTTPS certificate validation are complementary safeguards.</p>
<h2>Reverse DNS</h2>
<p>Mail servers often use PTR records to assert identity; home users rarely touch this. Knowing that “IP to name” is a separate query direction helps—and it is not directly a privacy control.</p>
<h2>Propagation of authoritative changes</h2>
<p>After a site migrates and updates NS and A records, global convergence can take tens of minutes to hours. Some users still hit the old address during that window, so operations need a rollback plan.</p>
<h2>Private zones and enterprise split DNS</h2>
<p>Internal .local or split-brain DNS can resolve the same name to different IPs inside and outside the company. Remote-work tunnels must also carry internal DNS, or intranet service names will not resolve.</p>
<h2>Default DoH policy</h2>
<p>Browser DoH can bypass parental or router policies. Households should agree on policy at the gateway rather than fight silently in the browser.</p>
<h2>ECS and the privacy trade-off</h2>
<p>Some recursive DNS services attach a coarse subnet hint to authoritative servers so answers can prefer a nearer CDN node. That speeds delivery and slightly increases privacy exposure; public-resolver policies state whether ECS is enabled.</p>
<p>If you self-host Pi-hole to filter ad domains, keep threat-intel blocklists updated, or newly active tracking domains will still pass.</p>
<h2>Log retention policy</h2>
<p>Public DNS providers state how long logs are kept in their privacy policy. Reading that section when choosing a resolver is closer to real privacy differences than latency leaderboards.</p>
<p>After an enterprise pushes “split DNS,” a personal laptop on the company tunnel may still resolve home gaming traffic via the corporate path. Disconnect the tunnel after work and flush the resolver cache to avoid odd matchmaking.</p>
<p>Running your own recursive resolver is high maintenance; for individuals it is more realistic to pick a reputable public DNS and lock it so malicious DHCP cannot silently change resolvers.</p>
HTML,
    'faq_json' => '[{"q":"Will switching to public DNS make browsing faster?","a":"It depends on geography and ISP routing; sometimes the gain is clear, sometimes almost none."},{"q":"Can DNS see webpage content?","a":"No; it only sees queried domain names. Page bodies are protected separately by HTTPS."},{"q":"How does parental-control DNS work?","a":"By returning block or redirect IPs for filtered categories; that is a different layer from HTTPS content filtering."}]',
];
