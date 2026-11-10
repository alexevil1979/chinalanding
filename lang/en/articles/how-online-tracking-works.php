<?php
return [
    'title' => 'How Online Tracking Technologies Work',
    'seo_title' => 'How Online Tracking Works: Cookies, Fingerprints, and Login State',
    'meta_description' => 'Explain how cookies, pixel beacons, device fingerprints, and login state are stitched into cross-site profiles, and which browser settings and account isolation each weaken—beyond clearing cookies alone.',
    'content_html' => <<<'HTML'
<p>Advertising and analytics industries need you to be “recognizable,” but they do not always need your real name. Cookies, device fingerprints, and login identifiers in the browser are stitched across sites into a cross-site profile.</p>
<h2>How identifiers stack</h2>
<p>First-party cookies record that you visited this site; third-party tracking scripts read identifiers on other domains; pixel beacons report when an email was opened. If you are logged into a unified account, the profile merges with your real identity.</p>
<h2>When fingerprints appear without cookies</h2>
<p>Font lists, screen resolution, Canvas rendering differences, and WebGL traits can form a probabilistic identifier. Clearing cookies does not automatically zero out fingerprints.</p>
<h2>Levers you can adjust</h2>
<ul>
<li>Use separate browser profiles by scenario; limit third-party storage and enable tracking protection.</li>
<li>When logged in, assume you are “already linked”; run sensitive searches in an isolated environment.</li>
<li>Understand how <a href="/articles/browser-privacy-settings">browser privacy settings</a> work with an overall <a href="/articles/protect-online-privacy">privacy strategy</a>.</li>
</ul>
<p>For technical background, see MDN documentation on storage and tracking protection; strategically, avoid believing that “incognito mode equals being invisible.”</p>
<h2>Walled gardens and super-apps</h2>
<p>Inside ecosystems such as WeChat or Douyin, the account ID is a first-party identifier; the “anonymous” view ad networks see is often only an off-platform supplement. Limiting cookies outside the garden has limited effect on in-app personalization.</p>
<h2>Pixels in email</h2>
<p>Marketing messages embed 1×1 images that report time and IP when opened. Ask before remotely loading images, or read sensitive correspondence in plain-text mode.</p>
<h2>Compliance banners are not technical shields</h2>
<p>GDPR consent boxes mainly address legal basis; technically you still need tracking protection in the browser and fewer cross-site logins. See <a href="/articles/choose-privacy-tools">tool selection</a> for a combination that fits you.</p>
<h2>Redirect chains</h2>
<p>Affiliate marketing attaches tracking IDs along redirect chains; even when the final page is first-party, intermediaries already recorded the click. Opening the final URL in a private window removes one layer.</p>
<h2>Local storage APIs</h2>
<p>IndexedDB and localStorage can keep identifiers long-term and are not governed by the cookie-clear dialog. Clear site data together in browser settings.</p>
<h2>Retailer membership codes</h2>
<p>Scanning points codes offline and merging them with an online account pulls physical shopping into the profile. You can still collect points—just know the linkage exists, and avoid registering a real-name email that will receive junk tracking mail.</p>
<p>Logging a video account into the living-room TV stacks viewing history onto a personal profile; when sharing with children, switch to a kids profile.</p>
<h2>Embedded SDKs</h2>
<p>In-app analytics SDKs report behavior in the background, unrelated to browser cookies. Before installing, read permissions and privacy labels—games and utilities especially like to bundle advertising identifiers.</p>
<p>Streaming “continue watching” buttons make account habits obvious. When roommates share the living-room TV logged into your main account, they may see adult or medical documentary history—separate profiles cause less embarrassment than clearing history afterward.</p>
<p>Birthday promo emails that arrive on the exact day show that profiles include date fields. You need not tell every brand your real birthday; a fixed fake date breaks coincidence marketing.</p>
HTML,
    'faq_json' => '[{"q":"Can a private window stop tracking?","a":"It mainly avoids keeping local history; cross-site tracking, fingerprints, and login state may still exist."},{"q":"Will disabling cookies break shopping sites?","a":"It can affect login and carts; a more common approach is limiting third-party cookies rather than banning all of them."},{"q":"Does resetting the advertising ID help?","a":"It can break some mobile ad linkage, but after you log into an account the profile may merge again."}]',
];
