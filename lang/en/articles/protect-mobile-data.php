<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>A phone often carries chat, payments, access badges, and second-factor channels at once. Protecting data is not just locking the photo album—it is controlling who can read what, and whether an old device stays online.</p>
<h2>Lock screen and system updates</h2>
<p>Use a strong passcode or biometrics and set a short auto-lock interval. Delaying OS and security patches leaves publicly known bugs for everyday links to exploit.</p>
<h2>App permission boundaries</h2>
<ul>
<li>Grant SMS, notification-read, accessibility, and device-admin rights only to apps that truly need them—and review regularly.</li>
<li>Install only from official stores or vendor channels; mystery APKs often pose as “free membership.”</li>
<li>Separate convenience from risk: cloud sync and backups widen the exposure surface together.</li>
</ul>
<h2>Sessions and retirement</h2>
<p>Before swapping phones, sign out of iCloud, Google, and frequent apps everywhere; factory-reset and confirm the old SIM and storage card are removed. If the phone is lost, remote-wipe first, then replace services.</p>
<p>Further reading: <a href="/articles/protect-online-accounts">protecting online accounts</a>, <a href="/articles/two-factor-authentication-guide">two-factor authentication</a>, <a href="/articles/prevent-personal-data-leaks">preventing personal data leaks</a>.</p>
<h2>Backup and sync trade-offs</h2>
<p>Auto-sync for photos, contacts, and chat makes a new phone easier—and leaves another cloud copy. Choose strategies per content type: work documents can live in an encrypted enterprise drive; private photos can disable auto-upload or back up only on Wi-Fi.</p>
<h2>Mobile payments and biometrics</h2>
<p>Small contactless payments trade convenience for risk. Add a second confirmation for payment apps; in public, hide payment-result notification previews so bystanders cannot see amounts and merchants.</p>
<h2>Travel and roaming</h2>
<p>Abroad, watch for fake carrier SMS and Wi-Fi captive portals; prefer a temporary local eSIM data plan over resetting bank passwords on unknown networks. For tunnels and DNS, see <a href="/articles/what-is-vpn">VPN</a>.</p><h2>Kids’ and elders’ devices</h2><p>Installing apps with your own Apple ID ties your payments and cloud to their phone. Register separate accounts for elders, enable install limits and Screen Time, and reduce accidental scam downloads.</p><h2>Repair and lending</h2><p>Before repair, back up, sign out, and wipe—or at least enable repair mode. When lending a phone to someone you know, use a guest profile so they do not see verification codes in notifications.</p><h2>Work files and personal albums</h2><p>Mixing company scans with travel photos in one album pushes confidential PDFs into personal backups via cloud sync. Keep business PDFs in a system secure folder or enterprise container and disable external link sharing for that directory.</p><p>If you use a USB-C dock to cast to a shared display, check whether notifications still mirror in “mirror only” mode—meeting content can leak to bystanders in the room.</p><h2>Firmware and baseband</h2><p>Carrier baseband updates matter as much as major OS releases; delaying them can leave known over-the-air sniffing holes. Turn on automatic security updates and, after travel, manually check for patches missed while roaming.</p><p>After binding transit cards or car keys via NFC, losing the phone also loses physical entry. Revoke virtual cards in the wallet app before remote wipe, then void building-access badges with property management—the reverse order can leave you locked out of cloud consoles while standing outside.</p><p>When a watch mirrors notifications, codes sit on the wrist for shoulder-surfers. Disable watch previews for finance apps, or require a complex gesture before expanding SMS content.</p>
HTML;
return [
  'title' => 'How to protect personal data on your phone',
  'seo_title' => 'How to protect phone data: permissions, backups, and device swaps',
  'meta_description' => 'How app permissions, lock strength, install sources, cloud-backup policy, and wipe-before-swap flows protect personal data, payment sessions, and second-factor channels on phones—especially before replacing or losing a device; verify the outcome once.',
  'content_html' => $content,
  'faq_json' => '[{"q":"Is mobile antivirus enough?","a":"Antivirus alone does not replace permission control, system updates, and account hardening—use all three together."},{"q":"Is cloud photo backup a privacy risk?","a":"Default cloud sync widens exposure; encrypt sensitive content locally or turn off auto-upload."},{"q":"What must I do before retiring an old phone?","a":"Sign out of all cloud accounts, revoke device sessions, then factory-reset."}]',
];
