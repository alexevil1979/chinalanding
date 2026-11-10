<?php
declare(strict_types=1);
$content = <<<'HTML'
<p>The browser is the largest daily data exit point: searches, forms, camera permissions, and extension background behavior all pass through it. Defaults often favor convenience—you need to tighten them deliberately.</p>
<h2>Start with these</h2>
<ul>
<li>Keep automatic updates on; retire unsupported old versions.</li>
<li>In site permissions, turn off unnecessary location, camera, and notification access.</li>
<li>Limit third-party cookies or enable tracking protection.</li>
</ul>
<h2>Extensions are a double-edged sword</h2>
<p>Ad blockers and password fillers are convenient, but “read data on all websites” is roughly half a spyware permission. Periodically uninstall extensions you have not used in a long time.</p>
<h2>Profile isolation</h2>
<p>Use different profiles for work, entertainment, and anonymous search; do not install experimental scripts in the environment where you log into your bank. For how tracking works, see <a href="/articles/how-online-tracking-works">online tracking</a>; for the overall approach, see <a href="/articles/protect-online-privacy">online privacy</a>.</p>
<p>Spotting malicious pages: <a href="/articles/identify-malicious-websites">malicious websites</a>.</p>
<h2>Container tabs</h2>
<p>Approaches such as Firefox Multi-Account Containers isolate cookie jars so work and shopping logins do not contaminate each other. That is less hassle than repeatedly clearing the cache.</p>
<h2>Autofill risks</h2>
<p>When the browser remembers credit cards and addresses, one-click fill on a lookalike domain leaks faster. Disable form autofill on high-value sites and let a password manager enable it only on trusted domains.</p>
<h2>Experimental APIs</h2>
<p>Sites can query fingerprint surfaces such as GPU and battery status. Keep advanced experimental features off by default unless you have a specific development need.</p>
<h2>Timezone and language</h2>
<p>A fixed fingerprint mix includes timezone offset and UI language. Extreme anonymity needs mean accepting that some sites will refuse login for risk-control reasons.</p>
<h2>Service Worker</h2>
<p>Background workers can keep syncing tracking data. When uninstalling a PWA, clear site data—not just delete the icon.</p>
<h2>Download folder monitoring</h2>
<p>Malicious extensions occasionally watch the download directory for wallet files. Clean the downloads folder regularly, and deny extensions “all files” access.</p>
<p>Use different browser color themes for different banks to lower the chance of misusing autofill on a lookalike page.</p>
<h2>Built-in PDF reader</h2>
<p>When a PDF opens in the browser, JavaScript may still run. Download sensitive contracts and read them offline, or disable JS in the reader.</p>
<p>Mixing an office laptop with a personal account on the same Chrome profile makes it easy to miss logged-in SaaS when clearing cookies at departure. On handover day, create a new system user instead of only deleting history.</p>
<p>When school lab Chrome policies ban extensions, personal bookmarks may still sync to the cloud. Before graduation, export HTML bookmarks and sign out of the school account.</p>
<p>“Privacy protection” rankings in extension stores shift with vote stuffing; download counts and open-source Stars are more objective than rank. Keep what you still need after two weeks; uninstall the rest to shrink the attack surface.</p>
<p>Even with sync off, confirm that sessions already signed out on each device are no longer uploading history.</p>
<p>You can also switch the default search engine to a more privacy-friendly option.</p>
<p>Before uninstalling a browser, export bookmarks and saved passwords, then run the uninstaller’s data-clear option.</p>
HTML;
return [
  'title' => 'Browser privacy settings guide',
  'seo_title' => 'Browser privacy settings guide: cookies, permissions, and extensions',
  'meta_description' => 'A checklist of browser auto-update, site permissions, third-party cookies, tracking protection, and extension permissions—plus separating work and leisure profiles to reduce correlation. Re-check after major version upgrades.',
  'content_html' => $content,
  'faq_json' => '[{"q":"Is always clearing cookies a good idea?","a":"It signs you out of most sites; a more balanced approach is per-site management or container tabs."},{"q":"Is the built-in password manager safe?","a":"It depends on the master password and sync policy; compared with a dedicated password manager, weigh backup and cross-platform needs."},{"q":"Is the Do Not Track header still useful?","a":"Most sites ignore it; rely on the browser’s built-in tracking protection and permission controls."}]',
];
