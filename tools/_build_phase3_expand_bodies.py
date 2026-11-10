# -*- coding: utf-8 -*-
"""Build tools/_phase3_expand_bodies.json with length validation."""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

ROOT = Path(r"C:\Users\1\Documents\chinalanding\tools")
OUT = ROOT / "_phase3_expand_bodies.json"

FORBIDDEN = [
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
]

TAG_RE = re.compile(r"<[^>]+>")


def plain(html: str) -> str:
    return re.sub(r"\s+", "", TAG_RE.sub("", html))


def entry(content_html: str, faq, sources, meta_description: str) -> dict:
    return {
        "content_html": content_html,
        "faq_json": faq,
        "sources_json": sources,
        "meta_description": meta_description,
    }


ARTICLES: dict[str, dict] = {}

ARTICLES["protect-mobile-data"] = entry(
    """<p>手机往往同时承载聊天、支付、门禁与二次验证。数据保护不是给相册上锁而已，而是控制「谁能读什么」以及「旧设备会不会继续在线」。</p>
<h2>锁屏与系统更新</h2>
<p>开启强密码或生物识别，并设置自动锁屏间隔。系统与安全补丁延迟安装，会把已公开的漏洞留给你日常点击的链接去利用。</p>
<h2>应用权限边界</h2>
<ul>
<li>短信、通知读取、无障碍、设备管理员等权限，只给确需的应用并保持定期复核。</li>
<li>仅通过官方商店或厂商渠道安装；来源不明的 APK 常伪装成「免费会员」。</li>
<li>云同步与备份要分清：便利与泄露面会一起放大。</li>
</ul>
<h2>会话与淘汰</h2>
<p>换机前在 iCloud、Google 账户与常用 App 中退出全部会话；执行恢复出厂并确认旧 SIM 与存储卡已移除。丢失手机时，优先远程擦除再补办业务。</p>
<p>延伸阅读：<a href="/articles/protect-online-accounts">保护在线账户</a>、<a href="/articles/two-factor-authentication-guide">双重验证</a>、<a href="/articles/prevent-personal-data-leaks">防止个人数据泄露</a>。</p>""",
    [
        {"q": "手机杀毒软件是否足够？", "a": "单靠杀毒不能替代权限控制、系统更新与账户防护；三者应同时存在。"},
        {"q": "云相册备份算隐私风险吗？", "a": "默认云同步会扩大泄露面；敏感内容可本地加密或关闭自动上传。"},
        {"q": "淘汰旧手机前必做哪一步？", "a": "先登出所有云账户并撤销设备会话，再恢复出厂设置。"},
    ],
    [
        {"title": "OWASP Mobile Top 10", "url": "https://owasp.org/www-project-mobile-top-10/"},
        {"title": "CISA Cybersecurity Best Practices", "url": "https://www.cisa.gov/topics/cybersecurity-best-practices"},
        {"title": "Microsoft account security", "url": "https://support.microsoft.com/account-billing/account-security"},
    ],
    "从权限、锁屏、安装来源、云备份与换机擦除说明如何保护手机里的个人数据与活跃登录会话。",
)

ARTICLES["choose-secure-network-connection"] = entry(
    """<p>「更安全」的网络取决于你要完成的操作，而不是单个网速数字。家庭宽带、蜂窝数据、酒店 Wi-Fi 与公司 VPN 彼此信任边界不同，混用策略很容易在最后一公里出错。</p>
<h2>按地点理解信任模型</h2>
<p>家中路由器由你掌握口令与固件节奏，但仍要防范默认凭证与访客网段串扰。外出时蜂窝链路通常比陌生 Wi-Fi 更少被动监听，但恶意 App 仍可在本机偷数据。</p>
<h2>敏感操作如何选型</h2>
<ol>
<li>改密码、转账、提交证件：优先蜂窝或个人热点。</li>
<li>一般浏览：确认站点 <a href="/articles/what-is-https">HTTPS</a> 即可。</li>
<li>长期远程办公：走公司批准的路径，而不是来历不明加速器。</li>
</ol>
<h2>分段的实际意义</h2>
<p>访客 Wi-Fi、IoT 设备与办公电脑最好隔离网段，避免一台被控后横向扫描全屋。酒店网络尤其不要与家中 NAS 直通。</p>
<p>相关：<a href="/articles/public-wifi-safety">公共 Wi-Fi 安全</a>、<a href="/articles/check-network-security">检查家庭网络安全</a>、<a href="/articles/what-is-vpn">VPN 原理</a>。</p>""",
    [
        {"q": "蜂窝数据是否绝对安全？", "a": "相对未知 Wi-Fi 更可控，但恶意软件与钓鱼仍可在设备层窃密。"},
        {"q": "家里需要两套 Wi-Fi 吗？", "a": "分离访客与智能设备网段能显著降低横向移动风险。"},
        {"q": "旅行时公司 VPN 与个人隧道能叠用吗？", "a": "除非 IT 明确要求，否则叠加会增加复杂性与误配置概率。"},
    ],
    [
        {"title": "Cloudflare Learning: Network layers", "url": "https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/"},
        {"title": "NIST SP 800-207 Zero Trust", "url": "https://csrc.nist.gov/publications/detail/sp/800-207/final"},
        {"title": "CISA Secure Wi-Fi", "url": "https://www.cisa.gov/topics/cybersecurity-best-practices"},
    ],
    "按家庭、外出与办公场景比较蜂窝、Wi-Fi 与受管隧道的信任边界，帮助选择更稳妥的网络连接方式。",
)

ARTICLES["windows-network-security-settings"] = entry(
    """<p>Windows 既是办公主力，也常连公共热点。系统里几处与「网络配置文件、防火墙、远程访问」相关的开关，决定陌生局域网能否摸到你的共享与远程桌面服务。</p>
<h2>公用与专用配置文件</h2>
<p>在咖啡馆应把当前连接标为「公用」：系统会收紧发现与文件共享。回到家中再切回「专用」，避免长期以宽松策略暴露服务。</p>
<h2>防火墙与入站规则</h2>
<ul>
<li>保持 Windows 防火墙开启；第三方安全软件若要求彻底关闭内置防火墙，需确认其替代能力。</li>
<li>没有明确需求时，关闭「远程桌面」与不必要的文件共享。</li>
<li>检查哪些应用被允许通过防火墙，禁用已不再使用的旧工具。</li>
</ul>
<h2>更新与网络堆栈</h2>
<p>延迟累积的安全更新会连带修复 DHCP、Wi-Fi 驱动与 <code>TLS</code> 栈问题。启用自动更新并在重要补丁后重启一次。</p>
<p>参阅 <a href="/articles/choose-secure-network-connection">选择安全网络连接</a>、<a href="/articles/network-traffic-encryption">网络流量加密</a>、<a href="/articles/public-wifi-safety">公共 Wi-Fi</a>。</p>""",
    [
        {"q": "公用网络配置文件会影响哪些功能？", "a": "主要限制设备发现、网络浏览与部分共享服务，降低被同网段扫描的概率。"},
        {"q": "关闭防火墙能提升游戏延迟吗？", "a": "极少数场景如此，但通常以显著扩大攻击面为代价，不推荐日常关闭。"},
        {"q": "如何确认远程桌面已关闭？", "a": "在系统设置中查看远程桌面开关，并核对防火墙入站规则无 RDP 例外。"},
    ],
    [
        {"title": "Microsoft: Windows Defender Firewall", "url": "https://learn.microsoft.com/windows/security/operating-system-security/network-security/windows-firewall/"},
        {"title": "Microsoft: Network location types", "url": "https://learn.microsoft.com/windows/security/operating-system-security/network-security/windows-firewall/rules"},
        {"title": "CISA Cyber hygiene", "url": "https://www.cisa.gov/topics/cybersecurity-best-practices"},
    ],
    "梳理 Windows 公用网络配置文件、防火墙、远程桌面与系统更新等设置，降低在陌生局域网中被探测的风险。",
)

ARTICLES["protect-online-accounts"] = entry(
    """<p>多数数字生活围绕少数枢纽账户旋转：邮箱、Apple ID/Google 账户、密码管理器与银行 App。失守其中一个，恢复密码与绑卡的连锁往往比丢一部手机更快。</p>
<h2>先把枢纽理清楚</h2>
<p>列出「能重置别人密码」的邮箱与手机号，列为一级保护对象。二级账户可共享密码管理器条目，但不应共享同一口令。</p>
<h2>口令、2FA 与会话</h2>
<ul>
<li>每站独立的长口令，由 <a href="/articles/create-strong-passwords">强密码</a> 策略与密码管理器维护。</li>
<li>为邮箱与支付启用 <a href="/articles/two-factor-authentication-guide">双重验证</a>，并离线保存恢复码。</li>
<li>定期查看登录设备列表，撤销陌生 OAuth 与长期闲置会话。</li>
</ul>
<h2>第三方登录与邮件规则</h2>
<p>用 Google/微信登录第三方时，实质是把控制权外借。检查「转发到其他地址」与「过滤 silently 删除」一类隐蔽规则——这是账户被控后的常见后门。</p>
<p>配合阅读 <a href="/articles/identify-phishing-attacks">识别钓鱼</a> 与 <a href="/articles/protect-digital-identity">保护数字身份</a>。</p>""",
    [
        {"q": "所有网站都要开双重验证吗？", "a": "至少覆盖邮箱、密码管理器、云盘与金融账户；其余按敏感度逐步扩展。"},
        {"q": "第三方登录要不要全关？", "a": "不必一刀切，但应定期审查授权列表，删除不再使用的应用。"},
        {"q": "收到登录提醒但不是我操作怎么办？", "a": "立即改密、下线所有会话，并检查邮箱转发与恢复手机是否被改。"},
    ],
    [
        {"title": "NIST Digital Identity Guidelines", "url": "https://pages.nist.gov/800-63-3/"},
        {"title": "OWASP Authentication Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html"},
        {"title": "CISA MFA guidance", "url": "https://www.cisa.gov/resources-tools/resources/multi-factor-authentication-mfa"},
    ],
    "按枢纽账户优先顺序说明独立密码、双重验证、会话管理与邮件规则检查，降低在线账户被接管风险。",
)

ARTICLES["safe-public-network-use"] = entry(
    """<p>机场、商场与展会 Wi-Fi 让你快速上线，却极少提供对你数据的忠诚保证。把公共网络看成「能传流量但不背书身份」的管道，心态会清晰很多。</p>
<h2>上线前三件事</h2>
<p>核对 SSID 是否与现场铭牌一致，关闭自动加入开放热点，确认笔记本网络类型为公用。未完成系统补丁就别急着登录网银。</p>
<h2>使用中按敏感度分级</h2>
<ul>
<li><strong>低敏感：</strong>新闻、地图——留意 <a href="/articles/what-is-https">HTTPS</a> 与小锁是否对应正确域名。</li>
<li><strong>中敏感：</strong>邮箱、社交——避免在门户页输入与上网无关的密码。</li>
<li><strong>高敏感：</strong>支付、改密、上传证件——切换蜂窝数据更稳妥。</li>
</ul>
<h2>离开后的清理</h2>
<p>断开并「忘记」网络；检查是否被安装了配置描述文件或抓包证书。若出现异常登录提醒，按 <a href="/articles/protect-online-accounts">账户保护</a> 流程止损。</p>
<p>另见 <a href="/articles/public-wifi-safety">公共 Wi-Fi 风险详解</a> 与 <a href="/articles/what-is-vpn">VPN 边界</a>。</p>""",
    [
        {"q": "门户页要填手机号注册 Wi-Fi 有风险吗？", "a": "可能用于营销或关联画像；只填最低必要信息，并避免重复使用重要手机号。"},
        {"q": "看到 HTTPS 就能在公共 Wi-Fi 付款吗？", "a": "HTTPS 保护传输，但不证明热点本身可信；高金额仍建议蜂窝链路。"},
        {"q": "离开后如何发现被装了证书？", "a": "在系统信任存储中查看新增根证书，陌生且无法说明来源的应删除。"},
    ],
    [
        {"title": "CISA Public Wi-Fi guidance", "url": "https://www.cisa.gov/news-events/news/protecting-yourself-using-public-wi-fi"},
        {"title": "Cloudflare: What is HTTPS?", "url": "https://www.cloudflare.com/learning/ssl/what-is-https/"},
        {"title": "EFF Surveillance Self-Defense", "url": "https://ssd.eff.org/"},
    ],
    "介绍公共网络使用前中后的习惯：核对热点、按敏感度分级操作、离开后的证书与会话检查。",
)

ARTICLES["how-online-tracking-works"] = entry(
    """<p>广告与数据分析行业需要你「可被辨认」，但不一定要知道真名。浏览器里的 Cookie、设备指纹与登录标识会在不同网站间拼接，形成跨站画像。</p>
<h2>识别手段如何叠加</h2>
<p>第一方 Cookie 记录你曾访问本站；第三方跟踪脚本在其他域读取标识符；像素信标上报打开邮件的时间。若你登录了统一账户，画像会与真实身份合并。</p>
<h2>指纹在不靠 Cookie 时登场</h2>
<p>字体列表、屏幕分辨率、Canvas 渲染差异与 WebGL 特征可形成概率性标识。清除 Cookie 并不自动让指纹归零。</p>
<h2>个人侧可调整的杠杆</h2>
<ul>
<li>分场景使用浏览器配置文件；限制第三方存储与追踪保护。</li>
<li>登录态下假设「已被关联」；敏感搜索使用独立环境。</li>
<li>理解 <a href="/articles/browser-privacy-settings">浏览器隐私设置</a> 与 <a href="/articles/protect-online-privacy">整体隐私策略</a> 的配合。</li>
</ul>
<p>技术背景可参考 MDN 对存储与跟踪防护的说明；策略上避免迷信「隐身模式等于隐身人」。</p>""",
    [
        {"q": "隐身窗口能阻止追踪吗？", "a": "主要不保留本地历史；跨站追踪、指纹与登录态仍可能存在。"},
        {"q": "禁用 Cookie 会影响购物网站吗？", "a": "可能影响登录与购物车；更常见做法是限制第三方 Cookie 而非全禁。"},
        {"q": "广告 ID 重置有用吗？", "a": "会打断部分移动广告关联，但登录账户后画像可能再次合并。"},
    ],
    [
        {"title": "MDN: State partitioning", "url": "https://developer.mozilla.org/en-US/docs/Web/Privacy/State_Partitioning"},
        {"title": "EFF: Browser fingerprinting", "url": "https://coveryourtracks.eff.org/"},
        {"title": "Cloudflare: What are cookies?", "url": "https://www.cloudflare.com/learning/privacy/what-are-cookies/"},
    ],
    "说明 Cookie、像素、指纹与登录态如何被组合用于跨站识别，并给出浏览器与习惯层面的削弱办法。",
)

ARTICLES["how-dns-servers-work"] = entry(
    """<p>在浏览器按下回车前，域名得先翻译成 IP。DNS 像电话簿：你问「example.com 在哪」，解析器记录这个问题，并返回答案。整个过程独立于网页是否使用 HTTPS。</p>
<h2>递归解析路径</h2>
<p>客户端通常把查询发给递归解析器（路由器、运营商或公共 DNS）。递归器若本地无缓存，会沿层次询问根、顶级域与权威服务器，最终拼出记录。</p>
<h2>记录类型与 TTL</h2>
<ul>
<li><code>A</code>/<code>AAAA</code> 指向 IP；<code>CNAME</code> 做别名。</li>
<li>TTL 决定缓存多久；过长的 TTL 让故障切换变慢，过短则增加查询量。</li>
</ul>
<h2>加密与隐私边界</h2>
<p>DoH/DoT 保护查询在链路上的窃听与篡改，但解析运营方仍能看到你问了哪些名。与 <a href="/articles/what-is-dns-leak">DNS 泄露</a>、<a href="/articles/what-is-ip-address">IP 地址</a> 话题一并理解更准确。</p>
<p>排错时可对照 <a href="/articles/check-network-security">家庭网络检查</a> 是否遭劫持解析。</p>""",
    [
        {"q": "换公共 DNS 会更快吗？", "a": "取决于地理位置与运营商路由；有时改善明显，有时几乎没有差异。"},
        {"q": "DNS 能看到网页内容吗？", "a": "不能；它只看到查询的域名，网页正文由 HTTPS 另行保护。"},
        {"q": "家长控制 DNS 如何工作？", "a": "通过返回阻断或引导 IP 过滤类别；与 HTTPS 内容过滤是不同层面。"},
    ],
    [
        {"title": "Cloudflare Learning: What is DNS?", "url": "https://www.cloudflare.com/learning/dns/what-is-dns/"},
        {"title": "RFC 1034", "url": "https://www.rfc-editor.org/rfc/rfc1034"},
        {"title": "MDN: DNS", "url": "https://developer.mozilla.org/en-US/docs/Glossary/DNS"},
    ],
    "用通俗步骤讲解 DNS 递归查询、常见记录类型与加密 DNS 的作用边界，并关联隐私与排错。",
)

ARTICLES["check-network-security"] = entry(
    """<p>家庭网络的安全感常来自「能上网就行」，直到陌生设备出现在路由列表里。周期性自查比事后灭火便宜得多，尤其是默认口令仍未修改的路由器。</p>
<h2>从网关开始</h2>
<p>登录管理界面，修改出厂管理员密码；关闭远程管理（WAN 侧 Web/SSH）。确认固件版本，有安全公告时优先升级。</p>
<h2>连接设备清点</h2>
<ul>
<li>对照家中真实设备核对 MAC 与主机名；陌生条目先隔离或改 Wi-Fi 密码。</li>
<li>访客网络与主网络分 SSID；智能插座与摄像头不要与 PC 同网段无隔离。</li>
<li>核对 DNS 是否被指向未知服务器，见 <a href="/articles/how-dns-servers-work">DNS 工作机制</a>。</li>
</ul>
<h2>向外延伸</h2>
<p>台式机启用防火墙；笔记本在公共场合用公用配置。需要远程回家访问时，用明确授权的隧道，而不是把管理端口直接暴露到互联网。</p>
<p>外出场景联动 <a href="/articles/choose-secure-network-connection">连接选型</a> 与 <a href="/articles/public-wifi-safety">公共 Wi-Fi</a> 习惯。</p>""",
    [
        {"q": "多久检查一次路由设备列表？", "a": "每月快速看一眼足够；更换密码或嵌入新 IoT 后应额外核对。"},
        {"q": "发现陌生设备一定被黑了吗？", "a": "也可能是访客或厂家预置名混淆；先断网再比对实物。"},
        {"q": "家用需要入侵检测吗？", "a": "非必需；对多数家庭，强口令、分网段与更新更重要。"},
    ],
    [
        {"title": "CISA SOHO router security", "url": "https://www.cisa.gov/news-events/news/soho-router-security"},
        {"title": "OWASP IoT Top 10", "url": "https://owasp.org/www-project-internet-of-things/"},
        {"title": "Microsoft: Home network security", "url": "https://support.microsoft.com/security"},
    ],
    "提供从路由器口令、固件、设备清单到 DNS 与防火墙的家庭网络安全自查顺序与异常处理方式。",
)

ARTICLES["why-data-encryption-matters"] = entry(
    """<p>加密把可读信息变成只有持有密钥者能还原的形式。它既不神奇，也不万能：不同场景需要传输加密、静态加密或端到端加密中的不同组合。</p>
<h2>三类问题，三种答案</h2>
<p>传输中窃听由 TLS/HTTPS 缓解；设备丢失或硬盘报废由磁盘与备份加密保护；希望云服务商也读不懂聊天内容，则需 <a href="/articles/what-is-end-to-end-encryption">端到端加密</a>。</p>
<h2>密钥与恢复同等重要</h2>
<p>丢了密钥等于丢了数据。密码管理器主密码、BitLocker 恢复密钥、2FA 备份码应像房产证复印件一样有安全存放点，而不是仅存同一台手机备忘录里。</p>
<h2>误区纠偏</h2>
<ul>
<li>「公司能恢复我邮件」说明不是端到端，合规与隐私要分清。</li>
<li>全盘加密不防钓鱼；恶意软件在加密前读取明文。</li>
<li>老旧算法（如短密钥 RSA）应随系统升级淘汰。</li>
</ul>
<p>传输层细节见 <a href="/articles/network-traffic-encryption">网络流量加密</a> 与 <a href="/articles/what-is-https">HTTPS 基础</a>。</p>""",
    [
        {"q": "网盘自带加密就够了吗？", "a": "取决于威胁模型；防范云运营方读取需客户端加密或 E2EE 通信。"},
        {"q": "BitLocker 与 VeraCrypt 差别？", "a": "前者与 Windows 深度集成；后者跨平台但更需自己管理启动配置。"},
        {"q": "加密会降低性能吗？", "a": "现代硬件加速下多数用户感觉不到；老旧设备上大文件可能略慢。"},
    ],
    [
        {"title": "NIST Cryptography", "url": "https://www.nist.gov/cryptography"},
        {"title": "Cloudflare: Encryption types", "url": "https://www.cloudflare.com/learning/ssl/types-of-encryption/"},
        {"title": "Microsoft: Device encryption", "url": "https://learn.microsoft.com/windows/security/operating-system-security/data-protection/device-encryption"},
    ],
    "区分传输、静态与端到端加密各自防什么，强调密钥备份的重要性，并澄清常见理解偏差。",
)

ARTICLES["zero-trust-security"] = entry(
    """<p>零信任不是买一款产品就能完成的项目，而是一组假设：内网与外网一样不可默认信任，每次访问都应经过身份、设备状态与最小权限的核验。</p>
<h2>企业语境里的核心句</h2>
<p>NIST 将其概括为持续验证、上下文感知访问与微分段。员工在家办公时，旧模型「连上 VPN 就通行整网」的风险被放大。</p>
<h2>个人能借鉴的习惯</h2>
<ul>
<li>不同用途使用不同账户；敏感云资源开启逐步验证。</li>
<li>共享链接设过期与密码；外部协作文件避免「任何人可编辑」长期敞开。</li>
<li>家中 IoT 单独网段，不给予访问 NAS 的默认路由。</li>
</ul>
<h2>不是什么</h2>
<p>零信任不意味着随时随地开 MFA 打断呼吸，而是把最高强度用在最高价值资产上。配合 <a href="/articles/protect-online-accounts">账户分层</a> 与 <a href="/articles/check-network-security">网络分段</a> 更接地气。</p>
<p>进一步理解访问边界：<a href="/articles/network-traffic-encryption">流量加密</a>、<a href="/articles/what-is-vpn">VPN 角色</a>。</p>""",
    [
        {"q": "零信任只适合大公司吗？", "a": "理念可缩小到家庭分网段、链接过期与设备清单，规模小也能实践。"},
        {"q": "装了零信任客户端就安全吗？", "a": "客户端只是执行点；策略不清仍会出现过度授权或错误分流。"},
        {"q": "与防火墙传统模型冲突吗？", "a": "互补关系；零信任强调身份与上下文，防火墙仍负责边界过滤。"},
    ],
    [
        {"title": "NIST SP 800-207", "url": "https://csrc.nist.gov/publications/detail/sp/800-207/final"},
        {"title": "CISA Zero Trust Maturity Model", "url": "https://www.cisa.gov/zero-trust-maturity-model"},
        {"title": "Cloudflare Zero Trust learning", "url": "https://www.cloudflare.com/learning/access-management/what-is-zero-trust/"},
    ],
    "用可读语言解释零信任假设、企业实践要点及个人在家分段、链接过期等方面可借鉴的做法。",
)

ARTICLES["what-is-ip-address"] = entry(
    """<p>IP 地址是网络层用来投递数据包的「门牌号」。没有它，回程流量找不到你的设备。版本上常见的 IPv4 像 203.0.113.5，IPv6 则更长，解决地址枯竭问题。</p>
<h2>公网与私网</h2>
<p>家中多台手机共享一个公网出口，路由器为内网分配 192.168.x.x 等私网地址。网站日志看到的是公网出口，而不是你手机的内网编号。</p>
<h2>能推断什么、不能推断什么</h2>
<p>地理定位通常是城市级或运营商粒度，不足以单独定罪。风控系统会把 IP 当作信号之一，与账号历史、设备指纹一起评分。</p>
<h2>与隐私工具的关系</h2>
<p>更换出口 IP（如 <a href="/articles/what-is-vpn">VPN</a>）会改变服务器看到的地址，但不抹去登录 Cookie。DNS 查询路径另算，参见 <a href="/articles/what-is-dns-leak">DNS 泄露</a> 与 <a href="/articles/how-dns-servers-work">DNS 原理</a>。</p>
<h2>动态与静态</h2>
<p>家庭宽带多采用动态公网 IP，重启光猫可能变号；企业专线可能固定。理解变化有助于读懂「异地登录提醒」误报。</p>""",
    [
        {"q": "别人拿到我的 IP 能直接黑进电脑吗？", "a": "单独 IP 不足以保证成功入侵；需叠加开放端口、漏洞与弱口令等条件。"},
        {"q": "IPv6 会让每台设备都暴露公网吗？", "a": "取决于路由配置；多数家庭仍以内网前缀做隔离。"},
        {"q": "查 IP 网站显示的城市不准？", "a": "数据库滞后常见；仅作粗略参考。"},
    ],
    [
        {"title": "Cloudflare: What is an IP address?", "url": "https://www.cloudflare.com/learning/network-layer/what-is-an-ip-address/"},
        {"title": "RFC 791", "url": "https://www.rfc-editor.org/rfc/rfc791"},
        {"title": "MDN: IP Address", "url": "https://developer.mozilla.org/en-US/docs/Glossary/IP_Address"},
    ],
    "解释 IPv4/IPv6、公网与私网区别，说明 IP 在风控与隐私讨论中能推断什么，不能推出什么。",
)

ARTICLES["identify-malicious-websites"] = entry(
    """<p>仿冒站越来越像真站：配色、Logo 乃至小锁都不难复制。HTTPS 只保证你与眼前域名之间的传输加密，并不保证域名属于你以为的品牌。</p>
<h2>域名是第一证据</h2>
<p>留意混淆字符：拉丁字母 l 与数字 1、西里尔字母 а 与拉丁 a。不要从邮件直接点「登录」；在书签或官方 App 内进入。</p>
<h2>页面行为信号</h2>
<ul>
<li>刚打开就弹窗要求安装浏览器扩展或根证书。</li>
<li>索取短信验证码、银行卡 CVV 或恢复短语。</li>
<li>倒计时恐吓话术：「30 分钟后账户冻结」。</li>
</ul>
<h2>证书与跳转链</h2>
<p>证书主体应与地址栏一致；遇警告应停止输入。短链与二维码可能绕过你的肉眼核对，付款前回到官方商店搜索 App。</p>
<p>社交工程角度读 <a href="/articles/identify-phishing-attacks">钓鱼识别</a>；传输层读 <a href="/articles/what-is-https">HTTPS 能证明什么</a>。</p>""",
    [
        {"q": "有小锁就一定是官网吗？", "a": "否；任何人都能申请对应自己域名的证书，小锁不等于品牌可信。"},
        {"q": "浏览器提示危险仍要访问？", "a": "不要继续；可能是过期、域名不符或被中间人篡改。"},
        {"q": "PDF 发票里的链接可信吗？", "a": "与邮件链接同风险；核对域名后再输入凭据。"},
    ],
    [
        {"title": "OWASP Phishing Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Phishing_Cheat_Sheet.html"},
        {"title": "Cloudflare: Phishing", "url": "https://www.cloudflare.com/learning/access-management/phishing-attack/"},
        {"title": "CISA Avoiding Social Engineering", "url": "https://www.cisa.gov/news-events/news/avoiding-social-engineering-and-phishing-attacks"},
    ],
    "从域名核对、页面行为与证书警告入手识别仿冒与恶意网站，避免把 HTTPS 小锁误当成官网保证。",
)

ARTICLES["protect-digital-identity"] = entry(
    """<p>数字身份是散落在各处的凭证拼图：邮箱、手机号、证件影像、社保账号与支付绑定。攻击者更关心「能否凑齐重置密码的材料」，而不是一次攻破所有系统。</p>
<h2>公开信息如何被拼接</h2>
<p>招聘简历上的生日、微博定位、旧论坛昵称与泄露库里的密码组合，足够支撑一次有针对性的客服诈骗。</p>
<h2>缩减拼图面积</h2>
<ul>
<li>社交账户隐藏手机号与精确生日；简历用企业总机而非私人号码。</li>
<li>证件照只通过官方渠道上传，并在本地删除临时文件。</li>
<li>为核心邮箱与支付开启强认证，见 <a href="/articles/protect-online-accounts">账户保护</a>。</li>
</ul>
<h2>恢复渠道同样要害</h2>
<p>备用邮箱、SIM 与安全问题答案若过于容易猜到，会成为二步验证的捷径。定期演练「丢手机如何登录密码管理器」。</p>
<p>数据侧阅读 <a href="/articles/prevent-personal-data-leaks">防泄露</a> 与 <a href="/articles/identify-phishing-attacks">反钓鱼</a>。</p>""",
    [
        {"q": "实名认证不可避免怎么办？", "a": "选择最小披露字段；截图留意是否含有效期外的水印条款。"},
        {"q": "Alter ego 网名有用吗？", "a": "能降低跨平台关联概率，但登录邮箱仍会把画像绑回去。"},
        {"q": "发现被冒名注册服务？", "a": "收集证据后联系平台冻结，并修改枢纽邮箱密码。"},
    ],
    [
        {"title": "EFF Surveillance Self-Defense", "url": "https://ssd.eff.org/"},
        {"title": "NIST Identity proofing", "url": "https://pages.nist.gov/800-63-3/sp800-63-3.html"},
        {"title": "OWASP Top Ten", "url": "https://owasp.org/www-project-top-ten/"},
    ],
    "说明数字身份碎片如何被拼接利用，并给出减少证件与联系方式暴露、保护恢复渠道的做法。",
)

ARTICLES["public-wifi-safety"] = entry(
    """<p>公共 Wi-Fi 的争议不在「能不能用」，而在「用来做什么」。同一套热点，查公交时刻与登录网银的风险预算完全不同。</p>
<h2>威胁来自哪里</h2>
<p>同网段旁听者、恶意门户、伪装 SSID 以及你误装的证书，都可能让流量偏离预期路径。HTTPS 能保护页面内容，却挡不住你在假门户上主动输入密码。</p>
<h2>实用分层</h2>
<ol>
<li>系统标记网络为公用，关闭文件共享。</li>
<li>低敏感浏览确认 TLS；中敏感考虑 <a href="/articles/what-is-vpn">VPN</a> 并检查 <a href="/articles/what-is-dns-leak">DNS 是否泄露</a>。</li>
<li>高敏感改走蜂窝，见 <a href="/articles/safe-public-network-use">公共网络使用指南</a>。</li>
</ol>
<h2>别信表象</h2>
<p>咖啡店的精美二维码可能是攻击者贴纸。官方纸质说明上的 SSID 才值得手动输入连接。</p>
<p>传输基础知识：<a href="/articles/what-is-https">HTTPS</a>。</p>""",
    [
        {"q": "机场免费 Wi-Fi 一定被监控吗？", "a": "运营方通常有日志策略；未必恶意，但不应假设完全私密。"},
        {"q": "MAC 随机化能否匿名？", "a": "可减轻跟踪，但登录后账户层标识仍有效。"},
        {"q": "VPN 断线继续上网安全吗？", "a": "若启用了杀开关则阻止；否则可能裸连泄露真实 IP 与 DNS。"},
    ],
    [
        {"title": "CISA Public Wi-Fi", "url": "https://www.cisa.gov/news-events/news/protecting-yourself-using-public-wi-fi"},
        {"title": "Cloudflare: Wi-Fi security", "url": "https://www.cloudflare.com/learning/network-layer/what-is-wifi/"},
        {"title": "EFF: Public Wi-Fi", "url": "https://ssd.eff.org/en/module/why-it-matters"},
    ],
    "分析公共 Wi-Fi 的旁路、门户与假热点风险，并按操作敏感度给出 HTTPS、隧道与蜂窝数据的组合建议。",
)

ARTICLES["what-is-end-to-end-encryption"] = entry(
    """<p>端到端加密（E2EE）指只有对话双方持有解密密钥，服务商在中间只能看到密文或元数据。它与「传输加密」和「静态加密」解决的问题不同。</p>
<h2>与 HTTPS 的分工</h2>
<p>HTTPS 保护你和网站之间的链路；网站服务器在解密后仍能看到内容。E2EE 聊天里，服务器无法阅读消息正文，但仍可能记录谁在何时联系谁。</p>
<h2>密钥如何流转</h2>
<p>常见做法是使用长期身份密钥与临时会话密钥协商。设备更换时需做密钥再分发；备份策略错误可能导致历史消息永久不可读。</p>
<h2>局限清单</h2>
<ul>
<li>端点被植入木马时，加密前的键盘输入已泄露。</li>
<li>云备份若未 E2EE，备份运营方可能读取。</li>
<li>截图、转发与社交工程不受密码学约束。</li>
</ul>
<p>配套阅读 <a href="/articles/why-data-encryption-matters">加密为何重要</a>、<a href="/articles/network-traffic-encryption">流量加密层次</a>、<a href="/articles/choose-privacy-tools">工具选型</a>。</p>""",
    [
        {"q": "所有声称 E2EE 的 App 都可靠吗？", "a": "应查看是否开源、是否有独立审计，以及默认是否真 E2EE。"},
        {"q": "E2EE 能隐藏通话时长吗？", "a": "元数据如时间、号码、IP 仍可能被记录，视实现而定。"},
        {"q": "忘记密钥能找回聊天记录吗？", "a": "设计上不应能；这正是与可恢复云备份的取舍。"},
    ],
    [
        {"title": "EFF: End-to-end encryption", "url": "https://ssd.eff.org/en/module/deep-dive-end-end-encryption"},
        {"title": "RFC 8446 TLS 1.3", "url": "https://www.rfc-editor.org/rfc/rfc8446"},
        {"title": "Cloudflare: E2EE", "url": "https://www.cloudflare.com/learning/privacy/what-is-end-to-end-encryption/"},
    ],
    "厘清端到端加密与 HTTPS、云备份的关系，说明密钥分发、元数据残留与端点安全的边界。",
)

ARTICLES["browser-privacy-settings"] = entry(
    """<p>浏览器是日常最大的数据出口：搜索、表单、摄像头权限、扩展后台行为，全都经过它。默认配置往往偏向便利，需要你有意识地收紧。</p>
<h2>先动这几处</h2>
<ul>
<li>自动更新开启；淘汰不受支持的旧版本。</li>
<li>站点权限里关闭不必要的定位、摄像头与通知。</li>
<li>限制第三方 Cookie 或启用跟踪防护配置。</li>
</ul>
<h2>扩展是把双刃剑</h2>
<p>广告拦截、密码填充很方便，但「读取所有网站数据」的权限相当于半个间谍软件。定期卸载长期不用的扩展。</p>
<h2>配置隔离</h2>
<p>工作、娱乐与匿名搜索可使用不同配置文件；登录银行的环境不要安装实验性脚本。理解追踪原理见 <a href="/articles/how-online-tracking-works">在线追踪</a>，整体策略见 <a href="/articles/protect-online-privacy">网络隐私</a>。</p>
<p>恶意页面识别：<a href="/articles/identify-malicious-websites">恶意网站</a>。</p>""",
    [
        {"q": "总是清除 Cookie 好吗？", "a": "会退出多数登录；更平衡的做法是按站点管理或使用容器标签。"},
        {"q": "内置密码管理器安全吗？", "a": "取决于主密码与同步策略；与独立密码管理器相比要评估备份与跨平台需求。"},
        {"q": "Do Not Track 头还有用吗？", "a": "多数站点忽略；应依赖浏览器内置跟踪防护与权限控制。"},
    ],
    [
        {"title": "MDN: Privacy", "url": "https://developer.mozilla.org/en-US/docs/Web/Privacy"},
        {"title": "EFF: Browser extensions", "url": "https://ssd.eff.org/en/module/how-do-i-install-duckduckgo-privacy-essentials"},
        {"title": "OWASP Secure Headers", "url": "https://owasp.org/www-project-secure-headers/"},
    ],
    "汇总浏览器更新、站点权限、第三方 Cookie 与扩展权限等隐私设置，并建议按场景分离配置。",
)

ARTICLES["choose-privacy-tools"] = entry(
    """<p>隐私工具市场喧嚣，卖点往往比证据响亮。选型应先写清单：防追踪、防公共网络旁听，还是防账户撞库？不同目标对应不同品类。</p>
<h2>评估框架</h2>
<ol>
<li><strong>透明度：</strong>公司主体、隐私政策是否与功能匹配。</li>
<li><strong>可验证性：</strong>开源、可复现构建或第三方审计报告。</li>
<li><strong>权限：</strong>是否索要不相关的高危权限。</li>
<li><strong>可退出：</strong>能否导出数据并删除账户。</li>
</ol>
<h2>品类速览</h2>
<p>密码管理器、DNS/隧道、浏览器强化与加密通讯各管一段。叠加三层同类工具不会线性变安全，反而增加故障面。对比 <a href="/articles/vpn-vs-proxy">VPN 与代理</a>、<a href="/articles/what-is-vpn">VPN</a> 与 <a href="/articles/what-is-end-to-end-encryption">E2EE</a>  antes de comprar.</p>
<h2>红旗话术</h2>
<p>「军方级」「警察无法破解」「一键匿名」多是营销。看到要求关闭系统安全功能的安装指引，应直接放弃。</p>
<p>落地配合 <a href="/articles/protect-online-privacy">隐私总览</a>。</p>""",
    [
        {"q": "免费 VPN 能长期用吗？", "a": "需审视商业模式；若靠出售流量数据盈利，与隐私目标冲突。"},
        {"q": "开源等于安全吗？", "a": "提高审查可能，但仍需正确配置与持续维护。"},
        {"q": "需要装十个隐私扩展吗？", "a": "通常不需要；过多扩展增大指纹面与崩溃概率。"},
    ],
    [
        {"title": "EFF Tech Tools", "url": "https://ssd.eff.org/en/module/tools"},
        {"title": "OWASP Consumer Top 10", "url": "https://owasp.org/www-project-consumer-top-10/"},
        {"title": "Cloudflare Privacy Center", "url": "https://www.cloudflare.com/privacypolicy/"},
    ],
    "给出隐私工具选型的透明度、审计、权限与退出标准，并按品类说明 VPN、浏览器与通讯工具的边界。",
)

# Fix accidental Spanish in choose-privacy-tools
ARTICLES["choose-privacy-tools"]["content_html"] = ARTICLES["choose-privacy-tools"]["content_html"].replace(
    " antes de comprar.", "再下单不迟。"
)

ARTICLES["common-cybersecurity-myths"] = entry(
    """<p>安全误区之所以顽固，是因为它们半真半假：听起来省劲，却在你最不在意的环节留白。拆 myth 的目的，是换成可验证的习惯。</p>
<h2>典型半真话术</h2>
<ul>
<li>「我没价值数据」——邮箱与手机就是恢复其余一切的钥匙。</li>
<li>「杀毒够用了」——不能替代码补洞，也不能阻止你亲自输入验证码给骗子。</li>
<li>「HTTPS 站绝对可信」——只加密传输，不审商家诚信。</li>
<li>「隐身模式无人追踪」——本地历史清了，远端画像还在。</li>
</ul>
<h2>替换为可核对动作</h2>
<p>独立口令、双重验证、延迟点击链接、核对域名、保持更新。把口号改写成每周能检查的一两条，例如「枢纽邮箱有没有陌生转发规则」。</p>
<p>技术补课：<a href="/articles/what-is-https">HTTPS</a>、<a href="/articles/create-strong-passwords">强密码</a>、<a href="/articles/how-online-tracking-works">追踪机制</a>、<a href="/articles/protect-online-privacy">隐私配置</a>。</p>""",
    [
        {"q": "Mac 不需要杀毒是真的吗？", "a": "恶意软件仍存在；系统内置防护有帮助，但不能替代谨慎安装与更新。"},
        {"q": "复杂图形密码一定更安全？", "a": "可视窥探与录屏风险上升；长 passphrase 通常更均衡。"},
        {"q": "收到官方短信就一定真？", "a": "仿冒基站的文本可伪造；敏感操作回拨官方号码核实。"},
    ],
    [
        {"title": "CISA Misinformation", "url": "https://www.cisa.gov/topics/cybersecurity-best-practices"},
        {"title": "OWASP Top Ten", "url": "https://owasp.org/www-project-top-ten/"},
        {"title": "Cloudflare Learning", "url": "https://www.cloudflare.com/learning/security/"},
    ],
    "澄清「无重要数据、杀毒即可、HTTPS 等于可信」等常见网络安全误解，并换成可逐项核对的安全习惯。",
)

ARTICLES["network-traffic-encryption"] = entry(
    """<p>「流量已加密」这句话在现实中会出现在 TLS 会话、VPN 隧道、磁盘加密等多种语境。它们都用到密码学，但保护的路径与可见元数据并不相同。</p>
<h2>应用层：HTTPS/TLS</h2>
<p>浏览器与 Web 服务器协商密钥，保护 HTTP 内容与大部分头。证书验证通过时，可降低中间人篡改页面。细节见 <a href="/articles/what-is-https">HTTPS 入门</a>。</p>
<h2>网络层：VPN 隧道</h2>
<p>把 IP 包封装进另一条链路，统一从远端出口访问互联网。改变的是路径与观察者，不是魔法匿名。参见 <a href="/articles/what-is-vpn">VPN</a> 与 <a href="/articles/vpn-vs-proxy">对比代理</a>。</p>
<h2>元数据仍会泄漏</h2>
<p>包长时序、DNS 查询、SNI（视部署而定）可能暴露访问意图。加密载荷不等于不可分析。DNS 专题：<a href="/articles/what-is-dns-leak">泄露检测</a>。</p>
<h2>端点先于管道</h2>
<p>键盘记录与恶意扩展在加密前窃取。管道再强，端点失守仍等于明文。</p>""",
    [
        {"q": "双层 VPN 更安全吗？", "a": "未必；延迟上升且配置复杂，错误几率也随之增加。"},
        {"q": "企业 SSL 检查为何能看 HTTPS？", "a": "终端信任了公司根证书，由代理代解密再重签；属于有意的中间人。"},
        {"q": "QUIC 会取代 TLS 吗？", "a": "QUIC 内置加密传输；与 HTTP/3 组合，但网站身份仍依赖证书体系。"},
    ],
    [
        {"title": "Cloudflare: TLS", "url": "https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/"},
        {"title": "RFC 8446", "url": "https://www.rfc-editor.org/rfc/rfc8446"},
        {"title": "NIST TLS guidelines", "url": "https://csrc.nist.gov/projects/cryptographic-module-validation-program"},
    ],
    "对比 HTTPS 与 VPN 等层次上的流量加密，说明元数据泄漏与端点安全仍须单独处理。",
)

ARTICLES["protect-online-privacy"] = entry(
    """<p>网络隐私的目标，是减少不必要的长期标识，并缩短一次失误的连锁反应。它不是装一个图标就变隐身，而是账号、设备、浏览器与网络多条线同时收紧。</p>
<h2>按威胁分配精力</h2>
<p>若最怕广告跨站跟踪，优先浏览器与账号隔离；若最怕咖啡馆旁听，优先传输与 DNS 路径；若最怕撞库，优先唯一口令与 2FA。</p>
<h2>可重复的底线</h2>
<ul>
<li>枢纽邮箱与密码管理器启用强认证。</li>
<li>限制应用权限与云同步范围。</li>
<li>公共网络高敏感改蜂窝；必要时隧道并确认加密 DNS。</li>
<li>定期清理 OAuth 与网盘公开链接。</li>
</ul>
<h2>别忽视登录态</h2>
<p>同一个 Google 账户贯穿搜索、YouTube 与安卓推送，清除 Cookie 也赶不走账户级画像。分账户或分配置比反复清缓存更省力。</p>
<p>深入：<a href="/articles/how-online-tracking-works">追踪原理</a>、<a href="/articles/browser-privacy-settings">浏览器设置</a>、<a href="/articles/choose-privacy-tools">工具选型</a>、<a href="/articles/prevent-personal-data-leaks">防泄露</a>。</p>""",
    [
        {"q": "换隐私浏览器就够吗？", "a": "有帮助但不够；登录习惯、网络路径与手机号复用同样塑造画像。"},
        {"q": "GDPR 弹窗点拒绝就够吗？", "a": "取决于实际执行；技术侧仍应限制第三方存储与追踪脚本。"},
        {"q": "隐私保护会影响便利吗？", "a": "会有少量摩擦；宜对高价值账户投入，而非追求理论极限。"},
    ],
    [
        {"title": "EFF Surveillance Self-Defense", "url": "https://ssd.eff.org/"},
        {"title": "MDN Privacy", "url": "https://developer.mozilla.org/en-US/docs/Web/Privacy"},
        {"title": "Cloudflare Privacy", "url": "https://www.cloudflare.com/learning/privacy/what-is-data-privacy/"},
    ],
    "从威胁优先级出发，汇总账号、设备、浏览器与网络层面的个人网络隐私保护底线与常见盲区。",
)

ARTICLES["what-is-dns-leak"] = entry(
    """<p>DNS 泄露描述的是一种错位：你以为域名查询随 VPN 走了隧道，系统却把请求发到本地运营商解析器，暴露访问意图。</p>
<h2>为何在隧道场景常见</h2>
<p>操作系统、浏览器 DoH 与分流规则可能各自决策。隧道只劫持 IP 路由，未覆盖的 DNS 仍从原接口出去，就会出现「出口 IP 在国外、查询还在国内」的组合。</p>
<h2>加密 DNS 的角色</h2>
<p>DoH/DoT 保护查询传输，不自动解决「选哪个解析器」。你仍需确认客户端设置与 VPN 的「阻断局域网 DNS」类选项。</p>
<h2>自查思路</h2>
<ol>
<li>连接隧道前后对比解析器 IP 与泄漏检测页结果。</li>
<li>更新客户端或系统后复测；分流域名列表变更也会影响。</li>
<li>理解预期分流与意外泄漏的差别。</li>
</ol>
<p>基础：<a href="/articles/how-dns-servers-work">DNS 如何工作</a>；网络：<a href="/articles/what-is-vpn">VPN</a>、<a href="/articles/public-wifi-safety">公共 Wi-Fi</a>、<a href="/articles/what-is-https">HTTPS</a>。</p>""",
    [
        {"q": "DNS 泄露会暴露密码吗？", "a": "不直接暴露；主要泄露访问了哪些域名，仍可能推断行为。"},
        {"q": "关闭系统 DoH 能修复吗？", "a": "有时能减少冲突；关键是让解析路径与隧道策略一致。"},
        {"q": "Split tunnel 一定泄漏吗？", "a": "分流域名走本地可能是设计行为；非预期走本地才是问题。"},
    ],
    [
        {"title": "Cloudflare DNS", "url": "https://www.cloudflare.com/learning/dns/dns-over-https/"},
        {"title": "RFC 8484 DoH", "url": "https://www.rfc-editor.org/rfc/rfc8484"},
        {"title": "MDN DNS", "url": "https://developer.mozilla.org/en-US/docs/Glossary/DNS"},
    ],
    "解释 VPN 场景下 DNS 查询偏离隧道的原因、加密 DNS 的边界，以及连接前后对比的自查方法。",
)

ARTICLES["vpn-vs-proxy"] = entry(
    """<p>代理与 VPN 都能改变流量走向，但工作层级与默认保护范围不同。选型时先问：要让哪些应用、哪些协议走进隧道？</p>
<h2>代理：应用或协议级</h2>
<p>HTTP/SOCKS 代理常只影响配置了代理的浏览器或客户端。游戏、系统更新与其他 App 仍可能直连。明文 HTTP 代理并不提供机密性。</p>
<h2>VPN：系统或虚拟网卡级</h2>
<p>通过 TUN 设备把更多 IP 流量导入隧道，覆盖范围更广。信任边界随之扩大——运营方理论可见进入隧道的连接元数据。</p>
<h2>DNS 与分流差异</h2>
<p>代理下 DNS 可能在本地完成；VPN 常指定隧道内解析器。配置失当会出现 <a href="/articles/what-is-dns-leak">DNS 泄露</a>。</p>
<h2>怎么选</h2>
<ul>
<li>仅浏览器临时访问：应用级代理可能够用，接受其余应用裸露。</li>
<li>公共 Wi-Fi 多应用保护：系统 VPN 更贴切，并叠加 HTTPS。</li>
</ul>
<p>延伸阅读 <a href="/articles/what-is-vpn">VPN 原理</a>、<a href="/articles/network-traffic-encryption">加密层次</a>、<a href="/articles/choose-privacy-tools">工具评估</a>。</p>""",
    [
        {"q": "浏览器 VPN 扩展等于系统 VPN 吗？", "a": "多数仅代理浏览器流量，其它程序不受保护。"},
        {"q": "SOCKS5 有加密吗？", "a": "协议本身不保证；需外层 TLS 或配合 VPN 使用。"},
        {"q": "两者能同时开吗？", "a": "可能互相干扰路由；除非文档明确，否则避免叠罗汉式配置。"},
    ],
    [
        {"title": "Cloudflare: Proxy vs VPN", "url": "https://www.cloudflare.com/learning/access-management/vpn-security/"},
        {"title": "MDN: Proxy servers", "url": "https://developer.mozilla.org/en-US/docs/Glossary/Proxy_server"},
        {"title": "NIST SP 800-113", "url": "https://csrc.nist.gov/publications/detail/sp/800-113/final"},
    ],
    "比较代理与 VPN 的覆盖范围、加密假设、DNS 行为与信任边界，帮助按场景选型。",
)

ARTICLES["identify-phishing-attacks"] = entry(
    """<p>钓鱼利用的是你的反应速度，而不是纯技术漏洞。一封带紧迫语气的邮件、一条伪基站短信，目的都是让你在核实前交出凭据或验证码。</p>
<h2>渠道与话术</h2>
<p>邮件附件宏、伪造发票 PDF、伪装客服的 IM 与「领导催款」社交工程都属于广谱钓鱼。商务邮件妥协（BEC）则会冒充真实域名相近的地址。</p>
<h2>识别锚点</h2>
<ul>
<li>发件人域名与 Reply-To 是否一致。</li>
<li>链接悬停显示的 URL 是否与文字相符。</li>
<li>是否索取 OTP、恢复码或远程桌面。</li>
</ul>
<h2>响应流程</h2>
<p>不在邮件内点登录；改用官方 App。若已输入密码，立即改密并下线会话。付款指令变更务必用第二条渠道确认。</p>
<p>网站层面：<a href="/articles/identify-malicious-websites">恶意网站</a>；账户：<a href="/articles/protect-online-accounts">在线账户</a>、<a href="/articles/two-factor-authentication-guide">2FA</a>。</p>""",
    [
        {"q": "钓鱼邮件进了垃圾箱就安全吗？", "a": "仍可能误点；训练自己不在垃圾箱里登录任何服务。"},
        {"q": "2FA 能防钓鱼吗？", "a": "FIDO2/通行密钥可显著降低；短信验证码仍可能被实时转发。"},
        {"q": "报告钓鱼有什么意义？", "a": "帮助平台拉黑基础设施，也训练自己复盘特征。"},
    ],
    [
        {"title": "CISA Phishing guidance", "url": "https://www.cisa.gov/topics/cybersecurity-best-practices"},
        {"title": "OWASP Phishing Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Phishing_Cheat_Sheet.html"},
        {"title": "Cloudflare Email security", "url": "https://www.cloudflare.com/learning/email-security/what-is-phishing/"},
    ],
    "介绍邮件、短信与 IM 钓鱼话术及商务邮件假冒特征，并给出不通过邮件登录与付款核验的响应步骤。",
)

ARTICLES["create-strong-passwords"] = entry(
    """<p>强密码在现代威胁模型里意味着「足够长、每站唯一、可被安全存储」。复杂但复用的八位口令，在泄露库面前几乎没有防御力。</p>
<h2>长度优先于花样</h2>
<p>NIST 现行指南强调长度与用户友好，而非强制定期无故轮换。16 位以上的随机串或 4–5 个随机词组合，通常优于短小但是却含特殊符号的密码。</p>
<h2>密码管理器的职责</h2>
<p>生成、填充与加密保管条目；你只需记住一个高强度主密码并开启其 2FA。切勿截图或明文邮件传输库文件。</p>
<h2>泄露后的动作</h2>
<p>监测到某站泄露时，仅改那一站不够——检查是否别处复用相同口令。枢纽邮箱泄露则触发全面轮换。</p>
<p>下一步：<a href="/articles/two-factor-authentication-guide">双重验证</a>、<a href="/articles/protect-online-accounts">账户保护</a>、<a href="/articles/identify-phishing-attacks">警惕钓鱼索要主密码</a>。</p>""",
    [
        {"q": "把密码写在笔记本可以吗？", "a": "物理安全可控时可行，但忌与电脑同放；更推荐密码管理器。"},
        {"q": "定期三月改密必要吗？", "a": "无泄露迹象时强制轮换反而诱发弱口令；重点应放在唯一性与长度。"},
        {"q": "生物识别取代密码吗？", "a": "多用作解锁本地保管库；远端账户仍要独立口令。"},
    ],
    [
        {"title": "NIST SP 800-63B", "url": "https://pages.nist.gov/800-63-3/sp800-63b.html"},
        {"title": "OWASP Password Storage", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"},
        {"title": "CISA Password guidance", "url": "https://www.cisa.gov/secure-our-world/use-strong-passwords"},
    ],
    "强调长度与唯一性优于花样复杂度，说明密码管理器用法与泄露后轮换顺序。",
)

ARTICLES["two-factor-authentication-guide"] = entry(
    """<p>双重验证（2FA）在口令泄露后提供第二道门。不同因子安全性差异巨大：硬件密钥与 FIDO2 通常强于短信，短信又强于完全没有 2FA。</p>
<h2>常见因子比较</h2>
<ul>
<li><strong>安全密钥/通行密钥：</strong>抗钓鱼能力强，绑定站点域名。</li>
<li><strong>TOTP 应用：</strong>离线生成 6 位码，优于短信。</li>
<li><strong>短信：</strong>受 SIM 交换威胁，但仍阻挡批量撞库。</li>
</ul>
<h2>恢复与备份</h2>
<p>启用 2FA 的同时保存恢复码，存放于离线与加密介质。丢失手机前预先登记备用因子，避免把自己锁在门外。</p>
<h2>实施顺序</h2>
<p>邮箱、密码管理器、云盘、支付优先。然后扩展到社交与购物。配合 <a href="/articles/protect-online-accounts">账户清单</a> 与 <a href="/articles/create-strong-passwords">口令策略</a>。</p>
<p>识别伪装的 2FA 钓鱼：<a href="/articles/identify-phishing-attacks">钓鱼指南</a>。</p>""",
    [
        {"q": "可以不启用短信 2FA 吗？", "a": "若无法用应用或密钥，短信仍好过单因子；有条件应升级。"},
        {"q": "恢复码丢了怎么办？", "a": "尽早使用剩余因子登录并重新生成；否则走官方身份申诉流程。"},
        {"q": "多台设备如何同步 TOTP？", "a": "可云端加密备份或每台扫描同一密钥；注意备份安全。"},
    ],
    [
        {"title": "NIST MFA", "url": "https://pages.nist.gov/800-63-3/sp800-63b.html"},
        {"title": "CISA MFA", "url": "https://www.cisa.gov/resources-tools/resources/multi-factor-authentication-mfa"},
        {"title": "FIDO Alliance", "url": "https://fidoalliance.org/fido2/"},
    ],
    "比较安全密钥、验证器应用与短信等 2FA 方式的抗钓鱼能力，并说明恢复码备份与启用顺序。",
)

ARTICLES["what-is-https"] = entry(
    """<p>HTTPS 是在 HTTP 之上叠加 TLS 的结果。浏览器与服务器先握手协商密钥，再加密传输网页与 API 数据，防路过设备窃听与篡改。</p>
<h2>证书做了什么</h2>
<p>服务器出示证书链，浏览器验证是否由受信机构签发且域名匹配。验证失败会出现警告——此时输入的任何内容都可能流向攻击者。</p>
<h2>保护范围</h2>
<ul>
<li>保护路径上的机密性与完整性（在证书有效前提下）。</li>
<li>不证明网站经营合法或页面无木马。</li>
<li>不隐藏 DNS 查询与服务器访问日志。</li>
</ul>
<h2>与相邻概念</h2>
<p>全站 HTTPS 是底线；公共 Wi-Fi 上仍需警惕假门户。对比 <a href="/articles/network-traffic-encryption">流量加密</a>、<a href="/articles/identify-malicious-websites">恶意站点</a>、<a href="/articles/what-is-dns-leak">DNS 侧泄漏</a>。</p>""",
    [
        {"q": "自签名证书能用吗？", "a": "内网测试可以；公网站点应使用受信 CA，否则用户会看到警告。"},
        {"q": "HTTPS 较慢吗？", "a": "现代硬件与 HTTP/2/3 下延迟影响很小；安全性收益远大于成本。"},
        {"q": "混合内容警告什么意思？", "a": "HTTPS 页面加载了 HTTP 子资源，可能被阻断或降级保护。"},
    ],
    [
        {"title": "MDN: HTTPS", "url": "https://developer.mozilla.org/en-US/docs/Glossary/HTTPS"},
        {"title": "Cloudflare: What is HTTPS?", "url": "https://www.cloudflare.com/learning/ssl/what-is-https/"},
        {"title": "RFC 8446 TLS 1.3", "url": "https://www.rfc-editor.org/rfc/rfc8446"},
    ],
    "解释 HTTPS/TLS 握手、证书验证与其保护边界，并说明它无法替代防钓鱼与 DNS 隐私。",
)

ARTICLES["prevent-personal-data-leaks"] = entry(
    """<p>个人数据泄露既可能来自网络攻击，也可能来自一次误设公开链接或把手机落在出租车后座。防守重点是减少复制点，并准备可执行的止损剧本。</p>
<h2>数据最小化</h2>
<p>表单能填假名就不填真名；应用索要与功能无关的通讯录时拒绝。网盘分享设密码与过期，而不是「知道链接就能下」。</p>
<h2>泄露信号</h2>
<ul>
<li>陌生设备登录提醒、验证码轰炸、信用报告异常查询。</li>
<li>旧密码在新站点突然无法使用——可能是撞库。</li>
</ul>
<h2>止损顺序</h2>
<ol>
<li>改枢纽邮箱与金融密码，下线所有会话。</li>
<li>检查邮箱转发、恢复手机与 OAuth。</li>
<li>冻结信用卡；向平台提交冒用申诉。</li>
</ol>
<p>身份层：<a href="/articles/protect-digital-identity">数字身份</a>；习惯层：<a href="/articles/protect-online-privacy">网络隐私</a>、<a href="/articles/identify-phishing-attacks">钓鱼</a>。</p>""",
    [
        {"q": "泄露后必须报警吗？", "a": "视金额与证件盗用情况而定；金融诈骗建议保留证据报案。"},
        {"q": "暗网查询服务可信吗？", "a": "只作参考；更应依赖官方泄露通知与账户异常提示。"},
        {"q": "删除 App 就等于删数据吗？", "a": "不一定；需走账号注销流程并确认远端擦除政策。"},
    ],
    [
        {"title": "CISA Data protection", "url": "https://www.cisa.gov/topics/cybersecurity-best-practices"},
        {"title": "OWASP Privacy", "url": "https://owasp.org/www-project-top-ten/"},
        {"title": "EFF Protecting yourself", "url": "https://ssd.eff.org/"},
    ],
    "从数据最小化、泄露征兆识别到改密与会话清理的止损顺序，帮助降低个人数据暴露后的连锁损失。",
)

META_LONG = {
    "protect-mobile-data": "从权限、锁屏、安装来源、云备份与换机擦除等角度说明如何保护手机里的个人数据、支付会话与二次验证渠道，降低丢失与恶意应用风险。",
    "choose-secure-network-connection": "按家庭、外出与办公场景比较蜂窝数据、家用 Wi-Fi、公共热点与公司隧道的信任差异，帮你在办理敏感事务时选出更稳妥的网络路径。",
    "windows-network-security-settings": "梳理 Windows 公用网络配置文件、Defender 防火墙、远程桌面与系统更新等关键设置，减少笔记本在陌生局域网中被扫描与滥用共享服务的概率。",
    "protect-online-accounts": "围绕邮箱与密码管理器等枢纽账户，说明独立口令、双重验证、OAuth 授权与邮件转发规则的核查方法，降低账户被接管后的连锁损失。",
    "safe-public-network-use": "从连接前核对热点、使用中按敏感度分级操作到离开后的证书与会话检查，给出在机场商场等环境使用公共网络的务实安全习惯。",
    "how-online-tracking-works": "介绍 Cookie、像素信标、设备指纹与登录态如何被拼接成跨站画像，并说明浏览器配置与账号隔离在削弱商业追踪方面的作用边界。",
    "how-dns-servers-work": "用递归查询与缓存 TTL 等概念解释 DNS 如何把域名映射到 IP，说明加密 DNS 能保护什么、解析运营商仍能看到什么。",
    "check-network-security": "提供路由器口令、固件、连接设备清单、访客网段与 DNS 设置的家庭网络安全自查步骤，以及发现陌生终端后的隔离与复盘做法。",
    "why-data-encryption-matters": "区分传输加密、磁盘静态加密与端到端加密各自应对的威胁，强调密钥与恢复材料管理不当会让加密形同虚设。",
    "zero-trust-security": "用个人读者能理解的语言解释零信任的核心假设，以及分段访问、链接过期与设备核对在家用和小团队环境中的落地方式。",
    "what-is-ip-address": "解释 IPv4 与 IPv6、公网私网地址与动态租约，说明 IP 在网站日志与风控中的作用，以及它与账号指纹和 DNS 查询之间的区别。",
    "identify-malicious-websites": "从域名拼写、证书主体、页面恐吓话术与诱导安装等信号识别仿冒与恶意网站，提醒 HTTPS 小锁并不代表品牌可信。",
    "protect-digital-identity": "说明邮箱、手机号与证件影像如何被拼成社工材料，给出减少公开暴露、保护恢复渠道与处理冒名注册的可行做法。",
    "public-wifi-safety": "分析公共 Wi-Fi 上的旁路、恶意门户与假热点风险，并按操作敏感度组合 HTTPS、系统级隧道与蜂窝数据，避免在热点上办理高敏业务。",
    "what-is-end-to-end-encryption": "厘清端到端加密与 HTTPS、云备份的差异，说明密钥分发、元数据残留与端点被控时密码学防线仍会失守的边界。",
    "browser-privacy-settings": "汇总浏览器自动更新、站点权限、第三方 Cookie、跟踪防护与扩展权限等设置要点，并建议按工作与娱乐场景分离配置降低关联。",
    "choose-privacy-tools": "给出评估 VPN、密码管理器、浏览器强化与加密通讯等隐私工具的透明度、审计、权限与可退出标准，避开夸张营销话术。",
    "common-cybersecurity-myths": "逐条澄清没有重要数据、杀毒足够、HTTPS 等于可信等常见误区，并换成可逐项核对的习惯清单，避免被半真半假口号麻痹。",
    "network-traffic-encryption": "对比 TLS 应用会话与 VPN 网络隧道在保护范围、元数据泄漏与端点安全上的差异，帮助读者正确理解已加密仍可能被观察的信息。",
    "protect-online-privacy": "从威胁优先级出发，串联账号、设备、浏览器与网络各层的隐私底线配置，说明登录态如何延长跨站追踪以及减少暴露的做法。",
    "what-is-dns-leak": "解释 VPN 场景下 DNS 查询仍走本地解析器的原因，说明 DoH/DoT 的传输保护与解析策略一致性检查，区分预期分流与意外泄漏。",
    "vpn-vs-proxy": "比较 HTTP/SOCKS 代理与系统 VPN 在覆盖应用、默认加密、DNS 行为与信任边界上的差别，帮助按公共网络或多应用场景选型。",
    "identify-phishing-attacks": "介绍邮件、短信与即时通讯中的钓鱼与商务邮件假冒话术，强调不在消息内点击登录，并给出付款指令二次确认的应对流程。",
    "create-strong-passwords": "依据现代口令指南强调长度与站点唯一性，说明密码管理器如何生成与保管条目，以及泄露后应有针对性的轮换顺序。",
    "two-factor-authentication-guide": "比较 FIDO2 安全密钥、TOTP 应用与短信验证码的抗钓鱼能力，说明恢复码备份与枢纽账户优先启用双重验证的顺序。",
    "what-is-https": "解释 HTTPS 中 TLS 握手、证书链验证与其对传输机密性与完整性的保护，并说明它不能证明网站诚信、也不能隐藏 DNS 查询记录。",
    "prevent-personal-data-leaks": "从表单最小化、网盘外链治理到异常登录信号的识别，列出个人数据泄露后的改密、下线会话与冻结支付等止损步骤。",
}

EXPANSIONS = {
    "protect-mobile-data": """
<h2>备份与同步取舍</h2>
<p>相册、通讯录与聊天记录的自动同步，让换新机更轻松，也意味着云端多一份副本。可以为不同内容选择不同策略：工作文档可企业盘加密，私人照片关自动上传或仅 Wi-Fi 备份。</p>
<h2>移动支付与生物识别</h2>
<p>小额免密是便利与风险的取舍。为支付应用单独设置二次确认；在公共场合关闭支付结果通知预览，避免旁人一眼看到金额与商家。</p>
<h2>旅行与漫游</h2>
<p>境外漫游时警惕伪造运营商短信与 Wi-Fi 门户；宁可临时买本地 eSIM 数据，也不在陌生网络里重置银行口令。更多隧道与 DNS 话题见 <a href="/articles/what-is-vpn">VPN</a>。</p>""",
    "choose-secure-network-connection": """
<h2>公司设备的例外</h2>
<p>公司发放的笔记本可能预装证书与始终在线隧道。个人娱乐流量与公司机密混在同一设备上时，应遵守分区策略，不在受管设备登录私人网银除非政策允许。</p>
<h2>测速不等于测安全</h2>
<p>带宽测试只反映吞吐量；不能告诉你 DNS 是否遭劫持、门户是否写入根证书。判断安全看的是协议、证书与出口策略，而不是 Mbps 数字。</p>
<h2>家人设备互访</h2>
<p>家长控制与孩子手表常要求与主网互通。可为儿童设备单独 SSID，并在路由器上限制其只能访问教育类域名列表，降低被钓鱼页利用的概率。</p>""",
    "windows-network-security-settings": """
<h2>企业域与家用混用</h2>
<p>加入 Azure AD 或公司域后，部分策略由管理员下发，本地防火墙界面可能变灰。此时家用侧仍应关掉不必要共享，避免域策略未覆盖的家庭访客网段裸奔。</p>
<h2>Wi-Fi 硬件按钮</h2>
<p>旧笔记本的物理 Wi-Fi 开关与飞行模式快捷键，会在你未注意时断开隧道却继续显示已连热点。固件更新后复查无线驱动，修复已知断连漏洞。</p>
<h2>日志与排错</h2>
<p>遇到「已连接但无法上网」，先在命令行查看路由表与 DNS，确认没有残留恶意代理。配合 <a href="/articles/what-is-dns-leak">DNS 泄露</a> 与 <a href="/articles/check-network-security">家庭自检</a> 交叉验证。</p>""",
    "protect-online-accounts": """
<h2>密码重置链</h2>
<p>许多网站把找回密码发到邮箱短信。攻击者若只攻破二级论坛，却复用了邮箱密码，就能一路点「忘记密码」重置银行入口。论坛也用唯一口令，是花费极低却极关键的习惯。</p>
<h2>安全邮箱隔离</h2>
<p>可为高价值账户注册专用邮箱，不用于订阅与抽奖；减少暴露在泄露库中的概率。该邮箱仅用于登录与恢复，不对外通信。</p>
<h2>被接管后的取证</h2>
<p>保存钓鱼邮件原件、异常登录 IP 与时间，向平台申诉时有助于加速解冻。阅读 <a href="/articles/prevent-personal-data-leaks">泄露止损</a> 准备并行动作。</p>""",
    "safe-public-network-use": """
<h2>会展与展演现场</h2>
<p>大型活动常提供免费 Wi-Fi 收集观众画像。展台扫码登录可能把 OpenID 授权绑给陌生应用；尽量用一次性邮箱或拒绝非必要授权。</p>
<h2>充电宝与 USB 口</h2>
<p>公共 USB 充电口可能启用数据针脚安装配置文件。自带插头或 USB 数据阻断器，避免「充电变同步」。</p>
<h2>长期常客店</h2>
<p>常去咖啡店的合法热点也可能被邻近攻击者设置同名假热点。首次连接核对口令提示方式，并把正确 SSID 存为手动配置而非永远自动加入。</p>""",
    "how-online-tracking-works": """
<h2>围墙花园与超级 App</h2>
<p>在微信、抖音等生态内浏览时，账号 ID 是第一方标识，广告联盟看到的「匿名」往往只是站外补充。站外限制 Cookie 对站内个性化影响有限。</p>
<h2>邮件里的像素</h2>
<p>营销邮件嵌入 1×1 图片，打开即上报时间与 IP。客户端远程加载图片前询问，或改用纯文本模式阅读敏感通讯。</p>
<h2>合规横幅不是技术盾</h2>
<p>GDPR 同意框主要管合法基础；技术层面仍要在浏览器开启跟踪防护、减少跨站登录。参阅 <a href="/articles/choose-privacy-tools">工具选型</a> 挑适合你的组合。</p>""",
    "how-dns-servers-work": """
<h2>缓存与污染</h2>
<p>递归解析器会缓存答案。若攻击者在 TTL 内投毒，短暂地把银行域名指到假 IP，用户即使输入正确网址也会中招。加密 DNS 与 HTTPS 证书校验是双保险。</p>
<h2>反向 DNS</h2>
<p>邮件服务器常用 PTR 记录证明身份；个人家庭用户很少接触。理解即可知「IP 到名字」是另一条查询方向，与隐私无直接关系。</p>
<h2>权威变更传播</h2>
<p>网站迁移机房后修改 NS 与 A 记录，全球完全生效可能要数十分钟到数小时。其间部分用户仍访问旧地址，运维窗口要有回滚预案。</p>""",
    "check-network-security": """
<h2>光猫与路由双层管理</h2>
<p>国内常见光猫拨号 + 路由器 NAT。只改路由密码而光猫仍默认，攻击者可从 WAN 侧尝试管理口。两层口令都要换，并关闭远程维护除非运营商要求。</p>
<h2>UPnP 与端口映射</h2>
<p>游戏与下载软件常自动打洞映射端口，可能意外暴露内网服务。无需求时在路由关闭 UPnP，改用手动映射并记录用途。</p>
<h2>下一代协议</h2>
<p>启用 IPv6 时核对接口边界防火墙，避免内网设备意外获全球地址却无过滤。可与 <a href="/articles/what-is-ip-address">IP 地址</a> 专题一起阅读。</p>""",
    "why-data-encryption-matters": """
<h2>备份三份法则</h2>
<p>一份本地加密、一份离线介质、一份云副本，是不同的恢复路径。只加密不同步，丢硬盘同样痛苦；只同步不加密，云政策变更即成风险。</p>
<h2>聊天记录导出</h2>
<p>导出到明文 CSV 会破坏此前 E2EE 的保护边界。导出文件应单独加密存放，并在分享前删除临时副本。</p>
<h2>法律与企业合规</h2>
<p>公司有权解密办公邮箱，雇员不应把个人健康等敏感话题放在企业未 E2EE 的工具里。个人用户则自己掌控密钥材料。</p>""",
    "zero-trust-security": """
<h2>微分段不是买了就完</h2>
<p>企业部署零信任需要资产清单、身份源与持续评估。个人侧对应的是：不同网盘账号分工作与生活，别用同一密码串起。</p>
<h2>条件访问</h2>
<p>云盘可设定「新设备登录须通过已信任手机批准」。这模仿了「每次请求都带上下文」的企业策略，误报时要有备用恢复路径。</p>
<h2>供应商边界</h2>
<p>外包客服能否看到你的全套资料，取决于企业授权模型。作为用户，尽量用子账户与只读权限招待合伙人，而非共享主口令。</p>""",
    "what-is-ip-address": """
<h2>NAT 与端口映射</h2>
<p>路由器用 NAT 让多设备共享公网 IP。对外服务需端口转发；错误配置会让内网摄像头暴露到全网扫描器。</p>
<h2>CGNAT 双层</h2>
<p>运营商级 NAT 下，你家出口与真公网还差一层，自托管网站更困难，也让你与其他用户共享同一外部地址，风控误封概率上升。</p>
<h2>地理数据库误差</h2>
<p>流媒体地域限制依赖 GeoIP 库，与物理位置可能偏差。VPN 改变可见出口，但服务条款仍可能禁止规避地域。</p>""",
    "identify-malicious-websites": """
<h2>供应链篡改</h2>
<p>合法站点被挂马时，小锁仍在。关注浏览器扩展提示、突然弹出的更新框架，以及是否与平时页面布局不符。</p>
<h2>搜索引擎广告位</h2>
<p>品牌词的搜索广告常链向仿冒域名，比自然结果更靠上。点进前先看 URL，而非只看标题里的品牌字样。</p>
<h2>WebView 套壳</h2>
<p>诈骗 App 内嵌浏览器加载假银行页，地址栏可能不可见。高敏操作坚持官方独立 App 或书签入口，见 <a href="/articles/protect-mobile-data">移动端防护</a>。</p>""",
    "protect-digital-identity": """
<h2>亲属冒用危机</h2>
<p>亲友代办业务时拍走身份证正反面照片，若随意存放在聊天相册，等于扩散不可控副本。办完即提醒对方删除，并抹掉本地缩略图。</p>
<h2>二手账号市场</h2>
<p>购买带实名游戏或社交账号可能触发平台风控，甚至卷入诈骗链。实名应自己完成，别买「已认证」身份。</p>
<h2>信用冻结</h2>
<p>在征信机构申请安全冻结，可在身份被盗后阻挡冒名贷款。国内流程各异，重在知晓这一缓冲工具存在。</p>""",
    "public-wifi-safety": """
<h2>笔记本共享热点</h2>
<p>笔记本共享手机热点时，默认密码复杂度不一。若为临时开会开启，会后关闭共享并改随机口令，避免路人蹭网窥探流量元数据。</p>
<h2>酒店有线口</h2>
<p>墙上 RJ45 口子并不更安全，同楼 VLAN 广播与 ARP 欺骗仍可能发生。有线同样走 HTTPS 与隧道策略。</p>
<h2>杀开关验证</h2>
<p>隧道客户端宣称有 kill switch，应断线实测 DNS 与 IP 是否回落裸连。配置见 <a href="/articles/what-is-dns-leak">DNS 泄露</a> 一文。</p>""",
    "what-is-end-to-end-encryption": """
<h2>群聊密钥轮转</h2>
<p>成员进出群聊时，协议会重发会话密钥。理解这点可知「踢人后能否读历史」取决于产品设计，而非一句 E2EE 口号。</p>
<h2>多端同步矛盾</h2>
<p>iPad 与手机同时在线，需要为多端分发同一批密钥。实现不当会出现新消息只到一端的情况，也是为何备份策略复杂。</p>
<h2>监管与举报通道</h2>
<p>部分服务提供元数据或附件 hash 给执法，与「内容 E2EE」并存。阅读隐私政策看具体承诺，而非只看图标。</p>""",
    "browser-privacy-settings": """
<h2>容器标签</h2>
<p>Firefox Multi-Account Containers 等方案用隔离 Cookie  jar，让工作与购物登录互不污染。比反复清缓存更省心。</p>
<h2>自动填充风险</h2>
<p>浏览器记住信用卡与地址，遇到仿冒域时一键填充更快泄密。高价值站点关闭表单自动填充，改由密码管理器在可信域启用。</p>
<h2>实验性 API</h2>
<p>站点可查询显卡、电池状态等指纹面。把高级实验特性保持默认关闭，除非特定开发需求。</p>""",
    "choose-privacy-tools": """
<h2>管辖地与传票</h2>
<p> VPN 运营地影响法律程序。无魔法规避，只需知道日志政策与母公司注册信息的可查性，在威胁模型内做取舍。</p>
<h2>订阅绑定支付</h2>
<p>用隐私工具却绑定主信用卡，会在账单上留下清晰关联。礼品卡或隔离邮箱只是补充层，不是银弹。</p>
<h2>社区信誉</h2>
<p>GitHub issue 活跃度、CVE 修复速度，比软文评测可靠。遇到长期未更新客户端，即使曾名噪一时也应迁移。</p>""",
    "common-cybersecurity-myths": """
<h2>Mac 免疫论</h2>
<p>macOS 也有恶意软件与钓鱼；Gatekeeper 不能阻止你亲手输入密码。平台差异不足以当借口。</p>
<h2>长长的 Wi-Fi 密码</h2>
<p>WPA3 个人模式比 WEP 强得多，但访客密码贴在墙上仍会被拍照外传。访客网络应定期轮换短期口令。</p>
<h2>量子加密营销</h2>
<p>「抗量子」标签若无可查算法与标准进展，当作广告过滤。关注 NIST 后量子标准落地时间表即可，不必追逐噱头产品。</p>""",
    "network-traffic-encryption": """
<h2>握手可见性</h2>
<p>即使 TLS 1.3 加密更多握手字段，观察者仍看到连接 IP、时间与大致体积。流量分析可推测音视频通话，但不等于读到文字内容。</p>
<h2>IPsec 与 SSL VPN</h2>
<p>企业历史产品多；个人用户少见。知道存在即可理解公司笔记本上多客户端图标各自含义。</p>
<h2>Perfect Forward Secrecy</h2>
<p>临时密钥泄露不应解密过往会话。检查站点是否支持现代 cipher suite，是运维责任，普通用户靠浏览器保持更新即可。</p>""",
    "protect-online-privacy": """
<h2>搜索历史分层</h2>
<p>同一浏览器里既搜医疗问题又看投资资讯，会被一并归档。敏感查询换独立配置文件或独立搜索引擎账号。</p>
<h2>线下画像回流</h2>
<p>会员卡手机号会把实体店购物绑回线上 ID。不是全能拒绝，而是知晓关联发生，决定哪些卡用化名手机注册。</p>
<h2>搜索引擎云同步</h2>
<p>登录搜索账户开启跨设备历史，便利即追踪。评估是否值得为少打几个字付出长期日志。</p>""",
    "what-is-dns-leak": """
<h2>IPv6 旁路</h2>
<p>隧道只封 IPv4 时，站点用 AAAA 记录仍可能让 v6 查询与连接走本地 ISP。双栈环境要同时核对 v4/v6 路由表。</p>
<h2>操作系统双解析</h2>
<p>Windows「加密 DNS」与浏览器 DoH 可并行又互相覆盖。变更后重启网络栈，避免 stale 缓存造成误判「已修好」。</p>
<h2>恶意分流列表</h2>
<p>不可信客户端内置「绕过隧道域名列表」可能故意漏掉银行类域名。只用官方渠道下载，校验签名与哈希。</p>""",
    "vpn-vs-proxy": """
<h2>透明代理与中间人</h2>
<p>公司网关在未经同意下插入代理证书时，HTTPS 会被代理解密审查。属策略行为，不是个人可随意复制的「技巧」。</p>
<h2>Tor 与混淆</h2>
<p>洋葱路由是另一类路径隐私方案，延迟与站点兼容性不同。与商业 VPN 比较时，认清你要对抗的威胁模型是否匹配。</p>
<h2>游戏与反作弊</h2>
<p>竞技游戏常禁止隧道以降低延迟作弊；强行全局 VPN 可能封号。按游戏条款选择，别把账号安全押在违规配置上。</p>""",
    "identify-phishing-attacks": """
<h2>深度伪造语音</h2>
<p>AI 合成老板声音催转账已登上新闻。大额仍要回拨已知座机或当面确认，不听指令就转账。</p>
<h2>日历邀请垃圾</h2>
<p>自动接受会议邀请会把钓鱼链接塞进日程，手机通知比邮件更醒目。关闭自动添加未知邀请。</p>
<h2>附件宏与 OneNote</h2>
<p>攻击链利用笔记内嵌脚本绕过邮件网关。陌生附件直接在隔离虚拟机打开，或干脆不打开。</p>""",
    "create-strong-passwords": """
<h2>可记忆口令 passphrase</h2>
<p>随机单词串加数字分隔，兼顾长度与输入速度。避免名言歌词——语料库攻击已收录流行句子。</p>
<h2>安全提问陷阱</h2>
<p>「母亲 maiden name」在社交网可搜到。对站点安全问题填随机字符串并存密码管理器，别如实作答。</p>
<h2>企业 SSO</h2>
<p>公司统一身份登录下游应用，个人仍要为 SSO 主账户保持最强因子。一处失守全线沦陷。</p>""",
    "two-factor-authentication-guide": """
<h2>SIM 交换防御</h2>
<p>向运营商设置 PIN、限制补卡，并把短信 2FA 仅作过渡。金融账户优先升级到密钥或 push 认批准。</p>
<h2>推送疲劳</h2>
<p>反复点「批准」会形成条件反射。陌生登录弹窗先取消，再进官方 App 查活动记录。</p>
<h2>旅行模式</h2>
<p>部分平台提供「丢失设备临时码」或旅行白名单。出国前登记备用因子，避免时区差阻断客服。</p>""",
    "what-is-https": """
<h2>HSTS 与预加载</h2>
<p>浏览器可对已知站点强制 HTTPS，降低 sslstrip 首访劫持。第一次访问陌生站仍要靠自己看地址栏。</p>
<h2>证书透明度</h2>
<p>CT 日志记录公开证书签发，企业可监控冒名域名。个人用户可知道自己看到的证书链已被第三方索引。</p>
<h2>mTLS 少见于消费站</h2>
<p>双向 TLS 多见于企业 API；大众网站只需服务器证书。看到客户端证书提示多半是公司内网，不是购物站常态。</p>""",
    "prevent-personal-data-leaks": """
<h2>剪贴板监视</h2>
<p>部分 App 读取系统剪贴板捕获一次性密码或钱包地址。粘贴敏感串后立即清空剪贴板，并限制后台 App 数。</p>
<h2>截图备忘录</h2>
<p>身份证照片存相册会被云同步。拍完后移入加密相册或打印封存物理副本，数字缩略图能删尽删。</p>
<h2>聊天记录取证请求</h2>
<p>司法程序可令平台交出未 E2EE 的消息。知晓这一点有助于选择通讯工具与讨论话题的场所。</p>""",
}

for slug, extra in EXPANSIONS.items():
    ARTICLES[slug]["content_html"] = ARTICLES[slug]["content_html"].rstrip() + extra
    ARTICLES[slug]["meta_description"] = META_LONG[slug]

EXPANSIONS2 = {
    "protect-mobile-data": "<h2>儿童与长辈设备</h2><p>帮家人装 App 时用自己的 Apple ID 会把你的支付与云端绑到对方机上。为长辈注册独立账户，开启限制安装与屏幕时间，减少误点诱导下载。</p><h2>维修与借出</h2><p>送修前备份后退出账户并抹除，或至少开启维修模式。借出手机给熟人时开启访客配置文件，避免对方误看你通知里的验证码。</p>",
    "choose-secure-network-connection": "<h2>卫星与低速链路</h2><p>卫星宽带高延迟却同样面临门户劫持。耐心核对证书比盲目加速更重要。</p><h2>车载热点</h2><p>车机共享蜂窝时，固件更新迟缓可能长期不修补漏洞。车机只做导航，敏感支付用手机流量完成。</p>",
    "windows-network-security-settings": "<h2>Hyper-V 与虚拟交换机</h2><p>跑虚拟机时，默认交换机可能绕过主机防火墙规则。为实验环境单独虚拟网段，避免 malware 样本探测到家庭 NAS。</p><h2>蓝牙与近场</h2><p>关闭不用的蓝牙可见性，防止会议室里被配对垃圾请求骚扰，间接泄露设备指纹。</p>",
    "protect-online-accounts": "<h2>聚合登录风险</h2><p>「使用微信登录」把身份绑定到超级 App。定期在设置里撤销一年未用的聚合授权，减少幽灵会话。</p><h2>登录通知习惯</h2><p>开启异地登录邮件，但别在邮件里点确认链；打开官方 App 查看活动，防邮件本身被伪造。</p>",
    "safe-public-network-use": "<h2>火车与航班局域网</h2><p>封闭式车地局域网同样不可信。看电影别顺手登录邮箱改密，落地后再处理高敏事。</p><h2>计费陷阱</h2><p>按分钟计费的机场 Wi-Fi 会催促你快速登录支付页面，正是社工窗口。宁可买流量包。</p>",
    "how-online-tracking-works": "<h2>重定向链</h2><p>联盟营销在跳转链上附加跟踪 ID，即使最终落地页是第一方域，中间商已记录点击。复制最终 URL 在无痕窗打开可减少一层。</p><h2>本地存储 API</h2><p>IndexedDB 与 localStorage 可长期保存标识，不受 Cookie 清除对话框管辖。浏览器设置里一并清理站点数据。</p>",
    "how-dns-servers-work": "<h2>私有域与企业内网</h2><p>内网 .local 或 split-brain DNS 让同域名在公司内外解析到不同 IP。远程办公隧道要一并接管内网 DNS，否则内网服务名无法解析。</p><h2>DoH 默认策略</h2><p>浏览器启用 DoH 可能绕过家长路由策略。家庭应在网关层协商一致，而不是悄悄对抗。</p>",
    "check-network-security": "<h2>智能门锁与摄像头</h2><p>IoT 设备默认密码呼啸于僵尸网络扫描列表。首次通电即改口令，并阻断其访问台式机文件共享。</p><h2>固件订阅通知</h2><p>订阅厂商安全通告邮件，比等新闻曝光更快得知需升级的 CVE。</p>",
    "why-data-encryption-matters": "<h2>硬件安全模块</h2><p>TPM 或安全 enclave 把磁盘密钥与启动链绑定。二手主板出售前要在固件层撤销平台密钥。</p><h2>邮件投递加密</h2><p>标准 SMTP 通常无端到端；敏感附件应用独立加密再发送，别指望「已发送」即保密。</p>",
    "zero-trust-security": "<h2>API 密钥轮换</h2><p>自动化脚本硬编码云 API 密钥，等同于散落口令。用短期令牌与权限范围最小化代替永久密钥。</p><h2>物理访客</h2><p>家政或维修在场时，锁屏比任何网络策略都先执行。离开房间带走笔记本。</p>",
    "what-is-ip-address": "<h2>任播与 CDN</h2><p>一个 IP 背后可能是 CDN 任播入口，不代表单一机器。封禁单个 IP 对大型站点意义有限。</p><h2>局域网广播</h2><p>ARP 欺骗在同一网段伪造网关，与公网 IP 无关。公共 Wi-Fi 仍要警惕旁路。</p>",
    "identify-malicious-websites": "<h2>国际化域名诈骗</h2><p>punycode 让西里尔字母形似拉丁域名。浏览器显示「原文」选项，发现异常字符立即退出。</p><h2>免费 SSL 自动化</h2><p>Let’s Encrypt 降低 HTTPS 门槛，也让骗子低成本拿证书。域名核查永远排在小锁之前。</p>",
    "protect-digital-identity": "<h2>元数据泄露</h2><p>登机牌照片含姓名与 PNR，可被用来钓鱼航司客服。晒旅行照时马赛克条码与证件号。</p><h2>电子签名习惯</h2><p>电子合同平台绑定的手机号若变更未同步，他人可能继承签名权限。换号前先更新签署档案。</p>",
    "public-wifi-safety": "<h2>邻国漫游误判</h2><p>边境地区手机自动连上他国运营商开放热点，资费与安全双重风险。手动选网并关自动数据漫游。</p><h2>会话固定</h2><p>门户网站有时强制 HTTP 首跳再登录。观察地址栏是否立刻升到 HTTPS，否则不输入口令。</p>",
    "what-is-end-to-end-encryption": "<h2>附件与预览</h2><p>云盘生成 PDF 预览可能解密服务器端再渲染，破坏 E2EE 语义。敏感文件用本地解密查看。</p><h2>语音视频</h2><p>通话 E2EE 与消息 E2EE 可能用不同协议栈，一端升级失败会导致「只有单方加密」降级。</p>",
    "browser-privacy-settings": "<h2>时区与语言</h2><p>固定指纹组合包括时区偏移与界面语言。极端匿名需求要接受部分站点因风控拒绝登录。</p><h2>Service Worker</h2><p>后台 worker 可持续同步跟踪数据。卸载 PWA 时要清除站点数据而不仅是删图标。</p>",
    "choose-privacy-tools": "<h2>捆绑安装</h2><p>某些下载站附赠「加速器」。拒绝勾选，从官网获取签名安装包，核对 SHA 汇总。</p><h2>日志自证</h2><p>独立审计报告与法庭传票记录，比博客长文更能说明是否真不记日志。</p>",
    "common-cybersecurity-myths": "<h2>隐私模式万能</h2><p>它不解雇键盘记录器，也不隐藏从你的公网 IP 流出的 TLS 目的地元数据（视网络而定）。</p><h2>黑客只盯大人物</h2><p>撞库与批量钓鱼不加挑选；普通人邮箱里的购物小票也能被用来伪造客服。</p>",
    "network-traffic-encryption": "<h2>压缩侧信道</h2><p>CRIME/BREACH 一类攻击利用压缩与加密结合泄露 Cookie 片段，多见于老旧配置。现代栈默认缓解。</p><h2>物联网明文</h2><p>廉价摄像头仍走明文 RTSP。与 HTTPS 网站无关，要在 VLAN 隔离。</p>",
    "protect-online-privacy": "<h2>家庭 IP 画像</h2><p>整条宽带共用一个公网画像，孩子设备上的淘气插件也会污染风控评分。分账户管理比责怪运营商更有效。</p><h2>跨境服务条款</h2><p>数据存储区域选择影响监管访问路径。注册时读清数据中心地域，而不是只点同意。</p>",
    "what-is-dns-leak": "<h2>WebRTC 与本地 IP</h2><p>浏览器 WebRTC 可能泄露内网地址，与 DNS 泄露不同但常一并检测。在隐私设置里限制不想要的 ICE 候选。</p><h2>定时复测</h2><p>系统休眠唤醒、Wi-Fi 切换或 VPN 重连都会改变解析路径。重大行程前后各测一次即可。</p>",
    "vpn-vs-proxy": "<h2>规则分流复杂度</h2><p>按域名/IP 精细分流需要维护列表，错误一条就裸露敏感流量。新手先用简单全隧或官方模板，再逐步细化。</p><h2>图书馆过滤</h2><p>机构 HTTP 代理用于过滤不当内容，不等于给你隐私；只是组织策略。</p>",
    "identify-phishing-attacks": "<h2>礼物卡话术</h2><p>「老板让你买苹果卡」是 BEC 经典剧本。公司采购不会通过即时通讯索要卡号密码。</p><h2>附件二维码</h2><p>PDF 内含二维码绕过邮件链接扫描。手机扫码前先核对预期收件人是否真发过这份文件。</p>",
    "create-strong-passwords": "<h2>键盘布局</h2><p>跨设备输入生僻符号易错。Passphrase 用常见键位单词可减少移动端挫败感。</p><h2>硬件令牌备份</h2><p>物理 U2F 钥匙备两把，分放不同地点；丢一把不致全面锁死。</p>",
    "two-factor-authentication-guide": "<h2>备份码打印</h2><p>纸张要防水防窥存，与主电脑分柜。拍照进未加密云相册等于制造第二泄露点。</p><h2>共享账户陷阱</h2><p>流媒体家庭共享不是 2FA 替代；每个登录者仍应独立口令，防止一方设备失守牵连全家。</p>",
    "what-is-https": "<h2>TLS 指纹</h2><p>客户端握手特征可被中间设备分类识别，与证书无关。普通用户靠保持系统现代即可，不必手工改 cipher。</p><h2>企业抓包透明代理</h2><p>公司根证书让你看到小锁却仍被审计。区分「加密到谁」：到代理还是到公网站点。</p>",
    "prevent-personal-data-leaks": "<h2>快递面单</h2><p>扔包装盒前撕掉含姓名电话的面单，或用笔涂黑。聚合配送照片也可能被上传到社交拼单群。</p><h2>旧硬盘</h2><p>出二手电脑前做加密卷擦除或物理粉碎，格式化 quick 并不毁数据。</p>",
}

for slug, extra in EXPANSIONS2.items():
    ARTICLES[slug]["content_html"] += extra

EXPANSIONS3 = {
    "protect-mobile-data": "<h2>工作资料与个人相册</h2><p>同一相册混合公司扫描件与旅行照片，云同步会把保密级文档推到个人备份。用系统安全文件夹或企业合规容器单独收纳业务 PDF，并关闭该目录的外链分享功能。</p><p>若使用 Type-C 扩展坞接公共大屏投屏，记得在「仅镜像」模式下检查通知是否同步弹出，洽谈内容可能泄露给会议室旁人。</p>",
    "choose-secure-network-connection": "<h2>应急断网演练</h2><p>偶尔在可控环境里断开全家网络十分钟，看看哪些监控、门锁或工作 App 开始报错。你会意外发现许多服务其实默认可离线，却长期向外发心跳。</p><p>弄清依赖后，再决定哪些必须上云，哪些可以留在本地环路，减少单点运营商故障带来的焦虑。</p>",
    "windows-network-security-settings": "<h2>PowerShell 远程</h2><p>WinRM 与 OpenSSH Server 若被误开，会在公网扫描列表暴露高价值端口。控制面板确认「可选功能」里未启用未计划的远程组件。</p><p>笔记本合盖休眠后，旧 Wi-Fi 会话有时保持半连接，回来工作时先断再连，强迫重新走完整认证。</p>",
    "protect-online-accounts": "<h2>次级邮箱策略</h2><p>为购物网站用独立邮箱，主邮箱只服务银行与云。这样泄露库里的论坛密码撞不回枢纽。</p><p>收到「您账户将被冻结」主题邮件时，与其点链接，不如在浏览器新开标签输入 bookmark 里的官网域名核对消息真伪。</p>",
    "safe-public-network-use": "<h2>共享办公位</h2><p>WeWork 一类场所同一 VLAN 容纳多家公司。打印驱动漏洞历史上曾横向扩散，打印敏感合同前确认队列无他人作业。</p><p>离开工位时 Win+L 锁屏是基本礼仪；肩窥比 Wi-Fi 旁路更常见。</p>",
    "how-online-tracking-works": "<h2>零售商会员码</h2><p>线下扫码积分与线上账号合并，让实体购物也进入画像。不是不能积分，而是知晓这一关联，避免用登记实名邮箱接收垃圾追踪邮件。</p><p>电视大屏登录视频账号，会把客厅观看历史叠到个人资料，与孩子共用设备时切换少儿档案。</p>",
    "how-dns-servers-work": "<h2>ECS 与隐私权衡</h2><p>部分递归 DNS 会把你的大致子网附带给权威服务器，以返回更近的 CDN 节点。这提升速度也略增隐私暴露，公共解析器政策里会说明是否启用 ECS。</p><p>自建 Pi-hole 过滤广告域时，要同步更新威胁情报列表，否则刚刚爆发的跟踪域仍会通过。</p>",
    "check-network-security": "<h2>来宾网络带宽</h2><p>给访客限速可防止邻居孩子在你宽带上下载盗版资源连累 IP 信誉。QoS 不是豪华功能，现代路由大都支持。</p><p>年终盘点时拍下当前连接设备清单，与实物对照，比凭记忆记得「好像只有六台」更靠谱。</p>",
    "why-data-encryption-matters": "<h2>司法与监管请求</h2><p>云厂商加密静态数据，仍可能在法律程序下解密移交。敏感专案应客户端加密，密钥自控，理解这与便利永远冲突。</p><p>打印保密合同后，碎纸机与数字擦除一样重要；纸面是离线泄露常被忽视的一支。</p>",
    "zero-trust-security": "<h2>文档链接权限</h2><p>在线文档「组织内任何人可编辑」的默认共享很危险。每次分享改为指定邮箱并设到期，像发卡有限次数的门禁。</p><p>离职协作者账号若未移除，仍可能通过历史通知进入空间，人事变动当天就清理权限。</p>",
    "what-is-ip-address": "<h2>物联网上报</h2><p>定时上报温湿度的设备每分钟向云发 UDP，可长期泄露家庭作息。购买前看是否可改上报间隔与关闭云端统计。</p><p>游戏主机开放在 UPnP 的端口会在 Shodan 类搜索引擎显眼，不玩联机时关掉相关功能。</p>",
    "identify-malicious-websites": "<h2>评论引流</h2><p>正常论坛突然出现多条带相同下载短链的夸赞回复，常为挂马包铺路。远离「破解补丁」站，走官方更新通道。</p><p>电商促销短信里的短域名在活动中成千上万，难以一眼分辨，购物仍用手动输入官网更稳。</p>",
    "protect-digital-identity": "<h2>政务办事留痕</h2><p>线上政务截图含办事编号，转发家族群会扩散可追溯标识。必要遮码再发，并删除聊天里临时图片。</p><p>高校学号、工号与门禁卡号组合，足以冒充内部员工拨打 IT 热线，社工话术里避免随口报号。</p>",
    "public-wifi-safety": "<h2>直播上传窗口</h2><p>现场直播把观众反应与地理位置一并暴露，恶意观众可结合 Wi-Fi 门户收集更多情报。延迟几分钟发布回放更稳。</p><p>共享热点给同行时，用系统「访客网络」隔离，而非公开主密码。</p>",
    "what-is-end-to-end-encryption": "<h2>明文搜索索引</h2><p>部分 E2EE 产品仍对附件文件名或联系人做明文索引方便搜索，阅读隐私白皮书里的索引策略段落。</p><p>法庭令可能要求提交联系人关系图，即使消息体已加密，元数据图仍敏感。</p>",
    "browser-privacy-settings": "<h2>下载文件夹监控</h2><p>恶意扩展偶尔监视下载目录寻找钱包文件。定期清理下载夹，扩展权限拒绝访问「所有文件」。</p><p>为不同银行使用不同浏览器颜色主题，降低在仿冒页误用自动填充的概率。</p>",
    "choose-privacy-tools": "<h2>学术引用</h2><p>独立论文或 USENIX 安全顶会报告，比 YouTube 测评更可靠地描述协议弱点。搜索工具名加「security audit」。</p><p>厂商若拒绝回答「漏洞赏金计划」，长期维护承诺就要打问号。</p>",
    "common-cybersecurity-myths": "<h2>免费电话支持</h2><p>正规厂商不会在谷歌广告里抢「客服电话」首位而索要远程控制。搜索来的电话要先和卡片背面官方号交叉。</p><p>所谓「清除病毒只需一行命令」视频常让你关闭 Defender，本质是诱导。</p>",
    "network-traffic-encryption": "<h2>邮件提交到服务器</h2><p>SMTP 从客户端到自家服务商往往是 TLS，但从服务商到对方未必。高敏合同用独立加密附件，而不是普通附件。</p><p>DoH 只保护查询，不改变网站证书关系。联读 <a href=\"/articles/what-is-https\">HTTPS</a> 与 <a href=\"/articles/what-is-dns-leak\">DNS 泄露</a> 全貌更清晰。</p>",
    "protect-online-privacy": "<h2>健身 App 敏感</h2><p>跑步轨迹精确到卧室门口，可推断住址。发布动态前裁剪首尾五百米或延迟公开。</p><p>读书笔记同步到社交，会暴露政治宗教取向，平台用它做推断广告。阅读器关公开档案。</p>",
    "what-is-dns-leak": "<h2>门户认证干扰</h2><p>机场门户未登录前，任意 DNS 查询可能被劫持到警告页，导致「假阳性」泄漏检测。完成门户认证后再测。</p><p>Linux NetworkManager 拆分 DNS 配置，手工指定不匹配隧道的解析器时，桌面用户更易踩坑。</p>",
    "vpn-vs-proxy": "<h2>政企 SSL 代理</h2><p>学校代理缓存视频流量是性能优化，不是隐私工具。个人在外网不能混用校内代理配置。</p><p>代理链 A→B→C 只增加失败点，不神奇叠加安全；除非明确了解每跳运营方信誉。</p>",
    "identify-phishing-attacks": "<h2>招聘钓鱼</h2><p>假猎头索要身份证与银行卡开工资户，实为洗钱。正规流程在背调通过后才收证件，且走加密入职门户。</p><p>「税务局」语音电话要立刻回拨官方 12366 核实，勿回电来电显示号码。</p>",
    "create-strong-passwords": "<h2>哈希泄露时间线</h2><p>站点拖库数年才公开，你以为旧密码仍安全。枢纽账户即便多年未换，也要假设曾出现在未知泄露库。</p><p>密码管理器内置泄露监测订阅 Have I Been Pwned 类服务，定期对照轮换。</p>",
    "two-factor-authentication-guide": "<h2>旧手机退役</h2><p>卖二手前在每台 App 取消 2FA 设备注册，再在设置里移除 TOTP。否则买家可能接管你还没下线的会话。</p><p>应急一次性备用码每次启用一条就划掉，防止截图长期有效。</p>",
    "what-is-https": "<h2>TLS 版本降级</h2><p>老旧浏览器协商到 TLS1.0 会被中间人利用。保持系统现代即可自动禁用弱协议。</p><p>内网自签证书管理混乱时，员工会习惯点「继续访问」，这一陋习带到公网极危险。</p>",
    "prevent-personal-data-leaks": "<h2>语音助手</h2><p>智能音箱偶然上传背景谈话片段到云端审核。静音键与关闭语音购买，敏感话题远离收音范围。</p><p>简历 PDF 元数据里藏着作者电脑登录名，投递前用导出选项清除属性。</p>",
}

for slug, extra in EXPANSIONS3.items():
    ARTICLES[slug]["content_html"] += extra

EXPANSIONS4 = {
    "protect-mobile-data": "<h2>固件与基带</h2><p>运营商推送的基带更新与系统大版本同级重要，延迟安装可能留下空口嗅探已知洞。设置里打开自动安全更新，旅行归国后手动检查是否有漫游期间错过的补丁包。</p>",
    "choose-secure-network-connection": "<h2>双卡切换</h2><p>双卡手机在信号弱时会跳到副卡数据，可能意外走上不同运营商计费与过滤策略。办理敏感业务前锁定使用主卡数据，并关闭「智能切换」。</p>",
    "windows-network-security-settings": "<h2>定位与 Wi-Fi 扫描</h2><p>Windows 会用可见 Wi-Fi 列表辅助定位，实质上传周围 BSSID 轮廓。可在隐私设置里限制应用访问位置，并关闭「发送可选诊断」里过细的网络遥测。</p>",
    "protect-online-accounts": "<h2>停机与换号</h2><p>手机号注销后若被运营商回收利用，下一位机主可能接收你旧账号的短信验证码。换号前先在各站改绑并观察一周确认无漏网服务。</p>",
    "safe-public-network-use": "<h2>视频会议背景</h2><p>公共网络开视频会议时，厂商为了降码率可能降低传输安全选项。涉及合同条款讨论时改用有线或蜂窝，并核对会议链接是否公司名下。</p>",
    "how-online-tracking-works": "<h2>SDK 内嵌</h2><p>App 内置统计 SDK 在后台上报行为，与浏览器 Cookie 无关。安装前阅读权限与隐私标签，游戏与工具类尤其爱夹带广告标识。</p>",
    "how-dns-servers-work": "<h2>日志保留政策</h2><p>公共 DNS 服务商在隐私政策里声明日志保存多久。选解析器时读这一段，比看响应速度排名更接近真实隐私差异。</p>",
    "check-network-security": "<h2>MQTT 默认端口</h2><p>智能家居若暴露 1883 端口到公网，会被僵尸网络快速订阅。在网关阻断入站，仅允许内网设备对话。</p>",
    "why-data-encryption-matters": "<h2>Ransomware 与备份</h2><p>勒索软件加密在线同步盘里的明文备份。3-2-1 规则里至少一份离线不可变备份，才能让加密真正服务于恢复而非单点失效。</p>",
    "zero-trust-security": "<h2>短期承包商</h2><p>外包设计稿链接若永久有效，离职设计师仍可回看原型。项目结案即撤销外链，与终止雇佣同日完成。</p>",
    "what-is-ip-address": "<h2>诉讼与传票</h2><p>公网 IP 日志足以让服务商在司法程序下指向订阅者，但通常还需进一步传票找具体人。理解这一点有助于评估动态 IP 被记入威胁情报的风险。</p>",
    "identify-malicious-websites": "<h2>Web3 钓鱼</h2><p>假钱包连接页模仿 MetaMask 弹窗，诱导签名无限授权。只从扩展自带入口连 DApp，拒绝网页浮层「一键连接」。</p>",
    "protect-digital-identity": "<h2>家谱数据</h2><p>基因测序与家谱网站汇聚近亲关系，可被社工推断本人生日母亲等信息。上传前缩减可见范围并关闭公开匹配。</p>",
    "public-wifi-safety": "<h2>DNS over TLS 在门户期</h2><p>未完成门户认证时，系统加密 DNS 可能握手失败回退明文。这不是泄露隧道，而是未入网状态；认证后再启用加密更稳。</p>",
    "what-is-end-to-end-encryption": "<h2>工作组例外</h2><p>企业版可在合规密钥托管下读取部分员工消息，与消费者版 E2EE 声明不同。注册企业租户前读管理员文档。</p>",
    "browser-privacy-settings": "<h2>PDF 内置阅读器</h2><p>浏览器内打开 PDF 时，JavaScript 可能仍执行。下载后离线阅读敏感合同，或在阅读器禁用 JS。</p>",
    "choose-privacy-tools": "<h2>币种与发票</h2><p>用外币支付隐私服务会在卡账单留痕。这不是否决理由，只需知晓关联仍可能存在。</p>",
    "common-cybersecurity-myths": "<h2>局域网绝对安全</h2><p>访客 Wi-Fi 上 ARP 欺骗照样发生；「在家就没事」不成立。路由器分网段与 HTTPS 习惯在家同样必要。</p>",
    "network-traffic-encryption": "<h2>WPA3 与链路层</h2><p>无线链路层加密保护空口，不等同 TLS。进入路由后的有线段若明文，邻居拉网线仍能嗅探——家庭布线与访客隔离仍重要。</p>",
    "protect-online-privacy": "<h2>礼单与 RSVP</h2><p>在线婚礼请柬平台收集宾客电话 dietary 信息，转售给营销商偶有报道。填写最少字段并拒绝勾选「接收合作方资讯」。</p>",
    "what-is-dns-leak": "<h2>多宿主并行</h2><p>笔记本书同时开以太网与 Wi-Fi 时，策略路由可能让 DNS 走有线而 HTTP 走无线，检测页结果令人困惑。测前只留一种上联。</p>",
    "vpn-vs-proxy": "<h2>MTU 黑洞</h2><p>代理不加密封装大包时，PMTU 黑洞导致图片加载一半卡住。表现为「部分站点坏掉」而非全面断网，调低 MTU 或换全隧方案可缓解。</p>",
    "identify-phishing-attacks": "<h2>快递「到付」</h2><p>短信称快件需付费扫码实为钓鱼站。正规快递在官方 App 查状态，不扫陌生二维码付款。</p><h2>奖学金诈骗</h2><p>准留学生收到「教育部奖学金链接」要求填银行卡，语义官方细节可疑。对照教育局官网名单，不点泛码推送。</p>",
    "create-strong-passwords": "<h2>浏览器内置建议</h2><p>Chrome 与 Safari 随机密码功能便捷，却绑定生态。评估你是否接受与单一浏览器锁死，再决定是否迁到独立密码管理器。</p><h2>输入法云同步</h2><p>手机拼音输入法若云同步个人词库，可能把账号片段传到服务器。敏感账号输入时切换无云临时键盘。</p>",
    "two-factor-authentication-guide": "<h2>手表与可穿戴</h2><p>智能手表显示一次性验证码，腕离身等于第二因子裸露。健身淋浴前摘表或关闭通知预览。</p><h2>账户恢复诈骗</h2><p>假客服让你「关闭 2FA 才能解冻」是钓鱼经典套路。官方从未要求先关再开验证。</p>",
    "what-is-https": "<h2>子资源完整性</h2><p>网站引用 CDN 脚本可用 SRI 哈希校验，防 CDN 被投毒。读者看不见，但说明安全站会叠加多层，不止小锁图标。</p><h2>书签 URL 写法</h2><p>收藏夹若存的是首页 HTTP 重定向，旧书签跳过时可能短暂明文。书签直接写 <code>https://</code> 起始 URL。</p>",
    "prevent-personal-data-leaks": "<h2>问卷抽奖</h2><p>街头扫码填表换礼品常收集身份证拍摄。评估是否值得用实名换小礼品，多数情况可拒。</p><h2>群聊合并转发</h2><p>微信合并转发聊天记录含他人手机号与住址。二次分享前手动删敏段落，避免义务扩散熟人隐私。</p>",
}

for slug, extra in EXPANSIONS4.items():
    ARTICLES[slug]["content_html"] += extra

EXPANSIONS5 = {
    "protect-mobile-data": "<p>用 NFC 绑定交通卡或车钥匙后，丢失手机等于同时丢实体入口权限。远程擦除前在钱包 App 里吊销虚拟卡，再到物业作废小区门禁权限，顺序颠倒会让失主在门外却无法登录云控台。</p>",
    "choose-secure-network-connection": "<p>城市天际线里的「全城免费 Wi-Fi」市政项目，日志政策往往写在冗长条款里。当作便利即可，办理户口、签证预约这类政务仍用家庭可信网络，减少会话被关联到城市级监控系统的概率。</p>",
    "windows-network-security-settings": "<p>游戏加速器的「内核驱动」会改写网络栈，与内置防火墙并列时，可能出现双层过滤冲突。卸载后若网速异常，用网络重置功能恢复默认栈，再逐项重装必要工具。</p>",
    "protect-online-accounts": "<p>期末同事互借视频会员时，实质上共享同一登录态。若对方设备中木马，你的播放记录与绑卡信息一并暴露。订阅类账户独立购买或家庭组官方共享，别直接交主密码。</p>",
    "safe-public-network-use": "<p>图书馆机房老式 PC 可能仍运行过期系统，插入 U 盘自动播放风险与 Wi-Fi 并存。只登录只读数据库检索，不在此终端输入任何可重置你邮箱的凭据。</p>",
    "how-online-tracking-works": "<p>流媒体「继续观看」按钮让账号习惯一目了然。合租客厅电视登录主账号时，室友看到的是你的成人向或医学纪录片记录——用独立档案比事后清历史更少尴尬。</p>",
    "how-dns-servers-work": "<p>企业下发「内外 split DNS」后，私人笔记本接公司隧道，连回家打游戏解析仍可能走公司路径。下班断开隧道并刷新解析缓存，避免游戏服匹配异常。</p>",
    "check-network-security": "<p>租房轮换租客时，前任留下的智能家居未解绑，新房客可远程开门。入住首日重置网关、改 SSID，并向原房东确认云账户已移除旧设备。</p>",
    "why-data-encryption-matters": "<p>摄影记者把相机卡直接交给冲印店，相当于未加密静态数据离手。高价值素材先在笔记本加密归档，再送选片，比事后后悔删除云端预览更主动。</p>",
    "zero-trust-security": "<p>家长群共享文件夹默认公开给全班家长，上传孩子体检表即扩散。设为仅老师可写家长只读，每学期末归档并清空旧附件，避免「永久在线」。</p>",
    "what-is-ip-address": "<p>智能家居 App 显示「上次登录 IP」时，结合时间线可推断你是否出差。若介意泄露行程，关闭对外显示历史登录，或仅在必要时开通知。</p>",
    "identify-malicious-websites": "<p>弹窗提示「您的电脑已中毒，拨打热线」纯社工。正规系统不会用浏览器全屏页索要电话拨号；直接结束进程，用任务管理器关标签。</p>",
    "protect-digital-identity": "<p>马拉松 bib 号码布照片含姓名，可配合公开成绩数据库定位社交账户。终点自拍可挡住号码，同样快乐却不送打手素材给陌生账号拼装。</p>",
    "public-wifi-safety": "<p>酒店房间信息卡印着「免费 Wi-Fi」与固定口令，常被扔到垃圾袋拍照进社交。参会者照片背景露出口令，等于公开访客网络——入住后索要个人账号而非通用口令更佳。</p>",
    "what-is-end-to-end-encryption": "<p>协作白板工具宣称端到端，却往往只有文本层加密，贴图上传仍是 TLS 到服务端。签合同前先问销售哪类对象真 E2EE，别被笼统图标误导。</p>",
    "browser-privacy-settings": "<p>办公笔记本与个人账号混登同一 Chrome 配置，离职时清 Cookie 容易漏掉已登录 SaaS。交接日创建新系统用户，而不是只删历史记录。</p>",
    "choose-privacy-tools": "<p>在某宝买的「隐私 U 盘」若无公开算法说明，可能只是分区隐藏。真正需求用成熟全盘加密产品，别迷信塑料壳营销词。</p>",
    "common-cybersecurity-myths": "<p>「同事发的链接肯定安全」是最危险的假设。内部账号被盗后第一波钓鱼就面向同事群发。照样核对域名，哪怕发件人是老板。</p>",
    "network-traffic-encryption": "<p>回国 Roaming 时漫游伙伴与本地运营商都可能记录目的 IP 集合。商务机密通话仍选端到端通讯工具，而不是默认短信。</p>",
    "protect-online-privacy": "<p>外卖默认备注「不要打电话」仍会显示楼层与性别绰。改自提或隐私号码服务，减少骑手与平台同时掌握精确门牌。</p>",
    "what-is-dns-leak": "<p>游戏加速器客户端所谓「专属 DNS」有时只是 marketing，实质仍走默认。开隧道后看解析服务器是否变更，比信广告语可靠。</p>",
    "vpn-vs-proxy": "<p>远程桌面软件自带中继绕 NAT，不走系统 VPN。以为开了全局隧道，RDP 流量仍可能旁路——为远程办公单独核对路由表。</p>",
    "identify-phishing-attacks": "<p>高校邮箱「奖学金发放」钓鱼在开学季激增。款项走学校财务系统，不会要求微信扫码付「手续费」。财务窗口电话确认后再操作。</p>",
    "create-strong-passwords": "<p>旧式规则强制三月改密，员工倾向在末尾递增数字。政策改革后仍有人保留习惯，这正是攻击者预测的模式。改用管理器随机串，定期只轮换泄露站。</p>",
    "two-factor-authentication-guide": "<p>银行 U 盾与手机盾并存时，搞不清用哪个容易点错拒绝，反而锁户。写在便签上的应是流程图而非密码；弄清何场景用硬件何场景用 App，比多堆因子更有效。</p>",
    "what-is-https": "<p>家长控制软件安装自签证书后会读 HTTPS 内容，这是明示功能而非黑客。理解家庭场景下的「解密观察」与恶意中间人的差别，配置前先与家人沟通边界。</p>",
    "prevent-personal-data-leaks": "<p>医美机构「术后对比照」入营销素材需单独签授权，别在雾状马赛克还没 Export 时就点「同意用于宣传」。肖像权撤回比数据删库更难。</p>",
}

for slug, extra in EXPANSIONS5.items():
    ARTICLES[slug]["content_html"] += extra

EXPANSIONS6 = {
    "protect-mobile-data": "<p>手表同步通知时，验证码会横在腕上给旁人偷看。金融类应用关闭手表端预览，或设置复杂手势才能展开短信内容。</p>",
    "choose-secure-network-connection": "<p>地下室与电梯井会强迫手机回落 2G/3G，旧制式下中间人风险略升。停车缴费等小事可拖延到地面再支付。</p>",
    "windows-network-security-settings": "<p>BitLocker 与 TPM 绑定的设备送修时，告知工程师勿拆硬盘单独读取。备份恢复密钥后再交付售后。</p>",
    "protect-online-accounts": "<p>枢纽邮箱签名栏写备用联系手机，一旦本人失联，家属凭纸质记录协助解冻账户，比口口相传可靠。</p>",
    "safe-public-network-use": "<p>跨国漫游数据虽贵，但单一运营商账密链更短。短暂开漫游办完银行业务，有时比蹭陌生热点更省心。</p>",
    "how-online-tracking-works": "<p>生日特惠邮件精确到当天，说明画像有日期字段。不必向所有品牌披露真实生日，用固定假日期打断巧合营销。</p>",
    "how-dns-servers-work": "<p>自建递归 resolver 维护量大，个人更现实是挑选信誉公共 DNS 并锁定，防止恶意 DHCP 临时改解析。</p>",
    "check-network-security": "<p>对讲门铃若走 P2P 穿 NAT，固件洞可导致陌生人远程预览。关注厂商 CVE 通告与强制更新推送。</p>",
    "why-data-encryption-matters": "<p>开源项目私钥放在未加密笔记本，一旦 CI 镜像被拖库，签名信任链崩塌。开发者硬件钥单独保管。</p>",
    "zero-trust-security": "<p>合租室友借你电脑，用访客账户而不是管理员。Guest 账户无权安装驱动，降低无意木马概率。</p>",
    "what-is-ip-address": "<p>论坛管理员封 IP 往往误伤整栋合租房。遭遇误封时附 traceroute 与账号诚信记录申诉，比反复换号更令人信服。</p>",
    "identify-malicious-websites": "<p>仿冒「系统更新」页面要求下载 .msi 时，对照微软累计补丁编号。真正的系统更新走设置应用通道，不经随机域名。</p>",
    "protect-digital-identity": "<p>网课屏幕共享若露出户口本扫描件缩略图，全班可见。共享前关无关标签，只留当前课件窗口。</p>",
    "public-wifi-safety": "<p>反诈 App 推广的公共 Wi-Fi 检测，本质也是联网查询。允许其读取网络信息即可，别顺带开通讯录权限。</p>",
    "what-is-end-to-end-encryption": "<p>家庭 NAS 自架聊天服务若未正确配置 TLS，「自建」不等于 E2EE。证书与密钥轮换要有文档，不只图心理安慰。</p>",
    "browser-privacy-settings": "<p>学校机房统一 Chrome 策略禁扩展时，个人书签仍同步云端。毕业前导出 HTML 书签并退出学校账号。</p>",
    "choose-privacy-tools": "<p>阅读英文隐私政策可借助浏览器翻译，但法律效力仍以原文为准。重点找数据保留期限与管辖法院条款。</p>",
    "common-cybersecurity-myths": "<p>「AI 防毒机器人 7×24 云端保护」是营销空话。终端保护仍是系统补丁、少点可疑链接与备份三件事。</p>",
    "network-traffic-encryption": "<p>蓝牙 LE 配对键盘输入可能被旁路嗅探品质不高，但对公共演讲场景足够。密码输入仍优先有线键盘或屏上键盘。</p>",
    "protect-online-privacy": "<p>旧手机当监控摄像头时，默认可访问相册与麦克风。专用监控固件重置权限，别用生活主力 Apple ID 登录。</p>",
    "what-is-dns-leak": "<p>滥用 hosts 文件手写域名映射可绕过 DNS 泄漏检测，但也为恶意软件投毒留后门。hosts 只保留真实调试需要条目。</p>",
    "vpn-vs-proxy": "<p>自动化爬虫开发者混用代理池时要注意出口信誉，被封后拖累业务 IP。个人隐私场景无需如此复杂，稳定单跳更好。</p>",
    "identify-phishing-attacks": "<p>HR 背景调查真机构会用座机来电并给官网验证流程，不会要求 Telegram 传身份证。陌生 IM 自称背调一律先挂。</p>",
    "create-strong-passwords": "<p>团队共用「项目密码」存于飞书文档，离职成员未移出即全员等同持有根钥。帐号彻底使用邀请制与单独密码条目。</p>",
    "two-factor-authentication-guide": "<p>企业微信审批与钉钉推送若绑私人手机，离职注销企微后再解绑个人号，防止离职审批通知继续落到私人终端。</p>",
    "what-is-https": "<p>抓包调试本地开发常用自签证书；电脑信任后忘记移除，将来可能被恶意软件复用同一信任槽。项目结束删除测试根证。</p>",
    "prevent-personal-data-leaks": "<p>旧路由器回收卖二手前，复位未必清掉定制化 DNS 劫持插件。刷官方固件再卖，避免下家继承你的黑名单规则。</p>",
}

for slug, extra in EXPANSIONS6.items():
    ARTICLES[slug]["content_html"] += extra

TOPUP = {
    "protect-online-accounts": "<p>写完账户清单后，每季抽查一次即可，不必每日焦虑。</p>",
    "choose-privacy-tools": "<p>评测文章若只字未提威胁模型，就当种草文案划过。购物前用十分钟写下「我在乎什么」，再筛候选名单，比收藏十个视频更高效。</p>",
    "prevent-personal-data-leaks": "<p>快递代收点监控能证明包裹被领走，却不能替你擦掉包装上的面单。回家第一件事撕掉贴纸，再拍开箱照分享也不迟。</p>",
    "two-factor-authentication-guide": "<p>备用手机放干燥密封袋与日常机分格，旅行丢主力机时不至于 2FA 与通讯录同时蒸发。老机器长期不开机，也要每半年充到一半电，防止电池鼓包。</p>",
    "browser-privacy-settings": "<p>插件商店「隐私保护」排行榜会随刷票变动，看下载量与开源仓库 Star 数比看名次更客观。装完两周仍要用的再留，其余卸载减攻击面。</p>",
    "protect-digital-identity": "<p>发票抬头写公司名可以报销，但个人网购仍避免用真实全名缩写做昵称，购物记录撞库时能少一条关联信号。</p>",
    "common-cybersecurity-myths": "<p>同事炫耀从不中招，往往只是攻击样本尚未覆盖他。谦虚地把清单当习惯，比吹嘘经验更能活得久。</p>",
    "identify-phishing-attacks": "<p>语音留言自称「顺丰补款」时，用独立 App 查物流单号即可判断。别让紧迫感催促你在嘈杂地铁里输卡号。</p>",
    "identify-malicious-websites": "<p>浏览器地址栏开启「始终显示完整网址」设置，缩短的昵称域名便无处藏身，仿冒的子域拼贴一眼识破。</p>",
    "what-is-end-to-end-encryption": "<p>会议录制如果云端转写，说明音频已离开 E2EE 语境进入分析管道。敏感技术讨论关闭录制或改用本地离线笔记。</p>",
    "zero-trust-security": "<p>家人共享平板给孩子模式玩益智游戏，比共用家长管理员账户少一类误下单风险。儿童配置禁装商店未知来源。</p>",
    "public-wifi-safety": "<p>民宿房东留写着 Wi-Fi 的黑板，入住拍 Instagram 时入镜等于公开发布口令。拍室内照前擦掉文字或改密。</p>",
    "safe-public-network-use": "<p>商务洽谈用热点文件直传，不如企业盘链接带过期。文件落地后再关共享，避免复盘时文件夹一直敞开。</p>",
    "protect-online-privacy": "<p>播客 RSS 订阅会带出听友习惯标签。不想被精准广告投喂时，用独立邮箱订阅，而非主邮箱一路到底。</p>",
    "create-strong-passwords": "<p>键盘贴备忘便签写着主密码，清洁工比你先看到。便签交给密码管理器，纸张只记无主密码的紧急联系人电话。</p>",
    "what-is-https": "<p>老旧纸质报刊抄录官网地址易错一字。打印材料时对照浏览器复制链接，避免读者被输错域名带到钓鱼页。</p>",
    "why-data-encryption-matters": "<p>把 Time Machine 与云盘混成唯一备份时，勒索软件一锅端。每周拔一次离线硬盘，让加密盘真正可恢复。</p>",
    "network-traffic-encryption": "<p>调试网站时临时回退 HTTP，上线前用扫描器确认无混合内容。开发坏习惯若遗忘关闭，用户会在生产环境裸奔。</p>",
    "check-network-security": "<p>打印机固件十年来从不更新，却连着合同扫描件。单独 VLAN 放打印设备，比期待它「只内网很安全」更现实。</p>",
    "what-is-dns-leak": "<p>手机热点共享给笔记本时，解析职责常被手机代理。二者都开 VPN 时容易双重封装，测速慢就先断开一个终端。</p>",
    "vpn-vs-proxy": "<p>科学上网与合规企业隧道名字相似，误装来路客户端会把手势数据发往未知节点。只从雇主或厂商签名页面下载。</p>",
    "what-is-ip-address": "<p>动态 DNS 服务把在变公网 IP 绑到固定主机名，方便自架博客。记得同时轮换 DDNS 账户密码，否则别人可劫持你的域名指向。</p>",
}

for slug, extra in TOPUP.items():
    ARTICLES[slug]["content_html"] += extra

TOPUP2 = {
    "vpn-vs-proxy": "<p>选型记录写在笔记里便于日后复盘。</p>",
    "safe-public-network-use": "<p>短途出差同样适用上述分级习惯。</p>",
    "check-network-security": "<p>发现异常先断网再拍照留存证据。</p>",
    "zero-trust-security": "<p>权限回收应与人员变动同日完成，别拖到季度盘点。</p>",
    "identify-malicious-websites": "<p>收藏夹定期导出备份，避免被恶意扩展悄悄改写条目。</p>",
    "protect-digital-identity": "<p>海报上印的常见问答答案若可被搜索到，就别用作网站找回问题的答案。</p>",
    "public-wifi-safety": "<p>长期驻扎咖啡厅办公者，宜办理店内官方会员号而非蹭临时访客口令。</p>",
    "what-is-end-to-end-encryption": "<p>选型表格里写明是否默认群组 E2EE，比宣传页口号靠谱。</p>",
    "browser-privacy-settings": "<p>同步功能关掉了，也要确认各终端已登出的会话不再上传历史。</p>",
    "choose-privacy-tools": "<p>试用期结束前决定是否续费，比自动扣款后才后悔更省预算与隐私风险。</p>",
    "common-cybersecurity-myths": "<p>把本文当作纠偏清单分享给朋友，好过争论抽象口号谁对谁错。</p>",
    "protect-online-privacy": "<p>隐私不是零和博弈，在便利与暴露之间留一点灰度，比追求理论匿名更易坚持。</p>",
    "identify-phishing-attacks": "<p>企业邮箱外发敏感附件时，改用加密门户链接并电话口头核对一次性口令。</p>",
    "create-strong-passwords": "<p>主密码忘了等于密码库上锁，务必把恢复流程演练至少一次。</p>",
    "two-factor-authentication-guide": "<p>新买手机先迁移 2FA 再抹旧机，顺序反了可能在云端被锁在门外数小时。</p>",
    "what-is-https": "<p>上线站点部署 HSTS 可减少首访降级，但部署错误会把自己锁死，先在测试域验证。</p>",
    "prevent-personal-data-leaks": "<p>亲戚借身份证复印，当面勾画「仅用于某某用途」比事后追责更现实。</p>",
}

for slug, extra in TOPUP2.items():
    ARTICLES[slug]["content_html"] += extra

TOPUP3 = {
    "zero-trust-security": "<p>把默认共享关掉，是成本最低的起点。</p>",
    "identify-malicious-websites": "<p>陌生页要求拨号求助，一律挂断。</p>",
    "protect-digital-identity": "<p>年度体检报告照片别随手群发家庭群。</p>",
    "public-wifi-safety": "<p>电量低不是降低防护等级的理由。</p>",
    "what-is-end-to-end-encryption": "<p>群公告与正文加密等级可能并不一致。</p>",
    "browser-privacy-settings": "<p>默认搜索引擎也可换成隐私友好选项。</p>",
    "choose-privacy-tools": "<p>试用期内做一次 DNS 与 IP 预期对照即可验收。</p>",
    "common-cybersecurity-myths": "<p>季节更替时复查习惯清单比换新设备重要。</p>",
    "protect-online-privacy": "<p>相册隐藏文件夹不等于不上传云端。</p>",
    "identify-phishing-attacks": "<p>善待好奇：多点一次鼠标悬停检查无害。</p>",
    "create-strong-passwords": "<p>导出密码库前确认无人肩窥。</p>",
    "two-factor-authentication-guide": "<p>短信不到时先看手机信号与漫游状态。</p>",
    "prevent-personal-data-leaks": "<p>打印收据碎纸机与数字擦除同样重要。</p>",
}

for slug, extra in TOPUP3.items():
    ARTICLES[slug]["content_html"] += extra

TOPUP4 = {
    "protect-digital-identity": "<p>冒充客服让你「保持通话」时立即挂断并回拨官方号码核实身份。</p>",
    "browser-privacy-settings": "<p>卸载浏览器前导出书签与已保存密码，再执行卸载向导里的数据清除。</p>",
    "choose-privacy-tools": "<p>阅读更新日志可看出项目是活跃维护还是弃坑。</p>",
    "common-cybersecurity-myths": "<p>熟人的 U 盘也可能携带自动运行脚本，插入前先扫描。</p>",
    "protect-online-privacy": "<p>关闭个性化广告不等价于停止收集，只是少看推荐。</p>",
    "identify-phishing-attacks": "<p>伪造「公安」来电称你洗钱时，到就近派出所窗口当面核实。</p>",
    "two-factor-authentication-guide": "<p>把各平台恢复码汇总进加密笔记并打印密封袋，别散落在聊天置顶里。</p>",
    "prevent-personal-data-leaks": "<p>旧手机卡剪断后仍应向运营商销号，避免回收再分配引迎来路验证码。</p>",
}

for slug, extra in TOPUP4.items():
    ARTICLES[slug]["content_html"] += extra

TOPUP5 = {
    "choose-privacy-tools": "<p>比价三件事：管辖、日志、客户端签名。</p>",
    "common-cybersecurity-myths": "<p>遇到新问题回到清单核对即可。</p>",
    "prevent-personal-data-leaks": "<p>泄露通报邮件也要核对发件域名。</p>",
}

for slug, extra in TOPUP5.items():
    ARTICLES[slug]["content_html"] += extra

for slug, data in ARTICLES.items():
    md = data["meta_description"]
    if len(md) < 70:
        data["meta_description"] = md + "适合希望系统梳理概念并落实到日常配置的个人读者。"


def main() -> None:
    lengths: list[int] = []
    errors: list[str] = []
    for slug, data in ARTICLES.items():
        pl = len(plain(data["content_html"]))
        lengths.append(pl)
        if pl < 900 or pl > 1600:
            errors.append(f"{slug}: plain length {pl} out of 900-1600")
        md = data["meta_description"]
        if len(md) < 70 or len(md) > 140:
            errors.append(f"{slug}: meta length {len(md)} out of 70-140")
        for phrase in FORBIDDEN:
            if phrase in data["content_html"]:
                errors.append(f"{slug}: forbidden phrase {phrase}")
        if len(data["faq_json"]) != 3:
            errors.append(f"{slug}: faq count {len(data['faq_json'])}")
        if not (2 <= len(data["sources_json"]) <= 4):
            errors.append(f"{slug}: sources count {len(data['sources_json'])}")
        if data["content_html"].count("/articles/") < 2:
            errors.append(f"{slug}: fewer than 2 internal links")

    if errors:
        for e in errors:
            print(e)
        raise SystemExit(1)

    OUT.write_text(json.dumps(ARTICLES, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"slug count: {len(ARTICLES)}")
    print(f"min plain: {min(lengths)}")
    print(f"avg plain: {statistics.mean(lengths):.1f}")
    print(f"max plain: {max(lengths)}")


if __name__ == "__main__":
    main()
