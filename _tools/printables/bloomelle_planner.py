#!/usr/bin/env python3
"""Render the Bloomelle weekly planner PDFs (A4 and US Letter, landscape) and the page preview image.

Usage: python3 _tools/printables/bloomelle_planner.py
Output: bloomelle/weekly-planner/pdf/*.pdf and bloomelle/weekly-planner/preview.jpg (needs Google Chrome and sips on macOS).
"""
import os, subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(ROOT, 'bloomelle', 'weekly-planner')
FONT = 'file://' + os.path.join(ROOT, 'assets', 'fonts', 'fraunces-latin.woff2')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
A = '#B14865'
A2 = '#C97B90'
TINT = '#FAEEF1'
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
CATS = ['Workout', 'Focus work', 'Big decisions', 'Rest / lighter']


def circles(n):
    return '<span class="c"></span>' * n


def doc(paper):
    size = 'A4 landscape' if paper == 'a4' else 'letter landscape'
    head = '<div class="lab"></div>' + ''.join(f'<div class="dh">{d}<span>date ____</span></div>' for d in DAYS)
    cd = '<div class="lab">Cycle day</div>' + '<div class="cell sm"></div>' * 7
    cat_rows = ''
    for c in CATS:
        cells = ''.join('<div class="cell tall"><span class="fit"><i>G</i><i>S</i><i>N</i></span></div>' for _ in DAYS)
        cat_rows += f'<div class="row"><div class="lab">{c}</div>{cells}</div>'
    chk = ''
    for name in ['Energy 1-5', 'Focus 1-5', 'Mood 1-5']:
        chk += f'<div class="row"><div class="lab">{name}</div>' + ''.join(f'<div class="cell sm mid">{circles(5)}</div>' for _ in DAYS) + '</div>'
    chk += '<div class="row"><div class="lab">Did the plan fit?</div>' + ''.join('<div class="cell sm mid"><span class="t">yes</span><span class="c"></span><span class="t">partly</span><span class="c"></span><span class="t">no</span><span class="c"></span></div>' for _ in DAYS) + '</div>'
    pat = ''.join(f'<div class="tr"><div>{p}</div><div></div><div></div><div></div></div>' for p in ['Period', 'Follicular (after the period, before ovulation)', 'Around ovulation', 'Luteal (after ovulation, before the next period)'])
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:F;src:url("{FONT}")}}
@page{{size:{size};margin:0}}
*{{margin:0;box-sizing:border-box}}
body{{font-family:-apple-system,'Helvetica Neue',Arial,sans-serif;color:#2B2426}}
.page{{width:100vw;height:100vh;padding:4.5vh 3.5vw 3vh;display:flex;flex-direction:column;page-break-after:always;overflow:hidden}}
.page:last-child{{page-break-after:auto}}
h1{{font-family:F,Georgia,serif;font-weight:600;font-size:5vh;color:{A}}}
.sub{{font-size:1.75vh;color:#5C5050;margin:.5vh 0 1.4vh}}
.grid{{flex:1;min-height:0;display:flex;flex-direction:column;border:.25vh solid #5C5050;border-radius:.8vh;overflow:hidden}}
.row{{display:grid;grid-template-columns:11vw repeat(7,1fr);flex:1;min-height:0;border-bottom:.15vh solid #D8C2C8}}
.row:last-child{{border-bottom:0}}
.row.hd{{flex:none;height:6vh;background:{TINT};border-bottom:.25vh solid #5C5050}}
.row.cd{{flex:none;height:4.2vh}}
.row>div{{border-right:.15vh solid #D8C2C8;display:flex;align-items:center;justify-content:center;position:relative}}
.row>div:last-child{{border-right:0}}
.lab{{justify-content:flex-start!important;padding-left:.9vw;font-weight:700;font-size:1.6vh;color:#44302C;background:{TINT}}}
.dh{{font-weight:700;font-size:1.9vh;flex-direction:column;gap:.2vh}}
.dh span{{font-weight:400;font-size:1.15vh;color:#5C5050}}
.cell.tall{{align-items:flex-end;justify-content:center}}
.fit{{display:flex;gap:.6vw;margin-bottom:.9vh}}
.fit i{{font-style:normal;font-size:1.15vh;font-weight:600;color:#5C5050;width:2.2vh;height:2.2vh;border:.2vh solid #9E8E84;border-radius:50%;display:flex;align-items:center;justify-content:center}}
.mid{{gap:.3vw}}
.c{{width:1.8vh;height:1.8vh;border:.2vh solid #9E8E84;border-radius:50%;display:inline-block}}
.t{{font-size:1.1vh;color:#5C5050}}
.foot{{margin-top:1.1vh;display:flex;justify-content:space-between;font-size:1.4vh;color:#5C5050;gap:2vw}}
.foot b,.foot a{{color:{A}}}
h2{{font-family:F,Georgia,serif;font-weight:600;font-size:3vh;color:{A};margin:1.2vh 0 1vh}}
ol{{padding-left:2vw;font-size:1.95vh;line-height:1.45;max-width:90vw}}
ol li{{margin-bottom:.9vh}}
.note{{font-size:1.7vh;line-height:1.45;color:#5C5050;border-left:.6vh solid {A2};padding-left:1.2vw;margin:1.4vh 0}}
.tally{{flex:1;min-height:0;border:.25vh solid #5C5050;border-radius:.8vh;overflow:hidden;display:flex;flex-direction:column;margin-top:.8vh}}
.tr{{display:grid;grid-template-columns:20vw 1fr 1fr 1fr;flex:1;border-bottom:.15vh solid #D8C2C8;font-size:1.7vh}}
.tr:last-child{{border-bottom:0}}
.tr>div{{display:flex;align-items:center;padding:0 .9vw;border-right:.15vh solid #D8C2C8}}
.tr>div:last-child{{border-right:0}}
.tr.h{{background:{TINT};font-weight:700;font-size:1.5vh;flex:none;height:5vh}}
</style></head><body>
<div class="page">
<h1>Weekly Cycle Planner</h1>
<div class="sub">Week of ______________ &nbsp; First day of my last period: ______________ &nbsp; Cycle day on Monday: ______ &nbsp; In each cell circle G (good fit), S (so-so) or N (not ideal).</div>
<div class="grid">
<div class="row hd">{head}</div>
<div class="row cd">{cd}</div>
{cat_rows}
{chk}
</div>
<div class="foot"><span><b>Bloomelle</b> &middot; Plan your week around your cycle &middot; <a href="https://another1dd.github.io/bloomelle/">another1dd.github.io/bloomelle/</a></span><span>&copy; 2026 Chepatapa Apps &middot; Free for personal use &middot; Page 1 of 2</span></div>
</div>
<div class="page">
<h1>How to use the planner</h1>
<div class="sub">Two minutes at the start of the week and ten seconds a day.</div>
<ol>
<li><b>Start from your own dates.</b> Day 1 of the cycle is the first day of your period. Write the date and the cycle day for each column.</li>
<li><b>Plan with a light touch.</b> For each of workout, focus work, big decisions and rest, mark the days that look good, so-so or not ideal. These are starting points, not rules.</li>
<li><b>Check in each evening.</b> Circle energy, focus and mood from 1 to 5 and note whether the plan fit. It takes about ten seconds.</li>
<li><b>Look back after two or three cycles.</b> Fill in the table below with what you actually noticed. Your own notes are the data.</li>
</ol>
<div class="note">Cycles vary: sources describe lengths from about 21 to 38 days, and a cycle can change from month to month. The evidence on whether cycle phase changes performance is limited and mixed, so treat phase-based planning as an experiment and not as a rule. This planner doesn't diagnose anything. If something about your cycle worries you, talk to a doctor.</div>
<h2>What I noticed</h2>
<div class="tally">
<div class="tr h"><div>Phase</div><div>Energy and focus tended to be&hellip;</div><div>What worked well</div><div>What I'd do differently</div></div>
{pat}
</div>
<div class="foot"><span><b>Bloomelle</b> does the forecast for you, with a daily check-in &middot; <a href="https://another1dd.github.io/bloomelle/">another1dd.github.io/bloomelle/</a></span><span>&copy; 2026 Chepatapa Apps &middot; Free for personal use &middot; Page 2 of 2</span></div>
</div>
</body></html>'''


def main():
    os.makedirs(os.path.join(OUT, 'pdf'), exist_ok=True)
    for paper in ('a4', 'letter'):
        html_path = f'/tmp/bloomelle-planner-{paper}.html'
        with open(html_path, 'w', encoding='utf-8') as fh:
            fh.write(doc(paper))
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--allow-file-access-from-files', '--no-pdf-header-footer',
                        f'--print-to-pdf={OUT}/pdf/bloomelle-weekly-cycle-planner-{paper}.pdf', f'file://{html_path}'], capture_output=True)
    # preview of page 1 (A4)
    with open('/tmp/bloomelle-planner-a4.html', encoding='utf-8') as fh:
        page = fh.read().replace('</style>', '.page:nth-of-type(2){display:none}</style>')
    with open('/tmp/bloomelle-planner-p1.html', 'w', encoding='utf-8') as fh:
        fh.write(page)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--allow-file-access-from-files', '--hide-scrollbars', '--window-size=1123,794',
                    '--screenshot=/tmp/bloomelle-planner-p1.png', 'file:///tmp/bloomelle-planner-p1.html'], capture_output=True)
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '82', '-Z', '1100', '/tmp/bloomelle-planner-p1.png', '--out', os.path.join(OUT, 'preview.jpg')], capture_output=True)


if __name__ == '__main__':
    main()
