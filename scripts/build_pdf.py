#!/usr/bin/env python3
"""Create the short PDF from the same reviewed data as the reader.

Requires reportlab. Use --output outside the source checkout.
For other hosts, pass a CJK TrueType font with --font.
"""
import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'guide/cards.json').read_text(encoding='utf-8'))
POLICY = {c['id']: c for c in json.loads((ROOT / 'references/policy-cards.json').read_text(encoding='utf-8'))['cards']}
CHAPTERS = {'P01':'第六十二章第一节','P02':'第六十二章第二节','P03':'第四章第一节','P04':'第五章第一节','P05':'第五章第二节','P06':'第六章第一节','P07':'第十三章第一节','P22':'第四十章第一节','P23':'第四十一章第二节'}
GREEN = colors.HexColor('#254d3c')
ORANGE = colors.HexColor('#bb5732')
INK = colors.HexColor('#24362e')
MUTED = colors.HexColor('#657267')
PAPER = colors.HexColor('#f5f3ec')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--font', default='/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
    parser.add_argument('--audit-citations', action='store_true',
                        help='Add edition-specific PDF pages for an explicitly requested source audit')
    args = parser.parse_args()
    pdfmetrics.registerFont(TTFont('GuideCJK', args.font))
    styles = {
        'body': ParagraphStyle('body', fontName='GuideCJK', fontSize=11.3, leading=19, textColor=INK, spaceAfter=8, wordWrap='CJK'),
        'small': ParagraphStyle('small', fontName='GuideCJK', fontSize=8.7, leading=13.8, textColor=MUTED, spaceAfter=6, wordWrap='CJK'),
        'label': ParagraphStyle('label', fontName='GuideCJK', fontSize=8.5, leading=13, textColor=ORANGE, spaceAfter=9, wordWrap='CJK'),
        'h1': ParagraphStyle('h1', fontName='GuideCJK', fontSize=24, leading=34, textColor=GREEN, spaceAfter=17, wordWrap='CJK'),
        'h2': ParagraphStyle('h2', fontName='GuideCJK', fontSize=13.5, leading=20, textColor=GREEN, spaceBefore=10, spaceAfter=8, wordWrap='CJK'),
        'cover': ParagraphStyle('cover', fontName='GuideCJK', fontSize=40, leading=57, textColor=GREEN, spaceAfter=24, wordWrap='CJK'),
        'deck': ParagraphStyle('deck', fontName='GuideCJK', fontSize=16, leading=26, textColor=MUTED, spaceAfter=16, wordWrap='CJK'),
    }
    story=[]
    def p(text, style='body'):
        return Paragraph(escape(text).replace('\n','<br/>'),styles[style])
    def add(text,style='body'):
        story.append(p(text,style))
    def heading(text): add(text,'h2')
    def callout(title,text,background='#e8ecdf'):
        t=Table([[p(title,'label')],[p(text)]],colWidths=[483])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor(background)),('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),('TOPPADDING',(0,0),(0,0),10),('BOTTOMPADDING',(0,-1),(-1,-1),10)]))
        story.append(t);story.append(Spacer(1,10))
    def link(title,url):
        story.append(Paragraph(f'<link href="{escape(url)}" color="#254d3c"><u>{escape(title)}</u></link>',styles['small']))
    def page(label,title):
        story.append(PageBreak());add(label,'label');add(title,'h1')

    add('2026 → 2030  /  十五五与个人选择','label')
    story.append(Spacer(1,43))
    add('未来五年，\n普通人的机会\n与避坑指南','cover')
    add('基于十五五规划的\n职业与小生意决策参考','deck')
    story.append(Spacer(1,20))
    callout('读完，先查清一个问题','我可以服务谁？交付哪项任务？谁愿意付款？下一步用什么小实验验证？')
    add('5个具体场景 · 政策出处 · 参与门槛 · 两周行动','body')
    story.append(Spacer(1,25))
    add('作者 xingyou1439  /  v0.2.1  /  内容核验 2026-10-18','small')
    add('以下采用假设案例。你可以参考思路，但还需要结合自己的能力、客户需求和当地规则判断。','small')
    link('打开手机阅读版与后续更新',DATA['reader_url'])

    page('01 / 使用方法','把一个大方向，拆成一个能验证的选择。')
    add('先从下方挑一个与你有关的问题，读对应卡片。每张卡分为“判断与依据”和“验证与停止”两页。')
    for c in DATA['cards']: add(f'{c["id"]}  {c["title"]}')
    heading('沿这五环追问')
    for title,text in [
        ('政策方向','原文说了什么？是正式纲要、实施通知，还是研究观点？'),
        ('实施工具与项目','哪个地区、部门或企业负责？当前项目处于什么阶段？'),
        ('客户与付款方','谁使用、谁验收、谁审批付款？预算是否真实存在？'),
        ('可交付任务','你能做哪项具体工作？哪些能力、资质或合作关系还缺？'),
        ('验证与停止','两周内先查清什么？什么结果支持继续，什么结果让你停下？')]:
        heading(title);add(text)
    add('规划引文用于说明政策方向。卡片中的服务设想、试验人数和时间是作者建议，可按实际资源调整；客户是否采购、你能否参与，需要分别核实。','small')

    for c in DATA['cards']:
        titles = {'01': '给制造企业做 AI，\n先培训、实施，还是做软件？', '03': '想做养老业务，\n老人、子女、机构，谁会付钱？', '05': '已有营销、设计或培训经验，\n怎样参与新方向？'}
        page(f'案例 {c["id"]} / 判断与依据',titles.get(c['id'],c['title']))
        add(c['lead'],'deck')
        add('构造情境：'+c['situation'])
        callout('当前判断',c['judgment'])
        heading('政策依据')
        for pid in c['policy_ids']:
            for ref in POLICY[pid]['source_refs']:
                add('“'+ref['quote_zh']+'”')
                citation=f'《十五五规划纲要》{CHAPTERS[pid]}'
                if args.audit_citations:
                    citation += f'；PDF第{ref["pdf_page"]}页（项目收录版本）'
                link(citation, DATA['source_url'])
        heading('你可以从哪里入手')
        add(c['interpretation'])
        for role in c['roles']:add('• '+role)
        heading('谁可能付款')
        add(c['payer'])
        link('官方全文与本卡完整出处',DATA['reader_url']+'cards/'+c['slug']+'.html')

        page(f'案例 {c["id"]} / 验证与停止',c['short_title'])
        heading('要准备什么')
        add(c['capability'])
        heading('先查清这件事')
        add(c['gap'])
        heading('接下来两周')
        for i,step in enumerate(c['steps'],1):add(f'{i}. {step}')
        callout('有这些进展，再继续',c['success'])
        callout('出现这些情况，先停一停',c['stop'],'#f4e9df')
        add('使用提醒：'+c['boundary'],'small')
        if c['update_ids']:
            heading('相关文件')
            for uid in c['update_ids']:
                s=next(s for s in DATA['updates'] if s['id']==uid)
                link(f'《{s["title"]}》（{s["document_date"]}）',s['url'])
                add(s['summary']+' '+s['scope'],'small')
        link('复制提问，把你的城市、能力与选项带入分析',DATA['reader_url']+'cards/'+c['slug']+'.html')

    page('工作纸 / 先填一张','我的两周验证计划')
    add('先选一张卡。用事实补空白，暂时查不到的写“未知”。不要把模糊兴趣算作购买需求。')
    for label in ['我所在城市、已有能力与作品','我正在比较的两个现实选项','我能交付的一项具体任务','使用者、决策人、实际付款方','已经找到的官方依据与适用范围','目前最缺的证据','两周行动与投入上限','继续、停止或调整的条件']:
        heading(label)
        table=Table([[''],['']],colWidths=[483],rowHeights=[16,16]);table.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),.5,colors.HexColor('#d9ded2'))]));story.append(table)
    story.append(Spacer(1,16));link('手机填写并下载个人验证清单',DATA['reader_url']+'#plan')

    page('参考资料','想看依据，可以从这里查。')
    add('《中华人民共和国国民经济和社会发展第十五个五年规划纲要》（2026年3月）。卡片引用的原文可按下列章、节查阅。','body')
    if args.audit_citations:
        add('本次按核验要求附PDF页码，对应项目收录的2026年纲要版本；其他版本可能分页不同。','small')
    link('官方全文：北京市人大网站转载新华社受权发布文本',DATA['source_url'])
    add('引用章节：第四章第一节，第五章第一、二节，第六章第一节，第十三章第一节，第四十章第一节，第四十一章第二节，第六十二章第一、二节。','small')
    for s in DATA['updates']:
        heading('《'+s['title']+'》')
        add(s['issuer']+'，'+s['document_date'],'small')
        add('参见'+s['locator']+'。'+s['scope'],'small')
        link('查看原文 · '+s['host'],s['url'])
    heading('复用与更新')
    add('项目按MIT许可开放。转载与改编时保留作者和许可声明，建议保留卡片编号、来源、核验日期与适用边界。新增地区规则、客户案例与市场数字另列来源。','small')
    add('v0.2.1改进引用和读者表达。公众阅读页包含5张示例决策卡和4条补充官方依据。原Skill的三期规划语料与跨期比较保留；本次补查不代表已全面更新所有行业与地方规则。','small')
    link('原始内容、Skill安装与纠错',DATA['repository'])

    args.output.parent.mkdir(parents=True,exist_ok=True)
    def decorate(canvas,doc):
        w,h=doc.pagesize
        canvas.saveState()
        canvas.setFillColor(PAPER);canvas.rect(0,0,w,h,fill=1,stroke=0)
        canvas.setStrokeColor(colors.HexColor('#d9ded2'));canvas.line(48,40,w-48,40)
        canvas.setFont('GuideCJK',8);canvas.setFillColor(MUTED)
        canvas.drawString(48,25,'未来五年 · 机会与避坑指南  |  v0.2.1  |  2026-10-18')
        canvas.drawRightString(w-48,25,str(doc.page))
        canvas.restoreState()
    doc=SimpleDocTemplate(str(args.output),pagesize=(595.276,841.89),rightMargin=48,leftMargin=48,topMargin=46,bottomMargin=57,title=DATA['title'],author=DATA['author'],subject=DATA['subtitle'],pageCompression=1)
    doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
    print('Created',args.output.name)


if __name__=='__main__':
    main()
