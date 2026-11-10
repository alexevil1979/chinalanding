# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

import paramiko

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

META = {
    "what-is-vpn": "从隧道封装、加密、DNS、出口 IP 与元数据边界解释 VPN 工作原理，并说明服务商角色、典型威胁模型，以及它无法替代的账户与设备安全措施。",
    "what-is-wireguard": "依据官方协议解读 WireGuard 的 Noise 握手、Curve25519、ChaCha20-Poly1305、BLAKE2s、SipHash24、密钥轮换与 Cryptokey Routing 配置要点。",
    "what-is-vless": "根据 Xray 文档说明 VLESS 的无状态设计、与 VMess 差异、TLS/REALITY、flow 兼容性，以及协议本身不保证匿名或节点运营可信。",
    "vpn-vs-proxy": "比较 HTTP/SOCKS 代理与系统 VPN 在覆盖应用、默认加密、DNS 行为与信任边界上的差别，帮助按公共网络或多应用保护场景完成选型。",
    "what-is-dns-leak": "解释 VPN 场景下 DNS 仍走本地解析器的原因，说明 DoH/DoT 的传输保护边界，并给出区分预期分流与意外泄漏的检查与复测方法。",
    "network-traffic-encryption": "对比 TLS 应用会话与 VPN 网络隧道的保护范围，说明内容加密后仍可能暴露的时间、体积、DNS 与端点风险等元数据问题。",
    "protect-online-privacy": "从账号、设备、浏览器与网络分层给出可复查的隐私底线配置，说明登录态如何延长跨站追踪以及数据最小化的做法。",
    "public-wifi-safety": "分析公共 Wi-Fi 的旁路嗅探、恶意门户与假热点风险，并按操作敏感度组合 HTTPS、可信隧道与移动数据降低暴露。",
    "what-is-end-to-end-encryption": "厘清端到端加密与 HTTPS、云备份的差异，说明安全码核对、元数据残留，以及终端失陷时密码学防线仍会失效的边界。",
    "choose-privacy-tools": "用透明度、审计、权限、更新频率与可退出成本评估 VPN、密码管理器与加密通讯工具，避开绝对匿名等夸张承诺。",
    "protect-mobile-data": "从权限、锁屏、安装来源、云备份与换机擦除说明如何保护手机中的个人数据、支付会话与二次验证渠道。",
    "windows-network-security-settings": "梳理 Windows 公用网络配置文件、防火墙、远程桌面与系统更新设置，降低笔记本在陌生局域网被扫描与滥用的风险。",
    "why-data-encryption-matters": "区分传输加密、磁盘静态加密与端到端加密各自应对的威胁，强调密钥与恢复材料管理不当会让加密保护失效。",
    "protect-online-accounts": "围绕邮箱与密码管理器等枢纽账户，说明独立口令、双重验证、OAuth 授权与邮件转发规则的核查方法，降低连锁失守。",
    "protect-digital-identity": "说明邮箱、手机号与证件影像如何被拼成社工材料，并给出减少公开暴露、保护恢复渠道与处理冒名注册的做法。",
    "zero-trust-security": "用个人可读的语言解释零信任的核心假设，以及分段访问、链接过期与设备核对在家庭和小团队环境中的落地方式。",
    "safe-public-network-use": "从连接前核对热点、使用中按敏感度分级操作到离开后检查会话，给出机场商场等环境使用公共网络的安全习惯。",
    "choose-secure-network-connection": "按家庭、外出与办公场景比较蜂窝数据、家用 Wi-Fi、公共热点与公司隧道的信任差异，帮你选择更稳妥网络路径。",
    "browser-privacy-settings": "汇总浏览器自动更新、站点权限、第三方 Cookie、跟踪防护与扩展权限等设置，并建议按场景分离配置降低关联。",
    "what-is-ip-address": "解释公网与私网地址、动态租约及其在网站日志与风控中的作用，并说明 IP 与账号指纹、DNS 查询之间的区别。",
    "how-online-tracking-works": "介绍 Cookie、像素信标、设备指纹与登录态如何被拼接成跨站画像，并说明浏览器配置与账号隔离能削弱什么。",
    "how-dns-servers-work": "用递归查询与缓存解释 DNS 如何把域名映射到 IP，说明加密 DNS 能保护传输、解析服务运营商仍可见查询内容。",
    "check-network-security": "提供路由口令、固件、已连接设备清单、访客网段与 DNS 设置的家庭网络自查步骤，以及发现陌生终端后的处理。",
    "identify-malicious-websites": "从域名拼写、证书主体、恐吓话术与诱导安装等信号识别仿冒网站，提醒 HTTPS 小锁并不能证明品牌可信。",
    "identify-phishing-attacks": "介绍邮件与短信中的钓鱼及假冒付款指令，强调不在消息内点击登录，并用第二渠道确认账户变更或转账请求。",
    "create-strong-passwords": "强调足够长度与站点唯一性，说明密码管理器如何生成保管条目，以及泄露命中后应按枢纽账户优先轮换。",
    "two-factor-authentication-guide": "比较安全密钥、TOTP 应用与短信验证码的抗风险能力，说明恢复码备份以及邮箱等枢纽账户应优先启用。",
    "what-is-https": "解释 TLS 握手与证书链验证如何保护传输机密性与完整性，并说明它不能证明网站诚信，也不能隐藏 DNS 查询。",
    "prevent-personal-data-leaks": "从表单最小化、网盘外链治理到异常登录信号识别，列出个人数据泄露后的改密、下线会话与冻结支付止损步骤。",
    "common-cybersecurity-myths": "澄清没有重要数据、杀毒足够、HTTPS 等于可信等常见误区，并换成可逐项核对的账户加固与设备更新习惯清单。",
}

SEO = {
    "what-is-vpn": "什么是 VPN：隧道、加密、DNS 与威胁模型详解",
    "what-is-wireguard": "什么是 WireGuard：Noise、曲线与 Cryptokey Routing",
    "what-is-vless": "什么是 VLESS：Xray 定位、TLS/REALITY 与边界",
    "vpn-vs-proxy": "VPN 和代理有什么区别：覆盖范围与信任边界",
    "what-is-dns-leak": "什么是 DNS 泄露：原理、检测与缓解方法",
    "network-traffic-encryption": "什么是网络流量加密：TLS、隧道与元数据",
    "protect-online-privacy": "如何保护个人网络隐私：分层可执行指南",
    "public-wifi-safety": "公共 Wi-Fi 安全吗：风险分级与防护建议",
    "what-is-end-to-end-encryption": "什么是端到端加密：保护范围与局限说明",
    "choose-privacy-tools": "如何选择可靠的隐私保护工具：评估清单",
    "protect-mobile-data": "如何保护手机个人数据：权限、备份与换机",
    "windows-network-security-settings": "Windows 网络安全设置：公用网络与防火墙",
    "why-data-encryption-matters": "为什么数据加密重要：传输、静态与密钥",
    "protect-online-accounts": "如何保护在线账户：密码、验证与会话管理",
    "protect-digital-identity": "如何保护数字身份：减少暴露与防冒用",
    "zero-trust-security": "什么是零信任安全：个人可落地的原则",
    "safe-public-network-use": "如何安全使用公共网络：分级操作指南",
    "choose-secure-network-connection": "如何选择安全网络连接：家庭外出与办公",
    "browser-privacy-settings": "浏览器隐私设置指南：Cookie、权限与扩展",
    "what-is-ip-address": "什么是 IP 地址：公网私网与隐私关系",
    "how-online-tracking-works": "在线追踪如何运作：Cookie、指纹与登录态",
    "how-dns-servers-work": "DNS 服务器如何工作：解析路径与加密 DNS",
    "check-network-security": "如何检查家庭网络安全：路由与设备自检",
    "identify-malicious-websites": "如何识别恶意网站：域名、证书与话术信号",
    "identify-phishing-attacks": "如何识别钓鱼攻击：话术特征与应对步骤",
    "create-strong-passwords": "如何创建强密码：长度、唯一性与管理器",
    "two-factor-authentication-guide": "双重验证指南：密钥、TOTP 与短信选型",
    "what-is-https": "什么是 HTTPS：TLS、证书与它不能证明的事",
    "prevent-personal-data-leaks": "如何防止个人数据泄露：最小化与止损",
    "common-cybersecurity-myths": "常见网络安全误区：用清单替代口号",
}


def main() -> None:
    payload = []
    for slug, meta in META.items():
        n = len(meta)
        if n < 70 or n > 120:
            raise SystemExit(f"bad meta {slug}: {n} {meta}")
        payload.append({"slug": slug, "meta_description": meta, "seo_title": SEO[slug]})
        print(f"{n:3d} {slug}")

    path = Path(__file__).with_name("_meta_fix.json")
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    php = r'''<?php
$config=require "/var/www/chinalanding/config/config.php";
$pdo=new PDO($config["db"]["dsn"],$config["db"]["user"],$config["db"]["password"],[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
$rows=json_decode(file_get_contents("/tmp/meta_fix.json"),true);
$upd=$pdo->prepare("UPDATE articles SET seo_title=?, meta_description=?, updated_at=NOW() WHERE slug=?");
foreach($rows as $r)$upd->execute([$r["seo_title"],$r["meta_description"],$r["slug"]]);
echo "updated=".count($rows)."\n";
echo "bad=".$pdo->query("SELECT COUNT(*) FROM articles WHERE meta_description LIKE '%适合希望系统梳理概念%' OR CHAR_LENGTH(meta_description)<70 OR CHAR_LENGTH(meta_description)>120")->fetchColumn()."\n";
'''
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect("94.249.188.139", username="root", password="qweasd333123", timeout=25, look_for_keys=False, allow_agent=False)
    s = c.open_sftp()
    s.put(str(path), "/tmp/meta_fix.json")
    with s.file("/tmp/meta_fix.php", "w") as f:
        f.write(php)
    s.close()
    stdin, stdout, stderr = c.exec_command("php /tmp/meta_fix.php")
    print((stdout.read() + stderr.read()).decode("utf-8", "replace"))
    c.close()


if __name__ == "__main__":
    main()
