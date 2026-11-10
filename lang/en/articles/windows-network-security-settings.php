<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>Windows is both an office workhorse and a frequent guest on public hotspots. A few switches around network profiles, the firewall, and remote access decide whether a strange LAN can reach your shares and Remote Desktop services.</p>
<h2>Public vs private profiles</h2>
<p>In a café, mark the current connection as Public: the system tightens discovery and file sharing. At home, switch back to Private so you are not left permanently exposed under a loose policy.</p>
<h2>Firewall and inbound rules</h2>
<ul>
<li>Keep the Windows firewall on; if third-party security software demands turning the built-in firewall completely off, confirm it truly replaces that protection.</li>
<li>Without a clear need, turn off Remote Desktop and unnecessary file sharing.</li>
<li>Review which apps are allowed through the firewall and disable old tools you no longer use.</li>
</ul>
<h2>Updates and the network stack</h2>
<p>Deferred security updates also fix DHCP, Wi-Fi drivers, and the <code>TLS</code> stack. Enable automatic updates and reboot once after important patches.</p>
<p>See <a href="/articles/choose-secure-network-connection">choosing a secure network connection</a>, <a href="/articles/network-traffic-encryption">network traffic encryption</a>, and <a href="/articles/public-wifi-safety">public Wi-Fi</a>.</p>
<h2>Mixing enterprise domain and home use</h2>
<p>After joining Azure AD or a company domain, some policies come from admins and the local firewall UI may grey out. On the home side, still disable unnecessary sharing so guest segments the domain policy never covers are not left wide open.</p>
<h2>Hardware Wi-Fi buttons</h2>
<p>Physical Wi-Fi switches and airplane-mode shortcuts on older laptops can drop a tunnel while still showing a hotspot connection. After firmware updates, recheck wireless drivers to fix known disconnect bugs.</p>
<h2>Logs and troubleshooting</h2>
<p>When you are “connected but offline,” first inspect the routing table and DNS at the command line and confirm no leftover malicious proxy remains. Cross-check with <a href="/articles/what-is-dns-leak">DNS leaks</a> and <a href="/articles/check-network-security">home self-checks</a>.</p>
<h2>Hyper-V and virtual switches</h2>
<p>When running VMs, the default switch may bypass host firewall rules. Give lab environments their own virtual segment so malware samples cannot probe the home NAS.</p>
<h2>Bluetooth and near-field</h2>
<p>Turn off Bluetooth discoverability when unused to avoid junk pairing requests in meeting rooms that also leak device fingerprints.</p>
<h2>PowerShell remoting</h2>
<p>If WinRM or OpenSSH Server is enabled by mistake, high-value ports appear on public scan lists. In Optional features, confirm you have not enabled unplanned remote components.</p>
<p>After lid-close sleep, old Wi-Fi sessions sometimes stay half-connected—disconnect and reconnect when you resume work so full authentication runs again.</p>
<h2>Location and Wi-Fi scanning</h2>
<p>Windows uses visible Wi-Fi lists to assist location, effectively uploading nearby BSSID outlines. Limit app location access in privacy settings and turn off overly detailed network telemetry under optional diagnostics.</p>
<p>Game “accelerators” with kernel drivers rewrite the network stack and can conflict with the built-in firewall’s dual filtering. After uninstall, if speed looks wrong, use Network reset to restore the default stack, then reinstall only what you need.</p>
<p>When a BitLocker/TPM-bound device goes for repair, tell technicians not to pull the disk alone for reading. Back up the recovery key before handing it over.</p>
HTML;
return [
  'title' => 'Windows network security settings guide',
  'seo_title' => 'Windows network security settings: public networks and the firewall',
  'meta_description' => 'Windows public network profiles, Defender Firewall, Remote Desktop toggles, and system updates—reducing the chance a laptop is scanned or has shares abused on an unfamiliar LAN.',
  'content_html' => $content,
  'faq_json' => '[{"q":"What does a public network profile affect?","a":"It mainly limits device discovery, network browsing, and some sharing services, lowering the chance of same-segment scans."},{"q":"Does turning off the firewall improve game latency?","a":"Rarely, and usually by greatly expanding the attack surface—not recommended for daily use."},{"q":"How do I confirm Remote Desktop is off?","a":"Check the Remote Desktop switch in system settings and verify there is no RDP exception in firewall inbound rules."}]',
];
