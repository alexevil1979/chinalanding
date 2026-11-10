<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>A sense of safety on the home network often comes from “as long as it works”—until an unknown device shows up in the router list. Periodic self-checks cost far less than cleaning up after the fact, especially when the router still uses a factory default password.</p>
<h2>Start at the gateway</h2>
<p>Log into the admin interface and change the factory administrator password; disable remote management (WAN-side Web/SSH). Confirm the firmware version and upgrade first when a security advisory applies.</p>
<h2>Inventory connected devices</h2>
<ul>
<li>Match MAC addresses and hostnames against real devices in the home; for unknown entries, isolate first or change the Wi-Fi password.</li>
<li>Keep guest and main networks on separate SSIDs; smart plugs and cameras should not share an unsegmented LAN with PCs.</li>
<li>Check whether DNS points to an unknown server—see <a href="/articles/how-dns-servers-work">how DNS works</a>.</li>
</ul>
<h2>Extend outward</h2>
<p>Enable the firewall on desktops; use the Public network profile on laptops in shared spaces. For remote access home, use an explicitly authorized tunnel instead of exposing management ports directly to the internet.</p>
<p>For travel scenarios, combine <a href="/articles/choose-secure-network-connection">connection choices</a> with <a href="/articles/public-wifi-safety">public Wi-Fi</a> habits.</p>
<h2>ONT and router: two layers of admin</h2>
<p>In many homes the optical modem (ONT) handles dial-up while the router does NAT. Changing only the router password while the ONT stays on defaults lets attackers try the management interface from the WAN side. Change both passwords and disable remote maintenance unless the ISP requires it.</p>
<h2>UPnP and port mapping</h2>
<p>Games and download tools often punch holes and map ports automatically, which can accidentally expose internal services. If you do not need it, turn UPnP off on the router and use manual mappings with a written purpose for each.</p>
<h2>Next-generation protocols</h2>
<p>When IPv6 is enabled, review interface-boundary firewalls so internal devices do not get global addresses without filtering. Read alongside the <a href="/articles/what-is-ip-address">IP address</a> article.</p><h2>Smart locks and cameras</h2><p>Default IoT passwords appear on botnet scan lists. Change credentials on first power-up and block these devices from reaching desktop file shares.</p><h2>Firmware advisory subscriptions</h2><p>Subscribe to vendor security advisory emails—you will often learn about CVEs that need upgrading sooner than waiting for news coverage.</p><h2>Guest network bandwidth</h2><p>Rate-limiting guests can stop a neighbor’s download habit from burning your IP reputation. QoS is not a luxury feature; most modern routers support it.</p><p>At year-end, photograph the current connected-device list and compare it with physical devices—more reliable than remembering “we only have about six.”</p><h2>Default MQTT ports</h2><p>If a smart-home stack exposes port 1883 to the public internet, botnets will subscribe quickly. Block inbound at the gateway and allow only LAN devices to talk.</p><p>When rentals turn over, previous tenants’ smart-home gear may stay bound; a new renter could unlock doors remotely. On move-in day reset the gateway, change the SSID, and confirm with the landlord that cloud accounts no longer list old devices.</p><p>If a doorbell uses P2P NAT traversal, firmware flaws can let strangers preview remotely. Watch vendor CVE notices and forced update pushes.</p><p>Printer firmware often goes a decade without updates yet still holds scanned contracts. Put printers on a separate VLAN—more realistic than hoping “LAN-only” is enough.</p><p>If you spot something odd, disconnect from the network first, then photograph evidence.</p>
<p>Further reading: <a href="/articles/windows-network-security-settings">Windows network security settings</a>.</p>
HTML;
return [
  'title' => 'How to check network connection security',
  'seo_title' => 'How to check home network security: router and device self-audit',
  'meta_description' => 'Home network self-check steps covering router admin passwords, firmware versions, connected-device lists, guest segments, and DNS settings, plus what to do when an unknown endpoint appears—review the device list about once a month.',
  'content_html' => $content,
  'faq_json' => '[{"q":"How often should I check the router device list?","a":"A quick monthly glance is enough; also recheck after password changes or when you add new IoT devices."},{"q":"Does an unknown device always mean a compromise?","a":"Not always—it may be a guest or a confusing factory hostname. Disconnect first, then match against physical devices."},{"q":"Do homes need intrusion detection?","a":"Not usually. For most households, strong passwords, network segmentation, and updates matter more."}]',
];
