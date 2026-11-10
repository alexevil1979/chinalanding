# -*- coding: utf-8 -*-
"""Generate tools/_phase4_other_key.json with validation."""
import json
import re
import html as html_mod
from pathlib import Path

FORBIDDEN = [
    "结合实际场景理解",
    "分层防护怎么做",
    "建议的复查频率",
    "可立即执行的下一步",
    "阅读官方文档的原因",
    "实践中的判断标准",
    "和家人或团队协作时",
    "延伸思考",
    "把知识用在下一次真实操作里",
    "把原则变成可检查的结果",
    "和商业工具的关系",
    "如果时间有限",
]

PLAIN_MIN, PLAIN_MAX = 1400, 2200
META_MIN, META_MAX = 70, 120

ALLOWED_TAGS = re.compile(r"</?(?!p\b|h2\b|h3\b|ul\b|ol\b|li\b|strong\b|a\b|code\b)[a-z][^>]*>", re.I)


def plain_len(content_html: str) -> int:
    text = re.sub(r"<[^>]+>", "", content_html)
    text = html_mod.unescape(text)
    return len(re.sub(r"\s+", "", text))


def check_forbidden(blob: str) -> list:
    return [p for p in FORBIDDEN if p in blob]


def count_internal_links(html: str) -> int:
    return len(re.findall(r'href="/articles/', html))


def validate_tags(html: str) -> str | None:
    if ALLOWED_TAGS.search(html):
        return "disallowed HTML tag"
    return None


data = {
    "what-is-vpn": {
        "seo_title": "什么是 VPN：隧道、加密、DNS 与威胁模型",
        "meta_description": "从隧道封装、加密完整性、DNS 路径、IP 路由与元数据边界解释 VPN 工作原理，说明服务商在出口解密中的角色及常见威胁模型下的适用与局限。",
        "content_html": r"""
<p>VPN（Virtual Private Network，虚拟专用网络）在操作系统层创建加密隧道，把选定的 IP 流量封装后发往远端节点，再由该节点代你访问互联网或内网资源。它主要改变<strong>网络路径与出口表现</strong>，既不自动等于匿名，也不能替代设备与账户层面的安全。</p>
<h2>隧道封装发生在哪一层</h2>
<p>与浏览器代理只影响单个应用不同，常见 VPN 客户端会安装虚拟网卡（TUN）或改写系统路由表，使匹配规则的数据包进入隧道。路径上的观察者通常能看到你与 VPN 服务器之间的 UDP/TCP 会话，却未必能直接读出内层访问的每一个目标 IP（仍可通过流量体积、时间等侧信道推断行为）。Cloudflare 在入门材料中把 VPN 描述为在不可信网络上扩展信任边界的手段，前提是你要信任隧道终点。</p>
<h2>加密与完整性保护什么</h2>
<p>现代协议（WireGuard、IPsec、OpenVPN、基于 TLS 的 SSL VPN 等）对隧道内载荷提供机密性与完整性，降低路径篡改风险。NIST SP 800-77 对 IPsec VPN 的部署要素有系统说明，可作为企业场景的参考框架。需要强调：<strong>加密发生在入隧之后</strong>；若终端已有键盘记录或恶意软件，数据可能在封装前就被读取。协议细节可读 <a href="/articles/what-is-wireguard">WireGuard</a>；分层概念见 <a href="/articles/network-traffic-encryption">网络流量加密</a>。</p>
<h2>DNS 为何常与 VPN 一起讨论</h2>
<p>访问网站前要先解析域名。若隧道已连接，但系统仍把 DNS 查询发往本地运营商解析器，就会出现「出口 IP 已变、查询仍在当地」的错位，即 DNS 泄露。可靠配置应在客户端或接口级指定隧道内 DNS，并在启用分流后核对预期行为。专题：<a href="/articles/what-is-dns-leak">什么是 DNS 泄露</a>。</p>
<h2>IP 路由：全隧道与分流</h2>
<p>连接成功后，默认路由或 <code>AllowedIPs</code> 一类前缀列表决定哪些流量进隧道。<strong>全隧道</strong>几乎把所有上网流量送到远端；<strong>分流（split tunneling）</strong>只加密办公网段或特定前缀，其余仍走本地网关。分流是策略选择，不是缺陷——但若你误以为「已全程保护」而实际直连，威胁模型就被打断。出口 IP 会变成服务商节点地址，网站风控据此看到的地理位置与未开隧道时不同。</p>
<h2>元数据不会随隧道消失</h2>
<p>即使载荷加密，你与 VPN 服务器之间的连接时长、上下行字节、握手重连频率仍可能被记录。VPN 不消除浏览器 Cookie、账号登录态、支付关联与设备指纹；它收缩的是<strong>本地网络到隧道入口</strong>这一段的暴露面。EFF 的自卫指南提醒：任何第三方隧道运营方在技术上都可能观察或记录会话特征。</p>
<h2>服务商角色与信任边界</h2>
<p>商业 VPN 在出口解密并替你向目标服务器转发连接。因此日志政策、司法辖区、客户端签名与供应链、是否接受独立审计，比「军事级加密」标语更能回答「你在信任谁」。自建 VPS 上跑 WireGuard 把信任收回到你自己，但运维、补丁与入侵响应责任也随之回到你手上。对比应用级路径见 <a href="/articles/vpn-vs-proxy">VPN 与代理</a>。</p>
<h2>威胁模型对照</h2>
<ul>
<li><strong>咖啡馆 Wi-Fi 旁路：</strong>可信隧道叠加 HTTPS，通常能抬高窃听成本。</li>
<li><strong>只想隐藏住宅 IP 做爬虫：</strong>可能触犯服务条款，且账号仍能把行为绑回你。</li>
<li><strong>钓鱼窃取密码：</strong>隧道不验证网页真伪，仍靠域名核对与双重验证。</li>
<li><strong>设备丢失：</strong>应靠全盘加密与锁屏，而非指望 VPN。</li>
</ul>
<h2>杀开关与双栈路由</h2>
<p>杀开关（kill switch）在隧道意外断开时阻断非 VPN 出口的流量，防止「以为仍受保护」的时刻把真实 IP 暴露给访问中的站点。实现方式因系统而异：有的由客户端注入防火墙规则，有的依赖操作系统的「仅 VPN 接口可上网」策略。IPv4 全隧道而 IPv6 仍走本地网关，是另一类经典绕行；排障时应在连接状态下同时检查两种协议的默认路由与 DNS 出口。</p>
<h2>配置与运维易错点</h2>
<ul>
<li>断线后未启用杀开关，流量静默回到默认网络。</li>
<li>IPv6 未入隧而 IPv4 已保护，形成绕行。</li>
<li>安装来源不明的客户端，供应链风险大于协议名称。</li>
<li>把「换出口 IP」等同于「网站认不出我」。</li>
</ul>
<p>企业远程接入常结合多因素认证与设备合规检查，那是身份层的补充，不能单靠隧道协议名称替代。个人选型应先弄清应用级代理与系统隧道的覆盖差异，再决定是否值得引入常驻隧道。</p>
""".strip(),
        "faq_json": [
            {"q": "VPN 能让我对网站完全匿名吗？", "a": "不能。它主要改变网络路径与出口 IP；账号、Cookie 与指纹仍可能识别你。"},
            {"q": "只用 HTTPS 还需要 VPN 吗？", "a": "取决于威胁。HTTPS 保护单站传输；VPN 改变系统级路径，二者目标不同，可叠加。"},
            {"q": "免费 VPN 是否一定更危险？", "a": "不一定，但需审视商业模式、客户端来源与历史事件；免费不等于恶意，也少见得可验证。"},
            {"q": "隧道断开后还会泄漏吗？", "a": "若未配置杀开关或防火墙规则，断线后流量可能走本地默认路由，应实测验证。"},
        ],
        "sources_json": [
            {"title": "Cloudflare Learning: What is a VPN?", "url": "https://www.cloudflare.com/learning/access-management/what-is-a-vpn/"},
            {"title": "NIST SP 800-77 Rev. 1 Guide to IPsec VPNs", "url": "https://csrc.nist.gov/pubs/sp/800/77/r1/final"},
            {"title": "OWASP Transport Layer Protection Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"},
            {"title": "EFF Surveillance Self-Defense", "url": "https://ssd.eff.org/"},
        ],
    },
    "what-is-dns-leak": {
        "seo_title": "什么是 DNS 泄露：成因、检测与 DoH/DoT 边界",
        "meta_description": "说明 VPN 下 DNS 查询仍走本地解析器的典型原因，如何区分意外泄露与预期分流，以及 DoH、DoT 在传输保护与解析策略一致性上的能力与局限。",
        "content_html": r"""
<p>DNS 泄露指：你已经启用 VPN 或以为查询会走受信路径，但域名解析仍经由本地网络、运营商解析器、路由器或浏览器内置解析通道完成，从而向非预期的观察者暴露<strong>你问了哪些域名</strong>。这与网页内容是否 HTTPS 无关——查询阶段的意图泄漏独立存在。</p>
<h2>DNS 在连接链条中的位置</h2>
<p>用户输入 <code>example.com</code> 后，系统或应用向递归解析器发起查询，获得 A/AAAA 记录，再向对应 IP 建立 TCP/TLS 连接。递归解析器天然能看到查询名；若查询未加密，同一局域网或上游网络也可能观察到。基础机制见 <a href="/articles/how-dns-servers-work">DNS 服务器如何工作</a>。</p>
<h2>VPN 场景为何高发</h2>
<p>隧道通常只保证<strong>进入隧道的 IP 包</strong>按新路径转发；DNS 是另一通道。常见成因包括：客户端未推送隧道 DNS；操作系统仍优先使用 DHCP 下发的解析器；浏览器单独启用 DoH 指向与 VPN 无关的服务商；分流规则让部分域名故意走直连，但你未意识到该域名落在直连列表。意外泄露与<strong>预期分流</strong>的区别在于行为是否符合你写下的策略，而不是「有没有本地解析」这一事实本身。</p>
<h2>Split tunnel 与 leak 的辨析</h2>
<p>企业 VPN 常让内网域名走本地解析、互联网域名走隧道——这是设计如此。家庭用户若希望「全部上网隐私一致」，却仅加密 HTTP 流量而 DNS 仍指向运营商，就属于配置错误。核对时应同时看 IP 出口、DNS 出口与分流表，而不是只看客户端显示「已连接」。相关：<a href="/articles/what-is-vpn">VPN 原理</a>。</p>
<h2>DoT 与 DoH 能缓解什么</h2>
<p>DNS over TLS（RFC 7858）与 DNS over HTTPS（RFC 8484）在传输层加密查询，降低路径窃听与篡改，并让客户端固定指向指定解析策略。但它们<strong>不自动</strong>把查询藏进 VPN 隧道：若 DoH 在浏览器层指向 Cloudflare，而网页流量走 VPN 出口，可能出现「IP 在德国、DNS 在美国」的刻意或无意组合。解析服务商仍能看到完整查询列表。Mozilla 文档对 Firefox 中 DoH 的行为与策略有说明。</p>
<h2>如何检测</h2>
<ul>
<li>连接 VPN 前后，使用你信任的检测页或自建脚本，对比显示的 DNS 与 IP 是否符合策略。</li>
<li>更换客户端版本、系统升级或安装新浏览器后复测；泄露状态不是一次通过就永久有效。</li>
<li>检查 IPv6：若仅 IPv4 入隧而 IPv6 仍直连，会形成绕过。</li>
<li>确认厂商文档中的「仅隧道 DNS」「阻止 LAN DNS」等选项是否按预期开启。</li>
</ul>
<h2>缓解思路</h2>
<ol>
<li>在 VPN 配置中指定隧道内 DNS，并验证查询出口与隧道一致。</li>
<li>在路由器或系统层统一加密 DNS，减少应用各自解析。</li>
<li>理解分流清单：预期直连的域名不应被误报为泄露。</li>
<li>高敏感场景叠加 HTTPS，并限制在不可信网络上进行账户关键操作。</li>
</ol>
<h2>WebRTC 与系统解析缓存</h2>
<p>部分浏览器在 WebRTC 场景下可能泄露本地接口或 STUN 探测结果，与 DNS 泄露并列是另一类「隧道已开但仍有侧信道」的问题。系统级 DNS 缓存与 <code>hosts</code> 文件也会让检测页结果与即时抓包不一致——改配置后重启解析服务或清缓存再测更可靠。分流清单若以域名后缀匹配，要确认通配规则没有把本应入隧的流量误送进直连解析器。</p>
<h2>仍无法指望 DNS 加密单独完成的事</h2>
<p>DoH/DoT 不隐藏你对解析运营商的查询内容；不替代 HTTPS 对页面正文的保护；也不阻止已登录账户在服务端记录行为。流量模式、SNI（视协议版本与部署而定）与 IP 地址仍是独立信号。</p>
<h2>运营商与本地网关能看见什么</h2>
<p>未入隧的明文 DNS 查询会经过本地路由器与运营商递归，常被用于 parental control、恶意域名拦截或合规审计。加密 DNS 把「谁能看到查询名」转移到你所选的解析商，而不是让查询从地球上消失。更换 VPN 国家后若忘记同步 DoH 配置，检测页仍可能显示与出口国家不一致的解析位置——这正是许多用户误以为「VPN 坏了」的实际原因。</p>
<p>排障顺序建议：先确认 <a href="/articles/what-is-vpn">VPN</a> 路由与杀开关，再核对加密 DNS 策略，最后用 HTTPS 站点验证内容层是否独立正常。</p>
""".strip(),
        "faq_json": [
            {"q": "用了 VPN 就一定没有 DNS 泄露？", "a": "不一定。取决于客户端是否强制隧道 DNS，以及系统或浏览器是否另有解析路径。"},
            {"q": "加密 DNS 能隐藏网页内容吗？", "a": "不能。它主要保护查询通道；页面内容仍靠 HTTPS 等机制。"},
            {"q": "分流下本地解析算泄露吗？", "a": "若域名按策略应直连，本地解析可能是预期行为；意外绕行才是泄露。"},
            {"q": "IPv6 会导致泄露吗？", "a": "若隧道未处理 IPv6 而系统仍走 IPv6 直连，可能绕过预期路径，应确认双栈策略。"},
        ],
        "sources_json": [
            {"title": "Cloudflare Learning: What is DNS?", "url": "https://www.cloudflare.com/learning/dns/what-is-dns/"},
            {"title": "RFC 8484 DNS over HTTPS", "url": "https://www.rfc-editor.org/rfc/rfc8484"},
            {"title": "RFC 7858 DNS over TLS", "url": "https://www.rfc-editor.org/rfc/rfc7858"},
            {"title": "Mozilla: DNS over HTTPS in Firefox", "url": "https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Privacy/DNS_over_HTTPS"},
        ],
    },
    "what-is-https": {
        "seo_title": "什么是 HTTPS：TLS、证书与它不能证明的事",
        "meta_description": "解释 HTTPS 中 TLS 握手、证书链验证如何保护传输机密性与完整性，厘清小锁图标与域名匹配的含义，并说明其无法证明经营者诚信或隐藏 DNS 查询。",
        "content_html": r"""
<p>HTTPS 是在 HTTP 之上运行 TLS（Transport Layer Security）的结果：浏览器与服务器先完成握手与证书验证，再加密传输网页、表单与 API 数据。MDN 将其概括为 HTTP 的安全版本，核心收益是<strong>防路径窃听与篡改</strong>，并在验证成功时确认你连接的是证书所绑定的那个域名。</p>
<h2>TLS 握手在做什么</h2>
<p>典型流程包括：客户端宣告支持的协议版本与密码套件；服务器出示证书链；客户端验证链是否通向受信根证书，并检查证书中的域名是否与地址栏一致；双方协商对称会话密钥，后续数据用 AEAD 等方式加密。TLS 1.3（RFC 8446）缩短了握手往返，并移除了 numerous 不安全选项。NIST SP 800-52 对政府系统应如何配置 TLS 有持续更新的建议。</p>
<h2>证书证明了什么</h2>
<p>公有 CA 签发证书的意义是：某个实体控制了证书 SAN/CN 所列域名，且域名验证通过。验证通过意味着<strong>加密通道通向该域名</strong>，而不是「该域名一定属于你的银行」。钓鱼站只要控制形似真品牌的域名，同样可以获得有效证书。OWASP 传输层备忘强调：TLS 是机密性与完整性控制，不是业务可信印章。</p>
<h2>证书警告必须严肃对待</h2>
<p>名称不匹配、链不完整、过期或遭到中间人替换时，浏览器会阻断或警告。此时继续访问等于自愿接受未知证书，输入的密码与付款信息可能流向攻击者。企业内网若部署私有 CA，员工终端需显式信任该根——这与公网 PKIX 是不同信任模型。仿冒站往往复制视觉样式却改域名一字，识别应优先核对地址栏。</p>
<h2>HTTPS 保护与不保护的边界</h2>
<ul>
<li><strong>保护：</strong>路径上第三方难以读取或篡改 HTTP 内容与多数 Cookie（在 <code>Secure</code> 等属性配置正确时）。</li>
<li><strong>不保护：</strong>服务器侧明文处理、日志、执法合规请求；你在假站亲手输入的数据。</li>
<li><strong>不替代：</strong>终端恶意软件、钓鱼话术、弱口令。</li>
<li><strong>不隐藏：</strong>DNS 查询记录、服务器看到的来源 IP、访问时间与 URL 路径（在服务端日志中）。</li>
</ul>
<h2>与 VPN、E2EE 的关系</h2>
<p>HTTPS 保护<strong>浏览器到网站</strong>这一段；VPN 封装<strong>系统级 IP 流量</strong>到隧道终点；端到端加密则让服务端无法读取消息正文。三者可叠加但边界不同。分层说明：<a href="/articles/network-traffic-encryption">网络流量加密</a>。</p>
<h2>混合内容与 HSTS</h2>
<p>HTTPS 页面若加载 HTTP 子资源，可能触发混合内容阻断或削弱保护。HSTS 响应头指示浏览器在期限内仅通过 HTTPS 访问站点，可降低 sslstrip 类降级风险，但部署错误可能把自己锁死在错误配置里，应在测试域验证后再上生产。HTTP/2 与 HTTP/3 在 TLS 之上复用连接，减少握手次数，对移动网络高丢包环境尤为明显。</p>
<h2>OCSP 与证书透明度</h2>
<p>浏览器依赖证书吊销状态与证书透明度（Certificate Transparency）日志来发现异常签发。普通用户不必手工查 CT，但应知道：**证书有效**只回答密码学链路与域名绑定，不回答站点经营者是谁。企业透明代理在受管设备安装根证书后，小锁依旧可见，但解密点可能在公司网关——办公笔记本与个人网银分设备登录是更稳妥的分工。</p>
<h2>公共网络上的用法</h2>
<p>在不可信 Wi‑Fi 上，HTTPS 是浏览与登录的底线；仍需核对域名、警惕门户页伪造证书。DNS 路径问题见 <a href="/articles/what-is-dns-leak">DNS 泄露</a>；需要系统级路径加固时可理解 <a href="/articles/what-is-vpn">VPN</a> 的附加作用。</p>
<h2>Cookie 与安全属性</h2>
<p>站点可为 Cookie 设置 <code>Secure</code>、<code>HttpOnly</code> 与 <code>SameSite</code>，减少在非 HTTPS 环境被劫持或跨站滥用的概率。这些标志由服务器下发，浏览器强制执行；用户无法单靠「感觉安全」弥补缺失的配置。登录态一旦建立，服务端仍可按策略记录活动，与 TLS 是否存在无矛盾。</p>
""".strip(),
        "faq_json": [
            {"q": "地址栏小锁说明一定是官网吗？", "a": "不能。小锁表示与当前域名的 TLS 会话有效，不验证品牌归属或页面无欺诈。"},
            {"q": "自签名证书可以日常浏览吗？", "a": "仅限你明确信任的内网或测试环境；公网站点应使用受信 CA，否则应出现警告。"},
            {"q": "HTTPS 会让网站变慢吗？", "a": "现代硬件与 HTTP/2、HTTP/3 下开销很小，安全收益通常远大于延迟成本。"},
            {"q": "有了 HTTPS 还需要注意 DNS 吗？", "a": "需要。TLS 不加密 DNS 查询，解析路径仍是独立暴露面。"},
        ],
        "sources_json": [
            {"title": "MDN: HTTPS", "url": "https://developer.mozilla.org/en-US/docs/Glossary/HTTPS"},
            {"title": "Cloudflare Learning: What is HTTPS?", "url": "https://www.cloudflare.com/learning/ssl/what-is-https/"},
            {"title": "RFC 8446 TLS 1.3", "url": "https://www.rfc-editor.org/rfc/rfc8446"},
            {"title": "NIST SP 800-52 Rev. 2 TLS Guidelines", "url": "https://csrc.nist.gov/pubs/sp/800/52/r2/final"},
            {"title": "OWASP Transport Layer Protection Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"},
        ],
    },
    "what-is-end-to-end-encryption": {
        "seo_title": "什么是端到端加密：与 TLS 的差异与边界",
        "meta_description": "说明端到端加密如何让服务方无法读取消息正文，对比 TLS 仅保护传输的特点，并澄清元数据残留、终端被控、多设备同步与云备份通道上的残余风险。",
        "content_html": r"""
<p>端到端加密（End-to-End Encryption，E2EE）指内容在发送方设备上加密，仅在接收方设备上解密，通信服务商在协议设计上无法获取明文。Cloudflare 将其与「仅传输加密」区分：后者常在服务器端终止 TLS 后看到明文。E2EE 解决的是<strong>服务端读取内容</strong>的问题，不是「通信从未发生」的隐身。</p>
<h2>与 HTTPS/TLS 的关键差异</h2>
<p>访问 HTTPS 网站时，TLS 保护浏览器到服务器链路；服务器必须能解密 HTTP 才能生成页面、做搜索索引或反垃圾。即时通讯、部分邮件与文件同步产品则把长期密钥材料放在用户设备上，服务器转发密文包。实践里常见<strong>双层</strong>：消息体 E2EE，外层仍用 TLS 送到服务器。理解分层有助于避免把「小锁网页」误当成「运营商读不懂聊天」。详见 <a href="/articles/what-is-https">HTTPS</a> 与 <a href="/articles/network-traffic-encryption">网络流量加密</a>。</p>
<h2>密钥、身份与核对</h2>
<p>成熟 E2EE 设计提供安全码或指纹比对，用于发现中间人替换密钥。多设备登录要在新设备上安全分发或派生会话密钥；设备丢失后的远程注销与密钥轮换策略，直接决定「端到端」是否在你失机瞬间失效。NIST 密码学专题强调密钥生命周期管理，与算法选型同等重要。</p>
<h2>元数据仍然泄漏什么</h2>
<p>即使正文不可读，服务侧常仍掌握账号标识、对话双方关系、时间戳、消息长度或频率、设备类型等元数据。流量分析在国家级对手面前仍可绘制社交图。E2EE 不消除「谁在和谁说话」这一层面的观察，只是把<strong>说了什么</strong>从运营方视野里拿走（在实现正确、未被后门的前提下）。</p>
<h2>端点与人为因素</h2>
<p>屏幕偷拍、被胁迫解锁、终端木马、备份到未 E2EE 的云盘，都会在加密之外开辟泄密口。对方设备若失陷，你发给对方的明文仍会被读取。EFF 在「与他人通信」模块提醒：密码学保护假设端点是诚实且未被入侵的。</p>
<h2>备份与多设备陷阱</h2>
<p>许多产品提供「云端聊天备份」以换机恢复。若备份未同样端到端加密，或备份密钥由厂商托管，则<strong>历史消息</strong>可能在服务器上恢复为明文。选购前应阅读白皮书：默认是否 E2EE、备份密钥是否只存在于你的设备、关闭 E2EE 是否影响功能。</p>
<h2>如何阅读产品声明</h2>
<ul>
<li>默认开启还是可选？关闭后能否发现？</li>
<li>群组、通话、文件是否同一加密模型？</li>
<li>是否有独立审计或开源客户端可复现构建？</li>
<li>元数据保留多久、能否被执法请求？</li>
</ul>
<p>工具评估维度见 <a href="/articles/choose-privacy-tools">如何选择隐私工具</a>。</p>
<h2>法定访问与产品架构</h2>
<p>各国法律可能要求服务商配合元数据或特定内容的披露；E2EE 产品的架构选择（客户端加密、密钥托管方式）决定了执法请求能否在技术上落实。Signal、WhatsApp 等公开材料对这一问题有不同程度的说明，选购前应阅读其透明度报告，而不是只看广告里的「无法破解」。</p>
<h2>群组与通话是否同一模型</h2>
<p>群聊密钥轮换、语音视频通话的密钥协商路径，可能与文字消息不同步升级。产品更新日志若仅写「聊天 E2EE」却未提群语音，值得向支持团队索要技术说明。联邦互通协议还会在信任锚上引入第三方服务器，安全码核对范围也随之扩大。</p>
<h2>转发截图与通知预览</h2>
<p>消息在端上解密后，通知栏预览、最近任务切换器缩略图、云相册里的聊天截图，都会把 E2EE 的保护面打穿到物理世界。关闭敏感会话的通知预览、对屏幕共享设黑名单，与启用 E2EE 同样属于日常配置。企业监管手机若强制备份到 MDM，也要确认备份链是否仍满足你个人的保密预期。</p>
<h2>E2EE 不直接防御的攻击</h2>
<p>钓鱼骗取验证码、假冒客服索要恢复码、在假登录页输入密码——这些攻击发生在 E2EE 通道之外。账户加固仍依赖强口令、双重验证与防钓鱼习惯。</p>
<p>读毕本篇后，可把加密通讯与网页浏览的威胁分开记录：聊天 App 对照 E2EE 白皮书，网站登录对照 HTTPS 与域名核对，避免用单一工具名覆盖全部场景。</p>
""".strip(),
        "faq_json": [
            {"q": "有 E2EE 运营方就完全看不到任何信息吗？", "a": "通常仍处理元数据与账号数据；具体范围取决于产品与管辖法律，应阅读官方安全文档。"},
            {"q": "为什么还要核对安全码？", "a": "用于发现密钥被中间人替换，尤其在首次通信或联系人密钥变更后。"},
            {"q": "E2EE 能防止钓鱼吗？", "a": "不能。钓鱼发生在浏览器或人为受骗层面，需核对入口与域名。"},
            {"q": "云备份开启后 E2EE 还有效吗？", "a": "取决于备份是否同样端到端加密；厂商托管备份密钥会改变威胁模型。"},
        ],
        "sources_json": [
            {"title": "Cloudflare: What is end-to-end encryption?", "url": "https://www.cloudflare.com/learning/privacy/what-is-end-to-end-encryption/"},
            {"title": "EFF SSD: Communicating with Others", "url": "https://ssd.eff.org/module/communicating-others"},
            {"title": "NIST Cryptography Resource Center", "url": "https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines"},
            {"title": "MDN: Web Security", "url": "https://developer.mozilla.org/en-US/docs/Web/Security"},
        ],
    },
    "choose-privacy-tools": {
        "seo_title": "如何选择隐私保护工具：评估清单与红旗",
        "meta_description": "从威胁模型、透明度、独立审计与开源可验证性、权限索取、商业模式与退出成本等维度评估 VPN、密码管理器与加密通讯工具，并列举常见夸张营销红旗话术。",
        "content_html": r"""
<p>隐私工具宣传常把复杂威胁简化成一句 slogan。可靠选型先写清<strong>你要防什么、覆盖哪些设备、能接受怎样的代价</strong>，再用可核对的事实筛选产品，而不是背排行榜。EFF 自卫指南强调：没有万能工具，只有与威胁模型匹配的组合。</p>
<h2>第一步：威胁与范围</h2>
<ul>
<li>对抗对象：同 Wi‑Fi 旁听、商业跨站追踪、账户撞库、设备丢失，还是针对性监视？</li>
<li>覆盖范围：仅浏览器、全系手机应用，还是包含路由器与 NAS？</li>
<li>预算与维护：能否持续付费、能否接受手动配置与排障？</li>
</ul>
<h2>评估清单（可按表打分）</h2>
<ol>
<li><strong>透明度：</strong>公司主体、隐私政策是否与功能一致，安全事件是否有公开说明。</li>
<li><strong>可验证性：</strong>核心是否开源、是否有独立审计或可复现构建；开源不等于无洞，但提高审查可能。</li>
<li><strong>权限最小化：</strong>是否索取短信、通讯录、无障碍等与宣称功能无关的权限。</li>
<li><strong>维护状态：</strong>近两年是否有安全更新；弃坑产品仍是攻击面。</li>
<li><strong>退出成本：</strong>能否导出数据、注销账户、卸载后无残留驱动。</li>
</ol>
<h2>按品类要问的问题</h2>
<p><strong>VPN/隧道：</strong>日志与元数据政策、司法辖区、杀开关与 DNS 行为、协议是否可核验（如 WireGuard 开源实现）。读本专题 <a href="/articles/what-is-vpn">VPN 原理</a> 后再挑供应商。</p>
<p><strong>密码管理器：</strong>主密码与 2FA、紧急访问、 breach 监测；主密码泄露等于库全失。</p>
<p><strong>浏览器与扩展：</strong>每个扩展的权限是否过大；追踪防护是否与登录策略冲突，应单独核对扩展清单。</p>
<p><strong>即时通讯：</strong>是否默认 <a href="/articles/what-is-end-to-end-encryption">端到端加密</a>，元数据如何处理。</p>
<h2>红旗信号</h2>
<ul>
<li>「绝对匿名」「军方级」「执法无法获取」等不可证伪承诺。</li>
<li>要求关闭系统防火墙、杀软或开发者模式才能安装。</li>
<li>只有应用商店刷单好评，没有技术白皮书或漏洞响应渠道。</li>
<li>订阅页面强调「限时终身」却看不清公司注册信息。</li>
<li>安装包来源非官网，且无法校验签名或哈希。</li>
</ul>
<h2>试用期如何验收</h2>
<p>在非核心设备上试用：观察 DNS 与 IP 出口是否符合预期、卸载是否干净、是否干扰系统 VPN 配置。试用期结束前决定续费，比自动扣款后才发现不兼容更省事。商业链接若出现在本站文章，会单独标注赞助关系。</p>
<h2>叠罗汉误区</h2>
<p>同时堆叠多个同类 VPN、代理或「隐私浏览器」，很少线性提升安全，却显著增加故障与指纹面。应先确保 HTTPS、唯一口令、2FA 与系统更新等底座，再按缺口加一层。流量分层理解：<a href="/articles/network-traffic-encryption">网络流量加密</a>。</p>
<h2>文档与支持的含金量</h2>
<p>正规厂商会公开漏洞披露流程、CVE 修复节奏与最低支持系统版本；只会在短视频里演示「一键连接」却找不到安全白皮书的应用，很难支撑长期威胁模型。把隐私政策里「与关联方共享」一节读完，常比看五星评价更能筛掉不合适的默认同步行为。</p>
<h2>支付痕迹与账户隔离</h2>
<p>用主信用卡订阅「隐私」服务，会在账单与发卡行侧留下稳定关联。这不等于不能用，但应在威胁模型里显式标注。为工具单独注册邮箱、避免与真实姓名强绑定社交媒体同一登录，可降低一次泄露把生活全貌串起来的概率。</p>
<h2>默认配置比宣传语重要</h2>
<p>许多浏览器追踪防护、VPN 分流、加密聊天都依赖默认开关。安装后应逐项打开设置页核对，而不是假设「装好等于安全」。厂商更新若把某隐私选项改为 opt-out，Release note 里往往只有一句话，订阅官方安全公告比刷短视频测评更可靠。</p>
<p>把最终候选名单控制在三五款以内，每款写一句「它替我防什么、我信任谁」，比收藏几十个下载链接更容易坚持长期维护。评测视频可用来发现候选，但不应替代你亲自阅读权限弹窗与卸载结果。</p>
<p>若某工具唯一卖点是「比别的都快」，却回避日志与权限问题，通常不适合承担枢纽账户或全盘流量保护这类高价值任务。真正值得长期留下的，往往文档枯燥却可核对。</p>
""".strip(),
        "faq_json": [
            {"q": "开源工具是否一定更安全？", "a": "不一定，但更易审计。仍要看维护、默认配置与供应链。"},
            {"q": "付费是否等于无日志 VPN？", "a": "不等于。应阅读政策、审计与历史案件，而不是价格标签。"},
            {"q": "需要安装很多隐私扩展吗？", "a": "通常不需要。过多扩展增大指纹面与崩溃概率，按场景精选即可。"},
            {"q": "免费 VPN 能否长期使用？", "a": "视商业模式而定；若靠出售数据盈利，与隐私目标可能冲突，应核实条款。"},
        ],
        "sources_json": [
            {"title": "EFF Surveillance Self-Defense", "url": "https://ssd.eff.org/"},
            {"title": "OWASP Secure Product Design Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html"},
            {"title": "Mozilla Privacy & Security", "url": "https://www.mozilla.org/en-US/privacy/"},
            {"title": "NIST Cybersecurity Framework", "url": "https://www.nist.gov/cyberframework"},
        ],
    },
    "what-is-ip-address": {
        "seo_title": "什么是 IP 地址：公网、私网与隐私工具的关系",
        "meta_description": "解释 IPv4 与 IPv6 地址在路由投递中的作用，区分公网出口与内网私网地址，说明 IP 在网站日志与风控中的含义，及其与 DNS 查询和账号标识的差异。",
        "content_html": r"""
<p>IP 地址是网络层用于寻址与投递数据包的标识。没有它，服务器无法把响应发回你的设备。日常语境里混用「IP」时，多在谈论<strong>公网出口地址</strong>——网站日志里看到的那一个，而不是手机在卧室 Wi‑Fi 里的内网编号。</p>
<h2>IPv4、IPv6 与格式</h2>
<p>IPv4 常写作点分四组（如 203.0.113.5，RFC 791）；地址空间枯竭推动了 IPv6 的更长十六进制表示。多数家庭宽带同时运行双栈，具体哪条协议先连上取决于应用、操作系统与网络配置。Cloudflare 入门材料用「邮件地址类比 IP」帮助理解其路由作用，但 IP 会随网络环境变化，并不是终身身份号。</p>
<h2>公网地址与私网地址</h2>
<p>RFC 1918 规定的 10.0.0.0/8、172.16.0.0/12、192.168.0.0/16 等<strong>私网段</strong>只在局域网内有效。路由器通过 NAT 让多台内网设备共享一个公网出口。因此电商后台看到的往往是「整户宽带」的 IP，无法直接对应到某一盏台灯。企业专线可能拥有固定公网 IP，家庭宽带多为运营商动态分配，重启光猫可能换号。</p>
<h2>IP 能说明什么、不能说明什么</h2>
<p>GeoIP 数据库常给出城市级或运营商级位置，误差与滞后普遍存在，不足以单独作为司法定位依据。风控系统把 IP 当作信号之一：异常地理位置、数据中心 IP、与历史行为不符的批量登录等会抬高风险分。但 IP 本身<strong>不承载</strong>你的真实姓名，也不等于设备已被入侵——攻击者仍需开放服务、漏洞或凭据才能进一步行动。</p>
<h2>与 DNS、HTTP 日志的分工</h2>
<p>访问站点时，服务器通常记录来源 IP、时间、请求路径与用户代理；DNS 查询发生在连接之前，由解析器掌握域名列表。三者互为补充：换掉 IP 不抹去 DNS 记录，更不抹去账号 Cookie。参见 <a href="/articles/how-dns-servers-work">DNS 工作机制</a> 与 <a href="/articles/what-is-dns-leak">DNS 泄露</a>。</p>
<h2>隐私工具如何改变 IP 表现</h2>
<p><a href="/articles/what-is-vpn">VPN</a> 或代理让远端服务器看到隧道出口 IP，而非你家宽带地址。这能改变部分地理风控结果，却不能阻止已登录账户关联行为。Tor 等多跳方案进一步隐藏起点，但性能与可用性代价更高，且仍可能面临端点与人为风险。应用级代理与系统隧道的信任边界不同，选型前应先弄清覆盖范围。</p>
<h2>动态 IP、CGNAT 与「别人背锅」</h2>
<p>运营商级 NAT（CGNAT）让多户共享少量公网 IP，某 IP 上的不良历史可能影响邻居的验证码通过率。动态租约到期换号后，「异地登录提醒」可能误报——理解机制可减少不必要的恐慌，同时仍应核实是否真有你未授权的会话。</p>
<h2>自我保护的不迷信 IP</h2>
<h2>任播、CDN 与日志保留</h2>
<p>大型站点前面常有 CDN 任播入口，封禁单个 IP 往往只影响边缘节点而非整站。网站对源 IP 的日志保留周期因产品与法律而异：有些几周后即聚合，有些为风控长期存档。你以访客身份无法控制对方的留存策略，只能减少在高风险站点留下可关联的身份线索。</p>
<h2>自我保护的不迷信 IP</h2>
<p>公开论坛发帖、游戏语音、P2P 下载都可能暴露当时 IP；但这与是否使用 HTTPS 无直接关系。减少关联靠的是账号隔离、最小化公开信息与正确的传输加密，而不是迷信「隐藏 IP 就隐身」。</p>
<h2>威胁情报与误封</h2>
<p>数据中心 IP、已知代理段与僵尸网络曾用过的地址，会进入共享威胁情报库。你可能只因邻居滥用而触发验证码变难，更换出口并不总是解药。向服务商礼貌申诉时，附上时间线与账号信誉，比反复注册小号更能恢复访问。</p>
<h2>NAT 与端口映射</h2>
<p>家庭网关做源 NAT 时，外站只能看到共享出口，无法区分是客厅电视还是书房 PC 发起的连接。开启 UPnP 或手工映射端口，会在公网暴露具体内网服务，日志里的 IP 仍是出口地址，但附带的端口号指示了背后哪项服务。关闭不必要的映射，比频繁换 IP 更能减少被扫描命中。</p>
""".strip(),
        "faq_json": [
            {"q": "别人知道我的 IP 能直接控制电脑吗？", "a": "不能仅凭 IP。通常还需要开放端口、未修补漏洞或弱口令等条件。"},
            {"q": "IPv6 会让每台设备都有全球地址吗？", "a": "取决于路由与防火墙配置；多数家庭仍以路由器前缀隔离内网。"},
            {"q": "查 IP 网站显示的城市不准？", "a": "常见。数据库更新滞后，只能作粗略参考。"},
            {"q": "开 VPN 后网站还能看到别的标识吗？", "a": "能。Cookie、账号、浏览器指纹等仍可能识别你。"},
        ],
        "sources_json": [
            {"title": "Cloudflare: What is an IP address?", "url": "https://www.cloudflare.com/learning/network-layer/what-is-an-ip-address/"},
            {"title": "RFC 791 Internet Protocol", "url": "https://www.rfc-editor.org/rfc/rfc791"},
            {"title": "RFC 1918 Address Allocation for Private Internets", "url": "https://www.rfc-editor.org/rfc/rfc1918"},
            {"title": "MDN Glossary: IP Address", "url": "https://developer.mozilla.org/en-US/docs/Glossary/IP_Address"},
        ],
    },
    "network-traffic-encryption": {
        "seo_title": "什么是网络流量加密：分层、TLS 与元数据",
        "meta_description": "对比 HTTPS 应用层会话、VPN 网络隧道与磁盘静态加密的保护范围，说明加密后仍可能泄漏的时间、体积、DNS 与 SNI 等元数据，并强调端点安全仍不可或缺。",
        "content_html": r"""
<p>「流量已加密」在新闻稿里出现频率极高，却极少说明<strong>哪一段</strong>对谁加密。网络流量加密是一族技术的总称：TLS 保护单次 Web 会话，VPN 封装 IP 包路径，磁盘加密保护静止数据，端到端加密限制服务端读聊天正文。混淆层次会导致误判风险，例如以为开了 VPN 就不必看证书警告。</p>
<h2>TLS / HTTPS：应用会话层</h2>
<p>浏览器与 origin 服务器之间的 TLS 保护 HTTP 内容与大部分 Cookie 属性（配置得当时）。证书验证成功表示你正在与证书所列域名协商密钥，不表示经营者诚实。TLS 1.3 减少握手延迟并禁用大量弱套件（RFC 8446）。应用层细节见专题 <a href="/articles/what-is-https">HTTPS</a>；OWASP 传输层备忘列出部署常见坑。</p>
<h2>VPN 隧道：网络路径层</h2>
<p>隧道客户端把多个应用的 IP 包封装进加密外壳，发往远端解封后再投递。它改变出口 IP 与本地到隧道入口的路径暴露，但<strong>隧道运营商</strong>在出口通常能看到你要连接的目标 IP 或域名（除非你再套一层应用加密）。常见实现包括 WireGuard 与 IPsec；概念总览：<a href="/articles/what-is-vpn">VPN</a>。</p>
<h2>端到端与静态加密：不同威胁</h2>
<p>E2EE 针对「服务商不应读内容」；全盘加密针对「设备丢失后硬盘不可读」。BitLocker、FileVault 与 LUKS 保护静止介质；TLS 与 VPN 保护在途数据包。二者都不替代补丁管理与权限控制。参见 <a href="/articles/what-is-end-to-end-encryption">端到端加密</a>。</p>
<h2>协议版本与降级</h2>
<p>客户端与服务器协商 TLS 版本与密码套件；老旧系统若被迫降到弱协议，中间人攻击面会扩大。保持操作系统与浏览器更新，是让栈自动禁用 TLS 1.0/1.1 的最低成本做法。IPsec 与 WireGuard 等隧道有各自的算法固定策略，部署文档应写明允许套件。</p>
<h2>载荷加密 vs 元数据</h2>
<p>即使密文不可读，观察者仍可能看到：</p>
<ul>
<li>连接开始与结束时间、字节数、包间隔（流量分析）。</li>
<li>DNS 查询域名（若查询路径未加密或解析商记录）。</li>
<li>TLS 握手中的 SNI、ALPN 等字段（视版本与 ECH 部署而定）。</li>
<li>账号登录后，服务端侧的会话与行为日志。</li>
</ul>
<p>DNS 专题：<a href="/articles/what-is-dns-leak">DNS 泄露</a>。NIST 与业界文档常把「机密性」与「可观察性降低」分开讨论——加密主要提供前者。</p>
<h2>端点仍是软肋</h2>
<p>恶意软件在加密前截获按键、企业透明代理在受管设备安装根证书后终止 TLS、用户在假 HTTPS 页输入密码——都属于端点或人为失效。传输加密不能替代防钓鱼、2FA 与系统更新。CISA 基础实践把补丁与备份与加密并列为最低成本防线之一。</p>
<h2>如何快速自检</h2>
<ol>
<li>敏感站点证书是否匹配域名、无持续警告？</li>
<li>VPN 连接后 IP 与 DNS 出口是否符合策略？</li>
<li>丢失设备时磁盘加密是否已开启、恢复密钥是否离线保存？</li>
<li>高价值通讯是否默认 E2EE 且备份路径同样受保护？</li>
</ol>
<h2>组合而非替代</h2>
<p>公共 Wi‑Fi 浏览：HTTPS 为底线，可信 VPN 为增强。远程办公：公司批准隧道加分区策略。隐私画像：还要处理 Cookie 与账号登录态。避免用一层加密掩盖另一层的缺口，应按缺口逐层补齐而非盲目叠装。</p>
<h2>邮件与旧协议</h2>
<p>SMTP、IMAP 在传统部署中可能长期未强制 STARTTLS，密码与邮件正文会在路径上以明文或弱保护形式出现。现代客户端与服务商多默认强制 TLS，但企业自建邮局仍要逐项核对。与 Web 会话相比，邮件链路跨多个 MTA，每一段都需单独评估，而不能用「网页能打开」类推「全程安全」。</p>
<p>自查时按数据流画一条线：从输入法到磁盘、再到网卡，标出每一跳是谁加密、谁可见明文。图解不必专业，但能迅速暴露「以为全加密、实则只有浏览器到 CDN」的缺口。</p>
<p>同一 Wi‑Fi 下，家人设备未加密备份到同一云账户，也会让你的磁盘加密与 TLS 努力在「家庭共享」处被打穿，应在加密分层图里单独标出。</p>
""".strip(),
        "faq_json": [
            {"q": "VPN 与 HTTPS 可以同时使用吗？", "a": "可以。它们保护不同阶段，常可叠加，但各有边界与信任假设。"},
            {"q": "加密后为何仍可能被推断访问对象？", "a": "DNS、流量模式、SNI 与账号行为等元数据或上层标识仍可能存在。"},
            {"q": "企业能看到我 HTTPS 网页内容吗？", "a": "若设备安装了公司根证书做 HTTPS 检查，公司代理可能在终端看到解密后内容；属明示策略时需知情。"},
            {"q": "全盘加密保护网络传输吗？", "a": "不保护。它针对设备丢失时的静态数据；传输仍需 TLS 或隧道。"},
        ],
        "sources_json": [
            {"title": "MDN: Transport Layer Security", "url": "https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security"},
            {"title": "Cloudflare Learning: What is encryption?", "url": "https://www.cloudflare.com/learning/ssl/what-is-encryption/"},
            {"title": "OWASP Transport Layer Protection Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"},
            {"title": "NIST SP 800-52 Rev. 2", "url": "https://csrc.nist.gov/pubs/sp/800/52/r2/final"},
        ],
    },
    "zero-trust-security": {
        "seo_title": "什么是零信任安全：个人可落地的原则",
        "meta_description": "用非厂商推销视角解释零信任「永不默认信任、持续验证」的核心假设，说明最小权限、设备状态核对与网络分段在家庭路由、云盘与协作账户上的可落地做法。",
        "content_html": r"""
<p>零信任（Zero Trust）不是某个防火墙 SKU 的别名，而是一组架构原则：无论流量来自公司园区网还是家庭宽带，都<strong>不默认信任</strong>，每次访问都应基于身份、设备状态与上下文重新评估。NIST SP 800-207 将其定义为持续验证、最小权限与假设违规已发生。对个人读者而言，重点是把口号翻译成可日常执行的习惯，而不是采购一整条产品线。</p>
<h2>打破的旧假设</h2>
<p>传统模型常说「内网＝安全区」，连上 VPN 即可横向浏览全网。远程办公与云 SaaS 普及后，攻击者一旦窃取笔记本会话，就能在内网横移。零信任反过来问：这名用户、这台设备、此刻的风险信号，是否足以访问<strong>这一条</strong>资源？CISA 零信任成熟度模型描述企业演进阶段，个人可借用其中的「身份」「设备」「网络」三分法整理自家配置。</p>
<h2>核心做法（翻译成人话）</h2>
<ul>
<li><strong>持续验证：</strong>敏感操作前再次确认——而不只是早上登录一次整天畅通。</li>
<li><strong>最小权限：</strong>网盘链接默认非公开；协作文档限编辑者名单；IoT 摄像头不能访问 NAS 共享。</li>
<li><strong>微分段：</strong>访客 Wi‑Fi、智能家电与办公电脑分 SSID 或 VLAN，减少一台中招全盘沦陷。</li>
<li><strong>上下文：</strong>新设备登录邮件账户时，旧设备应收到提醒并可一键下线。</li>
</ul>
<h2>个人场景举例</h2>
<p>家中：路由器为 IoT 开隔离网段，更改默认口令并关闭 WAN 侧管理页面。账户：邮箱与支付启用最强 2FA，普通论坛使用独立口令。分享：发给外包的设计链接设七天过期，而不是「知道链接的人永久可改」。公共网络：高敏事务改用蜂窝；<a href="/articles/what-is-vpn">VPN</a> 只加固路径层，不替代身份核对。</p>
<h2>不是什么</h2>
<p>零信任并不意味着每个网页刷新都弹 MFA——而是把高强度验证用在高价值资产上。也不是「零信任」标签贴在旧 VPN 上就等于转型完成；策略不清时，客户端只会带来更多弹窗却不减少越权。Cloudflare 学习中心的概述强调：理念重于单品。</p>
<h2>与加密分层的关系</h2>
<p>传输层加密（<a href="/articles/network-traffic-encryption">流量加密</a>、<a href="/articles/what-is-https">HTTPS</a>）保护链路；零信任管的是<strong>谁有资格在链路之上访问哪份资源</strong>。二者互补。选购网关类产品前，应确认策略是否能用日常语言复述，避免把营销标签当成不用改口令的万能盾牌。</p>
<h2>条件访问的平民版</h2>
<p>企业产品里的「条件访问」可翻译成：只有从已锁定笔记本、且系统补丁不超过 30 天的环境，才允许打开薪资表；手机丢失时远程擦掉工作 Profile。个人可以用分开的浏览器配置文件、不同的操作系统用户账户、以及网盘里「仅指定邮箱可访问」来代替全套 IAM 平台，核心仍是默认拒绝过剩权限。</p>
<h2>持续验证并不等于骚扰</h2>
<p>把每次刷新都弹出验证与「持续验证」混为一论，会让家人放弃执行。更务实的做法是：财务表、遗嘱扫描件、种子短语照片等资产落在单独账户与单独设备；访问它们时触发二次确认，而刷新闻的浏览器保持低摩擦。记录一次自己「从零登录邮箱改密」要点击几步，是衡量零信任有没有落地的简单标尺。</p>
<p>NIST 文档用大量企业术语，但「假设违规已发生」对个人同样成立：笔记本丢在历史里，要假设网盘外链仍可能被捡到——因此默认私密、链接短期有效，就是家里能执行的一版零信任。</p>
<h2>可从小处开始的三项</h2>
<ol>
<li>关闭云盘与协作工具的「任何人可编辑/可发现」默认共享。</li>
<li>为不同用途拆分账户或浏览器配置，减少一次泄露波及全部服务。</li>
<li>季度清点已登录设备与 OAuth 授权，撤销陌生条目。</li>
</ol>
<h2>小团队的轻量实践</h2>
<p>三五人工作室无需采购完整 SASE，仍可约定：财务表格仅指定邮箱可访问、离职当日回收全部外链、公司笔记本全盘加密且自动锁屏五分钟。身份提供商若已启用条件访问，把个人 Gmail 与工作日 Microsoft 账户分离登录配置，能降低会话串味。零信任是渐进迭代，而非一次性「上线完成」。</p>
""".strip(),
        "faq_json": [
            {"q": "零信任只适合大企业吗？", "a": "理念可缩小到分网段、链接过期与设备清单；规模小也能实践核心假设。"},
            {"q": "装零信任客户端就安全了吗？", "a": "客户端只是执行点；策略与权限不清仍会导致过度共享或错误放行。"},
            {"q": "零信任与防火墙冲突吗？", "a": "互补。防火墙过滤边界流量，零信任强调身份与每次访问决策。"},
            {"q": "与 VPN 老模型如何共存？", "a": "VPN 可成为接入渠道之一，但不应再意味着连上即可无差别访问全网。"},
        ],
        "sources_json": [
            {"title": "NIST SP 800-207 Zero Trust Architecture", "url": "https://csrc.nist.gov/publications/detail/sp/800/207/final"},
            {"title": "CISA Zero Trust Maturity Model", "url": "https://www.cisa.gov/zero-trust-maturity-model"},
            {"title": "Cloudflare Learning: What is Zero Trust?", "url": "https://www.cloudflare.com/learning/access-management/what-is-zero-trust/"},
        ],
    },
}

EXPECTED_SLUGS = [
    "what-is-vpn",
    "what-is-dns-leak",
    "what-is-https",
    "what-is-end-to-end-encryption",
    "choose-privacy-tools",
    "what-is-ip-address",
    "network-traffic-encryption",
    "zero-trust-security",
]

out_path = Path(__file__).resolve().parent / "_phase4_other_key.json"

errors = []
if set(data) != set(EXPECTED_SLUGS):
    errors.append(f"slug set mismatch: {set(data) ^ set(EXPECTED_SLUGS)}")

for slug, item in data.items():
    pl = plain_len(item["content_html"])
    if pl < PLAIN_MIN or pl > PLAIN_MAX:
        errors.append(f"{slug}: plain length {pl} not in [{PLAIN_MIN},{PLAIN_MAX}]")
    md = item["meta_description"]
    if len(md) < META_MIN or len(md) > META_MAX:
        errors.append(f"{slug}: meta_description length {len(md)}")
    links = count_internal_links(item["content_html"])
    if links < 2 or links > 4:
        errors.append(f"{slug}: internal links {links} (want 2-4)")
    tag_err = validate_tags(item["content_html"])
    if tag_err:
        errors.append(f"{slug}: {tag_err}")
    bad = check_forbidden(json.dumps(item, ensure_ascii=False))
    if bad:
        errors.append(f"{slug}: forbidden {bad}")
    if not (3 <= len(item["faq_json"]) <= 4):
        errors.append(f"{slug}: faq count {len(item['faq_json'])}")
    if not (3 <= len(item["sources_json"]) <= 5):
        errors.append(f"{slug}: sources count {len(item['sources_json'])}")

if errors:
    print("VALIDATION ERRORS:")
    for e in errors:
        print(" ", e)
    for slug in data:
        print(
            f"  {slug}: plain={plain_len(data[slug]['content_html'])}, "
            f"meta={len(data[slug]['meta_description'])}, "
            f"links={count_internal_links(data[slug]['content_html'])}"
        )
    raise SystemExit(1)

with out_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

report = {
    "path": str(out_path),
    "plain_lengths": {s: plain_len(data[s]["content_html"]) for s in EXPECTED_SLUGS},
    "forbidden_phrases_found": [],
}
for slug in EXPECTED_SLUGS:
    report["forbidden_phrases_found"].extend(
        [(slug, p) for p in check_forbidden(json.dumps(data[slug], ensure_ascii=False))]
    )

print(f"Wrote {out_path}")
for slug in EXPECTED_SLUGS:
    print(
        f"  {slug}: plain={report['plain_lengths'][slug]}, "
        f"meta={len(data[slug]['meta_description'])}, "
        f"links={count_internal_links(data[slug]['content_html'])}"
    )
print("Forbidden phrases:", "none" if not report["forbidden_phrases_found"] else report["forbidden_phrases_found"])
