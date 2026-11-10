# -*- coding: utf-8 -*-
"""Phase 3 priority article bodies (unique, sourced)."""

PRIORITY = {}

PRIORITY["what-is-vpn"] = {
  "seo_title": "什么是 VPN：隧道、加密、DNS 与威胁模型",
  "meta_description": "用威胁模型解释 VPN 的隧道封装、加密、DNS、出口 IP 与元数据边界，以及服务商角色和适用场景。",
  "content_html": """
<p>VPN（Virtual Private Network，虚拟专用网络）把设备上的部分或全部 IP 流量封装进一条加密隧道，再经由远端节点转发到互联网。它改变的是路径与出口表现，并不能自动提供匿名或设备安全。</p>
<h2>它解决什么问题</h2>
<p>常见目标包括：在不可信网络上降低旁路窃听风险；把流量集中到可控出口；在企业场景中远程接入内网。是否值得使用，取决于你要对抗谁：咖啡馆旁路观察者、运营商侧可见性，还是需要访问受控资源。</p>
<h2>隧道与封装</h2>
<p>客户端在本机创建虚拟网卡或接管路由，把原始 IP 包封装后发往 VPN 服务器。对路径上的中间节点而言，常见可见信息是“你的设备在与 VPN 服务器通信”，而不是内层访问的每一个明文目标（仍可能有流量大小、时间等侧信道）。</p>
<h2>加密与完整性</h2>
<p>现代 VPN 协议对隧道载荷做机密性与完整性保护，防止路径上篡改。协议选择（如 WireGuard、IPsec、基于 TLS 的方案）影响实现复杂度、性能与审计难度，但都无法替代端点安全：若设备已失陷，攻击者可在入隧前读取数据。</p>
<p>更细的协议细节见 <a href="/articles/what-is-wireguard">WireGuard 协议说明</a> 与 <a href="/articles/network-traffic-encryption">网络流量加密</a>。</p>
<h2>DNS 在隧道中的位置</h2>
<p>域名解析若仍走本地或运营商解析器，可能出现 DNS 泄露：隧道已建立，但查询域名的路径绕行。可靠部署会明确指定隧道内 DNS，或使用加密 DNS，并在变更配置后复查。详见 <a href="/articles/what-is-dns-leak">什么是 DNS 泄露</a>。</p>
<h2>IP 路由与出口</h2>
<p>连接成功后，默认路由或分流规则决定哪些前缀走隧道。全隧道把几乎所有流量送入远端；分流（split tunneling）只保护选定网段。出口 IP 变为服务商节点地址，网站与风控系统会据此看到“来自该节点的访问”，这与匿名不是一回事。</p>
<h2>元数据仍然存在</h2>
<p>即使载荷加密，连接起止时间、流量体积、与 VPN 服务器的会话本身仍可能被观察。VPN 不消除浏览器 Cookie、账号登录态与设备指纹；它主要改变网络路径层的暴露面。</p>
<h2>服务商扮演的角色</h2>
<p>你把流量交给运营方解密（在其出口）并转发。因此日志政策、司法管辖、客户端供应链与是否可独立审计，比广告语更重要。商业链接若出现在本站，会单独标注；任何服务都不能承诺“绝对无日志且绝对安全”。</p>
<h2>威胁模型示例</h2>
<ul>
<li><strong>公共 Wi-Fi 旁路嗅探：</strong>可信隧道 + HTTPS 通常有帮助。</li>
<li><strong>账号被钓鱼：</strong>VPN 基本无助，应靠验证入口与双重验证。</li>
<li><strong>设备丢失：</strong>需要磁盘加密与锁屏，不是 VPN。</li>
<li><strong>对抗全局强大攻击者：</strong>单一商业 VPN 往往不够，需更完整的对抗方案。</li>
</ul>
<h2>典型误区</h2>
<ul>
<li>把“换 IP”当成“隐身”。</li>
<li>安装来路不明的客户端，反而引入后门。</li>
<li>忽略 DNS 与杀开关（断线时是否泄漏直连流量）。</li>
<li>在已中木马的电脑上指望隧道保护输入内容。</li>
</ul>
<h2>与代理的关系</h2>
<p>代理多作用于单个应用；VPN 类隧道更接近系统路径变更。二者覆盖范围与信任边界不同，见 <a href="/articles/vpn-vs-proxy">VPN 和代理的区别</a>。</p>
""",
  "faq_json": [
    {"q": "VPN 能让我完全匿名吗？", "a": "不能。它改变部分网络路径与出口表现，不消除账号、Cookie、指纹等身份关联。"},
    {"q": "只用 HTTPS 还需要 VPN 吗？", "a": "取决于威胁模型。HTTPS 保护浏览器到网站的内容；VPN 额外改变系统级路径与出口，二者可叠加但目标不同。"},
    {"q": "免费 VPN 可以信任吗？", "a": "要额外审查商业模式与客户端来源。免费服务常以数据或广告支撑，不等于一定恶意，但风险更高。"},
    {"q": "断线后会泄漏流量吗？", "a": "若未启用杀开关或防火墙规则，隧道断开时流量可能回到默认网络。部署时应验证这一行为。"}
  ],
  "sources_json": [
    {"title": "Cloudflare Learning: What is a VPN?", "url": "https://www.cloudflare.com/learning/access-management/what-is-a-vpn/"},
    {"title": "NIST SP 800-77 Rev. 1 Guide to IPsec VPNs", "url": "https://csrc.nist.gov/pubs/sp/800/77/r1/final"},
    {"title": "OWASP: Transport Layer Protection Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"},
    {"title": "EFF Surveillance Self-Defense", "url": "https://ssd.eff.org/"}
  ],
}

PRIORITY["what-is-wireguard"] = {
  "seo_title": "什么是 WireGuard：Noise、曲线与 Cryptokey Routing",
  "meta_description": "依据官方协议说明，解读 WireGuard 的 Noise 握手、Curve25519、ChaCha20-Poly1305、BLAKE2s、SipHash24 与路由要点。",
  "content_html": """
<p>WireGuard 是一种以简洁实现著称的三层 VPN 隧道协议，基于 UDP 封装 IP 包。官方将密码学原语固定为一小组现代算法，并用 Cryptokey Routing 把对端公钥与允许的 IP 前缀绑定。</p>
<h2>设计目标</h2>
<p>相对传统 IPsec/OpenVPN 的庞杂选项，WireGuard 强调：代码量可控、配置面小、默认密码学套件固定、内核态可高效转发。它不提供“应用层代理”语义，而是虚拟网卡上的点对点安全隧道。</p>
<h2>Noise Protocol Framework</h2>
<p>握手建立在 Noise 框架之上。官方构造字符串为 <code>Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s</code>：即 IK 模式（发起方已知响应方静态公钥），并可选混入预共享密钥（psk2）以增强抗量子等场景的余量。Noise 负责把长期密钥与临时密钥的 Diffie–Hellman 组合编排成可分析的握手脚本。</p>
<h2>核心密码学原语</h2>
<ul>
<li><strong>Curve25519：</strong>用于椭圆曲线 Diffie–Hellman（ECDH），生成共享密钥材料。</li>
<li><strong>ChaCha20-Poly1305：</strong>按 RFC 7539 的 AEAD 构造保护数据包机密性与完整性；计数器型 nonce，避免重用。</li>
<li><strong>BLAKE2s：</strong>用于哈希与键控哈希（含 HMAC-BLAKE2s），并参与 HKDF 风格的密钥派生（官方引用 RFC 5869）。</li>
<li><strong>SipHash24：</strong>用于哈希表键等内部结构，降低哈希洪水一类攻击面。</li>
</ul>
<p>可选预共享密钥会混入握手；未启用时按全零 32 字节处理（协议定义行为）。</p>
<h2>Handshake 与密钥轮换</h2>
<p>连接开始时进行简短握手，建立对称会话密钥后传输数据。为提供前向保密，握手会按时间与报文计数等条件重新发起（官方描述为每隔数分钟量级轮换，并由定时器与报文阈值触发）。握手基于时间而非“必须依赖上一包内容”，以便在丢包网络中更稳健。</p>
<p>响应方在完成握手后，需等到收到发起方使用新会话加密的首个数据包（可为心跳空包）才确认新密钥，避免未完成确认就发送。</p>
<h2>Cryptokey Routing</h2>
<p>每个对端由 Curve25519 公钥标识，并配置 AllowedIPs（允许的源/目的前缀）。出站时按目的 IP 选择对应公钥加密；入站解密后，仅当内层源 IP 落在该公钥的允许集合内才接收，否则丢弃。这把“身份”与“可声明的 IP”绑在一起，简化防火墙推理，也要求 AllowedIPs 配置正确，否则会出现无法互通或误路由。</p>
<h2>MTU 与路由注意事项</h2>
<ul>
<li>外层 UDP/IP 与加密开销会降低有效 MTU；路径 MTU 发现失败时可能出现分片或大包丢弃，需按环境调整接口 MTU。</li>
<li>全隧道默认路由与本地局域网、DNS、回程路由冲突时，容易造成“连上即断网”，应明确分流与表优先级。</li>
<li>移动网络下的漫游依赖端点更新机制；防火墙需放行对应 UDP 端口。</li>
</ul>
<h2>安全使用边界</h2>
<p>WireGuard 保证的是隧道上的加密与对端认证（基于预置公钥），不自动审查服务端运营方，也不保护隧道终点之后的明文处理。私钥与配置文件等同于凭证，应限制权限并避免随手上传到不可信位置。与系统级 VPN 概念的关系见 <a href="/articles/what-is-vpn">什么是 VPN</a>；与代理对比见 <a href="/articles/vpn-vs-proxy">VPN 和代理</a>。</p>
<h2>典型错误</h2>
<ul>
<li>AllowedIPs 写错导致流量未入隧或非对称路由。</li>
<li>多台设备复用同一私钥，破坏身份模型。</li>
<li>忽略 DNS 仍走明文解析器。</li>
<li>把“协议现代”等同于“运营方可信”。</li>
</ul>
""",
  "faq_json": [
    {"q": "WireGuard 用的是哪种 Noise 模式？", "a": "官方实现基于 Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s，即 IK 握手并可混入预共享密钥。"},
    {"q": "为什么强调 Cryptokey Routing？", "a": "它用公钥标识对端，并用 AllowedIPs 约束加解密后可接受的 IP，把认证与路由策略绑在一起。"},
    {"q": "会话密钥会轮换吗？", "a": "会。官方设计通过定时与报文阈值重新握手，以提供前向保密，并在丢包环境保持可用性。"},
    {"q": "WireGuard 能替代账号安全吗？", "a": "不能。它保护的是网络路径层；钓鱼、弱密码与恶意客户端仍需单独防护。"}
  ],
  "sources_json": [
    {"title": "WireGuard: Protocol & Cryptography", "url": "https://www.wireguard.com/protocol/"},
    {"title": "WireGuard whitepaper (PDF)", "url": "https://www.wireguard.com/papers/wireguard.pdf"},
    {"title": "Noise Protocol Framework", "url": "https://noiseprotocol.org/noise.html"},
    {"title": "RFC 7539 ChaCha20-Poly1305", "url": "https://www.rfc-editor.org/rfc/rfc7539"},
    {"title": "RFC 7693 BLAKE2", "url": "https://www.rfc-editor.org/rfc/rfc7693"}
  ],
}

PRIORITY["what-is-vless"] = {
  "seo_title": "什么是 VLESS：Xray 中的定位、TLS/REALITY 与边界",
  "meta_description": "根据 Xray 文档说明 VLESS 的无状态设计、与 VMess 差异、TLS/REALITY、flow 兼容性，以及协议本身不保证什么。",
  "content_html": """
<p>VLESS 是 Xray 生态中的一种轻量、无状态传输协议，可作为客户端与服务端之间的桥接。它本身主要解决“如何标识用户并承载流量”，安全传输通常还要依赖外层的 TLS、REALITY 或文档允许的加密模式。</p>
<h2>协议定位</h2>
<p>按 Project X 文档，VLESS 分为 inbound/outbound，用 UUID（或可映射为 UUID 的短字符串）做用户标识，不依赖系统时间对齐。它被设计为比早期 VMess 更精简的承载层，而不是完整的“一键安全产品”。</p>
<h2>在 Xray 架构中的位置</h2>
<p>Xray 将入站、出站、路由与流设置（transport / security）分层。VLESS 多出现在 protocol 字段，真正的外表特征与加密由 <code>streamSettings</code>（如 TCP、TLS、REALITY）以及可选的 VLESS Encryption 等配置决定。换言之：讨论“VLESS 安不安全”时，必须同时说明外层安全如何配置。</p>
<h2>与 VMess 的主要差异</h2>
<ul>
<li>VLESS 强调无状态与轻量；文档明确其不依赖系统时间。</li>
<li>认证以 UUID 为主；VMess 有不同的历史设计与时间窗等行为。</li>
<li>二者都只是核心中的协议选项之一，实际风险还取决于客户端来源、分享订阅是否被篡改、以及节点运营方。</li>
</ul>
<h2>TLS 与 REALITY 的角色</h2>
<p>文档警告：除非链路本身可信（例如私有地址且受控）或启用了规定的 VLESS Encryption，否则 VLESS 应配合外层传输安全。TLS 提供常规的证书认证与加密通道；REALITY 等机制用于特定对抗场景，属于部署选择，不是 VLESS 名称自带的魔法。配置错误或证书校验被关闭时，协议名字帮不上忙。</p>
<h2>Flow 与兼容性</h2>
<p>用户对象可设置 <code>flow</code>。常见情况包括：空 flow 走标准 TLS 代理；<code>xtls-rprx-vision</code> 启用文档所述的 XTLS 相关模式（含内部握手随机填充等）。XTLS 仅在文档列出的组合下可用（例如 TCP+TLS/REALITY，或配合 VLESS Encryption 的条件）。客户端与服务端 flow 不一致会导致无法连接或行为异常。</p>
<h2>协议本身不保证什么</h2>
<ul>
<li>不保证节点运营方不记录或不明文处理出口流量。</li>
<li>不保证来路不明的“一键客户端”未被植入后门。</li>
<li>不保证绕过一切网络策略；可用性随环境变化。</li>
<li>不替代账号安全、系统更新与防钓鱼。</li>
</ul>
<p>若你的目标是理解系统级隧道，优先阅读 <a href="/articles/what-is-vpn">VPN</a> 与 <a href="/articles/what-is-wireguard">WireGuard</a>；若在比较工具选型，见 <a href="/articles/choose-privacy-tools">如何选择隐私工具</a>。</p>
<h2>安全使用建议</h2>
<p>只使用可核验来源的核心与客户端；把 UUID 与私钥当凭证保管；理解订阅链接泄露等于接入权泄露。本站若出现商业客户端链接，会标明“商业链接”，且不将其表述为绝对安全保证。</p>
""",
  "faq_json": [
    {"q": "VLESS 等于 VPN 吗？", "a": "不等同。它是 Xray 等实现中的传输/代理协议选项，通常还要配合 TLS 等外层安全与路由配置。"},
    {"q": "为什么文档强调必须配合外层安全？", "a": "VLESS 默认聚焦轻量承载；在不受信链路上，需要 TLS/REALITY 或文档允许的加密模式防止路径窃听与篡改。"},
    {"q": "flow 填错会怎样？", "a": "可能导致无法握手或功能不可用。服务端与客户端需按同一文档约定配置，尤其是 xtls-rprx-vision 等模式。"},
    {"q": "VLESS 能保证匿名吗？", "a": "不能。出口节点、DNS、账号与客户端供应链都会影响真实隐私效果。"}
  ],
  "sources_json": [
    {"title": "Xray docs: VLESS inbound", "url": "https://xtls.github.io/en/config/inbounds/vless.html"},
    {"title": "Xray docs (Chinese): VLESS", "url": "https://xtls.github.io/config/inbounds/vless.html"},
    {"title": "Project X documentation home", "url": "https://xtls.github.io/"},
    {"title": "Cloudflare Learning: What is TLS?", "url": "https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/"}
  ],
}

PRIORITY["vpn-vs-proxy"] = {
  "seo_title": "VPN 和代理有什么区别：覆盖范围与信任边界",
  "meta_description": "从覆盖范围、加密、DNS、信任边界与适用场景对比 VPN 隧道与代理，帮助按威胁模型选择。",
  "content_html": """
<p>VPN 与代理都可能改变流量路径，但作用层级、覆盖范围与失败方式不同。选型应先写清要保护的应用集合，再看加密与日志假设。</p>
<h2>覆盖范围</h2>
<p>HTTP/SOCKS 等代理通常只影响配置了代理的应用或浏览器；未走代理的应用仍直连。系统级 VPN 隧道通过虚拟网卡与路由，使更多（乃至全部）IP 流量进入隧道，除非你显式分流。</p>
<h2>加密程度</h2>
<p>“代理”一词本身不保证加密：明文 HTTP 代理几乎不提供传输保护；HTTPS 代理或带 TLS 的方案另论。VPN 协议的设计目标通常包含隧道加密与完整性。细节见 <a href="/articles/what-is-vpn">VPN 原理</a> 与 <a href="/articles/network-traffic-encryption">流量加密</a>。</p>
<h2>DNS 行为</h2>
<p>代理场景下，DNS 可能在本地解析后只把连接交给代理，或把域名交给代理解析，行为因实现而异。VPN 则常通过隧道内 DNS 或路由规则影响解析路径；配置不当会出现 <a href="/articles/what-is-dns-leak">DNS 泄露</a>。</p>
<h2>信任边界</h2>
<p>使用代理时，你信任该代理运营方看到（或转发）对应应用的流量。使用 VPN 时，信任边界扩大到进入隧道的所有流量。覆盖越广，运营方能看到的潜在内容越多（在出口解密之后）。</p>
<h2>典型场景</h2>
<ul>
<li><strong>仅浏览器临时访问：</strong>应用级代理可能足够，但要接受其他应用泄漏。</li>
<li><strong>公共网络多应用保护：</strong>系统级隧道更贴切，并叠加 HTTPS。</li>
<li><strong>企业内网接入：</strong>常使用受管 VPN，并配合设备合规，而不是浏览器插件代理。</li>
</ul>
<h2>常见错误</h2>
<ul>
<li>以为开了浏览器代理，聊天软件与系统更新也受保护。</li>
<li>叠加多层来路不明代理“图更安全”，实则增加错误配置与供应链风险。</li>
<li>忽略杀开关：隧道或代理失效时流量默默回直连。</li>
</ul>
<p>协议选型可继续阅读 <a href="/articles/what-is-wireguard">WireGuard</a>；工具评估见 <a href="/articles/choose-privacy-tools">隐私工具选择</a>。</p>
""",
  "faq_json": [
    {"q": "哪个更安全？", "a": "没有绝对答案。看覆盖范围是否匹配需求，以及运营方、客户端与 DNS 行为是否可信。"},
    {"q": "可以同时开 VPN 和代理吗？", "a": "可以，但路径会变复杂，排障困难。应能说清每一跳谁解密什么，避免盲目叠加。"},
    {"q": "代理一定加密吗？", "a": "不一定。协议与实现决定是否加密；不要被名称误导。"}
  ],
  "sources_json": [
    {"title": "MDN: Proxy server", "url": "https://developer.mozilla.org/en-US/docs/Glossary/Proxy_server"},
    {"title": "Cloudflare: What is a VPN?", "url": "https://www.cloudflare.com/learning/access-management/what-is-a-vpn/"},
    {"title": "OWASP: Transport Layer Protection", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"}
  ],
}

PRIORITY["what-is-dns-leak"] = {
  "seo_title": "什么是 DNS 泄露：原理、检测与缓解",
  "meta_description": "解释 DNS 泄露如何在隧道外暴露域名查询，以及加密 DNS、隧道内解析与分流场景下的注意点。",
  "content_html": """
<p>DNS 泄露指：你以为查询会走受保护路径（例如 VPN 隧道），实际上域名解析仍经由本地网络、运营商或其他非预期解析器完成，从而暴露访问意图。</p>
<h2>DNS 在连接中的位置</h2>
<p>浏览器访问网站前，通常需要把域名解析成 IP。解析器能看到你查询的域名；若查询不加密，路径上的观察者也可能看到。即便随后网页走 HTTPS，查询阶段的暴露仍然独立存在。基础概念见 <a href="/articles/how-dns-servers-work">DNS 服务器如何工作</a>。</p>
<h2>为何在 VPN 场景常见</h2>
<p>隧道建立后，若操作系统、浏览器或 remapper 仍把 DNS 发向原网络的解析器，就会出现“IP 已是远程出口，但域名查询在本地泄漏”。分流配置下，部分域名本就应直连，这与“误泄漏”不同，关键是行为是否符合你的预期。</p>
<h2>加密 DNS 能做什么</h2>
<p>DoH/DoT 等技术保护查询在传输中的机密性与完整性，降低路径窃听与篡改，但不会自动隐藏你对解析服务本身的查询内容。选择政策清晰的解析器，并确认浏览器扩展没有劫持解析。</p>
<h2>如何检查</h2>
<ul>
<li>连接隧道前后，对比 DNS 出口与预期是否一致（使用你信任的检测页或自建探测）。</li>
<li>变更客户端、系统更新或浏览器设置后重新测一次；泄露状态不是一次测试永久有效。</li>
<li>确认“阻止非隧道 DNS”或同类选项已按厂商文档开启。</li>
</ul>
<h2>缓解步骤</h2>
<ul>
<li>在 VPN 客户端指定隧道内 DNS，并验证。</li>
<li>系统或路由器统一配置可信加密 DNS，减少应用各自为政。</li>
<li>理解分流：预期直连的域名走本地解析不一定是缺陷；意外绕行才是。</li>
</ul>
<p>相关阅读：<a href="/articles/what-is-vpn">VPN 原理</a>、<a href="/articles/what-is-https">HTTPS</a>、<a href="/articles/public-wifi-safety">公共 Wi-Fi 安全</a>。</p>
""",
  "faq_json": [
    {"q": "换了 VPN 就一定没有 DNS 泄露？", "a": "不一定。取决于客户端是否强制隧道内 DNS，以及系统/浏览器是否另有解析路径。"},
    {"q": "加密 DNS 能隐藏访问的网站内容吗？", "a": "不能。它主要保护查询通道；页面内容仍靠 HTTPS 等机制保护。"},
    {"q": "IPv6 会导致泄露吗？", "a": "若隧道未妥善处理 IPv6，而系统仍走 IPv6 直连，可能绕过预期路径。应确认 IPv6 策略。"}
  ],
  "sources_json": [
    {"title": "Cloudflare Learning: What is DNS?", "url": "https://www.cloudflare.com/learning/dns/what-is-dns/"},
    {"title": "RFC 8484 DNS over HTTPS", "url": "https://www.rfc-editor.org/rfc/rfc8484"},
    {"title": "RFC 7858 DNS over TLS", "url": "https://www.rfc-editor.org/rfc/rfc7858"},
    {"title": "Mozilla: DNS over HTTPS (DoH)", "url": "https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Privacy/DNS_over_HTTPS"}
  ],
}

PRIORITY["network-traffic-encryption"] = {
  "seo_title": "什么是网络流量加密：TLS、隧道与元数据",
  "meta_description": "区分 HTTPS/TLS、VPN 隧道与磁盘加密各自保护的范围，并说明元数据、端点安全与验证方法。",
  "content_html": """
<p>网络流量加密泛指在传输路径上保护数据机密性与完整性的技术。HTTPS/TLS、VPN 隧道等属于不同层次，保护对象与可见元数据并不相同。</p>
<h2>TLS/HTTPS：应用会话层</h2>
<p>浏览器与网站之间的 TLS 保护 HTTP 等内容，并借助证书体系验证你连接的域名身份（在校验证常的前提下）。它不改变系统中其他应用的流量，也不能证明网站经营者诚实。详见 <a href="/articles/what-is-https">什么是 HTTPS</a>。</p>
<h2>VPN 隧道：路径封装层</h2>
<p>隧道把多应用的 IP 包封装并加密发往远端，再由远端出站。它改变出口与路径可见性，但终点运营方在出站后通常能看到目标连接。见 <a href="/articles/what-is-vpn">VPN</a> 与 <a href="/articles/what-is-wireguard">WireGuard</a>。</p>
<h2>内容 vs 元数据</h2>
<p>加密载荷后，时间、体积、目的端口、SNI（视协议与扩展而定）、DNS 查询等仍可能泄漏意图。因此“已加密”不等于“无可观察信息”。DNS 侧见 <a href="/articles/what-is-dns-leak">DNS 泄露</a>。</p>
<h2>端点安全仍关键</h2>
<p>若设备存在键盘记录或恶意软件，数据在加密前已被读取。传输加密不能替代系统更新、权限最小化与防钓鱼。</p>
<h2>如何验证加密生效</h2>
<ul>
<li>网站证书主体与域名匹配，无持续证书警告。</li>
<li>隧道客户端显示已连接，且 DNS/出口符合预期。</li>
<li>不在证书告警页输入密码；改走官方应用或已知域名。</li>
</ul>
<h2>实践选型</h2>
<p>防咖啡馆旁路：HTTPS 是底线，可信隧道是增强。防设备丢失：磁盘加密。防跨站追踪：还要处理 Cookie 与账号，见 <a href="/articles/protect-online-privacy">如何保护网络隐私</a>。</p>
""",
  "faq_json": [
    {"q": "VPN 和 HTTPS 可以一起用吗？", "a": "可以。它们保护的阶段不同，常可叠加，但都有边界。"},
    {"q": "加密后还需要强密码吗？", "a": "需要。传输保护不能替代账户凭据保护。"},
    {"q": "为什么仍能被推断访问了谁？", "a": "因为 DNS、SNI、流量模式与账号登录等元数据或上层标识仍然存在。"}
  ],
  "sources_json": [
    {"title": "MDN: Transport Layer Security (TLS)", "url": "https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security"},
    {"title": "Cloudflare Learning: What is Encryption?", "url": "https://www.cloudflare.com/learning/ssl/what-is-encryption/"},
    {"title": "OWASP Transport Layer Protection Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"},
    {"title": "NIST SP 800-52 Rev. 2 Guidelines for TLS", "url": "https://csrc.nist.gov/pubs/sp/800/52/r2/final"}
  ],
}

PRIORITY["protect-online-privacy"] = {
  "seo_title": "如何保护个人网络隐私：可执行的分层做法",
  "meta_description": "从账号、设备、浏览器、网络与数据最小化出发，给出可验证的个人网络隐私保护步骤与常见误区。",
  "content_html": """
<p>网络隐私保护的目标，是减少不必要的标识与长期追踪，并降低账号被接管后的连锁损失。它不是安装一个工具就结束，而是一组可复查的配置。</p>
<h2>先分清威胁</h2>
<p>商业追踪、公共网络旁路、针对性骚扰与数据泄露库撞库，对应措施不同。先写下最怕发生的一两件事，再分配精力。</p>
<h2>账号层</h2>
<ul>
<li>邮箱与密码管理器视为核心：独立强密码、双重验证、保存恢复码。</li>
<li>检查登录设备与邮件转发规则，撤销陌生 OAuth 应用。</li>
<li>减少到处复用同一手机号与邮箱作为唯一标识。</li>
</ul>
<p>延伸：<a href="/articles/protect-online-accounts">保护在线账户</a>、<a href="/articles/two-factor-authentication-guide">双重验证</a>。</p>
<h2>设备与应用层</h2>
<ul>
<li>系统与应用自动更新；限制通讯录、短信、无障碍等高危权限。</li>
<li>只从官方商店安装软件；淘汰设备前退出云会话并擦除。</li>
</ul>
<h2>浏览器与追踪</h2>
<p>限制第三方 Cookie、审查扩展权限、按场景分离登录配置。清除 Cookie 有帮助，但账号登录与指纹仍可能延续识别。见 <a href="/articles/how-online-tracking-works">在线追踪如何运作</a> 与 <a href="/articles/browser-privacy-settings">浏览器隐私设置</a>。</p>
<h2>网络层</h2>
<p>公共网络默认不信任：敏感操作优先移动数据；必要时使用可信隧道并确认 HTTPS。理解 VPN 的边界：<a href="/articles/what-is-vpn">VPN 原理</a>、<a href="/articles/public-wifi-safety">公共 Wi-Fi</a>。</p>
<h2>数据最小化</h2>
<p>能不填的证件号与通讯录就不填；网盘外链设过期；定期清理长期授权。工具选型见 <a href="/articles/choose-privacy-tools">如何选择隐私工具</a>。</p>
<h2>如何验证“有没有做好”</h2>
<ul>
<li>能否用恢复码重新登录核心邮箱？</li>
<li>陌生登录是否会收到通知？</li>
<li>浏览器扩展列表是否都能叫出名字？</li>
<li>公共网络下证书告警时，你是否会停止输入？</li>
</ul>
""",
  "faq_json": [
    {"q": "只开 VPN 够不够？", "a": "通常不够。VPN 主要影响路径层；账号、追踪标识与权限同样关键。"},
    {"q": "无痕模式等于隐私达标吗？", "a": "无痕主要减少本地残留，对已登录站点与服务端追踪帮助有限。"},
    {"q": "隐私和便利如何取舍？", "a": "把高暴露功能留给真正需要的场景，而不是全局永久开启所有同步与定位。"}
  ],
  "sources_json": [
    {"title": "EFF Surveillance Self-Defense", "url": "https://ssd.eff.org/"},
    {"title": "Mozilla Privacy & Security guides", "url": "https://www.mozilla.org/en-US/privacy/"},
    {"title": "OWASP Top Ten", "url": "https://owasp.org/www-project-top-ten/"},
    {"title": "NIST Digital Identity Guidelines", "url": "https://pages.nist.gov/800-63-3/"}
  ],
}

PRIORITY["public-wifi-safety"] = {
  "seo_title": "公共 Wi-Fi 安全吗：风险分级与可行防护",
  "meta_description": "分析公共 Wi-Fi 的旁路嗅探、钓鱼门户与假热点风险，并给出按敏感度分级的实用防护步骤。",
  "content_html": """
<p>公共 Wi-Fi 可用，但不应该被默认信任。风险来自同一局域网内的旁路观察、恶意门户页、假热点以及你在其上完成的高敏感操作。</p>
<h2>主要风险</h2>
<ul>
<li>未加密或弱加密链路上的旁路嗅探（现代 HTTPS 大幅缓解内容窃听，但门户与DNS仍可能被做手脚）。</li>
<li>仿冒登录页骗取邮箱或会员密码。</li>
<li>名称相近的假热点。</li>
<li>自动连接后开启的文件共享暴露。</li>
</ul>
<h2>按操作分级</h2>
<ul>
<li><strong>低敏感：</strong>看新闻、查地图——确认 HTTPS 即可。</li>
<li><strong>中敏感：</strong>邮件与社交——建议可信隧道，并避免在门户页输入无关密码。</li>
<li><strong>高敏感：</strong>网银、改密、提交证件——优先切换移动数据或个人热点。</li>
</ul>
<h2>可行防护</h2>
<ul>
<li>关闭自动加入开放网络；用完选择“忘记”。</li>
<li>系统网络配置文件选“公用”，限制发现与共享。</li>
<li>证书告警立即离开，不要点继续。</li>
<li>需要时使用可信 VPN 隧道，并检查 <a href="/articles/what-is-dns-leak">DNS 是否泄露</a>。</li>
</ul>
<p>延伸阅读：<a href="/articles/safe-public-network-use">安全使用公共网络</a>、<a href="/articles/what-is-https">HTTPS</a>、<a href="/articles/what-is-vpn">VPN</a>。</p>
<h2>常见错误</h2>
<ul>
<li>在门户页输入银行密码。</li>
<li>向陌生人索取的“店内 Wi-Fi”二维码扫码支付。</li>
<li>以为有小锁就代表热点运营方可信。</li>
</ul>
""",
  "faq_json": [
    {"q": "公共 Wi-Fi 一定不能用吗？", "a": "不是。关键是避免高敏感操作，并确认 HTTPS 与网络配置文件设置。"},
    {"q": "开了 VPN 就绝对安全吗？", "a": "不能绝对。还要防钓鱼门户、假客户端与 DNS 配置错误。"},
    {"q": "手机热点是否更安全？", "a": "通常信任边界更清晰，但仍需注意套餐费用与热点本身的口令设置。"}
  ],
  "sources_json": [
    {"title": "FTC: Public Wi-Fi networks", "url": "https://consumer.ftc.gov/articles/how-safe-your-public-wi-fi-network"},
    {"title": "CISA: Securing Public Wi-Fi Tips", "url": "https://www.cisa.gov/news-events/news/securing-public-wi-fi-networks"},
    {"title": "EFF SSD: Connecting to public Wi-Fi", "url": "https://ssd.eff.org/"},
    {"title": "Cloudflare: What is a VPN?", "url": "https://www.cloudflare.com/learning/access-management/what-is-a-vpn/"}
  ],
}

PRIORITY["what-is-end-to-end-encryption"] = {
  "seo_title": "什么是端到端加密：保护范围与局限",
  "meta_description": "解释端到端加密如何让服务端无法读取内容，并澄清元数据、终端安全、备份与多设备同步等边界。",
  "content_html": """
<p>端到端加密（E2EE）意味着数据在发送端加密、仅在接收端解密，服务运营方以协议设计为目标无法读取明文内容。它保护的是内容机密性，不是通信存在的事实本身。</p>
<h2>与“传输加密”的区别</h2>
<p>TLS 保护客户端到服务器的传输；服务器常可看到明文以提供检索、推荐或备份。E2EE 把解密密钥留在端侧，服务器主要转发密文。两者可同时存在：先 E2EE，再套 TLS 传输。</p>
<h2>密钥与身份</h2>
<p>可靠的 E2EE 系统会提供安全码/指纹核对，用于发现中间人。多设备同步需要谨慎的密钥分发；设备丢失时的远程注销与密钥轮换策略决定真实安全性。</p>
<h2>它不自动保护什么</h2>
<ul>
<li>屏幕偷窥、终端木马、被胁迫解锁。</li>
<li>元数据：谁与谁、何时、消息频率等。</li>
<li>若云备份未同样端到端，备份通道可能成为弱点。</li>
<li>错误把对方设备当成可信终点——对方设备失陷仍会泄露。</li>
</ul>
<p>磁盘与备份加密是另一层，见 <a href="/articles/why-data-encryption-matters">为什么数据加密重要</a>；传输层见 <a href="/articles/network-traffic-encryption">网络流量加密</a>。</p>
<h2>选型时要问的问题</h2>
<ul>
<li>默认是否开启 E2EE，还是仅“可选”？</li>
<li>能否验证联系人安全码？</li>
<li>多设备与备份如何实现，密钥是否离开终端？</li>
<li>是否有独立审计与清晰的威胁模型文档？</li>
</ul>
<p>工具评估框架见 <a href="/articles/choose-privacy-tools">如何选择隐私工具</a>。</p>
""",
  "faq_json": [
    {"q": "有 E2EE 就代表运营方完全看不到任何信息？", "a": "通常仍可能处理元数据与账号信息；要阅读具体产品的白皮书。"},
    {"q": "为什么还需要核对安全码？", "a": "用于发现中间人篡改密钥的情况，尤其在首次通信或密钥变更后。"},
    {"q": "E2EE 能防钓鱼吗？", "a": "不能直接防止你向假站点输入密码；防钓鱼仍靠核实入口。"}
  ],
  "sources_json": [
    {"title": "Cloudflare Learning: What is end-to-end encryption?", "url": "https://www.cloudflare.com/learning/privacy/what-is-end-to-end-encryption/"},
    {"title": "NIST: Encryption topics", "url": "https://www.nist.gov/cryptography"},
    {"title": "EFF: Communicating with Others", "url": "https://ssd.eff.org/module/communicating-others"},
    {"title": "MDN: Confidentiality, Integrity, and Availability", "url": "https://developer.mozilla.org/en-US/docs/Web/Security"}
  ],
}

PRIORITY["choose-privacy-tools"] = {
  "seo_title": "如何选择可靠的隐私保护工具：评估清单",
  "meta_description": "从威胁模型、透明度、审计、权限、商业模式与退出成本评估隐私工具，避免被过度承诺误导。",
  "content_html": """
<p>选择隐私工具前，先写清威胁模型与预算，再看证据，而不是广告词。工具应可卸载、可导出、可关闭；把生活绑死在无法离开的黑盒上，本身就是风险。</p>
<h2>第一步：写清需求</h2>
<ul>
<li>要防谁：商业追踪、公共网络、账户接管，还是设备丢失？</li>
<li>覆盖哪些设备与应用？</li>
<li>能否接受付费？不能接受时，免费产品的商业模式是什么？</li>
</ul>
<h2>评估维度</h2>
<ul>
<li><strong>透明度：</strong>是否有清晰文档、公司主体与联系方式。</li>
<li><strong>审计与开源：</strong>是否有独立审计报告或可复现构建；开源不等于自动安全，但提高可验证性。</li>
<li><strong>权限：</strong>是否强索无障碍、短信、通讯录等与功能无关的权限。</li>
<li><strong>更新：</strong>客户端是否仍在维护。</li>
<li><strong>退出：</strong>数据能否导出，账号能否注销。</li>
</ul>
<h2>按类别举例思考</h2>
<ul>
<li>密码管理器：是否支持强主密码、2FA、紧急访问与泄露报告。</li>
<li>VPN/隧道：日志政策、管辖地、杀开关、DNS 行为；协议是否可核验（如 <a href="/articles/what-is-wireguard">WireGuard</a>）。</li>
<li>浏览器与追踪防护：扩展权限是否过大；是否与你的登录策略冲突。</li>
<li>即时通讯：是否默认 E2EE，见 <a href="/articles/what-is-end-to-end-encryption">端到端加密</a>。</li>
</ul>
<h2>红旗信号</h2>
<ul>
<li>承诺“绝对匿名/军方加密/警察无法获取”。</li>
<li>要求关闭系统安全功能才能运行。</li>
<li>难以卸载或持续推送高危权限。</li>
<li>只有应用商店好评，没有任何技术文档。</li>
</ul>
<p>相关基础：<a href="/articles/protect-online-privacy">保护网络隐私</a>、<a href="/articles/what-is-vpn">VPN</a>、<a href="/articles/vpn-vs-proxy">VPN 与代理</a>。本站工具专题中的商业链接会明确标注。</p>
""",
  "faq_json": [
    {"q": "开源工具是否一定更安全？", "a": "不一定，但通常更易审计。仍需看维护状态、默认配置与供应链。"},
    {"q": "付费是否等于无日志？", "a": "不等于。应阅读政策、审计与历史事件，而不是只看价格。"},
    {"q": "如何做小范围试用？", "a": "先在非核心设备安装，观察权限、卸载难度与是否干扰系统安全功能，再决定迁移。"}
  ],
  "sources_json": [
    {"title": "EFF Surveillance Self-Defense", "url": "https://ssd.eff.org/"},
    {"title": "OWASP: Secure Product Design Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html"},
    {"title": "Mozilla: Privacy & Security", "url": "https://www.mozilla.org/en-US/privacy/"},
    {"title": "NIST Cybersecurity Framework", "url": "https://www.nist.gov/cyberframework"}
  ],
}
