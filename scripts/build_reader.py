#!/usr/bin/env python3
"""Build the static reader and Markdown cards from reviewed guide data."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'guide/cards.json').read_text(encoding='utf-8'))
POLICY = {c['id']: c for c in json.loads((ROOT / 'references/policy-cards.json').read_text(encoding='utf-8'))['cards']}
UPDATES = {s['id']: s for s in DATA['updates']}
CHAPTERS = {'P01':'第六十二章第一节','P02':'第六十二章第二节','P03':'第四章第一节','P04':'第五章第一节','P05':'第五章第二节','P06':'第六章第一节','P07':'第十三章第一节','P22':'第四十章第一节','P23':'第四十一章第二节'}
REPO = DATA['repository']
RELEASE = REPO + '/releases/download/v0.2.1/'
BASE = DATA['reader_url']
e = html.escape


def list_html(items, ordered=False):
    tag = 'ol' if ordered else 'ul'
    return f'<{tag}>' + ''.join(f'<li>{e(s)}</li>' for s in items) + f'</{tag}>'


def prompt(card):
    return (f"我在参考《{DATA['title']}》第{card['id']}张卡：{card['title']}。\n"
            "我的城市：____；已有能力与作品：____；可投入时间和预算：____；目前考虑的两个选择：____。\n"
            "请使用 china-five-year-plan-skill（如未安装请明确说明），核对当前官方依据，分别判断政策关联、真实需求、付款方、能力与时机。\n"
            "比较两个现实选项，列出最大证据缺口、一个两周验证动作和停止条件。查不到的留空，不编补贴、工资或订单。\n"
            f"参考卡片：{BASE}cards/{card['slug']}.html")


def source_html(card):
    parts = []
    for pid in card['policy_ids']:
        policy = POLICY[pid]
        for ref in policy['source_refs']:
            parts.append(f'<div class="evidence"><span class="fact-label">规划原文</span><p>“{e(ref["quote_zh"])}”</p><p class="source"><a href="{DATA["source_url"]}" target="_blank" rel="noopener">《十五五规划纲要》{e(CHAPTERS[pid])} ↗</a></p></div>')
    for uid in card['update_ids']:
        s = UPDATES[uid]
        parts.append(f'<div class="evidence"><span class="fact-label">相关文件</span><p>{e(s["summary"])}</p><p class="source"><a href="{s["url"]}" target="_blank" rel="noopener">《{e(s["title"])}》 ↗</a><br>{e(s["issuer"])}，{e(s["document_date"])}。参见{e(s["locator"])}。</p><p class="source">{e(s["scope"])}</p></div>')
    return ''.join(parts)


def shell(title, description, body, prefix='', canonical='', script=True):
    safe_data = json.dumps(DATA, ensure_ascii=False).replace('<', '\\u003c')
    scripts = f'<script id="guide-data" type="application/json">{safe_data}</script><script src="{prefix}app.js" defer></script>' if script else ''
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#254d3c"><link rel="canonical" href="{canonical or BASE}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="article"><link rel="stylesheet" href="{prefix}style.css"></head>
<body>{body}{scripts}<div id="toast" class="toast" role="status" hidden></div></body></html>'''


def header(prefix=''):
    return f'<div class="wrap"><header class="topbar"><a class="brand" href="{prefix}index.html"><span class="mark">五</span>未来五年 · 决策参考</a><nav class="nav" aria-label="主导航"><a href="{prefix}index.html#cases">读案例</a><a href="{prefix}index.html#downloads">下载</a><a class="desktop" href="{REPO}" target="_blank" rel="noopener">GitHub ↗</a></nav></header></div>'


def footer(prefix=''):
    return f'<div class="wrap"><footer class="footer"><p>独立开源项目 · xingyou1439 · MIT<br>v{DATA["version"]} · 内容核验 {DATA["reviewed"]}<br>5个构造场景，商业需求与个人适配待验证。</p><div class="footer-links"><a href="{REPO}/blob/codex/initial-release/SOURCE_NOTICE.md">来源说明</a><a href="{REPO}/issues/new?template=guide-feedback.yml">反馈与纠错</a><a href="{REPO}/blob/codex/initial-release/README.en.md">English</a></div></footer></div>'


def detail(card):
    blocks = f'''{header('../')}<main class="wrap detail" data-card="{card['id']}"><a class="back" href="../index.html#cases">← 返回全部案例</a><p class="eyebrow" style="margin:24px 0 0">DECISION {card['id']} / {e(card['topic'])}</p><h1>{e(card['title'])}</h1><p class="lead">{e(card['lead'])}</p><div class="status"><div><strong>场景性质</strong>构造示例</div><div><strong>政策关联</strong>{'条件性关联' if card['id']=='05' else '方向相关'}</div><div><strong>市场与准入</strong>具体情况待验证</div></div><p>{e(card['judgment'])}</p><div class="actions"><button class="btn" data-save="{card['id']}" aria-pressed="false">加入我的验证清单</button><button class="btn secondary" data-share="{card['id']}">复制卡片链接</button><a class="btn secondary" href="{RELEASE}decision-card-{card['id']}.png" download>下载分享图 ↓</a></div>
<div class="block"><h2>从你的情况出发</h2><p>{e(card['situation'])}</p></div>
<div class="block"><h2>规划里怎么说</h2>{source_html(card)}<p class="boundary">资料整理于{DATA['reviewed']}。具体地区后续的实施、项目和采购条件，还要另查。</p></div>
<div class="block"><h2>你可以从哪里入手</h2><p>{e(card['interpretation'])}</p>{list_html(card['roles'])}</div>
<div class="block"><h2>谁可能付款</h2><p>{e(card['payer'])}</p><h3>要准备什么</h3><p>{e(card['capability'])}</p><h3>先查清这件事</h3><p>{e(card['gap'])}</p></div>
<div class="block"><h2>接下来两周怎么试</h2><p>以下人数和时间可按实际资源调整。</p>{list_html(card['steps'],True)}<div class="twocol"><div class="good"><h3>有这些进展，再继续</h3><p>{e(card['success'])}</p></div><div class="stop"><h3>出现这些情况，先停一停</h3><p>{e(card['stop'])}</p></div></div><p class="boundary">{e(card['boundary'])}</p></div>
<div class="block"><h2>带入你的情况再分析</h2><p>填上自己的条件，复制到已安装 Skill 的助手中。这里提供提问模板，不在网页内调用模型。</p><pre class="prompt" id="prompt-{card['id']}">{e(prompt(card))}</pre><div class="actions"><button class="btn" data-prompt="{card['id']}">复制提问</button><a class="btn secondary" href="{REPO}#安装与使用">安装 Skill ↗</a></div></div></main>{footer('../')}'''
    return shell(card['title']+'｜未来五年决策参考',card['lead'],blocks,'../',BASE+'cards/'+card['slug']+'.html')


def markdown(card):
    lines=[f'# {card["title"]}', '', f'v{DATA["version"]} · 资料整理于{DATA["reviewed"]}', '', '> 以下是假设案例，请结合自己的情况使用。', '', card['lead'], '', '## 从你的情况出发', '',card['situation'],'',card['judgment'],'','## 规划里怎么说','']
    for pid in card['policy_ids']:
        for ref in POLICY[pid]['source_refs']:
            lines += [f'- “{ref["quote_zh"]}”——[《十五五规划纲要》{CHAPTERS[pid]}]({DATA["source_url"]})。']
    lines+=['']
    for uid in card['update_ids']:
        s=UPDATES[uid]
        lines += [f'- [《{s["title"]}》]({s["url"]})，{s["issuer"]}，{s["document_date"]}。参见{e(s["locator"])}。{s["summary"]} {s["scope"]}']
    for title,key in [('你可以从哪里入手','interpretation'),('谁可能付款','payer'),('要准备什么','capability'),('先查清这件事','gap')]:
        lines+=['',f'## {title}','',card[key]]
        if key=='interpretation':lines+=['']+['- '+r for r in card['roles']]
    lines+=['','## 接下来两周怎么试','','以下人数和时间可按实际资源调整。','']+[f'{i}. {s}' for i,s in enumerate(card['steps'],1)]
    for title,key in [('有这些进展，再继续','success'),('出现这些情况，先停一停','stop'),('使用提醒','boundary')]:lines+=['',f'**{title}：** {card[key]}']
    lines+=['','## 个性化提问','','```text',prompt(card),'```','']
    return '\n'.join(lines)


def share(card):
    policy_text=' / '.join('“'+POLICY[p]['source_refs'][0]['quote_zh']+'”' for p in card['policy_ids'])
    body=f'''<main class="share-sheet"><div class="card-meta"><span class="share-tag">未来五年 · 机会与避坑指南</span><span class="num">{card['id']} / 05</span></div><h1 class="share-title">{e(card['title'])}</h1><p class="share-lead">{e(card['lead'])}</p><div class="share-block"><h2>01 / 规划里怎么说</h2><p>{e(policy_text)}</p><div class="share-source"><a href="{DATA['source_url']}">《十五五规划纲要》{e(card['chapter'])}</a></div></div><div class="share-block"><h2>02 / 谁可能付款</h2><p>{e(card['payer'])}</p></div><div class="share-block"><h2>03 / 今天能做的一步</h2><p>{e(card['steps'][0])}</p></div><div class="share-block"><h2>04 / 什么时候先停下</h2><p>{e(card['stop'])}</p></div><div class="share-foot"><img class="share-qr" src="qr-{card['id']}.svg" alt="扫码打开完整决策卡">假设案例，请结合自己的情况使用。<br>作者 xingyou1439 · v{DATA['version']} · 资料整理于{DATA['reviewed']}<br><a href="{BASE}cards/{card['slug']}.html">扫码或点击，查看完整决策卡 ↗</a></div></main>'''
    return shell(card['title'],card['lead'],body,'../',BASE+'cards/'+card['slug']+'.html',False)


def main():
    site=ROOT/'site'
    teasers=''
    for c in DATA['cards']:
        teasers+=f'''<article class="teaser" data-audience="{e('|'.join(c['audience']))}" id="case-{c['id']}"><div class="card-meta"><span class="num">{c['id']}</span><span>{e(c['topic'])} · 构造场景</span></div><h3><a href="cards/{c['slug']}.html" style="text-decoration:none">{e(c['title'])}</a></h3><p>{e(c['lead'])}</p><div class="teaser-bottom"><a href="cards/{c['slug']}.html">看依据与两周动作 →</a><button class="bookmark" data-save="{c['id']}" aria-pressed="false">加入清单 ＋</button></div></article>'''
        (site/'cards'/f'{c["slug"]}.html').write_text(detail(c),encoding='utf-8')
        (site/'cards'/f'share-{c["id"]}.html').write_text(share(c),encoding='utf-8')
        (ROOT/'guide'/f'card-{c["id"]}.md').write_text(markdown(c),encoding='utf-8')
    filters=''.join(f'<button class="filter" data-filter="{s}" aria-pressed="{"true" if s=="全部" else "false"}">{s}</button>' for s in ['全部','准备创业','培训与咨询','技术与交付','行业从业者'])
    body=f'''{header()}<main class="wrap"><div class="hero"><div><div class="eyebrow">2026 → 2030 / 从政策到个人选择</div><h1>未来五年，<br>普通人的<em>机会</em><br>与避坑指南。</h1><p class="intro">基于十五五规划，帮你看清可以服务谁、交付什么，以及下一步先验证什么。每项判断附出处、参与门槛与停止条件。</p><div class="actions"><a class="btn" href="#cases">先看与我有关的案例 ↓</a><a class="btn secondary" href="{RELEASE}five-year-guide-v0.2.1.pdf">免费下载短版 PDF ↗</a></div><p class="tiny">无需安装即可阅读 · 免费开源 · 2026年10月18日核验</p></div><aside class="diagram"><div class="eyebrow">把大方向，拆到能行动的一步</div><h2>你的下一步，<br>走到哪一环了？</h2><div class="chain"><div><b>01</b><span>政策方向</span><span>找原文</span></div><div><b>02</b><span>实施工具与项目</span><span>查落实</span></div><div><b>03</b><span>客户与付款方</span><span>问采购</span></div><div><b>04</b><span>你能交付的任务</span><span>看能力</span></div><div><b>05</b><span>两周验证与停止条件</span><span>小步试</span></div></div><p class="tiny">找不到的一环，先留空。把缺口查清，本身就是有用的结果。</p></aside></div><div class="rail"><div><strong>先读 5 个具体问题</strong><span>按你已有的能力选</span></div><div><strong>分开看两种判断</strong><span>政策依据与商业假设</span></div><div><strong>带走一份验证清单</strong><span>先做一个小实验</span></div></div>
<section id="cases"><div class="section-head"><div><div class="eyebrow">01 / 找到你的起点</div><h2>从眼前的问题开始。</h2></div><p>以下均为构造场景。政策引文已与所用文本核对；客户、付款与个人适配需要继续验证。</p></div><div class="filters" aria-label="按已有能力筛选">{filters}</div><p id="result-count" class="tiny" aria-live="polite">显示全部5个案例</p><div class="card-grid">{teasers}</div></section>
<section><div class="section-head"><div><div class="eyebrow">02 / 读懂判断</div><h2>依据与机会，逐项看清。</h2></div></div><div class="method"><div><div class="method-number">01</div><h3>政策到底说了什么</h3><p>用书名、章节和原文链接说明依据。补充文件保留影响判断的日期、地区和适用范围。</p></div><div><div class="method-number">02</div><h3>哪些仍然是假设</h3><p>服务设想和行动建议还需要实际验证。先核实付款、采购条件和你的交付能力。</p></div><div><div class="method-number">03</div><h3>先验证，再扩大投入</h3><p>设一个两周能完成的小动作，同时写下继续与停止条件。周期和数量是建议值。</p></div></div></section>
<section id="plan"><div class="plan"><div class="plan-head"><div><div class="eyebrow">03 / 带走下一步</div><h2>我的两周验证清单</h2></div><span class="tiny">保存在当前浏览器，可下载留存</span></div><p id="plan-empty">从上方选择一张卡，先验证一个问题。这里的记录不会上传到服务器。</p><ul class="selected-list" id="selected-list"></ul><div class="form-grid"><label>我的城市与已有能力<input id="context" placeholder="例如：广州，有企业培训经验" maxlength="240"></label><label>这次最想查清的问题<input id="question" placeholder="例如：谁会采购一项询盘整理服务？" maxlength="240"></label><label>我愿意投入的时间与预算<textarea id="budget" placeholder="写一个能承受的试验上限" maxlength="500"></textarea></label><label>什么时候停止或调整<textarea id="stop" placeholder="例如：两周后仍找不到任务负责人，就换场景" maxlength="500"></textarea></label></div><div class="actions"><button class="btn" id="export-plan">下载我的验证清单 ↓</button><button class="btn secondary" id="clear-plan">清空本机记录</button></div><p class="tiny" id="storage-note">记录仅存当前浏览器。换设备或清理浏览器后可能丢失，请下载留存。</p></div></section>
<section id="downloads"><div class="section-head"><div><div class="eyebrow">04 / 继续使用</div><h2>先阅读，再带入你的情况。</h2></div><p>公开内容可按 MIT 许可转载、改编，保留作者、来源和版本日期。</p></div><div class="download-row"><div class="download-block"><h3>短版指南与分享图</h3><p>5张决策卡、判断方法、验证工作纸与官方出处。适合发给正在考虑转型或小生意的朋友。</p><a class="btn" href="{RELEASE}five-year-guide-v0.2.1.pdf">下载 PDF ↗</a><br><a href="{REPO}/releases/tag/v0.2.1">下载分享图与发布包 →</a></div><div class="download-block"><h3>用 AI 分析自己的选择</h3><p>完整 Skill 保留十三五至十五五对照，以及国内决策、Understanding China 和市场进入路径。</p><a class="btn secondary" href="{REPO}#安装与使用">查看安装方法 ↗</a><br><a href="{REPO}/issues/new?template=guide-feedback.yml">反馈：它改变了你的哪个判断？ →</a></div></div></section></main>{footer()}'''
    (site/'index.html').write_text(shell(DATA['title'],DATA['subtitle'],body),encoding='utf-8')
    (site/'.nojekyll').write_text('')
    lines=['# 未来五年普通人的机会与避坑指南','','基于十五五规划的职业与小生意决策参考。v0.2.1，核验日期2026-10-18。','','先选一个与你有关的问题，读依据、付款方与验证动作，再决定是否扩大投入。以下均为构造场景；商业需求和个人适配待验证。','']
    lines += [f'- [{c["title"]}](card-{c["id"]}.md)' for c in DATA['cards']]
    lines += ['',f'[手机阅读页]({BASE}) · [短版PDF]({RELEASE}five-year-guide-v0.2.1.pdf)','','## 如何转载与改编','','按项目MIT许可保留作者和许可声明，同时保留卡片编号、核验日期、官方来源及适用边界。新加的地区案例和市场数据请另列来源，不把推导改写成官方承诺。','','[内容与贡献规则](CONTRIBUTING.md) · [原始结构化内容](cards.json)','']
    (ROOT/'guide/README.md').write_text('\n'.join(lines),encoding='utf-8')
    print('Built reader, 5 detail pages, 5 share layouts and 5 Markdown cards.')


if __name__ == '__main__':
    main()
