<?php
return [
    'title' => 'What the WireGuard Protocol Is',
    'seo_title' => 'What WireGuard Is: Interface, Noise Handshake, and Cryptokey Routing',
    'meta_description' => 'Based on the WireGuard site: Interface, Peer, Noise_IKpsk2 handshake, and Cryptokey Routing—covering AllowedIPs, MTU, DNS, roaming, and keepalive deployment points.',
    'content_html' => <<<'HTML'
<p>WireGuard is a modern VPN tunnel protocol that runs over UDP. Jason A. Donenfeld and collaborators drove a mainline implementation into mainstream kernels. Its stance is clear: a fixed cryptography suite, a narrow configuration surface, and a short forwarding path in the kernel. For operators and individuals, understanding three threads—“virtual interface and peers,” “public-key routing,” and “handshake rotation”—matters more than memorizing CLI flags.</p>
<h2>What WireGuard is</h2>
<p>From the user’s view, WireGuard creates a TUN interface such as <code>wg0</code>, encapsulates selected IP traffic into UDP toward a peer, and after decryption injects packets into the peer’s network stack. It does not replace application-layer proxies and is not a browser-embedded SSL VPN; it is an OS-level point-to-point tunnel. Official builds cover Linux, Windows, macOS, iOS, Android, and more; protocol notes and papers are worth reading side by side.</p>
<p>As with the <a href="/articles/what-is-vpn">general VPN concept</a>, a tunnel changes path and egress—it does not automatically mean anonymity. Compared with a <a href="/articles/vpn-vs-proxy">proxy</a>, WireGuard by default covers the prefix set that IP-layer routing points at.</p>
<h2>Overall architecture</h2>
<p>Logically there are three object types: an <strong>Interface (local)</strong> holds the long-term private key and a listening UDP port; a <strong>Peer</strong> is identified by a Curve25519 public key and binds allowed IP prefixes plus a reachable address; the <strong>data plane</strong> encrypts inner IP packets with symmetric keys after the handshake. The control plane is UDP only—no TCP state machine—so reconnect depends on timed handshakes and keepalive, not an application heartbeat protocol.</p>
<h2>Interface and Peer</h2>
<p>In the config, the <code>[Interface]</code> section declares <code>PrivateKey</code>, <code>Address</code>, <code>DNS</code>, <code>ListenPort</code>, and similar; each <code>[Peer]</code> declares the peer <code>PublicKey</code>, <code>Endpoint</code>, <code>AllowedIPs</code>, and <code>PersistentKeepalive</code>. One interface can host many peers (typical hub-and-spoke: clients point at the server public key; the server creates one peer per client). The private key is a pass—restrict file permissions and do not reuse the same key pair across devices, or you confuse the identity binding Cryptokey routing depends on.</p>
<h2>Public and private keys</h2>
<p>Long-term identity is Curve25519: derive a public key from a 32-byte private key; peers must pre-provision the public key to complete the Noise handshake. An optional <code>PresharedKey</code> is mixed in per the protocol; if unset, the protocol treats it as 32 zero bytes. Key rotation happens at the session layer: ephemeral keys regenerate each handshake; long-term keys change only when you rotate them manually.</p>
<h2>Noise Protocol Framework (Noise_IKpsk2)</h2>
<p>WireGuard’s handshake comes from the Noise framework with identifier <code>Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s</code>: IK means the initiator already knows the responder’s static public key; <code>psk2</code> means a pre-shared key may be mixed in. The handshake completes in two messages, then both sides derive send and receive symmetric keys. Noise goals include identity hiding, forward secrecy, and resistance to key-compromise impersonation; the WireGuard paper and official protocol page give field-by-field layouts.</p>
<h2>Curve25519, ChaCha20-Poly1305, BLAKE2s, SipHash24</h2>
<ul>
<li><strong>Curve25519:</strong> ECDH for shared secrets in the handshake.</li>
<li><strong>ChaCha20-Poly1305:</strong> RFC 7539 AEAD for data packets; the nonce is 32 zero bits plus a 64-bit little-endian counter.</li>
<li><strong>BLAKE2s:</strong> hashing and keyed MAC, with HKDF (RFC 5869) to derive session keys.</li>
<li><strong>SipHash24:</strong> internal hash-table keys to mitigate hash-flood DoS.</li>
</ul>
<p>The algorithm set is fixed, avoiding the “pick a weak cipher” config traps of the OpenVPN/IPsec era and easing interoperable third-party audits.</p>
<h2>Cryptokey Routing</h2>
<p>This is the core of WireGuard’s routing semantics: each peer public key binds a set of <code>AllowedIPs</code>. On egress, packets are encrypted for the peer matching the destination prefix; on ingress after decrypt, packets are accepted only if the source IP is in that peer’s allow list—otherwise dropped. Misconfiguration often shows up as “handshake works but no traffic” or asymmetric black holes. In hub deployments, the server often gives each client a host <code>/32</code>, while the client points default route <code>0.0.0.0/0</code> at the server for a full tunnel.</p>
<h2>Handshake and key rotation</h2>
<p>Officially, re-handshakes are time-based with message-count thresholds so forward secrecy holds on lossy networks. Timer families include: jittered retries when responses are missing; empty keepalives after long quiet periods; forced new handshakes when session keys age out or message counts exceed limits; rejection of packets with expired keys or overflowed counters. After a new session, the responder confirms the switch only after the initiator’s first encrypted packet (which may be padding)—avoiding half-open reordering chaos.</p>
<h2>Persistent Keepalive</h2>
<p>Behind NAT, long idle periods expire mappings. Setting <code>PersistentKeepalive = 25</code> (or similar) makes the kernel send empty payloads on an interval to keep the mapping and help trigger timed handshakes. Too short wastes traffic; too long may fail the first packet after roaming—balance against carrier NAT behavior.</p>
<h2>Endpoint roaming</h2>
<p>When a mobile device switches Wi-Fi and cellular, the source UDP port and IP often change. WireGuard learns the source IP/port from valid encrypted packets and updates the peer’s current Endpoint without manual config edits. Firewalls must keep allowing inbound UDP to the listen port; under symmetric NAT, keepalive is especially important for address learning.</p>
<h2>AllowedIPs</h2>
<p>Besides Cryptokey filtering, AllowedIPs drive system routes: installing the config adds prefixes toward the tunnel interface. Split tunnel means writing only selected prefixes into AllowedIPs while the rest use the local default gateway. With policy routing and multiple tables, watch metrics and “exclude LAN” entries so printers or multicast are not sucked into the tunnel by mistake.</p>
<h2>MTU</h2>
<p>Outer UDP, the WireGuard header, and AEAD expansion shrink effective MSS. If path MTU discovery fails, large packets may black-hole or fragment heavily. A common practice is setting interface MTU in the 1280–1420 range and measuring, or relying on TCP MSS clamp. Cross-border links, PPPoE, and mobile networks are especially MTU-sensitive.</p>
<h2>DNS and routing caveats</h2>
<p>Interface-level <code>DNS = ...</code> hints the resolver through the tunnel, but system or browser DoH can still make the query path diverge from the tunnel—see <a href="/articles/what-is-dns-leak">DNS leaks</a>. For full tunnel, list the default route and “do not tunnel” LAN prefixes together; on Linux, advanced options such as <code>Table = off</code> avoid hijacking tables that should stay local.</p>
<h2>Protocol boundaries and limits</h2>
<p>WireGuard has no user-account system, no content audit, and no built-in multi-level ACL; authentication is simply “holds the matching private key.” DoS mitigation relies on cookie replies and MAC checks; under high load handshakes may be delayed. It also does not solve logging after the tunnel exit, malware, or phishing.</p>
<h2>Typical deployment scenarios</h2>
<ul>
<li><strong>Remote access to a company LAN:</strong> AllowedIPs contain only internal prefixes; everyday internet still exits locally.</li>
<li><strong>Hardening on public Wi-Fi:</strong> full tunnel to a self-hosted or trusted VPS, plus HTTPS—see <a href="/articles/public-wifi-safety">public Wi-Fi safety</a>.</li>
<li><strong>Site-to-site substitute:</strong> mutual public keys, static Endpoint, firewall allowing only the UDP port.</li>
<li><strong>Mobile roaming:</strong> moderate PersistentKeepalive and accept automatic Endpoint updates.</li>
</ul>
<p>When choosing, separate “modern protocol” from “who holds the server private key and whether connection metadata is logged.” WireGuard solves cryptographic goals on the tunnel; operational trust is still your judgment.</p>
<p>Further reading: <a href="/articles/what-is-vless">VLESS</a>.</p>
HTML,
    'faq_json' => '[{"q":"Which Noise handshake identifier does WireGuard use?","a":"Officially Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s, with an optional pre-shared key mixed into the handshake."},{"q":"What happens if AllowedIPs are wrong?","a":"Routes may miss the tunnel, Cryptokey filtering may drop valid packets, or unintended traffic may be pulled into the tunnel."},{"q":"What problem does Persistent Keepalive solve?","a":"It keeps UDP mappings alive behind NAT and triggers timed communication, helping mobile Endpoint learning and handshakes."},{"q":"Can WireGuard replace antivirus or anti-phishing?","a":"No. It protects payloads on the tunnel; endpoint malware and social engineering still need separate defenses."}]',
];
