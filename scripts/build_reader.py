#!/usr/bin/env python3
# coding: utf-8
"""Build the static reader and Markdown cards from reviewed guide data."""
import html
import json
import re
from xml.etree import ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'guide/cards.json').read_text(encoding='utf-8'))
POLICY = {c['id']: c for c in json.loads((ROOT / 'references/policy-cards.json').read_text(encoding='utf-8'))['cards']}
UPDATES = {s['id']: s for s in DATA['updates']}
CHAPTERS = {'P01':'第六十二章第一节','P02':'第六十二章第二节','P03':'第四章第一节','P04':'第五章第一节','P05':'第五章第二节','P06':'第六章第一节','P07':'第十三章第一节','P22':'第四十章第一节','P23':'第四十一章第二节'}
REPO = DATA['repository']
RELEASE = REPO + '/releases/download/v0.3.0/'
BASE = DATA['reader_url']
e = html.escape
CARDS = {c['id']: c for c in DATA['cards']}


def related(card):
    return [CARDS[cid] for cid in card.get('related_ids', [])]


def related_html(card):
    items = ''.join(f'<li><a href="{e(c["slug"])}.html">{e(c["seo_title"])}</a></li>' for c in related(card))
    return f'<div class="block"><h2>继续比较相关选择</h2><p>把当前问题和相邻环节放在一起核对：</p><ul>{items}</ul></div>'


def sitemap():
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    doc = ET.Element(f'{{{ns}}}urlset')
    for url in [BASE, BASE + 'first-session.html'] + [BASE + 'cards/' + c['slug'] + '.html' for c in DATA['cards']]:
        ET.SubElement(ET.SubElement(doc, f'{{{ns}}}url'), f'{{{ns}}}loc').text = url
    return ET.tostring(doc, encoding='unicode', xml_declaration=True) + '\n'


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
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#254d3c"><link rel="canonical" href="{canonical or BASE}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="article"><meta property="og:url" content="{canonical or BASE}"><meta property="og:locale" content="zh_CN"><link rel="stylesheet" href="{prefix}style.css"></head>
<body>{body}{scripts}<div id="toast" class="toast" role="status" hidden></div></body></html>'''


def header(prefix=''):
    return f'<div class="wrap"><header class="topbar"><a class="brand" href="{BASE}"><span class="mark">五</span>十五五 · 决策参考</a><nav class="nav" aria-label="主导航"><a href="{BASE}#start">怎么用</a><a href="{BASE}#downloads">先阅读</a><a class="desktop" href="{REPO}" target="_blank" rel="noopener">GitHub 开源资料 ↗</a></nav></header></div>'


def footer(prefix=''):
    return f'<div class="wrap"><footer class="footer"><p>独立开源项目 · xingyou1439 · MIT<br>v{DATA["version"]} · 内容核验 {DATA["reviewed"]}<br>政策资料的日期和适用范围见来源说明。</p><div class="footer-links"><a href="{REPO}/blob/codex/initial-release/SOURCE_NOTICE.md">来源说明</a><a href="{REPO}/issues/new?template=guide-feedback.yml">反馈与纠错</a><a href="{REPO}/blob/codex/initial-release/README.en.md">English</a></div></footer></div>'


def detail(card):
    blocks = f'''{header('../')}<main class="wrap detail" data-card="{card['id']}"><a class="back" href="{BASE}#cases">← 返回十五五职业创业案例</a><p class="eyebrow" style="margin:24px 0 0">DECISION {card['id']} / 十五五规划 · {e(card['topic'])}</p><h1>{e(card['seo_title'])}</h1><p class="lead">{e(card['lead'])}</p><div class="status"><div><strong>场景性质</strong>构造示例</div><div><strong>政策关联</strong>{'条件性关联' if card['id']=='05' else '方向相关'}</div><div><strong>市场与准入</strong>具体情况待验证</div></div><p>{e(card['judgment'])}</p><div class="actions"><button class="btn" data-save="{card['id']}" aria-pressed="false">加入我的验证清单</button><button class="btn secondary" data-share="{card['id']}">复制卡片链接</button><a class="btn secondary" href="{RELEASE}decision-card-{card['id']}.png" download>下载分享图 ↓</a></div>
<div class="block"><h2>从你的情况出发</h2><p>{e(card['situation'])}</p></div>
<div class="block"><h2>规划里怎么说</h2>{source_html(card)}<p class="boundary">资料整理于{DATA['reviewed']}。具体地区后续的实施、项目和采购条件，还要另查。</p></div>
<div class="block"><h2>你可以从哪里入手</h2><p>{e(card['interpretation'])}</p>{list_html(card['roles'])}</div>
<div class="block"><h2>谁可能付款</h2><p>{e(card['payer'])}</p><h3>要准备什么</h3><p>{e(card['capability'])}</p><h3>先查清这件事</h3><p>{e(card['gap'])}</p></div>
<div class="block"><h2>接下来两周怎么试</h2><p>以下人数和时间可按实际资源调整。</p>{list_html(card['steps'],True)}<div class="twocol"><div class="good"><h3>有这些进展，再继续</h3><p>{e(card['success'])}</p></div><div class="stop"><h3>出现这些情况，先停一停</h3><p>{e(card['stop'])}</p></div></div><p class="boundary">{e(card['boundary'])}</p></div>
<div class="block"><h2>带入你的情况再分析</h2><p>填上自己的条件，复制到已安装 Skill 的助手中。这里提供提问模板，不在网页内调用模型。</p><pre class="prompt" id="prompt-{card['id']}">{e(prompt(card))}</pre><div class="actions"><button class="btn" data-prompt="{card['id']}">复制提问</button><a class="btn secondary" href="{REPO}#安装与使用">安装 Skill ↗</a></div></div>{related_html(card)}<div class="block"><p><a href="{REPO}/blob/codex/initial-release/guide/card-{card['id']}.md">查看这张决策卡的 GitHub 原文与版本记录 ↗</a></p></div></main>{footer('../')}'''
    return shell(card['seo_title'],card['seo_description'],blocks,'../',BASE+'cards/'+card['slug']+'.html')


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
    lines+=['','## 相关决策卡','']+[f'- [{c["seo_title"]}](card-{c["id"]}.md)' for c in related(card)]
    lines+=['',f'[在线阅读本卡]({BASE}cards/{card["slug"]}.html) · [返回全部决策卡](README.md)']
    lines+=['','## 个性化提问','','```text',prompt(card),'```','']
    return '\n'.join(lines)


def share(card):
    policy_text=' / '.join('“'+POLICY[p]['source_refs'][0]['quote_zh']+'”' for p in card['policy_ids'])
    body=f'''<main class="share-sheet"><div class="card-meta"><span class="share-tag">未来五年 · 机会与避坑指南</span><span class="num">{card['id']} / 05</span></div><h1 class="share-title">{e(card['title'])}</h1><p class="share-lead">{e(card['lead'])}</p><div class="share-block"><h2>01 / 规划里怎么说</h2><p>{e(policy_text)}</p><div class="share-source"><a href="{DATA['source_url']}">《十五五规划纲要》{e(card['chapter'])}</a></div></div><div class="share-block"><h2>02 / 谁可能付款</h2><p>{e(card['payer'])}</p></div><div class="share-block"><h2>03 / 今天能做的一步</h2><p>{e(card['steps'][0])}</p></div><div class="share-block"><h2>04 / 什么时候先停下</h2><p>{e(card['stop'])}</p></div><div class="share-foot"><img class="share-qr" src="qr-{card['id']}.svg" alt="扫码打开完整决策卡">假设案例，请结合自己的情况使用。<br>作者 xingyou1439 · v{DATA['version']} · 资料整理于{DATA['reviewed']}<br><a href="{BASE}cards/{card['slug']}.html">扫码或点击，查看完整决策卡 ↗</a></div></main>'''
    return shell(card['title'],card['lead'],body,'../',BASE+'cards/'+card['slug']+'.html',False)


def start_panel():
    return f'''<section id="start"><div class="section-head"><div><div class="eyebrow">第一次使用</div><h2>一句话，就可以开始。</h2></div><p>先选你想做的事，再复制到已安装 Skill 的助手。本页生成提问，不调用模型。</p></div>
<div class="intent-list" aria-label="你想做什么"><button class="intent" data-intent="understand" aria-pressed="true"><strong>看懂一个方向</strong><span>一个词、一项政策，或历次规划的变化</span></button><button class="intent" data-intent="compare" aria-pressed="false"><strong>比较两个选择</strong><span>转行、学技能，或一个创业想法</span></button><button class="intent" data-intent="act" aria-pressed="false"><strong>安排下一步</strong><span>已经有方向，找今天能做的一步</span></button></div>
<div class="composer"><div class="form-grid"><label>我现在做什么（可选）<input id="ask-context" maxlength="300" placeholder="例如：做了5年品牌营销"></label><label>我最近想弄清楚什么<input id="ask-question" maxlength="600" placeholder="例如：学AI能不能沿用我的经验？"></label></div><p class="tiny" id="intent-help" aria-live="polite">只想了解政策？直接填问题，不需要职业、城市和预算。</p>
<pre class="prompt" id="prompt-start">请使用 china-five-year-plan-skill。我最近想弄清楚____。
请先用容易理解的话解释，给出实际读取的政策依据、适用范围，以及一个继续了解的方向。
只追问会改变答案的信息。如果该 Skill 尚未安装，请直接说明。</pre><div class="actions"><button class="btn" data-prompt="start">复制我的提问</button><a class="btn secondary" href="{REPO}#安装与使用">安装 Skill ↗</a><a href="first-session.html">看一次完整使用演示 →</a></div><p class="tiny">这两个输入框的内容只用于本页生成提问，不上传、不保存。复制到助手后，由相应宿主处理。</p><noscript><p>脚本未启用：直接复制上面的模板，替换空白即可。</p></noscript></div>
<div class="answer-preview"><span class="eyebrow">你会先得到什么</span><h3>一个判断、一两条依据、最该查清的事。</h3><p>先给简短回答；需要时再展开。没有选项，先一起缩小方向；查不到，不编收入、补贴或订单。<a href="first-session.html#step-3">看看示范回答 →</a></p></div>
<details class="takeaway"><summary>分析之后：保存选择单，或带着新信息回来</summary><p>在助手里发送下面任一句。完整选择单留作私人记录；需要截图分享时，再请助手精简并自行复核。</p><pre class="prompt" id="prompt-note">请把刚才的分析整理成“我的职业与创业选择单”：选项、当前判断、带日期的政策依据、最大未知、找谁问什么、今天的一步、复盘与停止条件。未知写明，不补造信息。请提供可复制文本；可以写文件时，经我指定位置再保存。</pre><button class="btn secondary" data-prompt="note">复制：保存选择单</button><pre class="prompt" id="prompt-share">请把刚才的选择单精简为适合截图的分享版，删去个人条件与商业细节，保留判断、来源日期、关键不确定性、一个可执行动作和项目入口。我会复核后决定是否分享；请不要替我发布。</pre><button class="btn secondary" data-prompt="share">复制：生成分享版</button><pre class="prompt" id="prompt-return">请使用 china-five-year-plan-skill。这是上次的选择单：____。新了解到____，来源和时间是____。请说明哪些判断要改、哪些仍成立，更新下一步。如果未找到该 Skill，请直接说明。</pre><button class="btn secondary" data-prompt="return">复制：带新信息复盘</button></details>
<p class="boundary">具体岗位、需求、收入和经营条件，还要结合现实信息核实。资料时点和适用范围见引用，较新的实施文件需另查。</p></section>'''


def walkthrough():
    """Render the small, controlled Markdown walkthrough without adding a runtime dependency."""
    source = (ROOT/'examples/first-session.md').read_text(encoding='utf-8')
    def inline(text):
        text = e(text)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{e(REPO + "/blob/codex/initial-release/references/decision-note.md" if m[2] == "../references/decision-note.md" else html.unescape(m[2]), quote=True)}">{m[1]}</a>', text)
        return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    blocks = []
    for part in source.strip().split('\n\n'):
        if part.startswith('# '): blocks.append('<h1>' + inline(part[2:]) + '</h1>')
        elif part.startswith('## '):
            title = part[3:]; number = title.split('.')[0]
            blocks.append(f'<h2 id="step-{e(number)}">{inline(title)}</h2>')
        elif part.startswith('> '): blocks.append('<blockquote>' + inline(part[2:]) + '</blockquote>')
        else: blocks.append('<p>' + inline(part).replace('\n','<br>') + '</p>')
    body = header() + '<main class="wrap detail walkthrough"><a class="back" href="index.html#start">← 返回，开始自己的问题</a>' + ''.join(blocks) + '</main>' + footer()
    return shell('十五五规划怎么用？品牌营销转AI的完整提问与选择单演示', '从一句自己的情况开始，看怎样补问、查政策、比较选择、保存与复盘。构造示范，非收益案例。', body, canonical=BASE+'first-session.html')


def main():
    site=ROOT/'site'
    teasers=''
    for c in DATA['cards']:
        teasers+=f'''<article class="teaser" data-audience="{e('|'.join(c['audience']))}" id="case-{c['id']}"><div class="card-meta"><span class="num">{c['id']}</span><span>{e(c['topic'])} · 构造场景</span></div><h3><a href="cards/{c['slug']}.html" style="text-decoration:none">{e(c['title'])}</a></h3><p>{e(c['lead'])}</p><div class="teaser-bottom"><a href="cards/{c['slug']}.html">看依据与两周动作 →</a><button class="bookmark" data-save="{c['id']}" aria-pressed="false">加入清单 ＋</button></div></article>'''
        (site/'cards'/f'{c["slug"]}.html').write_text(detail(c),encoding='utf-8')
        (site/'cards'/f'share-{c["id"]}.html').write_text(share(c),encoding='utf-8')
        (ROOT/'guide'/f'card-{c["id"]}.md').write_text(markdown(c),encoding='utf-8')
    filters=''.join(f'<button class="filter" data-filter="{s}" aria-pressed="{"true" if s=="全部" else "false"}">{s}</button>' for s in ['全部','准备创业','培训与咨询','技术与交付','行业从业者'])
    body=f'''{header()}<main class="wrap">
<div class="hero"><div><div class="eyebrow">免费开源 AI Skill / 2026 → 2030</div><h1>看懂十五五，<br>想清楚你的<em>下一步</em>。</h1><p class="intro">想换方向、学技能，或试一个创业想法？把你的情况告诉 AI，结合十三五、十四五与十五五规划，比较现实选项，找出下一步需要查清的事。</p><p>这套 Skill 是给 AI 助手使用的分析方法和参考资料。安装一次，之后用自己的问题开始。</p><div class="actions"><a class="btn" href="{REPO}#安装与使用">开始使用：安装 Skill ↗</a><a class="btn secondary" href="#start">一句话开始提问 ↓</a></div><p class="tiny">支持中英文 · 政策依据可查 · 适用于职业、创业与了解中国</p></div>
<aside class="diagram"><div class="eyebrow">你可以直接这样问</div><h2>想学 AI，<br>原来的经验还能怎么用？</h2><p>“我做了5年品牌营销，想学 AI，又不想丢掉原来的经验。结合十五五规划，我应该先了解哪些方向、补哪些能力？”</p><p class="tiny">从你的经验和正在犹豫的选择开始，无需先熟悉政策术语。</p></aside></div>
<div class="rail"><div><strong>看懂政策变化</strong><span>读原文，比较历次规划</span></div><div><strong>比较现实选择</strong><span>带入你的经验和投入条件</span></div><div><strong>带走选择单</strong><span>保存判断，带新信息继续分析</span></div></div>
{start_panel()}
<section id="downloads"><div class="section-head"><div><div class="eyebrow">可选阅读</div><h2>想先了解内容？从这里开始。</h2></div><p>无需安装即可阅读。资料日期与适用范围见各篇来源说明。</p></div><div class="download-row"><div class="download-block"><h3>短版 PDF</h3><p>用5个假设案例演示分析方法，附官方出处与验证工作纸，方便离线阅读。</p><a class="btn secondary" href="{RELEASE}five-year-guide-v0.3.0.pdf">下载短版指南 ↗</a><p class="tiny">本项目的入门材料。官方规划全文见<a href="{DATA['source_url']}">《十五五规划纲要》</a>。</p></div><div class="download-block"><h3>专题参考资料</h3><p>制造业 AI、机器人服务、养老服务等专题，展示怎样核对依据、了解需求并设计一次小试验。</p><a class="btn secondary" href="#cases">展开专题参考 ↓</a><p class="tiny">个性化分析可<a href="{REPO}#安装与使用">安装 Skill</a>后带入自己的情况。</p></div></div></section>
<details id="cases" class="case-library"><summary>专题案例与两周验证清单（可选，点击展开）</summary>
<section><div class="section-head"><div><div class="eyebrow">专题参考 / 可选</div><h2>看看分析方法怎样用于具体问题。</h2></div><p>以下均为构造场景。政策引文已与所用文本核对；客户、付款与个人适配需要继续验证。</p></div><div class="filters" aria-label="按已有能力筛选">{filters}</div><p id="result-count" class="tiny" aria-live="polite">显示全部5个案例</p><div class="card-grid">{teasers}</div></section>
<section id="plan"><div class="plan"><div class="plan-head"><div><div class="eyebrow">把阅读变成行动</div><h2>我的两周验证清单</h2></div><span class="tiny">保存在当前浏览器，可下载留存</span></div><p id="plan-empty">从上方选择一张卡，先验证一个问题。这里的记录不会上传到服务器。</p><ul class="selected-list" id="selected-list"></ul><div class="form-grid"><label>我的城市与已有能力<input id="context" placeholder="例如：广州，有企业培训经验" maxlength="240"></label><label>这次最想查清的问题<input id="question" placeholder="例如：谁会采购一项询盘整理服务？" maxlength="240"></label><label>我愿意投入的时间与预算<textarea id="budget" placeholder="写一个能承受的试验上限" maxlength="500"></textarea></label><label>什么时候停止或调整<textarea id="stop" placeholder="例如：两周后仍找不到任务负责人，就换场景" maxlength="500"></textarea></label></div><div class="actions"><button class="btn" id="export-plan">下载我的验证清单 ↓</button><button class="btn secondary" id="clear-plan">清空本机记录</button></div><p class="tiny" id="storage-note">记录仅存当前浏览器。换设备或清理浏览器后可能丢失，请下载留存。</p></div></section>
</details></main>{footer()}'''
    (site/'index.html').write_text(shell(DATA['seo_title'],DATA['seo_description'],body),encoding='utf-8')
    (site/'first-session.html').write_text(walkthrough(), encoding='utf-8')
    (site/'.nojekyll').write_text('')
    (site/'sitemap.xml').write_text(sitemap(), encoding='utf-8')
    lines=['# 十五五规划解读与职业创业决策卡','','基于十五五规划的职业与小生意决策参考。v0.3.0，核验日期2026-10-18。','','先选一个与你有关的问题，读依据、付款方与验证动作，再决定是否扩大投入。以下均为构造场景；商业需求和个人适配待验证。','']
    lines += [f'- [{c["seo_title"]}](card-{c["id"]}.md) · [在线阅读]({BASE}cards/{c["slug"]}.html)' for c in DATA['cards']]
    lines += ['',f'[手机阅读页]({BASE}) · [短版PDF]({RELEASE}five-year-guide-v0.3.0.pdf)','','## 如何转载与改编','','按项目MIT许可保留作者和许可声明，同时保留卡片编号、核验日期、官方来源及适用边界。新加的地区案例和市场数据请另列来源，不把推导改写成官方承诺。','','[内容与贡献规则](CONTRIBUTING.md) · [原始结构化内容](cards.json)','']
    (ROOT/'guide/README.md').write_text('\n'.join(lines),encoding='utf-8')
    print('Built reader, 5 detail pages, 5 share layouts and 5 Markdown cards.')


if __name__ == '__main__':
    main()
