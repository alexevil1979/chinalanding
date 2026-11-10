# -*- coding: utf-8 -*-
"""Generate tools/_phase4_priority.json with length and phrase checks."""
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

def plain_len(content_html: str) -> int:
    text = re.sub(r"<[^>]+>", "", content_html)
    text = html_mod.unescape(text)
    return len(re.sub(r"\s+", "", text))

def check_forbidden(blob: str) -> list:
    return [p for p in FORBIDDEN if p in blob]

WIREGUARD_HTML = r"""
<p>WireGuard 是一套跑在 UDP 上的现代 VPN 隧道协议，由 Jason A. Donenfeld 等人推动主线实现并入主流内核。它的取向很鲜明：密码学套件固定、配置面收窄、内核里转发路径尽量短。对运维与个人用户来说，先弄清「虚拟接口与对端」「公钥路由」「握手轮换」三条主线，比背命令行参数更有效。</p>
<h2>什么是 WireGuard</h2>
<p>从使用者视角，WireGuard 在本机创建名为 <code>wg0</code> 之类的 TUN 接口，把选中的 IP 流量封装进 UDP 发向对端；对端解密后再注入其网络栈。它不替代应用层代理，也不像传统 SSL VPN 那样嵌在浏览器里，而是操作系统级的点对点隧道。官方站点把其实现为 Linux、Windows、macOS、iOS、Android 等多端，协议说明与论文可对照阅读。</p>
<p>与 <a href="/articles/what-is-vpn">VPN 的一般概念</a> 相同：隧道改变的是路径与出口，不自动等于匿名；与 <a href="/articles/vpn-vs-proxy">代理</a> 相比，WireGuard 默认覆盖的是 IP 层路由所指向的前缀集合。</p>
<h2>整体架构</h2>
<p>逻辑上分为三类对象：<strong>Interface（本端接口）</strong>持有本机长期私钥与监听 UDP 端口；<strong>Peer（对端）</strong>用 Curve25519 公钥标识，并绑定允许通信的 IP 前缀与可达地址；<strong>数据平面</strong>在握手完成后用对称密钥加密内层 IP 包。控制面仅 UDP，无 TCP 状态机，因此「断线重连」依赖定时握手与 keepalive，而非应用层心跳协议。</p>
<h2>Interface 与 Peer</h2>
<p>配置文件中 <code>[Interface]</code> 段声明 <code>PrivateKey</code>、<code>Address</code>、<code>DNS</code>、<code>ListenPort</code> 等；每个 <code>[Peer]</code> 声明对端 <code>PublicKey</code>、<code>Endpoint</code>、<code>AllowedIPs</code>、<code>PersistentKeepalive</code>。一台接口可挂多个 Peer（典型星型：客户端指向服务器公钥；服务器为每个客户端各建一个 Peer）。私钥等同于通行证，应限制文件权限，避免与多台设备复用同一密钥对，否则会混淆 Cryptokey 路由所依赖的身份绑定。</p>
<h2>公钥与私钥</h2>
<p>长期身份基于 Curve25519：从 32 字节私钥导出公钥，对端预置公钥才能完成 Noise 握手。可选 <code>PresharedKey</code> 在握手时按协议混入，提供额外对称材料；未配置时协议按全零 32 字节处理。密钥轮换发生在会话层：临时密钥每次握手重新生成，长期密钥则仅在人为轮换时更换。</p>
<h2>Noise Protocol Framework（Noise_IKpsk2）</h2>
<p>WireGuard 握手机制取自 Noise 框架，构造标识符为 <code>Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s</code>：IK 表示发起方已知晓响应方静态公钥；<code>psk2</code> 表示可混合预共享密钥。握手分两报文完成，随后在双方派生发送与接收对称密钥。Noise 设计目标包含身份隐藏、前向保密与抵抗密钥泄露冒充等性质，WireGuard 论文与官网协议页给出了逐字段布局。</p>
<h2>Curve25519、ChaCha20-Poly1305、BLAKE2s、SipHash24</h2>
<ul>
<li><strong>Curve25519</strong>：ECDH 交换共享秘密，用于握手阶段。</li>
<li><strong>ChaCha20-Poly1305</strong>：按 RFC 7539 AEAD 保护数据包；nonce 由 32 位零与 64 位小端计数器组成。</li>
<li><strong>BLAKE2s</strong>：哈希与带密钥 MAC，配合 HKDF（RFC 5869）派生会话密钥。</li>
<li><strong>SipHash24</strong>：实现内部哈希表键，缓解哈希洪水类 DoS。</li>
</ul>
<p>算法组合固定，避免 OpenVPN/IPsec 时代「选配弱 cipher」的配置坑，也方便第三方实现互操作审计。</p>
<h2>Cryptokey Routing</h2>
<p>这是 WireGuard 路由语义的核心：每个 Peer 公钥绑定一组 <code>AllowedIPs</code>。出站时按目的地址前缀挑选 Peer 加密；入站解密后，仅当源 IP 属于该 Peer 允许列表才接受，否则丢弃。因此配置错误常表现为「能握手却无流量」或「非对称路由黑洞」。Hub 型部署里，服务器给客户端的 AllowedIPs 往往是单主机 <code>/32</code>，而客户端把默认路由 <code>0.0.0.0/0</code> 指向服务器，实现全隧道。</p>
<h2>握手与密钥轮换</h2>
<p>官方描述为基于时间的周期性重握手，辅以报文计数阈值，在丢包网络仍保持前向保密。定时器族包括：未收到响应则带抖动的重试；长时间无下行则发空包 keepalive；会话密钥过龄或报文数超限则强制新握手；过期密钥与计数器超限的报文直接拒绝。响应方在新会话建立后，须收到发起方首个加密包（可为 padding 空包）才确认切换，避免半开状态乱序。</p>
<h2>Persistent Keepalive</h2>
<p>NAT 后的客户端若长时间无上行，映射会超时。对端设置 <code>PersistentKeepalive = 25</code> 一类数值时，内核按间隔发送空载荷包维持映射，也有助于触发定时握手。间隔过短徒增流量，过长则漫游后首包可能失败，需与网络运营商 NAT 行为折中。</p>
<h2>Endpoint 漫游</h2>
<p>移动端切 Wi-Fi 与蜂窝时，源 UDP 口与 IP 常变。WireGuard 在收到合法加密包时学习来源 IP/端口并更新 Peer 的当前 Endpoint，无需手工改配置。防火墙需持续允许入站 UDP 到监听端口；对称 NAT 场景下，keepalive 对学习地址尤为重要。</p>
<h2>AllowedIPs</h2>
<p>除 Cryptokey 过滤外，AllowedIPs 还驱动系统路由：安装配置时添加指向隧道接口的前缀。分流（split tunnel）即只把特定前缀写入 AllowedIPs，其余仍走本地默认网关。与策略路由、多表路由共存时，要留意 metric 与「排除局域网」条目，避免本地打印机或组播被误吸入隧道。</p>
<h2>MTU</h2>
<p>外层 UDP、WireGuard 头与 AEAD 扩张减少有效 MSS。若路径 MTU 发现失败，大包可能黑洞或频繁分片。常见做法把接口 MTU 设为 1280–1420 区间并实测，或在 TCP 侧依赖 MSS clamp。跨国链路、PPPoE 与移动网络对 MTU 格外敏感。</p>
<h2>DNS 与路由注意点</h2>
<p>接口级 <code>DNS = ...</code> 会提示解析器走隧道，但若系统或浏览器另启 DoH，仍可能出现查询路径与隧道不一致，参见 <a href="/articles/what-is-dns-leak">DNS 泄露</a>。全隧道时默认路由与「不走隧道的内网前缀」要一并列出；Linux 下 <code>Table = off</code> 等进阶项避免劫持不该进隧道的表项。</p>
<h2>协议边界与局限</h2>
<p>WireGuard 不做用户账户体系、不做内容审计、不内置多级权限；认证仅是「持有对应私钥」。拒绝服务缓解依赖 cookie 回复与 MAC 校验，高负载下可能延迟握手。它也不解决隧道出口之后的日志、恶意软件与钓鱼问题。</p>
<h2>典型部署场景</h2>
<ul>
<li><strong>远程接入公司内网：</strong>AllowedIPs 只包含内网段，日常互联网仍本地出口。</li>
<li><strong>公共 Wi-Fi 加固：</strong>全隧道至自建或可信 VPS，叠加 HTTPS，见 <a href="/articles/public-wifi-safety">公共 Wi-Fi</a>。</li>
<li><strong>站点间专线替代：</strong>两端公钥互认，静态 Endpoint，配合防火墙仅放行 UDP 端口。</li>
<li><strong>手机漫游：</strong>开启适度 PersistentKeepalive，接受 Endpoint 自动更新。</li>
</ul>
<p>选型时把「协议现代」与「谁拿着服务器私钥、是否记录连接元数据」分开评估；WireGuard 解决的是隧道上的密码学目标，运营信任仍需你自行判断。</p>
""".strip()

MYTHS_HTML = r"""
<p>安全科普里有不少「听起来很对」的捷径，真遇到社工或批量攻击时却帮不上忙。下面八个误区在中文社区反复出现；每个误区拆开「误解—现实—机理—例子—做法」，方便你对照自己的设备与账户，而不是背一句口号。</p>
<h2>1 复杂密码不能解决一切</h2>
<h3>常见误解</h3>
<p>密码越复杂越好，其他防护可有可无。</p>
<h3>实际情况</h3>
<p>再长的口令也无法抵挡你在假页面上亲手输入，也无法修复已被拖库的复用密码。枢纽账户失守会连锁重置其他服务。</p>
<h3>技术解释</h3>
<p>离线破解速度取决于哈希算法与泄露形态，但撞库与凭证填充攻击直接复用明文对。NIST SP 800-63B 强调长度、唯一性与 breach 响应，而非无意义的高频轮换。</p>
<h3>现实例子</h3>
<p>某论坛数据库泄露后，攻击者用同一邮箱密码组合尝试登录邮箱与支付平台，与用户口令是否含特殊符号无关。</p>
<h3>用户该怎么做</h3>
<p>枢纽邮箱与金融账户使用密码管理器生成的唯一长口令，并启用 <a href="/articles/two-factor-authentication-guide">双重验证</a>；收到泄露通知时优先处理复用站点。弱站点可维持独立口令，避免为了「花样」牺牲可管理性。</p>
<h2>2 HTTPS 不等于网站可信</h2>
<h3>常见误解</h3>
<p>地址栏有小锁就说明是官网、无假货。</p>
<h3>实际情况</h3>
<p>TLS 只保护你与眼前域名之间的传输机密性与完整性，不审查经营者身份，也不阻止页面里的恶意脚本。</p>
<h3>技术解释</h3>
<p>任何能控制域名的实体都可申请公有 CA 证书。证书验证通过仅表示链路与域名匹配，参见 <a href="/articles/what-is-https">HTTPS 边界</a>。</p>
<h3>现实例子</h3>
<p>搜索品牌词时，广告位域名形似真站，证书有效，表单却把凭据送到攻击者服务器。</p>
<h3>用户该怎么做</h3>
<p>高价值登录从书签或官方 App 进入；付款前核对域名拼写，勿只凭小锁图标判断。</p>
<h2>3 VPN 不是绝对匿名</h2>
<h3>常见误解</h3>
<p>开 VPN 就没人知道你是谁、去过哪些站。</p>
<h3>实际情况</h3>
<p>隧道改变路径与出口 IP，账号 Cookie、设备指纹、支付关联与服务商可见的元数据仍在。</p>
<h3>技术解释</h3>
<p>VPN 在 IP 层封装流量，运营方在出口解密转发；时间、体积、连接目的地等元数据仍可能被记录或推断。若客户端带病或被替换成篡改版，隧道还会成为数据外泄通道而非屏障。见 <a href="/articles/what-is-vpn">VPN 工作原理</a>。</p>
<h3>现实例子</h3>
<p>用户开启商业 VPN 仍用同一 Google 账户登录，广告与风控画像与未开隧道时高度连续。</p>
<h3>用户该怎么做</h3>
<p>先写威胁模型：防旁路窃听与防账户关联是不同目标；分离浏览器配置，审查 VPN 司法辖区与客户端来源。</p>
<h2>4 杀毒软件不能防住所有威胁</h2>
<h3>常见误解</h3>
<p>装了套件就等于百毒不侵。</p>
<h3>实际情况</h3>
<p>零日、无文件攻击、社会工程与恶意扩展常绕过期望签名特征库。</p>
<h3>技术解释</h3>
<p>终端防护结合启发式、行为监控与系统完整性，但无法替代补丁管理与权限最小化。CISA 基础实践把补丁、备份与最小权限并列，而非单押杀毒。</p>
<h3>现实例子</h3>
<p>用户允许「远程协助」后，攻击者直接操作桌面转账，杀毒未触发因为是合法远程会话。</p>
<h3>用户该怎么做</h3>
<p>保持系统自动更新；拒绝不明宏与来源不明安装包；高敏操作不用已被索要远程控制的机器。</p>
<h2>5 无痕模式不能对运营商隐身</h2>
<h3>常见误解</h3>
<p>无痕窗口让 ISP、Wi-Fi 运营方看不见访问了什么。</p>
<h3>实际情况</h3>
<p>无痕主要不保留本地历史与部分 Cookie；链路层与递归 DNS 仍可见连接与查询（除非另配加密 DNS 与隧道）。</p>
<h3>技术解释</h3>
<p>隐私浏览不加密 IP 包载荷以外的元数据；登录账户后，服务端仍记录活动。运营商与网关仍可见你连向哪些 IP、何时连、流量规模几何。参见 <a href="/articles/how-online-tracking-works">在线追踪</a> 与 <a href="/articles/what-is-dns-leak">DNS 路径</a>。</p>
<h3>现实例子</h3>
<p>咖啡馆网络管理员通过网关日志看见无痕会话访问的新闻域名，与是否无痕无关。</p>
<h3>用户该怎么做</h3>
<p>敏感浏览分场景：本地不留痕不等于链路匿名；需要链路保护时结合 HTTPS 与可信隧道，高敏事务改蜂窝。</p>
<h2>6 双重验证降低风险但不消灭钓鱼</h2>
<h3>常见误解</h3>
<p>开了 2FA 就不可能被骗。</p>
<h3>实际情况</h3>
<p>短信与 TOTP 仍可在钓鱼页被实时转发；推送批准滥用「疲劳点击」可骗过用户本人。</p>
<h3>技术解释</h3>
<p>FIDO2/通行密钥绑定站点来源域，显著抗中继钓鱼；传统 OTP 不提供同等级域绑定。OWASP 认证备忘强调按资产选择因子强度。</p>
<h3>现实例子</h3>
<p>仿冒登录页同步把用户输入的 6 位 TOTP 转给真站，完成会话劫持。</p>
<h3>用户该怎么做</h3>
<p>金融与邮箱优先硬件密钥或可验证域的 WebAuthn；对推送登录逐项核对地点与应用名，拒绝陌生批准。</p>
<h2>7 更新确实重要</h2>
<h3>常见误解</h3>
<p>「从不中毒」的人可以长期推迟更新。</p>
<h3>实际情况</h3>
<p>公开 CVE 与在野利用不挑谨慎用户；操作系统、浏览器与固件补丁关闭的是已知洞，不是装饰。</p>
<h3>技术解释</h3>
<p>攻击链常从过期组件进入，再横向到凭据与数据。NIST 与 CISA 反复把及时补丁列为最低成本防线之一。</p>
<h3>现实例子</h3>
<p>未修补的路由器漏洞在僵尸网络扫描列表中长期可见，与主人是否「细心上网」无关。</p>
<h3>用户该怎么做</h3>
<p>开启自动安全更新；路由器与 NAS 纳入与手机同级的补丁节奏；重大漏洞新闻发布后优先核对自家设备型号。废弃不再维护的物联网固件设备，比抱着「从不点链接」更现实。</p>
<h2>8 备份不等于同步</h2>
<h3>常见误解</h3>
<p>文件进了云盘同步文件夹就等于有备份。</p>
<h3>实际情况</h3>
<p>同步镜像传播误删与勒索加密；真正可恢复需要版本历史、离线副本与定期演练还原。</p>
<h3>技术解释</h3>
<p>备份强调时间点可恢复性与不可变副本；同步强调多设备一致性。勒索软件会加密在线同步盘中的明文文件，使「备份」同时失效。版本保留与对象锁定（WORM）是云厂商提供的不同能力，选购前读清保留天数。</p>
<h3>现实例子</h3>
<p>用户误删项目文件夹，云同步立即在各端删除，未开版本历史则无法找回。勒索软件加密工作目录后，实时同步把密文文件推上云端，未分离的「备份」一并作废。</p>
<h3>用户该怎么做</h3>
<p>关键数据执行 3-2-1：至少一份离线或不可变；定期试恢复小文件；机密资料客户端加密后再上传。</p>
<p>以上八条互相叠加：传输加密护链路，账户加固护身份，补丁与备份护可用性。更多账户习惯见 <a href="/articles/protect-online-accounts">保护在线账户</a> 与 <a href="/articles/identify-phishing-attacks">识别钓鱼</a>；公共网络场景可读 <a href="/articles/public-wifi-safety">公共 Wi-Fi 安全</a>。</p>
""".strip()

VLESS_HTML = r"""
<p>VLESS 是 Project X（Xray）文档定义的一种<strong>无状态、轻量</strong>传输协议，作为客户端与服务端之间的承载层。它用 UUID 标识用户，不依赖系统时间同步——这一点与 VMess 的设计差异在官方文档中写得很清楚。讨论 VLESS 时务必同时说明外层 <code>streamSettings</code> 与安全配置，否则容易把「协议名」误当成完整安全方案。</p>
<h2>协议定位</h2>
<p>文档称 VLESS 分为 inbound 与 outbound，可在 Xray 路由体系中桥接流量。它解决的是「谁有权接入、字节如何被转发」，而不是操作系统级 TUN 的全局路由语义；与 <a href="/articles/what-is-vpn">传统 VPN</a> 或 <a href="/articles/what-is-wireguard">WireGuard</a> 对比时，要区分承载协议与终端隧道产品。</p>
<h2>认证：UUID</h2>
<p>服务端 <code>settings.users</code> 中的 <code>id</code> 可为标准 UUID，或短于 30 字节的自定义字符串（按 UUIDv5 映射规则与 UUID 等价）。<code>level</code> 对接本地策略；<code>email</code> 用于日志与统计区分。UUID 泄露等同于接入凭证泄露，应像密码一样保管订阅链接与配置文件。</p>
<h2>Inbound 与 Outbound</h2>
<p>Inbound 监听入站连接并校验用户；Outbound 把通过路由规则的流量发往下一跳。VLESS 只定义其中 <code>protocol: vless</code> 的语义，具体走哪条线路由 <code>routing</code> 与 <code>outbounds</code> 决定。两端须使用互相认可的 UUID、flow 与传输层参数。</p>
<h2>streamSettings 与 TCP</h2>
<p>常见组合为 TCP 承载，再配合 <code>security</code> 字段选择 TLS、REALITY 或 none。官方警告：除非对端是可信私有地址且链路受控，或启用了规定的 VLESS Encryption，否则不应在公网以 <code>security: none</code> 裸奔——否则路径上的观察者可直接读取载荷。</p>
<h2>TLS 与 REALITY</h2>
<p>TLS 提供证书校验与记录层加密，是大多数公网部署的外层。REALITY 属于特定部署选项，用于 mimics 真实站点握手等场景，配置门槛高于普通 TLS。无论哪种，证书校验被关闭或主机名不匹配时，协议标签无法补救中间人风险。TLS 基础可参考 Cloudflare Learning 对握手与记录层的说明。</p>
<h2>flow 与 xtls-rprx-vision</h2>
<p>用户对象可设 <code>flow</code>：空值时走标准 TLS 代理；<code>xtls-rprx-vision</code> 启用文档所述 XTLS 模式，含内层握手随机填充。XTLS 仅在文档列出的组合下生效，例如 TCP+TLS/REALITY 时在满足条件下对 TLS 1.3 载荷做底层拷贝优化；客户端与服务端 flow 不一致会导致无法连接或功能降级。全局 <code>settings.flow</code> 为空字符串时还会作为 per-user flow 的默认值，配置时要注意空字符串无法「关掉」 flow 的行为。</p>
<h2>VLESS Encryption</h2>
<p><code>decryption</code> 字段不能留空；禁用需显式 <code>none</code>。启用时，文档描述由多段点分块构成握手方式、流量外观、会话票据与填充策略等，并要求服务端与客户端精确匹配。官方建议多数用户用 <code>xray vlessenc</code> 生成，以免手写出错。它在不受信链路上可提供独立于 TLS 的加密选项，但并不自动等价于「完全隐匿」。</p>
<h2>fallbacks 与 reverse</h2>
<p><code>fallbacks</code> 可将未识别流量导向其他端口，用于与 Web 服务共存；<code>reverse</code> 结构表示该用户的连接可用于简化反向代理隧道，并会禁用该用户的常规正向代理。功能组合错误可能导致非预期暴露或环路。</p>
<h2>客户端与服务端兼容性</h2>
<p>须使用同一文档版本的 core，并对齐 UUID、flow、传输层、加密块与 SNI 等字段。第三方图形客户端只是配置的壳，安全取决于 core 来源是否可验证、更新是否及时，以及订阅是否被篡改。不应把某个商业 App 名称与 VLESS 协议划等号。</p>
<h2>协议本身不保证什么</h2>
<ul>
<li>不保证出口节点不记录元数据或遵守隐私承诺。</li>
<li>不保证绕开所有运营商策略或长期可用。</li>
<li>不替代系统补丁、账户 2FA 与防钓鱼习惯。</li>
<li>不证明分享链接中的节点未被掉包或植入恶意路由。</li>
</ul>
<p>评估节点时，应把「协议名称」与「运营方、日志、客户端签名与更新节奏」分开核对；测评文章若只展示连通性而不说明外层 security 配置，参考价值有限。工具选型背景可读 <a href="/articles/choose-privacy-tools">如何选择隐私工具</a>；若你主要需要链路加密与路由语义，先厘清 <a href="/articles/network-traffic-encryption">网络流量加密</a> 分层再决定是否采用 VLESS 栈。</p>
<h2>与 DNS 及分流</h2>
<p>VLESS 栈本身不替你选择 DNS 解析路径；若路由规则只代理部分域名，其余查询仍可能暴露访问意图。搭配分流模板时，应同时检查系统 DNS、<code>routing</code> 规则与出口是否一致，避免「代理显示已连接但查询仍走本地运营商」的错位。</p>
""".strip()

data = {
    "what-is-wireguard": {
        "seo_title": "什么是 WireGuard：接口、Noise 握手与 Cryptokey 路由",
        "meta_description": "依据 WireGuard 官网解读 Interface、Peer、Noise_IKpsk2 握手与 Cryptokey Routing，涵盖 AllowedIPs、MTU、DNS、漫游与 keepalive 等部署要点。",
        "content_html": WIREGUARD_HTML,
        "faq_json": [
            {"q": "WireGuard 使用哪种 Noise 握手标识？", "a": "官方为 Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s，可选预共享密钥混入握手。"},
            {"q": "AllowedIPs 写错会怎样？", "a": "可能导致路由不指路隧道、Cryptokey 过滤丢弃合法包，或把不该走的流量导入隧道。"},
            {"q": "Persistent Keepalive 解决什么问题？", "a": "在 NAT 后维持 UDP 映射并触发定时通信，便于移动端 Endpoint 学习与握手。"},
            {"q": "WireGuard 能替代杀毒或防钓鱼吗？", "a": "不能。它保护隧道上的载荷；端点恶意软件与社工仍需独立防护。"},
        ],
        "sources_json": [
            {"title": "WireGuard", "url": "https://www.wireguard.com/"},
            {"title": "WireGuard: Protocol & Cryptography", "url": "https://www.wireguard.com/protocol/"},
            {"title": "WireGuard whitepaper (PDF)", "url": "https://www.wireguard.com/papers/wireguard.pdf"},
            {"title": "Noise Protocol Framework", "url": "https://noiseprotocol.org/noise.html"},
            {"title": "RFC 7539 ChaCha20-Poly1305", "url": "https://www.rfc-editor.org/rfc/rfc7539"},
            {"title": "RFC 7693 BLAKE2", "url": "https://www.rfc-editor.org/rfc/rfc7693"},
        ],
    },
    "common-cybersecurity-myths": {
        "seo_title": "常见网络安全误区：八个可核对的事实",
        "meta_description": "分八条拆解复杂密码、HTTPS、VPN 匿名、杀毒万能、无痕隐身、双重验证、系统更新与云同步备份等误区，每条给出误解、机理与可执行的核对动作，便于对照账户与设备现状。",
        "content_html": MYTHS_HTML,
        "faq_json": [
            {"q": "HTTPS 小锁能证明网站是品牌官方吗？", "a": "不能。小锁只表示与地址栏域名的 TLS 会话有效，不验证经营者身份。"},
            {"q": "开了 VPN 为什么还要在意登录账户？", "a": "VPN 主要改变网络路径；站点仍可通过 Cookie 与账号识别你。"},
            {"q": "短信双重验证够强吗？", "a": "优于单因子，但可被钓鱼实时转发；高价值账户宜升级到 FIDO2 类因子。"},
            {"q": "云盘同步文件夹算备份吗？", "a": "不算完整备份；误删与勒索会同步破坏，需要版本与离线副本。"},
        ],
        "sources_json": [
            {"title": "OWASP Authentication Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html"},
            {"title": "NIST SP 800-63B Digital Identity", "url": "https://pages.nist.gov/800-63-3/sp800-63b.html"},
            {"title": "Cloudflare Learning: What is HTTPS?", "url": "https://www.cloudflare.com/learning/ssl/what-is-https/"},
            {"title": "EFF Surveillance Self-Defense", "url": "https://ssd.eff.org/"},
            {"title": "CISA Cybersecurity Best Practices", "url": "https://www.cisa.gov/topics/cybersecurity-best-practices"},
            {"title": "Cloudflare Learning: What is a VPN?", "url": "https://www.cloudflare.com/learning/access-management/what-is-a-vpn/"},
        ],
    },
    "what-is-vless": {
        "seo_title": "什么是 VLESS：Xray 无状态承载与 TLS/REALITY",
        "meta_description": "依据 Xray 官方文档说明 VLESS 的无状态设计、UUID 认证、streamSettings、flow 与 xtls-rprx-vision、VLESS Encryption 及客户端兼容性边界，并澄清协议本身不保证匿名与节点可信。",
        "content_html": VLESS_HTML,
        "faq_json": [
            {"q": "VLESS 与 VMess 的关键区别是什么？", "a": "官方强调 VLESS 更轻量且无状态，不依赖系统时间；二者认证与配置字段不同。"},
            {"q": "能否在公网使用 security none？", "a": "文档要求除非私有可信链路或启用 VLESS Encryption，否则须配 TLS 等外层安全。"},
            {"q": "flow 配置不一致会怎样？", "a": "常见结果是握手失败或无法使用 XTLS 优化；两端须按文档对齐。"},
            {"q": "使用 VLESS 是否等于完全匿名？", "a": "不等于。出口运营方、账号行为与客户端供应链都会影响真实隐私效果。"},
        ],
        "sources_json": [
            {"title": "Xray docs: VLESS inbound (English)", "url": "https://xtls.github.io/en/config/inbounds/vless.html"},
            {"title": "Xray docs: VLESS inbound (Chinese)", "url": "https://xtls.github.io/config/inbounds/vless.html"},
            {"title": "Project X documentation", "url": "https://xtls.github.io/"},
            {"title": "Cloudflare Learning: What is TLS?", "url": "https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/"},
        ],
    },
}

out_path = Path(__file__).resolve().parent / "_phase4_priority.json"

ranges = {
    "what-is-wireguard": (2200, 3200),
    "common-cybersecurity-myths": (2200, 3200),
    "what-is-vless": (1800, 2600),
}

errors = []
for slug, item in data.items():
    pl = plain_len(item["content_html"])
    lo, hi = ranges[slug]
    if pl < lo or pl > hi:
        errors.append(f"{slug}: plain length {pl} not in [{lo},{hi}]")
    md = item["meta_description"]
    if len(md) < 70 or len(md) > 120:
        errors.append(f"{slug}: meta_description length {len(md)}")
    bad = check_forbidden(json.dumps(item, ensure_ascii=False))
    if bad:
        errors.append(f"{slug}: forbidden {bad}")

if errors:
    print("VALIDATION ERRORS:")
    for e in errors:
        print(" ", e)
    for slug in data:
        print(f"  {slug}: {plain_len(data[slug]['content_html'])}")
    raise SystemExit(1)

with out_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Wrote {out_path}")
for slug in data:
    print(f"  {slug}: plain={plain_len(data[slug]['content_html'])}, meta={len(data[slug]['meta_description'])}")
print("Forbidden phrases: none")
