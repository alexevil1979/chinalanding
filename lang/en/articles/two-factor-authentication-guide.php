<?php
return [
    'title' => 'What Two-Factor Authentication Is For',
    'seo_title' => 'Two-Factor Authentication Guide: Security Keys, TOTP, and SMS Choices',
    'meta_description' => 'Compare security keys, TOTP authenticator apps, and SMS codes for risk resistance; cover recovery-code backups, why hub accounts such as email should enable 2FA first, migrate authenticators before a phone swap, and verify the result once.',
    'content_html' => <<<'HTML'
<p>Two-factor authentication (2FA) adds a second door after a password leak. Factor strength varies widely: hardware keys and FIDO2 are usually stronger than SMS, and SMS is still stronger than no 2FA at all.</p>
<h2>Comparing common factors</h2>
<ul>
<li><strong>Security keys / passkeys:</strong> strong phishing resistance, bound to the site domain.</li>
<li><strong>TOTP apps:</strong> generate offline 6-digit codes; better than SMS.</li>
<li><strong>SMS:</strong> exposed to SIM-swap threats, but still blocks bulk credential stuffing.</li>
</ul>
<h2>Recovery and backup</h2>
<p>When enabling 2FA, save recovery codes on offline encrypted media. Register backup factors before you lose the phone so you do not lock yourself out.</p>
<h2>Rollout order</h2>
<p>Prioritize email, the password manager, cloud storage, and payments. Then expand to social and shopping. Pair with an <a href="/articles/protect-online-accounts">account inventory</a> and a <a href="/articles/create-strong-passwords">password policy</a>.</p>
<p>Spot fake 2FA phishing: <a href="/articles/identify-phishing-attacks">phishing guide</a>.</p>
<h2>Defending against SIM swap</h2>
<p>Set a carrier PIN, restrict SIM replacement, and treat SMS 2FA as transitional only. Upgrade financial accounts to keys or push approval first.</p>
<h2>Push fatigue</h2>
<p>Repeatedly tapping “Approve” becomes a reflex. For unfamiliar login prompts, cancel first, then open the official app to review activity.</p>
<h2>Travel mode</h2>
<p>Some platforms offer temporary codes for lost devices or travel allowlists. Register backup factors before leaving the country so timezone gaps do not block support.</p>
<h2>Printing backup codes</h2>
<p>Store paper waterproof and out of view, in a different cabinet from the main computer. Photos in an unencrypted cloud album create a second leak point.</p>
<h2>Shared-account trap</h2>
<p>Streaming family sharing is not a 2FA substitute; each signer should still have an independent password so one compromised device does not take down the household.</p>
<h2>Retiring an old phone</h2>
<p>Before selling, unregister 2FA devices in every app, then remove TOTP entries in settings. Otherwise a buyer may inherit sessions you never signed out.</p>
<p>Cross out each one-time emergency backup code after use so screenshots do not stay valid forever.</p>
<h2>Watches and wearables</h2>
<p>A smartwatch that shows one-time codes leaves the second factor exposed when the wrist is away. Remove the watch or disable notification previews before a gym shower.</p>
<h2>Account-recovery scams</h2>
<p>Fake support asking you to “turn off 2FA to unfreeze the account” is a classic phishing pattern. Real vendors never require disabling verification first.</p>
<p>When a bank hardware token and a phone token coexist, confusion can cause accidental denials and lockouts. What belongs on a sticky note is a flowchart, not a password; knowing which scenario uses hardware versus an app beats stacking more factors.</p>
<p>If WeCom approvals or DingTalk pushes are bound to a personal phone, unbind the personal number after leaving the company WeCom tenant so approval notices stop landing on a private device.</p>
<p>Keep a spare phone in a dry sealed bag, separate from the daily device, so losing the primary phone while traveling does not erase 2FA and contacts at once. Even unused phones need a half charge every six months to reduce battery swelling risk.</p>
<p>On a new phone, migrate 2FA before wiping the old one—the reverse order can lock you out of cloud recovery for hours.</p>
<p>If SMS does not arrive, first check signal and roaming status.</p>
<p>Collect platform recovery codes into an encrypted note and a sealed printed bag—do not leave them pinned in chat.</p>
HTML,
    'faq_json' => '[{"q":"Can I skip SMS 2FA?","a":"If you cannot use an app or key, SMS is still better than a single factor; upgrade when you can."},{"q":"What if I lose recovery codes?","a":"Log in with remaining factors as soon as possible and regenerate codes; otherwise follow the vendor identity-appeal process."},{"q":"How do I sync TOTP across devices?","a":"Use encrypted cloud backup or scan the same secret on each device; protect the backup carefully."}]',
];
