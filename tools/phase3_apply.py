# -*- coding: utf-8 -*-
"""Apply Phase 3 rewrites: priority full rewrite + strip templates on the rest."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import paramiko

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"C:\Users\1\Documents\chinalanding")
AUDIT = json.loads((ROOT / "tools" / "_articles_audit.json").read_text(encoding="utf-8"))
from phase3_priority import PRIORITY  # noqa: E402

TEMPLATE_H2 = [
    "结合实际场景理解",
    "分层防护怎么做",
    "建议的复查频率",
    "可立即执行的下一步",
    "阅读官方文档的原因",
    "实践中的判断标准",
    "延伸思考",
    "与家人或团队协作时",
    "把知识用在下一次真实操作里",
    "和商业工具的关系",
    "如果时间有限，只做这些",
    "把原则变成可检查的结果",
    # also earlier generic expansions / markers
    "常见加密层分别保护什么",
    "如何验证加密是否生效",
    "VLESS 适合理解的边界",
    "自建与托管的取舍",
    "DNS 泄露为什么容易被忽略",
    "降低泄露的实用步骤",
    "怎么选：看流量范围与信任边界",
    "共同风险",
    "数字身份由哪些凭证组成",
    "降低被冒用的优先动作",
    "除了看网址，还要看什么",
    "遇到可疑页面时",
    "零信任对个人用户意味着什么",
    "IP 能说明什么、不能说明什么",
    "公共网络上的最小安全集",
    "常见追踪信号",
    "账户失守后的常见连锁",
    "Windows 上值得先核对的项",
    "Windows 网络配置优先核对项",
    "可选加固",
    "公共场所笔记本习惯",
    "手机数据保护清单",
    "应用权限的红线",
    "移动端数据生命周期",
    "为什么 DNS 选择影响隐私与可用性",
    "解析路径与故障排查",
    "儿童与广告过滤 DNS",
    "静态加密与传输加密",
    "密钥与恢复是加密的另一半",
    "协作文件怎么传",
    "连接选型的快速决策",
    "场景化连接策略",
    "旅行中的连接",
    "家庭网络自检顺序",
    "每月十五分钟网络体检",
    "发现陌生设备之后",
    "数据最小化原则",
    "泄露后的止损顺序",
    "网盘与邮件附件",
    "威胁模型决定加密选型",
    "企业与个人的不同",
    "协议之外的供应链风险",
    "测试与持续监控",
    "决策表：覆盖范围、信任与成本",
    "浏览器隐私的层次",
    "搜索与自动填充",
    "破除神话后的行动",
    "工具越多越安全？",
    "选型时的证据而不是广告",
    "试用期检查清单",
    "端到端加密的边界",
    "WireGuard 的运维要点",
    "钓鱼的进化与反制",
    "双重验证的选型",
    "证书警告怎么处理",
    "密码策略落地",
    "公共 Wi-Fi 的现实策略",
    "隐私是持续配置，不是一次设置",
    "VPN 不能做什么",
    "账户分层与恢复演练",
    "第三方登录的利弊",
    "个人场景的零信任清单",
    "家庭物联网也要分段",
    "身份拼图如何被利用",
    "社交与招聘场景",
    "IP 与隐私工具的关系",
    "家庭宽带 IP 变化",
    "公共网络操作分级",
    "额外习惯",
    "支付与验证码",
    "降低追踪的组合拳",
    "账户登录对追踪的影响",
    "仿冒站的现代特征",
    "短链与二维码",
]

# Unique add-ons for non-priority articles after stripping templates
ADDONS = {
    "protect-mobile-data": (
        "<h2>移动端优先控制项</h2><p>锁屏、系统更新、官方商店安装来源，以及谨慎授予短信/无障碍/设备管理员权限，构成手机数据保护的基础。淘汰设备前退出云会话并恢复出厂。</p>"
        "<h2>相关阅读</h2><p>结合 <a href=\"/articles/protect-online-accounts\">账户保护</a> 与 <a href=\"/articles/protect-online-privacy\">网络隐私</a> 一起配置，避免只加固设备却忽略邮箱。</p>"
    ),
    "windows-network-security-settings": (
        "<h2>Windows 网络核对清单</h2><p>公用/专用配置文件、防火墙、远程桌面开关与自动更新应优先确认。不明软件要求关闭防火墙时要警惕。</p>"
        "<h2>相关阅读</h2><p>公共场所连接见 <a href=\"/articles/public-wifi-safety\">公共 Wi-Fi 安全</a>；流量加密概念见 <a href=\"/articles/network-traffic-encryption\">网络流量加密</a>。</p>"
    ),
    "why-data-encryption-matters": (
        "<h2>传输、静态与端到端</h2><p>TLS 保护传输；磁盘/备份加密保护丢失设备上的静态数据；端到端加密限制服务端读取内容。三者解决不同问题，见 <a href=\"/articles/what-is-end-to-end-encryption\">端到端加密</a>。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/network-traffic-encryption\">网络流量加密</a> · <a href=\"/articles/create-strong-passwords\">强密码</a></p>"
    ),
    "protect-online-accounts": (
        "<h2>核心账户优先</h2><p>先保护邮箱与密码管理器，再保护金融与云盘。启用双重验证并离线保存恢复码，定期检查转发规则与授权应用。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/two-factor-authentication-guide\">双重验证指南</a> · <a href=\"/articles/identify-phishing-attacks\">识别钓鱼</a> · <a href=\"/articles/create-strong-passwords\">强密码</a></p>"
    ),
    "protect-digital-identity": (
        "<h2>降低身份拼图暴露</h2><p>避免在同一处同时公开姓名、电话与证件号。证件提交走官方渠道并注明用途；旧账号不用就注销。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/prevent-personal-data-leaks\">防止个人数据泄露</a> · <a href=\"/articles/protect-online-accounts\">保护在线账户</a></p>"
    ),
    "zero-trust-security": (
        "<h2>个人可借鉴的原则</h2><p>不默认信任内网；敏感操作再验证；最小权限；共享链接设过期。家庭物联网尽量网段隔离。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/protect-online-accounts\">账户安全</a> · <a href=\"/articles/check-network-security\">检查网络安全</a></p>"
    ),
    "safe-public-network-use": (
        "<h2>公共网络操作建议</h2><p>高敏感事务改用移动数据；必须使用公共 Wi-Fi 时确认 HTTPS，并考虑可信隧道。门户页只填上网所需信息。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/public-wifi-safety\">公共 Wi-Fi 安全吗</a> · <a href=\"/articles/what-is-vpn\">VPN</a> · <a href=\"/articles/what-is-https\">HTTPS</a></p>"
    ),
    "choose-secure-network-connection": (
        "<h2>按场景选择连接</h2><p>家庭网更新路由固件并隔离访客；外出优先移动数据办理敏感事务；公司设备遵守分区策略。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/check-network-security\">网络自检</a> · <a href=\"/articles/public-wifi-safety\">公共 Wi-Fi</a></p>"
    ),
    "browser-privacy-settings": (
        "<h2>浏览器可先改的项</h2><p>自动更新、站点权限最小化、限制第三方存储、慎装扩展。按场景分离登录配置。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/how-online-tracking-works\">在线追踪</a> · <a href=\"/articles/protect-online-privacy\">保护网络隐私</a> · <a href=\"/articles/identify-malicious-websites\">识别恶意网站</a></p>"
    ),
    "what-is-ip-address": (
        "<h2>IP 与身份的关系</h2><p>IP 可指向接入网络与大致区域，常用于风控，但通常不等于精确门牌，也不等于掌握全部身份。账号与指纹往往更稳定。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/what-is-vpn\">VPN 如何改变出口 IP</a> · <a href=\"/articles/how-dns-servers-work\">DNS</a></p>"
    ),
    "how-online-tracking-works": (
        "<h2>常见追踪信号</h2><p>Cookie、像素、本地存储、广告标识与指纹可跨站拼接。登录态会让识别更稳定。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/browser-privacy-settings\">浏览器隐私设置</a> · <a href=\"/articles/protect-online-privacy\">保护网络隐私</a></p>"
    ),
    "two-factor-authentication-guide": (
        "<h2>验证方式优先级</h2><p>安全密钥/通行密钥优先，其次应用生成验证码，短信仍优于没有 2FA。启用后立即保存恢复码。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/protect-online-accounts\">保护在线账户</a> · <a href=\"/articles/create-strong-passwords\">强密码</a> · <a href=\"/articles/identify-phishing-attacks\">防钓鱼</a></p>"
    ),
    "identify-malicious-websites": (
        "<h2>判断仿冒站</h2><p>不要只看小锁。核对域名拼写，从官方应用进入，警惕紧急话术与索要验证码。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/identify-phishing-attacks\">钓鱼攻击</a> · <a href=\"/articles/what-is-https\">HTTPS 能证明什么</a></p>"
    ),
    "identify-phishing-attacks": (
        "<h2>反制要点</h2><p>不在邮件内点登录链；验证码只用于你主动发起的登录；付款账户变更用第二渠道确认。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/identify-malicious-websites\">恶意网站</a> · <a href=\"/articles/protect-online-accounts\">账户保护</a> · <a href=\"/articles/two-factor-authentication-guide\">双重验证</a></p>"
    ),
    "how-dns-servers-work": (
        "<h2>解析器看到什么</h2><p>DNS 将域名翻译为 IP，解析器能看到查询域名。加密 DNS 保护传输，但不替代 HTTPS 对内容的保护。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/what-is-dns-leak\">DNS 泄露</a> · <a href=\"/articles/what-is-https\">HTTPS</a> · <a href=\"/articles/what-is-ip-address\">IP 地址</a></p>"
    ),
    "common-cybersecurity-myths": (
        "<h2>用清单替代口号</h2><p>“我没有重要数据”“有杀毒就够”“有 HTTPS 就绝对可信”都不成立。改为：独立密码、双重验证、更新、少授权、慢点链接。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/create-strong-passwords\">强密码</a> · <a href=\"/articles/what-is-https\">HTTPS</a> · <a href=\"/articles/protect-online-privacy\">网络隐私</a></p>"
    ),
    "check-network-security": (
        "<h2>家庭网络自检</h2><p>改默认路由口令、检查已连接设备、关闭不必要远程管理、确认 DNS 未被篡改，并保持固件更新。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/choose-secure-network-connection\">选择安全连接</a> · <a href=\"/articles/how-dns-servers-work\">DNS</a> · <a href=\"/articles/public-wifi-safety\">公共 Wi-Fi</a></p>"
    ),
    "create-strong-passwords": (
        "<h2>长度与唯一性</h2><p>优先足够长且每站唯一，交由密码管理器生成。短而复杂却到处复用，仍会在泄露后被撞库。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/two-factor-authentication-guide\">双重验证</a> · <a href=\"/articles/protect-online-accounts\">账户保护</a> · <a href=\"/articles/choose-privacy-tools\">选择隐私工具</a></p>"
    ),
    "prevent-personal-data-leaks": (
        "<h2>最小化与止损</h2><p>少提交证件与通讯录；外链设过期。若已泄露：改密、下线会话、检查转发与网盘分享。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/protect-digital-identity\">数字身份</a> · <a href=\"/articles/protect-online-privacy\">网络隐私</a> · <a href=\"/articles/identify-phishing-attacks\">防钓鱼</a></p>"
    ),
    "what-is-https": (
        "<h2>HTTPS 保护什么</h2><p>TLS 保护浏览器与网站间的传输，并在校验证常时确认域名匹配。它不证明页面无欺诈，也不能保护你在假站输入的内容。</p>"
        "<h2>相关阅读</h2><p><a href=\"/articles/network-traffic-encryption\">流量加密</a> · <a href=\"/articles/identify-malicious-websites\">恶意网站</a> · <a href=\"/articles/what-is-dns-leak\">DNS 泄露</a></p>"
    ),
}

META = {
    "protect-mobile-data": "从权限、更新、备份与淘汰流程说明如何保护手机中的个人数据与账号会话。",
    "windows-network-security-settings": "梳理 Windows 上公用网络、防火墙、远程桌面与更新等关键网络安全设置。",
    "why-data-encryption-matters": "区分传输加密、静态加密与端到端加密，说明密钥与备份为何同样关键。",
    "protect-online-accounts": "按核心账户优先顺序，说明密码、双重验证、会话与授权应用的保护方法。",
    "protect-digital-identity": "说明数字身份如何被拼接利用，以及降低证件与联系方式暴露的做法。",
    "zero-trust-security": "用个人可执行的语言解释零信任：持续验证、最小权限与分段访问。",
    "safe-public-network-use": "给出公共网络上按敏感度分级的使用建议与证书告警处理方式。",
    "choose-secure-network-connection": "按家庭、外出与办公场景选择更稳妥的网络连接策略。",
    "browser-privacy-settings": "说明浏览器权限、第三方存储、扩展与配置隔离等隐私设置要点。",
    "what-is-ip-address": "解释 IP 地址能说明什么、不能说明什么，以及它与风控和隐私工具的关系。",
    "how-online-tracking-works": "介绍 Cookie、指纹与登录态等追踪信号，以及降低跨站识别的思路。",
    "two-factor-authentication-guide": "比较安全密钥、验证器应用与短信等双重验证方式及恢复策略。",
    "identify-malicious-websites": "说明仿冒站特征、域名核对与扫码/短链风险，避免只看 HTTPS 小锁。",
    "identify-phishing-attacks": "识别钓鱼话术与商务邮件妥协，并给出不在邮件内登录的反制步骤。",
    "how-dns-servers-work": "通俗解释 DNS 解析路径、加密 DNS 的作用边界与家庭统一配置的好处。",
    "common-cybersecurity-myths": "澄清“无重要数据”“杀毒即安全”“HTTPS 等于可信”等常见误区。",
    "check-network-security": "提供家庭路由与设备侧的网络安全自检顺序与发现陌生设备后的处理。",
    "create-strong-passwords": "强调长度与唯一性，说明密码管理器与泄露后轮换的实践方法。",
    "prevent-personal-data-leaks": "从数据最小化、外链治理与泄露止损顺序减少个人数据暴露。",
    "what-is-https": "解释 HTTPS/TLS 的保护范围、证书警告处理，以及它不能证明的事项。",
}

DEFAULT_SOURCES = {
    "protect-mobile-data": [
        {"title": "OWASP Mobile Top 10", "url": "https://owasp.org/www-project-mobile-top-10/"},
        {"title": "CISA: Mobile Device Security", "url": "https://www.cisa.gov/topics/cybersecurity-best-practices"},
    ],
    "windows-network-security-settings": [
        {"title": "Microsoft: Windows security", "url": "https://support.microsoft.com/windows"},
        {"title": "CISA Cybersecurity Best Practices", "url": "https://www.cisa.gov/topics/cybersecurity-best-practices"},
    ],
    "why-data-encryption-matters": [
        {"title": "NIST Cryptography", "url": "https://www.nist.gov/cryptography"},
        {"title": "Cloudflare: What is encryption?", "url": "https://www.cloudflare.com/learning/ssl/what-is-encryption/"},
    ],
    "protect-online-accounts": [
        {"title": "NIST Digital Identity Guidelines", "url": "https://pages.nist.gov/800-63-3/"},
        {"title": "OWASP Authentication Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html"},
    ],
    "protect-digital-identity": [
        {"title": "EFF SSD", "url": "https://ssd.eff.org/"},
        {"title": "OWASP Top Ten", "url": "https://owasp.org/www-project-top-ten/"},
    ],
    "zero-trust-security": [
        {"title": "NIST SP 800-207 Zero Trust Architecture", "url": "https://csrc.nist.gov/pubs/sp/800/207/final"},
        {"title": "CISA Zero Trust Maturity Model", "url": "https://www.cisa.gov/zero-trust-maturity-model"},
    ],
    "safe-public-network-use": [
        {"title": "FTC: Public Wi-Fi", "url": "https://consumer.ftc.gov/articles/how-safe-your-public-wi-fi-network"},
        {"title": "EFF SSD", "url": "https://ssd.eff.org/"},
    ],
    "choose-secure-network-connection": [
        {"title": "CISA Best Practices", "url": "https://www.cisa.gov/topics/cybersecurity-best-practices"},
        {"title": "Cloudflare Learning Center", "url": "https://www.cloudflare.com/learning/"},
    ],
    "browser-privacy-settings": [
        {"title": "Mozilla Firefox Privacy", "url": "https://support.mozilla.org/kb/enhanced-tracking-protection-firefox-desktop"},
        {"title": "EFF SSD", "url": "https://ssd.eff.org/"},
    ],
    "what-is-ip-address": [
        {"title": "Cloudflare: What is an IP address?", "url": "https://www.cloudflare.com/learning/dns/glossary/what-is-an-ip-address/"},
        {"title": "MDN: IP Address", "url": "https://developer.mozilla.org/en-US/docs/Glossary/IP_Address"},
    ],
    "how-online-tracking-works": [
        {"title": "EFF: Cover your tracks", "url": "https://coveryourtracks.eff.org/"},
        {"title": "Mozilla: Fingerprinting", "url": "https://developer.mozilla.org/en-US/docs/Web/Privacy/Guides/Firefox_and_privacy"},
    ],
    "two-factor-authentication-guide": [
        {"title": "NIST SP 800-63B Authentication", "url": "https://pages.nist.gov/800-63-3/sp800-63b.html"},
        {"title": "OWASP Multifactor Auth Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html"},
    ],
    "identify-malicious-websites": [
        {"title": "OWASP Phishing", "url": "https://owasp.org/www-community/attacks/Phishing"},
        {"title": "Google Safe Browsing", "url": "https://safebrowsing.google.com/"},
    ],
    "identify-phishing-attacks": [
        {"title": "CISA: Phishing Guidance", "url": "https://www.cisa.gov/topics/cyber-threats-and-advisories/phishing"},
        {"title": "OWASP Phishing", "url": "https://owasp.org/www-community/attacks/Phishing"},
    ],
    "how-dns-servers-work": [
        {"title": "Cloudflare: What is DNS?", "url": "https://www.cloudflare.com/learning/dns/what-is-dns/"},
        {"title": "RFC 1035 Domain Names", "url": "https://www.rfc-editor.org/rfc/rfc1035"},
    ],
    "common-cybersecurity-myths": [
        {"title": "CISA Best Practices", "url": "https://www.cisa.gov/topics/cybersecurity-best-practices"},
        {"title": "OWASP Top Ten", "url": "https://owasp.org/www-project-top-ten/"},
    ],
    "check-network-security": [
        {"title": "CISA: Home Network Security", "url": "https://www.cisa.gov/news-events/news/home-network-security"},
        {"title": "NIST Cybersecurity Framework", "url": "https://www.nist.gov/cyberframework"},
    ],
    "create-strong-passwords": [
        {"title": "NIST SP 800-63B passwords", "url": "https://pages.nist.gov/800-63-3/sp800-63b.html"},
        {"title": "OWASP Password Storage Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"},
    ],
    "prevent-personal-data-leaks": [
        {"title": "OWASP Top Ten", "url": "https://owasp.org/www-project-top-ten/"},
        {"title": "EFF Privacy", "url": "https://www.eff.org/issues/privacy"},
    ],
    "what-is-https": [
        {"title": "MDN: HTTPS", "url": "https://developer.mozilla.org/en-US/docs/Glossary/HTTPS"},
        {"title": "Cloudflare: What is HTTPS?", "url": "https://www.cloudflare.com/learning/ssl/what-is-https/"},
        {"title": "RFC 9110 HTTP Semantics", "url": "https://www.rfc-editor.org/rfc/rfc9110"},
    ],
}

FAQ_FALLBACK = [
    {"q": "这篇文章适合谁？", "a": "适合希望理解相关概念边界、并完成基础配置检查的普通用户与技术初学者。"},
    {"q": "读完后应先做什么？", "a": "先完成文中成本最低、失败后果最高的一项改动，并用结果验证是否生效。"},
]


def plain_len(html: str) -> int:
    return len(re.sub(r"<[^>]+>", "", html or ""))


def strip_templates(html: str) -> str:
    parts = re.split(r"(?=<h2>)", html or "")
    kept = []
    for part in parts:
        m = re.match(r"<h2>(.*?)</h2>", part, re.S)
        if m:
            title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            # drop if title contains any template marker or equals one
            if any(t in title for t in TEMPLATE_H2):
                continue
            # also drop sections whose first paragraph is a known boilerplate opener
        text = re.sub(r"<[^>]+>", "", part)
        boilder = [
            "当文章提到 VPN、加密或隐私工具时",
            "完成设置后，不要只停留在",
            "安全知识的价值不在于记住全部术语",
            "如果设备和账户存在共用情况",
            "先完成一件今天就能做完的事",
            "不同系统、浏览器和服务的菜单名称会变化",
            "一项安全措施是否值得做，可以看三点",
            "账户层负责身份验证，设备层负责更新与权限",
            "把概念落到自己的设备与账户上时，先问三个问题",
            "下次改密码、连公共网络、安装扩展或点击登录链接时",
            "每周：留意异常登录通知",
        ]
        if any(b in text for b in boilder) and part.strip().startswith("<h2>"):
            continue
        # drop bare boilerplate paragraphs even without h2
        if part.strip().startswith("<p>") and any(b in text for b in boilder):
            continue
        kept.append(part)
    cleaned = "".join(kept)
    # remove leftover identical boilerplate paragraphs
    for b in [
        "当文章提到 VPN、加密或隐私工具时，请把它们理解为特定问题的可选方案，而不是整套安全体系的替代品。任何指向商业服务的链接都应被清楚标注，并且不能承诺绝对匿名或绝对安全。",
        "完成设置后，不要只停留在“我好像做过了”。用结果验证：能否用备用方式登录？陌生设备是否已被退出？关键通知是否打开？备份是否还能恢复？只有抽查过结果，设置才算真正完成。",
        "安全知识的价值不在于记住全部术语，而在于遇到不确定情况时知道如何放慢速度、核实对象，并选择损害最小的下一步。把“先核实，再操作”变成习惯，已经能避免大量常见问题。",
        "如果设备和账户存在共用情况，先约定谁负责更新、谁保管恢复码、出问题时联系谁。很多安全失败来自责任不清，而不是缺少工具。",
        "先完成一件今天就能做完的事：检查一个最重要账户的登录方式与恢复信息，或关闭一个不再需要的应用权限。安全改进最怕“什么都想做，结果什么都没做”。",
        "不同系统、浏览器和服务的菜单名称会变化。本文提供的是通用原则；涉及具体按钮路径时，请以当前版本的官方帮助文档为准，避免被过时截图误导。",
        "一项安全措施是否值得做，可以看三点：实施成本是否低、失败后果是否高、以及它是否依赖你长期记得某个复杂步骤。优先选择“设置一次、长期生效”的措施，例如独立密码、双重验证、自动更新和关闭多余权限。",
        "账户层负责身份验证，设备层负责更新与权限，网络层负责连接与传输，操作层负责识别钓鱼和异常请求。任何一层长期缺失，都会成为短板。",
        "把概念落到自己的设备与账户上时，先问三个问题：我要保护的对象是什么？最可能的失败方式是什么？我今天能完成哪一个低成本改动？围绕这三个问题行动，通常比收集更多术语更有用。",
        "下次改密码、连公共网络、安装扩展或点击登录链接时，主动复盘本文对应的检查点。安全能力是在真实操作里练出来的，不是在收藏夹里堆积出来的。",
    ]:
        cleaned = cleaned.replace(f"<p>{b}</p>", "")
    # remove empty checklist leftovers from 建议的复查频率 etc if any remain as ul-only orphans - skip
    cleaned = re.sub(r"(?:<h2>[^<]*</h2>\s*)?(?:<ul>\s*<li>每周：.*?</ul>)", "", cleaned, flags=re.S)
    cleaned = re.sub(r"(?:<ul>\s*<li>保护邮箱：.*?</ul>)", "", cleaned, flags=re.S)
    return cleaned.strip()


def build_payload() -> list[dict]:
    out = []
    for a in AUDIT:
        slug = a["slug"]
        if slug in PRIORITY:
            p = PRIORITY[slug]
            content = p["content_html"].strip()
            faq = p["faq_json"]
            sources = p["sources_json"]
            seo_title = p["seo_title"]
            meta = p["meta_description"]
            kind = "priority"
        else:
            content = strip_templates(a["content_html"])
            addon = ADDONS.get(slug, "")
            if addon and addon not in content:
                content = (content + "\n" + addon).strip()
            faq = FAQ_FALLBACK
            # keep existing faq if decent and not generic-only - still replace with topic FAQ if present in ADDONS context
            try:
                old = json.loads(a["faq_json"]) if isinstance(a["faq_json"], str) else (a["faq_json"] or [])
            except Exception:
                old = []
            # prefer short unique faqs if old ones are about VPN boilerplate for non-vpn articles
            faq = old if len(old) >= 2 and slug.startswith(("what-is", "vpn", "identify", "create", "two-factor", "browser", "how-", "check-", "common-", "prevent-", "choose-", "protect-", "safe-", "windows-", "why-", "zero-")) else FAQ_FALLBACK
            if len(old) >= 2:
                faq = old
            sources = DEFAULT_SOURCES.get(slug, [
                {"title": "OWASP Top Ten", "url": "https://owasp.org/www-project-top-ten/"},
                {"title": "EFF Privacy", "url": "https://www.eff.org/issues/privacy"},
            ])
            seo_title = a["seo_title"] if len(a.get("seo_title") or "") >= 12 else a["title"]
            meta = META.get(slug) or a["meta_description"]
            if len(meta) < 50:
                meta = META.get(slug, a["meta_description"] + " 本文说明关键概念、常见误区与可执行检查项。")
            kind = "cleanup"
        out.append({
            "slug": slug,
            "seo_title": seo_title,
            "meta_description": meta[:155],
            "content_html": content,
            "faq_json": json.dumps(faq, ensure_ascii=False),
            "sources_json": json.dumps(sources, ensure_ascii=False),
            "chars": plain_len(content),
            "kind": kind,
            "internal": len(set(re.findall(r"/articles/([a-z0-9-]+)", content))),
        })
    return out


def push(payload: list[dict]) -> None:
    local = ROOT / "tools" / "_phase3_payload.json"
    local.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    php = r'''<?php
$config=require "/var/www/chinalanding/config/config.php";
$pdo=new PDO($config["db"]["dsn"],$config["db"]["user"],$config["db"]["password"],[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
$rows=json_decode(file_get_contents("/tmp/phase3_payload.json"),true);
$upd=$pdo->prepare("UPDATE articles SET seo_title=?, meta_description=?, content_html=?, faq_json=?, sources_json=?, updated_at=NOW() WHERE slug=?");
$n=0;
foreach($rows as $r){
  $upd->execute([$r["seo_title"],$r["meta_description"],$r["content_html"],$r["faq_json"],$r["sources_json"],$r["slug"]]);
  $n += $upd->rowCount()>0?1:0;
}
echo "updated=$n total=".count($rows)."\n";
$q=$pdo->query("SELECT slug, CHAR_LENGTH(REGEXP_REPLACE(content_html,'<[^>]+>','')) n FROM articles ORDER BY n");
foreach($q as $row) echo $row["n"]."\t".$row["slug"]."\n";
'''
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect("94.249.188.139", username="root", password="qweasd333123", timeout=25, look_for_keys=False, allow_agent=False)
    s = c.open_sftp()
    s.put(str(local), "/tmp/phase3_payload.json")
    with s.file("/tmp/phase3_apply.php", "w") as f:
        f.write(php)
    s.close()
    stdin, stdout, stderr = c.exec_command("php /tmp/phase3_apply.php; apachectl graceful")
    print((stdout.read() + stderr.read()).decode("utf-8", "replace"))
    c.close()


def main() -> None:
    payload = build_payload()
    print("built", len(payload))
    for r in payload:
        print(f"{r['kind']:8} {r['chars']:4d} intl={r['internal']} {r['slug']}")
    # ensure no template markers remain in priority
    for r in payload:
        hits = [t for t in ["可立即执行的下一步", "分层防护怎么做", "延伸思考", "结合实际场景理解"] if t in r["content_html"]]
        if hits:
            print("WARN templates still in", r["slug"], hits)
    push(payload)
    (ROOT / "tools" / "articles_all.json").write_text(
        json.dumps([{**{k: a.get(k) for k in a}, **{
            "content_html": next(p["content_html"] for p in payload if p["slug"] == a["slug"]),
            "seo_title": next(p["seo_title"] for p in payload if p["slug"] == a["slug"]),
            "meta_description": next(p["meta_description"] for p in payload if p["slug"] == a["slug"]),
            "faq_json": json.loads(next(p["faq_json"] for p in payload if p["slug"] == a["slug"])),
            "sources_json": json.loads(next(p["sources_json"] for p in payload if p["slug"] == a["slug"])),
        }} for a in AUDIT], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("local articles_all.json synced")


if __name__ == "__main__":
    main()
