# -*- coding: utf-8 -*-
"""Expand short articles with topic-specific sections; sync to production."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import paramiko

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"C:\Users\1\Documents\chinalanding")
JSON_PATH = ROOT / "tools" / "articles_all.json"

ADDONS: dict[str, str] = {
    "network-traffic-encryption": """
<h2>常见加密层分别保护什么</h2>
<p>HTTPS 主要保护浏览器与网站之间的内容；VPN 再包一层隧道，改变出口路径并加密整段隧道流量；设备磁盘加密保护的是本地存储。把这三层混为一谈，容易高估或低估某一工具的作用。</p>
<p>选型时先明确威胁模型：你担心的是咖啡馆旁路嗅探、运营商侧观察，还是设备丢失后的本地数据？不同问题对应不同措施，没有“一个开关解决全部”。</p>
<h2>如何验证加密是否生效</h2>
<ul>
<li>网站地址栏是否显示 HTTPS，证书主体是否匹配域名。</li>
<li>若使用隧道工具，确认客户端状态为已连接，并抽查 DNS 是否仍走预期解析器。</li>
<li>对敏感操作，优先使用官方客户端或官方网页，避免第三方“加速器”夹带未知代理。</li>
</ul>
""",
    "what-is-vless": """
<h2>VLESS 适合理解的边界</h2>
<p>VLESS 是一种轻量传输协议思路，常出现在自建代理讨论中。对普通读者而言，关键不是背诵字段，而是明白：协议只是传输层选择之一，账号安全、客户端来源与节点运营方可信度同样决定风险。</p>
<p>若你只是想理解网络隐私工具，先掌握 VPN、WireGuard、HTTPS 与 DNS 泄露即可；深入到具体代理协议时，务必使用可核验来源的客户端，并避免把“能连通”当成“已安全”。</p>
<h2>自建与托管的取舍</h2>
<p>自建更可控，但需要持续维护证书、更新与访问策略；托管更省事，却意味着信任服务商。无论哪条路，都不要在聊天群随意下载“破解客户端”，也不要向不明脚本粘贴密钥。</p>
""",
    "what-is-dns-leak": """
<h2>DNS 泄露为什么容易被忽略</h2>
<p>很多人只盯着“IP 是否变化”，却忽略查询域名的解析路径。若 DNS 仍走本地运营商解析器，浏览意图可能在隧道之外被观察到。检查泄露，比争论品牌口号更有用。</p>
<h2>降低泄露的实用步骤</h2>
<ul>
<li>在系统或路由器中指定可信的加密 DNS（如支持 DoH/DoT 的解析器），并确认浏览器未被扩展劫持。</li>
<li>使用隧道时，开启客户端的“阻止非隧道 DNS”或同类选项（名称因软件而异）。</li>
<li>用可信的泄露检测页做抽查，但不要把单次测试结果当成永久保证——系统更新或新应用可能改回默认解析。</li>
</ul>
""",
    "vpn-vs-proxy": """
<h2>怎么选：看流量范围与信任边界</h2>
<p>代理通常作用于单个应用或浏览器；VPN 类隧道更接近系统级路径变更。代理配置灵活，但容易漏掉其他应用；系统隧道覆盖更广，却也意味着你把更多流量交给同一出口运营方。</p>
<p>若目标是保护公共 Wi-Fi 上的传输，优先考虑可信的系统级加密隧道，并同时确认网站使用 HTTPS。若只是临时访问某个区域资源，明确知道风险后再使用应用级代理，并限制其权限。</p>
<h2>共同风险</h2>
<p>无论 VPN 还是代理，日志政策、管辖权、客户端供应链与杀开关（断网保护）都比营销页面上的“军事级加密”更值得核对。付费不等于无日志，免费更要审查商业模式。</p>
""",
    "protect-digital-identity": """
<h2>数字身份由哪些凭证组成</h2>
<p>邮箱、手机号、政府证件扫描件、社交账号与支付账户共同构成可被拼接的身份画像。任意一环泄露，都可能被用于重置其他账户。因此“只保护密码”远远不够。</p>
<h2>降低被冒用的优先动作</h2>
<ul>
<li>邮箱开启双重验证，并检查陌生转发规则与应用专用密码。</li>
<li>为重要账户使用独立强密码，存放于密码管理器。</li>
<li>减少在非必要场景提交证件照片；必须提交时确认对方是官方渠道。</li>
<li>定期查看登录设备列表，注销长期不用的会话。</li>
</ul>
""",
    "identify-malicious-websites": """
<h2>除了看网址，还要看什么</h2>
<p>仿冒站常利用相似域名、紧急话术与伪造客服窗口。单靠“有没有小锁”不够——仿冒站也可以上 HTTPS。更可靠的是：从官方收藏或应用内入口进入，核对域名拼写，并对索要验证码、转账、远程控制的请求保持怀疑。</p>
<h2>遇到可疑页面时</h2>
<ul>
<li>不要在该页输入密码或验证码；改用官方 App 或手动输入已知域名。</li>
<li>若已输入，立刻在另一台可信设备上修改密码并撤销会话。</li>
<li>向平台或银行官方渠道报告，而不是回复页面上的“客服”联系方式。</li>
</ul>
""",
    "zero-trust-security": """
<h2>零信任对个人用户意味着什么</h2>
<p>企业零信任强调持续验证、最小权限与分段访问。落到个人场景，可以简化为：不默认信任内网或“已经登录过”；每个敏感操作都再确认一次身份与上下文。</p>
<p>实践上包括：不同用途分账户、远程访问不开永久端口、共享链接设过期时间、给每个应用最小权限。零信任不是买某一产品，而是减少“一次信任、长期敞开”的习惯。</p>
""",
    "what-is-ip-address": """
<h2>IP 能说明什么、不能说明什么</h2>
<p>IP 可大致指向网络接入位置与运营商，常被用于风控、限流与日志关联。它通常不能精确到门牌，也不等于“掌握了你的全部身份”。把 IP 绝对化，容易误判隐私风险。</p>
<p>若你关心出口地址暴露，可结合加密 DNS、HTTPS 与可信隧道理解分层保护；同时记住：登录账号、浏览器指纹与支付信息往往比 IP 更能识别个人。</p>
""",
    "safe-public-network-use": """
<h2>公共网络上的最小安全集</h2>
<ul>
<li>避免在公共 Wi-Fi 进行大额转账或提交证件；若必须，使用可信隧道并确认 HTTPS。</li>
<li>关闭自动连接未知热点；不要在门户页输入与热点无关的账户密码。</li>
<li>用完后忘记该网络，并检查是否仍开着文件共享。</li>
</ul>
<p>手机热点或离线办理敏感事务，往往比“将就用咖啡馆免费网”更稳妥。</p>
""",
    "how-online-tracking-works": """
<h2>常见追踪信号</h2>
<p>Cookie、像素、本地存储、广告标识符与浏览器指纹可在站点之间拼接行为。清除 Cookie 有帮助，但指纹与账号登录状态仍可能延续识别。</p>
<p>降低追踪的务实组合：限制第三方 Cookie、审查扩展权限、按场景使用容器或不同浏览器配置，并对“一键登录”保持克制。完全隐身很难；目标应是减少不必要的长期标识。</p>
""",
    "protect-online-accounts": """
<h2>账户失守后的常见连锁</h2>
<p>攻击者拿到邮箱后，常继续重置云盘、社交与支付。保护顺序应是：先邮箱与密码管理器，再金融与身份类服务，最后娱乐账号。</p>
<p>为每个重要账户保存恢复码离线副本；不要只依赖短信验证。发现异常登录时，先终止会话，再改密并检查转发规则与授权应用。</p>
""",
    "windows-network-security-settings": """
<h2>Windows 上值得先核对的项</h2>
<ul>
<li>系统与驱动更新是否自动；防火墙是否被不明软件关闭。</li>
<li>专用/公用网络配置文件是否正确，公用网络应限制发现与共享。</li>
<li>远程桌面若不用就关闭；必要开启时配合强认证与网络限制。</li>
<li>启动项与计划任务中是否有陌生联网程序。</li>
</ul>
""",
    "protect-mobile-data": """
<h2>手机数据保护清单</h2>
<ul>
<li>使用强锁屏与系统更新；避免给不明应用“无障碍”或设备管理员权限。</li>
<li>备份加密开启；淘汰设备前恢复出厂并确认云会话退出。</li>
<li>应用只从官方商店安装；定期清理长期未用且索权过多的 App。</li>
</ul>
""",
    "how-dns-servers-work": """
<h2>为什么 DNS 选择影响隐私与可用性</h2>
<p>解析器看到你查询的域名，也可能过滤或劫持结果。选择支持加密传输（DoH/DoT）且政策清晰的解析器，可降低路径上的窥探与篡改风险，但无法替代 HTTPS 对内容的保护。</p>
<p>企业或家庭路由统一配置，比每台设备各设一套更不易遗漏。变更后用多个域名测试解析是否正常，并保留回退方案。</p>
""",
    "why-data-encryption-matters": """
<h2>静态加密与传输加密</h2>
<p>磁盘/备份加密应对设备丢失；TLS/HTTPS 应对传输途中窃听。两者互补。云同步若只加密传输、服务端可明文处理，则运营方与其被攻破面仍可见内容——端到端加密产品对此有不同承诺，阅读条款时要分清。</p>
""",
    "choose-secure-network-connection": """
<h2>连接选型的快速决策</h2>
<p>家庭宽带：路由器改默认密码、固件更新、访客网络隔离物联网设备。移动网络：警惕伪基站话术与陌生安装包。公共 Wi-Fi：默认不信任，敏感操作叠加 HTTPS 与可信隧道。公司网络：遵守策略，不把私人账户永久登录在公用设备上。</p>
""",
    "check-network-security": """
<h2>家庭网络自检顺序</h2>
<ul>
<li>路由器管理页是否仍为默认口令；WAN/LAN 是否暴露不必要的远程管理。</li>
<li>已连接设备列表是否有陌生主机；物联网设备是否隔离。</li>
<li>DNS 是否被篡改；固件是否多年未更新。</li>
</ul>
<p>发现问题先改密、踢出陌生设备，再考虑更复杂的网段划分。</p>
""",
    "prevent-personal-data-leaks": """
<h2>数据最小化原则</h2>
<p>能不填的身份证号、地址与通讯录就不要填；能用临时邮箱或虚拟号的场景优先考虑。泄露往往来自“顺手授权”和“多年未清理的云盘链接”，而不是高深攻击。</p>
<p>每季度花十五分钟：检查网盘分享、社交可搜索性、已授权应用列表，并删除过期文件。</p>
""",
}

FAQ_EXTRA: dict[str, list[dict]] = {
    "network-traffic-encryption": [
        {"q": "只有公共 Wi-Fi 才需要加密吗？", "a": "不是。任何可能被中间观察或篡改的路径都值得用 HTTPS；隧道工具则按威胁模型选用。"},
        {"q": "如何判断自己被中间人攻击？", "a": "证书告警、异常登录、强制降级到不安全连接都是信号，应停止输入并改走官方渠道。"},
    ],
    "what-is-vless": [
        {"q": "VLESS 等于 VPN 吗？", "a": "不等同。它更接近代理/隧道协议讨论范畴，具体安全取决于实现、部署与运营方。"},
        {"q": "普通用户必须学协议细节吗？", "a": "不必。先掌握账户安全、HTTPS、DNS 与可信客户端来源，收益通常更大。"},
    ],
    "what-is-dns-leak": [
        {"q": "换了 VPN 就一定没有 DNS 泄露？", "a": "不一定。取决于客户端是否强制隧道内 DNS，以及系统/浏览器是否另有解析路径。"},
        {"q": "加密 DNS 能隐藏访问的网站内容吗？", "a": "不能。它主要保护查询过程；页面内容仍靠 HTTPS 等传输加密。"},
    ],
    "vpn-vs-proxy": [
        {"q": "浏览器代理够用吗？", "a": "仅保护该浏览器流量。其他应用仍可能直连，需按需求选择覆盖范围。"},
        {"q": "杀开关有什么用？", "a": "隧道断开时阻止流量泄露到默认网络，降低短暂暴露风险。"},
    ],
}


def plain_len(html: str) -> int:
    return len(re.sub(r"<[^>]+>", "", html or ""))


def normalize_faq(raw) -> list:
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except Exception:
            raw = []
    return list(raw or [])


def expand_local() -> list[dict]:
    arts = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    changed = []
    for a in arts:
        slug = a["slug"]
        before = plain_len(a.get("content_html", ""))
        addon = ADDONS.get(slug, "").strip()
        if addon and addon not in a["content_html"]:
            a["content_html"] = a["content_html"].rstrip() + "\n" + addon
        faqs = normalize_faq(a.get("faq_json"))
        for extra in FAQ_EXTRA.get(slug, []):
            if not any(x.get("q") == extra["q"] for x in faqs):
                faqs.append(extra)
        a["faq_json"] = faqs
        after = plain_len(a["content_html"])
        if after != before or slug in FAQ_EXTRA:
            changed.append((slug, before, after))
    JSON_PATH.write_text(json.dumps(arts, ensure_ascii=False, indent=2), encoding="utf-8")
    return arts, changed


def push_prod(arts: list[dict]) -> None:
    payload = [
        {
            "slug": a["slug"],
            "content_html": a["content_html"],
            "faq_json": a["faq_json"] if isinstance(a["faq_json"], str) else json.dumps(a["faq_json"], ensure_ascii=False),
            "sources_json": a["sources_json"]
            if isinstance(a.get("sources_json"), str)
            else json.dumps(a.get("sources_json") or [], ensure_ascii=False),
        }
        for a in arts
        if a["slug"] in ADDONS or a["slug"] in FAQ_EXTRA
    ]
    remote_json = "/tmp/expand_articles.json"
    remote_php = "/tmp/expand_articles.php"
    local_tmp = ROOT / "tools" / "_expand_payload.json"
    local_tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    php = r'''<?php
$config = require '/var/www/chinalanding/config/config.php';
$pdo = new PDO($config['db']['dsn'], $config['db']['user'], $config['db']['password'], [PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
$rows = json_decode(file_get_contents('/tmp/expand_articles.json'), true);
$upd = $pdo->prepare('UPDATE articles SET content_html=?, faq_json=?, sources_json=?, updated_at=NOW() WHERE slug=?');
$n=0;
foreach ($rows as $r) {
  $upd->execute([$r['content_html'], $r['faq_json'], $r['sources_json'], $r['slug']]);
  $n += $upd->rowCount();
}
echo "updated_rows=$n count=".count($rows)."\n";
$q=$pdo->query("SELECT slug, CHAR_LENGTH(REGEXP_REPLACE(content_html,'<[^>]+>','')) AS n FROM articles WHERE slug IN ('".implode("','", array_column($rows,'slug'))."') ORDER BY n");
foreach($q as $row) echo $row['n']."\t".$row['slug']."\n";
'''

    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect("94.249.188.139", username="root", password="qweasd333123", timeout=20, look_for_keys=False, allow_agent=False)
    s = c.open_sftp()
    s.put(str(local_tmp), remote_json)
    with s.file(remote_php, "w") as f:
        f.write(php)
    s.close()
    stdin, stdout, stderr = c.exec_command(f"php {remote_php}")
    print((stdout.read() + stderr.read()).decode("utf-8", "replace"))
    c.close()


def main() -> None:
    arts, changed = expand_local()
    print("local_changed", len(changed))
    for slug, b, a in changed:
        print(f"  {slug}: {b} -> {a}")
    push_prod(arts)
    print("done")


if __name__ == "__main__":
    main()
