from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit, ImageReader
from pathlib import Path
import pandas as pd, numpy as np, math

R=Path('/mnt/data'); O=R/'rr_2027_latest'; O.mkdir(exist_ok=True)
OUT=R/'Rajasthan_Royals_2027_Pink_RR_Acquirable_Top10_Batters_Bowlers.pdf'
F='/usr/share/fonts/truetype/lato/'
for k,v in [('Lato','Lato-Regular.ttf'),('Bold','Lato-Bold.ttf'),('Black','Lato-Black.ttf'),('Semi','Lato-Semibold.ttf'),('Italic','Lato-Italic.ttf')]:pdfmetrics.registerFont(TTFont(k,F+v))
W,H=960,540
NAV='#FFFFFF'; NAV2='#FFF5F9'; NAV3='#FFE6F0'; PINK='#E60070'; PINKL='#B5125D'; WHITE='#142338'; CREAM='#FFFFFF'; BLUE='#34465D'; SUB='#6C798D'; AQUA='#127F7A'; GOLD='#996B18'; ORANGE='#B96531'; RED='#C6365A'; BORDER='#EFC6D6'; GREEN='#167A5A'; ONPINK='#FFFFFF'
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('Rajasthan Royals 2027 | Pink Championship Blueprint and Eligible Auction Top-20')
c.setAuthor('Independent cricket analytics - dataset-grounded scouting')
page_count=0
co=lambda s:HexColor(s)
def rect(x,y,w,h,fill=NAV2,rad=0,stroke=None):
 c.setFillColor(co(fill)); c.setStrokeColor(co(stroke or fill));c.setLineWidth(.7)
 if rad:c.roundRect(x,y,w,h,rad,fill=1,stroke=bool(stroke))
 else:c.rect(x,y,w,h,fill=1,stroke=bool(stroke))
def ln(x1,y1,x2,y2,color=BORDER,w=1):c.setStrokeColor(co(color));c.setLineWidth(w);c.line(x1,y1,x2,y2)
def text(x,y,s,size=12,font='Lato',color=WHITE,align='left'):
 c.setFillColor(co(color));c.setFont(font,size)
 if align=='center':c.drawCentredString(x,y,str(s))
 elif align=='right':c.drawRightString(x,y,str(s))
 else:c.drawString(x,y,str(s))
def para(x,y,s,width,size=12,font='Lato',color=BLUE,lead=None,maxlines=None):
 lead=lead or size*1.34;lines=[]
 for seg in str(s).split('\n'):
  if seg:lines.extend(simpleSplit(seg,font,size,width))
  else:lines.append('')
 if maxlines is not None and len(lines)>maxlines:
  lines=lines[:maxlines-1]+[lines[maxlines-1].rstrip(' .')+'...']
 for i,l in enumerate(lines):text(x,y-i*lead,l,size,font,color)
 return y-len(lines)*lead

def kicker(x,y,s,col=PINKL):text(x,y,s.upper(),10,'Bold',col)
def foot(section='SCOUTING INTELLIGENCE'):
 global page_count
 ln(40,31,920,31)
 text(40,16,'RR 2027  /  THE TITLE BLUEPRINT',8,'Bold',SUB)
 text(477,16,'UPDATED 17 NOV 2026  |  INDEPENDENT ANALYSIS',8,'Lato',SUB,'center')
 text(920,16,f'{section}  /  {page_count:02d}',8,'Bold',PINKL,'right')
def page(section,title,subtitle=''):
 global page_count
 page_count+=1
 rect(0,0,W,H,NAV)
 for xx in range(810,970,20):ln(xx,540,xx-100,440,'#FBE1EC',1)
 rect(40,492,94,25,PINK,13);text(87,500,'RR  /  2027',10,'Bold',ONPINK,'center')
 kicker(155,501,section)
 rect(907,490,11,24,PINK,4)
 ty=443
 for l in simpleSplit(title,'Black',31,878):text(40,ty,l,31,'Black',PINK);ty-=37
 if subtitle:para(42,ty-4,subtitle,870,11,'Lato',SUB,15,3)
 foot()
 return ty-32
def end():c.showPage()
def box(x,y,w,h,bg=NAV2,border=None):rect(x,y,w,h,bg,12,border)
def rule(x,y,title,body,w=270,h=120,accent=PINK):
 box(x,y,w,h);rect(x,y+h-4,w,4,accent);kicker(x+16,y+h-29,title,accent);para(x+16,y+h-57,body,w-32,12,'Semi',WHITE,16,4)
def stat(x,y,w,big,title,desc='',col=PINK):
 box(x,y,w,109);text(x+16,y+58,big,34,'Black',col);text(x+17,y+38,title,11,'Bold',WHITE)
 if desc:para(x+17,y+19,desc,w-30,8,'Lato',SUB,10,2)
def caption(x,y,s):text(x,y,s,8,'Lato',SUB)
def win(s):
 rect(40,52,880,53,'#FFE6F0',10);rect(40,52,7,53,PINK)
 text(56,81,'THE WINNING MOVE',10,'Bold',PINKL)
 para(239,82,s,653,11,'Semi',WHITE,14,2)
def tab(x,top,width,headers,rows,colwidths=None,rowh=31,fs=10,headcolor=PINK,highlight=None):
 if colwidths is None:colwidths=[width/len(headers)]*len(headers)
 assert abs(sum(colwidths)-width)<1
 rect(x,top-29,width,29,NAV3,6)
 xx=x
 for j,h in enumerate(headers):text(xx+9,top-19,h,9,'Bold',PINKL);xx+=colwidths[j]
 yy=top-29
 for i,row in enumerate(rows):
  rect(x,yy-rowh,width,rowh,NAV2 if i%2==0 else '#FFECF3')
  if highlight is not None and i in highlight:rect(x,yy-rowh,4,rowh,PINK)
  xx=x
  for j,v in enumerate(row):
   ss=str(v)
   if len(ss)>42:ss=ss[:39]+'...'
   size=fs
   while pdfmetrics.stringWidth(ss,'Bold' if j==0 else 'Lato',size)>colwidths[j]-14 and size>7:size-=.4
   text(xx+9,yy-rowh+rowh*.34,ss,size,'Bold' if j==0 else 'Lato',WHITE if j==0 else BLUE)
   xx+=colwidths[j]
  ln(x,yy-rowh,x+width,yy-rowh,BORDER,.35)
  yy-=rowh
 return yy

def sourcebox(n,title,url,x=42,y=85,w=875):
 text(x,y,f'[{n}] {title}',9,'Bold',AQUA)
 c.linkURL(url,(x,y-2,x+w,y+11),relative=0)
def bullet(x,y,title,desc,w=380,col=PINK):
 rect(x,y-5,5,5,col);text(x+15,y-5,title,13,'Bold',WHITE)
 return para(x+15,y-25,desc,w-15,10,'Lato',BLUE,14,3)-7

def chips(items,x,y,widths=None):
 xx=x
 for i,s in enumerate(items):
  ww=widths[i] if widths else max(62,pdfmetrics.stringWidth(s,'Bold',9)+18)
  rect(xx,y,ww,25,NAV3,12)
  text(xx+ww/2,y+8,s,9,'Bold',PINKL,'center');xx+=ww+8

stats=pd.read_csv(O/'player_2025_2026_from_updated_raw.csv')
phases=pd.read_csv(O/'player_phase_2025_2026_from_updated_raw.csv')
team=pd.read_csv(O/'rr_phase_2025_2026_from_updated_raw.csv')
venues=pd.read_csv(R/'rr_2027_conditions/all_venues_2025_2026.csv')
def get(p,y,col):
 v=stats[(stats.player==p)&(stats.season==y)]
 if len(v)==0:return None
 z=v.iloc[0][col];return z if pd.notna(z) else None
fmt=lambda v: 'N/A' if v is None or pd.isna(v) else str(v)

# 1 cover - new original-pink report system using supplied real RR logo
page_count+=1
rect(0,0,W,H,NAV)
# diagonal pink geometry and repeatable brand motif
c.setFillColor(co(PINK)); p=c.beginPath();p.moveTo(0,H);p.lineTo(198,H);p.lineTo(0,346);p.close();c.drawPath(p,stroke=0,fill=1)
c.setFillColor(co('#F9C2D9')); p=c.beginPath();p.moveTo(202,H);p.lineTo(232,H);p.lineTo(0,310);p.lineTo(0,341);p.close();c.drawPath(p,stroke=0,fill=1)
rect(0,0,W,17,PINK)
# right-hand logo illustration uses exact user-supplied white logo pixels recolored pink
c.setFillColor(co('#FFF1F7')); c.circle(746,279,185,fill=1,stroke=0)
c.setStrokeColor(co('#F5BFD6'))
for rad in (120,158):c.setLineWidth(1);c.circle(746,279,rad,fill=0,stroke=1)
c.drawImage(ImageReader(str(R/'rr_logo_magenta_transparent.png')),653,161,width=186,height=288,mask='auto',preserveAspectRatio=True)
text(53,466,'RAJASTHAN ROYALS  /  INDEPENDENT CRICKET INTELLIGENCE',11,'Bold',PINKL)
text(53,395,'RR 2027',63,'Black',PINK)
text(53,333,'TITLE',63,'Black',WHITE)
text(53,271,'BLUEPRINT',63,'Black',PINK)
ln(54,252,533,252,PINK,3)
para(55,225,'Confirmed squad, auction-eligible top-10 batting and bowling targets, pressure evidence, venue plans and Impact Player strategies.',514,14,'Semi',BLUE,19,4)
rect(53,92,506,52,PINK,10)
text(306,112,'THE BLUEPRINT TO WIN IPL 2027',15,'Black',ONPINK,'center')
text(54,54,'RR 2027 AUCTION: TOP 10 BATTERS + TOP 10 BOWLERS',11,'Bold',PINKL)
text(905,32,'17 NOV 2026  /  RESEARCH EDITION',9,'Bold',SUB,'right')
end()

# 2 executive
page('THE EXECUTIVE CALL','2027 is a six-decision auction, not a rebuild.','Confirmed by Rajasthan Royals on 17 November 2026. Trading is completed; player registration for the auction remains pending.')
stat(42,266,214,'19','CURRENT SQUAD','17 retained + 2 traded in')
stat(269,266,214,'6','VACANCIES','Up to 3 overseas')
stat(496,266,214,'27.05','INR CRORE PURSE','Team-official figure')
stat(723,266,197,'3','OS SLOTS OPEN','5 overseas retained')
rule(42,124,'01  DO NOT OVERBUY','Opening batting and powerplay wicket-taking already have quality options.',420,120,PINK)
rule(500,124,'02  BUY THE GAPS','Prioritize Indian late-innings batting and phase-specific pace depth.',420,120,AQUA)
win('Protect Jaiswal + Vaibhav; spend for finishing stability, tactical pace cover and Impact Player optionality.')
end()



# ---------- RR-ACQUIRABLE SHORTLIST : REAL 2027 RELEASES ONLY ----------
T=pd.read_csv(R/'rr_2027_latest/rr_2027_acquirable_top10_batters_and_bowlers.csv')
BAT=T[T.discipline=='BATTER'].sort_values('rr_shortlist_rank')
BOWL=T[T.discipline=='BOWLER'].sort_values('rr_shortlist_rank')
def q(v,digits=1):
 return '-' if pd.isna(v) else f'{float(v):.{digits}f}'
def explain(page_section,df,subset):
 page(page_section,subset,'A real fit for RR does not require an expensive name - but it does require a verified release, a real squad role and evidence limitations.')
 for i,(_,r) in enumerate(df.iterrows()):
  y=312-i*62
  rect(43,y,875,63,NAV2,10)
  rect(43,y,7,63,PINK)
  text(60,y+43,f"{int(r['rr_shortlist_rank']):02d}  {r['player']}",14,'Black',PINK)
  text(896,y+43,f"{int(r['rr_fit_score_100'])}/100",12,'Black',PINK,'right')
  para(60,y+27,'FIT: '+str(r['reason']),826,9.25,'Semi',WHITE,11.2,2)
  para(60,y+13,'RISK: '+str(r['risk']),826,8.7,'Lato',SUB,10.8,1)
 caption(44,49,'Priority ranks are RR roster-fit judgments supported by supplied deliveries, not the global IPL/T20I pressure leaderboard.')
 end()

page('RR 2027 / AUCTION SHORTLIST','20 realistic names. Not 20 fictional transfers.','Every retained rival-team player, retired cricketer and Pakistan-national candidate has been removed. One uncapped free-agent prospect has an explicit registration caveat.')
for xx,side,df in [(42,'BATTERS',BAT),(495,'BOWLERS',BOWL)]:
 box(xx,86,423,310)
 rect(xx,363,423,33,PINK,9);text(xx+15,374,side,14,'Black',ONPINK)
 for k,(_,r) in enumerate(df.iterrows()):
  yy=344-k*25.2
  if k%2==0:rect(xx+9,yy-8,404,23,'#FFEAF2',4)
  text(xx+19,yy,str(int(r.rr_shortlist_rank)).zfill(2),10.6,'Black',PINK)
  label=str(r.player)
  if r.player=='Sanvir Singh':label+=' *'
  text(xx+51,yy,label,10.8,'Semi',WHITE)
  text(xx+402,yy,str(int(r.rr_fit_score_100)),11,'Black',PINK,'right')
caption(45,65,'* SANVIR: uncontracted prospect, auction registration not yet confirmed. All other names are recorded in 17 Nov release lists.')
end()

page('SCOUTING / ELIGIBILITY','First prove a player can actually join RR.','Published 17 Nov franchise releases are the screening baseline; auction registration closes later. All suggested acquisitions remain conditional until the official register.')
items=[('1 / FRANCHISE STATUS','2027 retained by another team -> exclude. Released by prior club -> candidate. Uncontracted Indian prospect -> pending verification.'),
('2 / PARTICIPATION','Retired, opted out for 2027, national/IPL restriction, or unavailable through injury -> do not recommend as active bidding target.'),
('3 / RR ROLE SCARCITY','A confirmed 19-player squad needs a finisher, pace/death competition, keeper cover and injury depth - not another luxury opener.'),
('4 / PRE-AUCTION CHECK','Confirm BCCI auction register, fitness/NOC, base price, overseas capacity and any further trades before bidding.')]
for i,(head,desc) in enumerate(items):
 xx=42+(i%2)*445;yy=263-(i//2)*146
 box(xx,yy,426,134)
 kicker(xx+17,yy+108,head,PINK)
 para(xx+17,yy+83,desc,392,12,'Semi',WHITE,17,4)
rect(42,64,876,37,'#FFE3EF',8)
para(56,86,'EXCLUDED EXAMPLES: Suryakumar, Bumrah, Narine and other rivals\' retained players; retired MS Dhoni; opted-out Head and Starc; Pakistan-based players.',849,10,'Semi',WHITE,12,2)
end()

page('SCOUTING / RATING RUBRIC','A clear 100-point auction-fit score - not a win probability.','The score is a reproducible, analyst-assigned decision rubric backed by delivery evidence. No player is awarded marks solely for fame.')
criteria=[('40%','RR ROLE FIT','0-5 expert grade: does this player cover finisher, death, powerplay rotation, keeper or matchup need?'),
('30%','RECENT FORM','0-5 grade: cleaned IPL 2025-26 strike rate, economy, wickets, balls faced, and verified domestic form.'),
('20%','PRESSURE SIGNAL','0-5 grade: historical 2022+ delivery pressure impact; small samples explicitly discounted to neutral.'),
('10%','EVIDENCE STRENGTH','0-5 grade: relevant deliveries, matches, and how recent observations are; tiny samples score lower.')]
for i,(pct,head,desc) in enumerate(criteria):
 xx=42+(i%2)*446;yy=261-(i//2)*140
 box(xx,yy,428,125);text(xx+15,yy+72,pct,33,'Black',PINK)
 text(xx+125,yy+86,head,12,'Bold',WHITE);para(xx+125,yy+65,desc,282,9.9,'Lato',BLUE,13,4)
rect(42,80,874,31,NAV3,8)
text(55,92,'FIT SCORE = 8 x ROLE + 6 x RECENT + 4 x PRESSURE + 2 x EVIDENCE   (each grade 1-5)',11,'Bold',PINK)
caption(45,62,'Pressure ratings in the original global task and these recruiter grades are different: RR requires the filter BEFORE ranking.')
end()

page('BATTING / DATA AUDIT','Top 10 batters: what the supplied records actually show.','2025 and 2026 IPL combined; only clean ordinary-rule matches. HP = historical pressure events across supplied IPL and T20Is from 2022.')
rows=[]
for _,r in BAT.iterrows():
 sr=f'{int(r.ipl_2025_26_bat_runs)}/{int(r.ipl_2025_26_bat_balls)}' if r.ipl_2025_26_bat_balls else 'No IPL sample'
 ss=q(r.ipl_2025_26_bat_sr)
 h=f"{int(r.hp_balls)} {'VALID' if bool(r.pressure_eligibility) else 'LOW N'}"
 rows.append([str(int(r.rr_shortlist_rank)),r.player,sr,ss,h,str(int(r.rr_fit_score_100))])
tab(42,387,875,['#','2027 POSSIBLE TARGET','2025-26 RUNS/BALLS','SR','HP BALLS / TEST','FIT /100'],rows,[43,218,234,95,166,119],27.5,10,highlight=[0,1,2])
para(45,58,'Domestic exception: Sanvir Singh scored 377 runs at SR 183.90 in Sher-e-Punjab T20 2026. This is a separate league, not silently added to IPL rows.',855,9.4,'Semi',SUB,12,2)
end()

page('BOWLING / DATA AUDIT','Top 10 bowlers: wickets, economy and pressure exposure.','2025 and 2026 IPL combined; economy from bowler-attributable runs / legal deliveries. Pressure sample spans 2022+ IPL and T20I.')
rows=[]
for _,r in BOWL.iterrows():
 w=f'{int(r.ipl_2025_26_bowl_wickets)}/{int(r.ipl_2025_26_bowl_legal)}' if r.ipl_2025_26_bowl_legal else 'No IPL sample'
 h=f"{int(r.hp_balls)} {'VALID' if bool(r.pressure_eligibility) else 'LOW N'}"
 rows.append([str(int(r.rr_shortlist_rank)),r.player,w,q(r.ipl_2025_26_bowl_econ,2),h,str(int(r.rr_fit_score_100))])
tab(42,387,875,['#','2027 POSSIBLE TARGET','WKTS / LEGAL BALLS','ECON','HP BALLS / TEST','FIT /100'],rows,[43,218,234,95,166,119],27.5,10,highlight=[0,1,2])
para(45,56,'Pathirana: 593 historical HP events, +35.33 impact/120. Avesh: 646 HP, -11.44. This model output is NOT proof of 2027 performance.',859,9.3,'Semi',SUB,12,2)
end()

explain('BATTERS / WHY THESE NAMES',BAT.iloc[:5],'Batters 1-5: buy roles, not headlines.')
explain('BATTERS / ALTERNATIVES',BAT.iloc[5:],'Batters 6-10: conditional or development targets.')
explain('BOWLERS / WHY THESE NAMES',BOWL.iloc[:5],'Bowlers 1-5: closing, new-ball and left-arm cover.')
explain('BOWLERS / ALTERNATIVES',BOWL.iloc[5:],'Bowlers 6-10: specialist depth, not must-buy names.')

page('AUCTION / IMPACT PLAN','Buy the substitution role before buying the player.','Pre-auction scenarios, not claims these players are already RR signings. Four overseas on the field is the hard constraint.')
items=[('BOWL FIRST / INDIAN FINISHER','If RR sign Shahrukh or Sanvir: start an extra Indian bowler and bring the batter in for the chase.','Adds specialist batting while allowing an extra bowler in the first innings.'),
('BAT FIRST / INDIAN DEATH BOWLER','If RR sign Avesh or Madhwal: begin with extra Indian batting and introduce the seamer after the batting innings.','Keeps a specialist defender for overs 16-20; pressure data warns against overconfidence.'),
('BAT FIRST / OVERSEAS PATHIRANA','If RR sign Pathirana: start with <=3 overseas players, then swap an Indian batter for him before bowling.','Max four overseas at any moment. Fitness and bid affordability determine viability.'),
('BOWL FIRST / WICKETKEEPING COVER','If RR sign Abishek Porel: keep a bowling-heavy XI, then use him for middle-order chase cover.','Wicketkeeping remains with Jurel unless team selects otherwise.')]
for i,(head,desc,why) in enumerate(items):
 xx=42+(i%2)*446;yy=255-(i//2)*143
 box(xx,yy,427,132);kicker(xx+14,yy+106,head)
 para(xx+14,yy+84,desc,394,10.3,'Semi',WHITE,14,3)
 para(xx+14,yy+34,why,395,9.1,'Lato',SUB,11,2)
win('The best Impact Player is the one who changes the tactical role after the toss - not a fixed twelfth man.')
end()

page('AUCTION / SIX REAL DECISIONS','A shortlist of 20 is not a shopping list of 20.','RR have six open spots and INR 27.05 crore; buying all high-ranked players is neither possible nor necessary.')
rows=[
['1','Indian finisher','Shahrukh / Sanvir','TOP PRIORITY - No.5-7 power with zero overseas cost'],
['2','Indian seam/death','Avesh / Madhwal / Tushar','Premium only with acceptable death-over scouting'],
['3','Indian LHB flexible middle','Nehal / Nitish','Complement Parag/Jurel; do not replace established openers'],
['4','Keeper-batter cover','Abishek Porel / cheaper backup','Preserve bench without adding a foreign wicketkeeper'],
['5','One foreign specialist','Pathirana / Blessing / Boult','Choose ONE if medically available and affordable'],
['6','Reserve development slot','Unadkat / local uncapped','Pitch/health/auction price determines last selection']]
tab(42,363,875,['SLOT','SQUAD JOB','SHORTLIST OPTIONS','WHY IT FITS'],rows,[55,204,240,376],38,10)
win('Do not chase Pathirana at any price. Indian middle-order and bowling cover are the structural priorities.')
end()

page('METHODOLOGY / IMPORTANT BOUNDARY','This shortlist answers RR recruitment, not the unrestricted Round 1 leaderboard.','The original competition asks the ten highest pressure performers in the entire supplied IPL/T20I sample. User-directed RR targeting is a different, acquisition-gated question.')
rule(42,267,'USER-DIRECTED SHORTLIST','Remove players owned by rivals, retired/unavailable cricketers and Pakistan-national candidates before comparison.',426,116,PINK)
rule(492,267,'SUPPLIED-DATA EVIDENCE','Recompute IPL 2025-26 delivery rates and bring historical pressure scores forward with eligibility labels.',426,116,AQUA)
rule(42,118,'LOW CONFIDENCE','Several targets have tiny recent IPL samples. No missing IPL stats are invented; mark data absent when necessary.',426,116,GOLD)
rule(492,118,'AUCTION REGISTER PENDING','Published release != confirmed auction entry. Registration, fitness, price and late trades can change the target pool.',426,116,RED)
caption(44,59,'For a strict Unstop submission requiring global pressure top 10, the separate original global leaderboard remains a distinct artifact.')
end()

# 3 retained group
page('SQUAD STATUS / OFFICIAL','The 19 players RR actually control today.','No released or rival-team player appears in this roster. Overseas designations affect the Impact Player plan.')
records=[
('Batting / wicketkeeping','Yashasvi Jaiswal, Vaibhav Sooryavanshi, Dhruv Jurel, Riyan Parag (C), Aman Rao Perala, Shubham Dubey'),
('Batting / all-round flexibility','Ravindra Jadeja, Donovan Ferreira (OS), Lhuan-dre Pretorius (OS), Dasun Shanaka (OS)'),
('Indian bowling','Mohammed Shami, Manimaran Siddharth, Sandeep Sharma, Brijesh Sharma, Ravi Bishnoi, Sushant Mishra, Yash Punja'),
('Overseas bowling','Jofra Archer (OS), Nandre Burger (OS)')]
for i,(title,body) in enumerate(records):
 xx=42+(i%2)*447; yy=240-(i//2)*130
 box(xx,yy,426,119);kicker(xx+16,yy+94,title)
 para(xx+16,yy+66,body,395,12,'Semi',WHITE,16,4)
win('RR have 5 retained overseas players; build combinations from this actual core, not previous-season XIs.')
end()

# 4 releases
page('SQUAD STATUS / THE CUT','Nine releases. Two new arrivals. Two old assumptions fixed.','This is the exact roster reset that changes the auction requirements and our earlier proposed playing XIs.')
box(42,215,426,164)
kicker(58,351,'RELEASED / NO LONGER IN RR')
para(58,320,'Shimron Hetmyer  |  Tushar Deshpande\nAdam Milne  |  Kuldeep Sen  |  Yudhvir Singh\nKwena Maphaka  |  Vignesh Puthur\nRavi Singh  |  Emanjot Singh Chahal',392,12,'Semi',WHITE,24,6)
box(486,215,431,164)
kicker(504,351,'OFFICIALLY TRADED')
para(504,313,'IN  /  Mohammed Shami\nIN  /  Manimaran Siddharth\nOUT  /  Sam Curran',395,17,'Semi',WHITE,35,3)
rect(42,125,875,69,NAV3,12)
para(59,168,'CORRECTION TO THE PREVIOUS REPORT',825,10,'Bold',PINKL)
para(59,143,'Tushar and Hetmyer cannot be selected from the retained squad. A Tushar return would require a fresh auction purchase.',819,12,'Semi',WHITE,16,2)
win('Treat the Shami/Siddharth trade as confirmed; retain auction budget discipline after freeing a finisher and seamer slot.')
end()

# 5 / RELEASES WITH EVIDENCE
page('RELEASE REVIEW / DATA','Why RR made room: departures tested against real output.','These are IPL-wide 2025-26 clean-sample figures, including appearances for other franchises; not all are RR-only records.')
rows=[
['Shimron Hetmyer','2025: 224 runs @ 144.5 SR','2026: 72 runs @ 116.1 SR','Finishing space + overseas slot freed'],
['Tushar Deshpande','2025: 9 wickets, 10.41 eco','2026: 3 wickets, 11.71 eco','Indian pace cover must be replaced'],
['Adam Milne','No 2025 sample','2026: 0 wickets / 20 balls, 12.30 eco','Insufficient 2026 evidence for impact'],
['Kwena Maphaka','2025: 1 wicket / 30 balls, 10.80 eco','No 2026 sample','Overseas pace development not retained'],
['Vignesh Puthur','2025: 6 wickets, 9.08 eco','No 2026 sample','Earlier 2025 output not RR-only'],
['Yudhvir Singh','2025: 4 wickets, 12.00 eco','No 2026 sample','Depth role released; sparse comparison']]
tab(42,368,875,['RELEASED PLAYER','2025 CLEAN SAMPLE','2026 CLEAN SAMPLE','TEAM CONSEQUENCE'],rows,[174,219,208,274],36,9.2)
para(44,103,'Kuldeep Sen and Emanjot Chahal had no qualifying 2025-26 IPL deliveries in this data. Ravi Singh faced only two balls in the 2026 sample. Absence of evidence is not evidence of poor ability.',857,9.7,'Lato',SUB,13,3)
end()

# 5 dataset scope
page('METHOD / REPRODUCIBLE','The evidence is the supplied ball-by-ball dataset.','Not reputations: every IPL number in this report is computed from the updated CSV and the match inclusion audit.')
stat(42,267,214,'138','ELIGIBLE IPL MATCHES','68 in 2025 + 70 in 2026',AQUA)
stat(270,267,214,'33,167','DELIVERY EVENTS','Cleaned 2025-26 sample',AQUA)
stat(498,267,214,'14','RECENT IPL VENUES','Venue estimates vary in size',AQUA)
stat(726,267,190,'2','COMPARISON YEARS','Form/role, not prediction',AQUA)
rule(42,124,'DATA RULES','Full-score nonstandard and DLS/tied matches excluded; wides/no-balls not legal deliveries; run-outs not credited to bowlers.',420,121,PINK)
rule(502,124,'INTERPRETATION','Observed venue scoring is not a live pitch forecast. Domestic league figures are separate from the supplied IPL data.',415,121,GOLD)
win('Compare roles by phase and season, and downgrade conclusions when the player or venue sample is small.')
end()

# 6 batting/bowling power
page('TEAM PERFORMANCE','Powerplay bowling is the highest-confidence repair.','RPO means runs per six legal balls. Bars compare RR bowling in the cleaned 2025 vs 2026 IPL samples.')
kicker(44,359,'RR CONCEDED / RUNS PER OVER')
for i,(ph,a,b) in enumerate([('POWERPLAY',9.46,10.46),('MIDDLE OVERS',9.56,9.48),('DEATH OVERS',12.15,10.69)]):
 y=313-i*82;text(44,y,ph,13,'Bold',WHITE)
 rect(208,y+3,465,13,NAV3,6);rect(208,y+3,465*a/14,13,'#AFD7D3',6)
 rect(208,y-19,465,13,NAV3,6);rect(208,y-19,465*b/14,13,PINK,6)
 text(693,y+5,f'2025  {a:.2f}',11,'Semi',BLUE)
 text(693,y-17,f'2026  {b:.2f}',11,'Semi',PINKL)
rect(44,115,870,61,NAV2,10)
text(60,152,'+1.00 RPO',20,'Black',RED);text(236,152,'Powerplay concession worsened.',14,'Semi',WHITE)
text(236,131,'Death economy improved - target the remaining phase gap, not a complete overhaul.',11,'Lato',BLUE)
win('Pair Shami with Archer/Burger early, then protect Archer + Brijesh in the closing overs.')
end()

# 7 batting summary
page('CURRENT XI / BATTING','Retention earns continuity. Selection earns the trophy.','Seasonal splits show both sustainable strengths and reasons not to extrapolate a few innings.')
batters=['Vaibhav Sooryavanshi','Yashasvi Jaiswal','Dhruv Jurel','Riyan Parag','Donovan Ferreira','Shubham Dubey','Lhuan Pretorius']
rows=[]
for n in batters:
 p25=get(n,2025,'bat_runs');p26=get(n,2026,'bat_runs');s25=get(n,2025,'bat_strike_rate');s26=get(n,2026,'bat_strike_rate')
 rows.append([n,f'{int(p25)} / {fmt(s25)}' if p25 is not None else 'no IPL sample',f'{int(p26)} / {fmt(s26)}' if p26 is not None else 'no IPL sample', 'LIMITED' if n=='Lhuan Pretorius' else ('ROLE CORE' if n in batters[:5] else 'BACKUP')])
tab(42,355,875,['BATTER','2025 RUNS / SR','2026 RUNS / SR','USE'],rows,[240,211,211,213],32,10)
para(43,75,'2026: Vaibhav 737 at SR 235.5; Jurel 513 at 155.5; Ferreira 317 at 179.1. Pretorius has only 8 IPL balls in this cleaned sample.',864,10,'Lato',SUB,14,2)
end()

# 8 bowlers
page('CURRENT XI / BOWLING','The best bowling recruitment may already be done.','Official new arrival Shami fills a specific phase; do not force him into an expensive death-overs role.')
focus=['Jofra Archer','Mohammed Shami','Brijesh Sharma','Nandre Burger','Ravi Bishnoi','Ravindra Jadeja','Manimaran Siddharth','Yash Punja']
rows=[]
for n in focus:
 w25=get(n,2025,'bowl_wickets');w26=get(n,2026,'bowl_wickets');e25=get(n,2025,'bowl_economy');e26=get(n,2026,'bowl_economy')
 rows.append([n,f'{int(w25) if w25 is not None else 0} / {fmt(e25)}',f'{int(w26) if w26 is not None else 0} / {fmt(e26)}'])
tab(42,351,875,['BOWLER','2025 WKTS / ECO','2026 WKTS / ECO'],rows,[310,282,283],32,11)
caption(43,58,'SHAMI 2026: 8 POWERPLAY WICKETS, 7.96 ECO (150 LEGAL BALLS). BRIJESH 2026: 8 DEATH-OVER WICKETS (93 BALLS).')
end()

# 9 role map
page('THE BOWLING BLUEPRINT','Make every bowler own a phase, not just four overs.','2026 supplied-data sample, phase-specific rates; small samples are marked before a selection recommendation.')
items=[('MOHAMMED SHAMI','POWERPLAY','8 wickets / 150 balls / 7.96 eco','Use overs 1, 3, possibly 5. Death 14.00 eco across 36 balls is a warning.',AQUA),('JOFRA ARCHER','STRIKE + DEATH','24 wickets / 348 balls / 9.34 overall','Protect the 18th or 19th over rather than spending all four early.',PINK),('BRIJESH SHARMA','DEATH DEVELOPMENT','8 death wickets / 93 balls / 10.58 eco','An Indian closing-over candidate, not an established world-class certainty.',GOLD),('NANDRE BURGER','PACE / LEFT-ARM','6 powerplay wickets / 150 balls / 9.96 eco','Conditions-led alternative to an extra spinner or batting foreigner.',GREEN)]
for i,(n,role,statv,desc,cc) in enumerate(items):
 x=42+(i%2)*447;y=219-(i//2)*150
 box(x,y,429,137);rect(x,y+132,429,5,cc);kicker(x+15,y+109,n,cc);text(x+15,y+85,role,15,'Black',WHITE)
 text(x+15,y+63,statv,11,'Semi',BLUE);para(x+15,y+41,desc,400,10,'Lato',BLUE,14,3)
win('Define a phase plan before the toss: Shami early; Archer on leverage balls; Brijesh in a managed death role.')
end()

# 10 spin map
page('SPIN / INTERNAL DEPTH','Spin choice must be matchup-led, not automatic.','RR have enough retained spin options to avoid treating every uncapped spinner as a critical auction target.')
rule(42,258,'JADEJA / CONTROL','2026: 10 wickets, 8.39 economy. Primary left-arm spinner with batting value.',415,128,AQUA)
rule(497,258,'BISHNOI / ATTACK','2026: 9 wickets, 9.67 economy. Leg-spin variety for wicket-taking middle overs.',420,128,PINK)
rule(42,112,'M. SIDDHARTH / MATCHUP','2026: 6 wickets in 4 clean IPL matches, 9.67 economy; left-arm change-up, limited sample.',415,128,GOLD)
rule(497,112,'YASH PUNJA / UPSIDE','2026: 9 wickets, 9.30 economy across 180 balls; develop rather than replace by reflex.',420,128,GREEN)
win('Only invest heavily in another spinner if the auction player clearly outperforms an existing role.')
end()

# 11 two existing finisher
page('THE FINISHING DECISION','Pretorius is the upside. Ferreira is the proven death hitter.','Replacing Hetmyer does not mean asking a top-order overseas hitter to suddenly become a No. 7 finisher.')
box(42,153,427,227);kicker(61,352,'LUHAN-DRE PRETORIUS / TOP-MIDDLE')
text(60,296,'463',52,'Black',AQUA);text(179,298,'RUNS',13,'Bold',WHITE)
text(62,273,'2026 CSA PRO T20 CUP  /  SR 195.36',11,'Bold',BLUE)
para(60,239,'Excellent recent domestic output: 463 off 237 balls. Yet only 8 IPL balls faced in the filtered 2026 sample.',380,12,'Lato',WHITE,18,4)
rect(61,169,384,34,NAV3,6);text(73,181,'DEPLOY AT NO. 3 / 4  -  NOT A PROVEN NO. 7',10,'Bold',PINKL)
box(487,153,428,227);kicker(505,352,'DONOVAN FERREIRA / FINISHER')
text(504,296,'221.7',52,'Black',PINK);text(708,298,'SR',13,'Bold',WHITE)
text(504,273,'2026 IPL DEATH OVERS  /  83 BALLS',11,'Bold',BLUE)
para(504,239,'317 IPL runs at overall SR 179.1 in the 2026 cleaned sample. The most direct evidence of late-innings hitting in the retained group.',383,12,'Lato',WHITE,18,4)
rect(505,169,388,34,NAV3,6);text(516,181,'KEEP AS DESIGNATED NO. 5 / 6 FINISHER',10,'Bold',PINKL)
win('Use Pretorius to unlock the order and Ferreira to close. Buy Indian late-order support, not a duplicate opener.')
end()

# 12 venue data
page('VENUE INTELLIGENCE','Every ground has a different scoring problem.','All 14 venues in the 2025-26 cleaned sample; rates are descriptive historical averages, never a pitch forecast.')
v=venues.sort_values('overall_rpo',ascending=False)
rows=[]
for _,r in v.iterrows():
 city=r.venue.split('/')[0].strip(); rows.append([city,str(int(r.matches)),f'{r.overall_rpo:.2f}',f'{r.pp_rpo:.2f}',f'{r.death_rpo:.2f}',r.sample_caution])
tab(42,373,875,['VENUE','MATCHES','RPO','PP RPO','DEATH RPO','CONFIDENCE'],rows,[260,87,95,105,130,198],20.9,9)
caption(42,42,'LOW: FEWER THAN SIX MATCHES. MODERATE: SIX TO NINE. MATCHES WITHOUT FULL STANDARD DATA EXCLUDED.')
end()

# 13 venue decisions
page('GROUND PLANS','Win the matchups, not the reputation of the pitch.','Selection templates are triggered by observed conditions and opposition, not just a stadium name.')
items=[('JAIPUR / 10.47 RPO','Attack pace and defend boundaries.','Start three overseas hitters/seamers only if boundary conditions validate; preserve an Indian death-impact option.'),('CHEPAUK / 8.99 RPO','Spin-control scenario.','Jadeja + Bishnoi, with Siddharth when conditions reward slow bowling. Protect an Indian pace-impact option.'),('GUWAHATI / 8.96 RPO','Small sample: verify pitch.','Only four clean matches; do not infer turn from one average. Use match-day visual evidence.'),('WANKHEDE / 10.06 RPO','Pace and finishing.','Keep Archer as a closing option, favor a real No. 6 hitter, monitor dew and chasing conditions.')]
for i,(nm,aa,bb) in enumerate(items):
 x=42+(i%2)*447;y=252-(i//2)*139
 box(x,y,426,125);kicker(x+15,y+100,nm,PINKL);text(x+15,y+75,aa,16,'Black',WHITE);para(x+15,y+53,bb,395,10.5,'Lato',BLUE,14,3)
win('Use historical venue data as a pre-match prior; finalize the XI after pitch inspection, boundary sizes and toss.')
end()

# 14 venue bands
page('VENUE INTELLIGENCE / OTHERS','Give the captain a decision rule at every IPL venue.','The recommended bowling mix changes with first-innings par, observed movement, dew, and opponent batting handedness.')
rows=[
['Dharamshala','10.60','5 - LOW','Pace + stronger death hitting; do not overfit sample'],
['Hyderabad','10.21','12','Boundary prevention and Indian finishing depth'],
['Mullanpur','10.00','12','Shami early; retain death specialist'],
['Bengaluru','9.90','9 - MOD','Protect powerplay; death-overs matchup critical'],
['Delhi','9.85','13','Use batting depth; rotate pacer/spinner by pitch'],
['Ahmedabad','9.61','17','Balanced XI; clear death-over allocations'],
['Kolkata','9.58','12','Check surface; Jadeja/Bishnoi/Siddharth flexibility'],
['Lucknow','9.48','13','Spin matchups may matter; stay evidence-led'],
['Visakhapatnam','10.10','2 - LOW','No fixed pitch label; prioritize real inspection'],
['Raipur','9.08','2 - LOW','Avoid data-only ground-specific verdicts']]
tab(42,369,876,['GROUND','RPO','SAMPLE','TACTICAL RESPONSE'],rows,[174,91,117,494],23,9.7)
win('Venue calibration must change team selection, not just decorate a statistical appendix.')
end()

# 15 required auction jobs
page('AUCTION / ROLE GAP AUDIT','Spend for roles that unlock multiple legal XIs.','Need = roster deficiency after the official releases, not a generic ranking of available cricket talent.')
rows=[
['1','INDIAN NO. 5-7 FINISHER','HIGH','Hetmyer out; partner Ferreira without 4th overseas bat'],
['2','INDIAN PACE / DEATH COVER','HIGH','Tushar out; give Archer/Shami/Brijesh injury insurance'],
['3','OVERSEAS SPECIALIST PACE','CONDITIONAL','Only if quality + medical + price justify it'],
['4','INDIAN WK-BAT COVER','MEDIUM','Jurel first choice, overseas keepers add flexibility'],
['5','INDIAN LEFT-ARM SEAM DEPTH','MEDIUM','Burger an overseas option; Indian balance valuable'],
['6','SPIN ALL-ROUNDER / PROJECT','LOW','Jadeja, Siddharth, Bishnoi and Punja already here']]
tab(42,363,875,['RANK','NEEDED ROLE','PRIORITY','WHY IT MATTERS'],rows,[64,258,144,409],36,10)
win('Auction should add Indian batting and pace depth before chasing expensive celebrity replacements.')
end()

# 16 shortlisted released IPL players
page('AUCTION / TESTED IN IPL','2027 released-list targets: judge the role, then the price.','All IPL figures below are from the user-supplied 2025-26 ball records; registration and auction availability are not yet confirmed.')
rows=[
['M Shahrukh Khan','No. 5-7 hitter','2025: 173 @ SR 184.0','2026: 43 @ SR 130.3','STRONG ROLE, FORM RISK'],
['Nehal Wadhera','LHB No. 4-6','2025: 335 @ SR 144.4','2026: 65 @ SR 114.0','MIDDLE ORDER NOT PURE FINISH'],
['Abishek Porel','WK / LH bat','2025: 244 @ SR 154.4','2026: 108 @ SR 122.7','KEEPER COVER, TOP-ORDER LEAN'],
['Prashant Veer','Spin all-rounder','No 2025 IPL sample','2026: 90 @ SR 134.3','UPSIDE, EXPENSIVE RISK'],
['Akash Madhwal','Indian pace','2025: 4 wkts / eco 11.07','2026: no clean IPL sample','DEATH ROLE NOT VERIFIED'],
['Matheesha Pathirana','OS strike pace','2025: 13 wkts / eco 10.14','2026: 8 legal balls','FITNESS / BIG-BID RISK']]
tab(42,369,875,['NAME','IPL ROLE','2025','2026','SCOUT VERDICT'],rows,[173,164,167,161,210],37,9.8)
win('Shahrukh is the clearest released-player finisher role fit; every alternative has a real limitation.')
end()

# 17 scouts domestic
page('AUCTION / DOMESTIC UPSIDE','Uncapped scouting should create value, not certainty.','Recent domestic numbers are separately sourced - the uploaded datasets contain IPL/T20I, not all domestic leagues.')
items=[
('SANVIR SINGH','377 runs / SR 183.90','Sher-e-Punjab T20 2026, 8 matches','Indian No. 5-7 power, if auction-registered. Test against pace before relying on death batting.'),
('SALMAN NIZAR','306 runs / SR 157.73','Kerala Cricket League 2026, 12 matches','Left-handed depth; a more conservative finisher candidate. State-league to IPL translation unproven.'),
('CHAMA MILIND','17 wickets / 9 matches','SMAT 2025-26, Hyderabad','Indian left-arm pace variety; overs/phase splits and auction registration need verification.')]
for i,(n,big,meta,details) in enumerate(items):
 x=42+i*296;box(x,140,280,245);rect(x,380,280,5,[PINK,AQUA,GOLD][i]);kicker(x+16,357,n,[PINKL,AQUA,GOLD][i]);text(x+16,313,big,19,'Black',WHITE)
 para(x+16,283,meta,247,10,'Semi',SUB,13,2);ln(x+16,244,x+263,244)
 para(x+16,220,details,249,12,'Lato',BLUE,18,5)
win('Prioritize uncapped specialists for cost-controlled depth; verify November 23 registration and the final auction list.')
end()

# 18 why vs what
page('AUCTION / THE TRADEOFFS','Why these names - and why not buy everyone?','The strongest scouting decisions have a role-based upside, a price ceiling and a documented downside.')
rows=[
['Shahrukh > another opener','2025 IPL SR 184.0 at 94 balls','He can bat No. 6; RR openers are set','2026 33 balls only / SR 130.3'],
['Sanvir > top-order depth','2026 domestic 377 @ 183.9','Indian finish option; frees OS bowling','IPL translation unknown'],
['Chama > expensive new-ball clone','17 SMAT wkts in 2025-26','Left-arm Indian seam balance','No IPL phase-level proof'],
['Porel > overseas WK cover','2025 IPL 244 @ SR 154.4','Domestic WK insurance; Indian-impact ready','No demonstrated death hitting'],
['Pathirana only at right price','2025 13 wickets','Possible death specialist when fit','2026 injury + tiny IPL sample'],
['Do not chase Deepak first','2025 10 wkts / 9.05 eco','Experienced powerplay option','Shami already performs that job']]
tab(42,369,875,['DECISION','SUPPORT','RR ROLE FIT','DOWNSIDE / CAVEAT'],rows,[214,177,253,231],35,9.3)
win('Select incremental marginal value over the existing 19, not reputation or auction hype.')
end()

# 19 budget
page('AUCTION / RESOURCE ALLOCATION','A disciplined six-slot bidding plan: keep a reserve.','Caps are analyst-imposed scenario limits, not auction forecasts. If prices exceed the ceiling, change the target.')
rows=[
['1','M Shahrukh Khan','Indian finishing specialist','6.00'],
['2','Sanvir Singh','Indian batting-impact upside','2.00'],
['3','Chama Milind','Indian left-arm seam cover','1.75'],
['4','Abishek Porel','Indian WK-bat cover','3.50'],
['5','Matheesha Pathirana','Overseas pace, only if medically cleared','7.00'],
['6','Akash Madhwal','Development pace / depth fallback','2.50']]
tab(42,376,876,['SLOT','EXAMPLE TARGET','PROPOSED JOB','MAX BID CR'],rows,[68,223,460,125],37,11)
spent=sum([6,2,1.75,3.5,7,2.5]);box(42,84,874,38,NAV3)
text(59,97,f'PLANNED MAX = INR {spent:.2f} CR',13,'Black',WHITE)
text(900,97,f'UNCOMMITTED RESERVE = INR {27.05-spent:.2f} CR',13,'Black',AQUA,'right')
caption(43,70,'SIX PURCHASES ASSUMED TO WIN AT OR BELOW CAPS. THE NUMBERS ARE A RESOURCE SCENARIO, NOT MARKET PRICES.')
end()

# 20 impact rule
page('MATCHDAY / IMPACT RULE','The 12th specialist is how RR buy tactical optionality.','The Impact Player rule is in force for the 2025-27 IPL cycle. Check the final match regulations on game day.')
rule(42,260,'FOUR OVERSEAS RULE','At most 4 overseas in the starting XI. When all 4 are named initially, an overseas Impact Player cannot be brought in.',425,120,PINK)
rule(494,260,'THREE-OVERSEAS ADVANTAGE','With 3 overseas starting, RR may introduce a fourth overseas Impact Player when substitution is legal.',423,120,AQUA)
rule(42,116,'LEGAL ACTIVATION','Typical opportunities: before innings, at end of an over, after a wicket / batter retirement under applicable conditions.',425,120,GOLD)
rule(494,116,'ONE SPECIALIST SWITCH','One player leaves and the Impact Player becomes a participant. Do not assume the replaced player can return.',423,120,GREEN)
win('Naming just three overseas initially allows a Burger-for-Pretorius or Indian-for-overseas tactical path.')
end()

# 21 batting first
page('MATCHDAY / BATTING FIRST','Bat deep. Then add the missing bowling specialist.','Scenario A: three overseas start; an extra Indian bat is available up to the innings switch.')
xi=['Yashasvi Jaiswal','Vaibhav Sooryavanshi','Lhuan-dre Pretorius (OS)','Riyan Parag (C)','Dhruv Jurel (WK)','Donovan Ferreira (OS)','Shubham Dubey','Ravindra Jadeja','Jofra Archer (OS)','Mohammed Shami','Ravi Bishnoi']
for i,n in enumerate(xi):
 y=364-i*23.4
 text(51,y,f'{i+1:02d}',10,'Bold',PINKL);text(85,y,n,11,'Semi',WHITE)
box(486,229,430,148);kicker(504,348,'WHEN FIRST INNINGS ENDS')
para(504,317,'Replace Shubham Dubey (if his batting role is complete) with Brijesh Sharma for Indian death bowling.',389,12,'Semi',WHITE,17,5)
box(486,90,430,125);kicker(504,186,'OVERSEAS ALTERNATIVE')
para(504,154,'On a pace-friendly surface, use Nandre Burger instead of Brijesh - 3 overseas become 4, which is allowed.',388,11,'Lato',BLUE,16,4)
caption(50,75,'STARTING OS = 3; INDIAN IMPACT = 3 OS; BURGER IMPACT = 4 OS. NO RELEASED PLAYERS INVOLVED.')
end()

# 22 bowling first spin
page('MATCHDAY / BOWLING FIRST','Use a specialist spinner, then bring in the chase batter.','Scenario B: two overseas in the starting XI allow Pretorius as a legal overseas Impact Player.')
xi=['Yashasvi Jaiswal','Vaibhav Sooryavanshi','Riyan Parag (C)','Dhruv Jurel (WK)','Donovan Ferreira (OS)','Ravindra Jadeja','Jofra Archer (OS)','Mohammed Shami','Ravi Bishnoi','Manimaran Siddharth','Brijesh Sharma']
for i,n in enumerate(xi):
 y=364-i*23.4;text(51,y,f'{i+1:02d}',10,'Bold',PINKL);text(85,y,n,11,'Semi',WHITE)
box(486,219,430,158);kicker(504,348,'AFTER BOWLING / START OF CHASE')
para(504,319,'Bring in Lhuan-dre Pretorius for Siddharth. Pretorius slots at No. 3; RR gain batting depth after using the spin specialist.',389,12,'Semi',WHITE,17,5)
box(486,93,430,111);kicker(504,174,'WHY THIS IS LEGAL')
para(504,146,'Initially 2 overseas; after the switch 3 overseas. Siddharth is finished bowling and the XI gains a batter.',390,11,'Lato',BLUE,16,4)
caption(50,72,'USE THIS PLAN ONLY IF THE MATCH DAY SURFACE WARRANTS A THIRD SPIN OPTION.')
end()

# 23 bowling first pace
page('MATCHDAY / BOWLING FIRST','The overseas pace-to-batter switch keeps the XI balanced.','Scenario C: start Burger as a pace specialist; replace him with Pretorius when chasing.')
xi=['Yashasvi Jaiswal','Vaibhav Sooryavanshi','Riyan Parag (C)','Dhruv Jurel (WK)','Donovan Ferreira (OS)','Ravindra Jadeja','Jofra Archer (OS)','Mohammed Shami','Nandre Burger (OS)','Ravi Bishnoi','Brijesh Sharma']
for i,n in enumerate(xi):
 y=364-i*23.4;text(51,y,f'{i+1:02d}',10,'Bold',PINKL);text(85,y,n,11,'Semi',WHITE)
box(486,204,430,174);kicker(504,347,'THE IMPACT EXCHANGE')
para(504,317,'BOWL: Burger complements Shami + Archer on a seam-friendly ground.\nCHASE: Pretorius replaces Burger, joins No. 3 / 4; the overseas count stays at 3.',383,12,'Semi',WHITE,18,6)
box(486,92,430,95);kicker(504,159,'WHEN NOT TO USE IT')
para(504,132,'Do not select Burger purely for reputation when the pitch clearly rewards spin.',389,11,'Lato',BLUE,15,3)
caption(50,73,'START WITH 3 OVERSEAS. AN OVERSEAS-FOR-OVERSEAS SWITCH IS PERMITTED IN THIS CASE.')
end()

# 24 multi-XI with purchased
page('MATCHDAY / POST-AUCTION','Bought players must have a defined Impact Player job.','Potential acquisition roles only - the following examples become available if RR actually acquires the named player.')
items=[
('SHAHRUKH / SANVIR','Batting first','Add to a batting-heavy XI at No. 6-7, then substitute a completed batting specialist for Brijesh or Siddharth.'),
('AKASH MADHWAL','Bowling second','Indian pace Impact option if RR need a fifth bowling specialist; cannot assume he fixes death economy.'),
('ABISHEK POREL','Batting insurance','Select as specialist batter or emergency keeper backup; if Jurel keeps, Porel does not need to be on the field.'),
('PATHIRANA (OS)','Three-OS start only','Can be introduced as fourth overseas Impact if he is purchased, available, medically cleared, and one legal role is replaced.')]
for i,(name,scenario,body) in enumerate(items):
 xx=42+(i%2)*447;yy=251-(i//2)*138
 box(xx,yy,426,125);kicker(xx+16,yy+101,name);text(xx+16,yy+77,scenario,14,'Black',WHITE)
 para(xx+16,yy+55,body,395,10.5,'Lato',BLUE,14,3)
win('Auction targets should be evaluated by which starting XI and Impact substitution they actually unlock.')
end()

# 25 decision board
page('TITLE PATH / MANAGEMENT','The championship checklist: every decision has an owner.','What RR should verify before bidding and what the analysts should track from game one.')
rows=[
['AUCTION','No. 6 Indian runs / pace cover / WK depth','Role-fit bids; avoid duplicate specialists'],
['MEDICAL','Archer, Shami, Burger, overseas target','Availability and workload review'],
['VENUE','14 observed venues + match-day conditions','Recompute par, phase scoring, right/left matchups'],
['IMPACT','Three overseas vs four at toss','Pre-register five options and substitute trigger'],
['PLAYER FORM','2025-26 IPL + domestic 2026','Trend, sample size, role, coaching assessment'],
['REVIEW','After each 3-match window','Phase RPO, wicket timing, death-overs execution']]
tab(42,361,875,['WORKSTREAM','QUESTION','MEASURABLE ACTION'],rows,[146,338,391],36,11)
win('A title blueprint is valuable only when it changes auction bids, playing XIs and in-match decisions.')
end()

# 26 limitations
page('INTEGRITY / EVIDENCE','What we can prove - and what we cannot predict.','A winning claim is credible only if the model separates observed evidence from decision assumptions.')
rule(42,257,'PROVEN / SOURCES','Official squad and trading status (17 Nov). Historical delivery-level 2025-26 stats from the supplied data.',426,131,AQUA)
rule(494,257,'OBSERVED, NOT CERTAIN','Stadium scoring averages; past roles; small domestic samples. No audited 2027 pitch, dew or opponent plan.',423,131,GOLD)
rule(42,109,'NOT YET CONFIRMED','Auction registration list, individual bids, availability of released players and final 2027 playing conditions.',426,131,PINK)
rule(494,109,'NO MATCH GUARANTEES','No model can promise RR the title. The goal is robust selection odds, resilience and repeatable improvement.',423,131,RED)
win('The promise is better decisions under uncertainty - not a fabricated guarantee of the IPL trophy.')
end()

# 27 sources
page('RESEARCH / PROVENANCE','Every high-stakes claim has a traceable source.','Source dates: RR official 17 Nov 2026, IPL official 2024 and 2026, domestic 2025-26 and 2026.')
sources=[
('RR official - 2027 retained, released, purse','https://www.rajasthanroyals.com/latest-news/ipl-2027-rr-players-retention-list-retained-released'),
('IPL official - Shami / Siddharth / Curran trade','https://www.iplt20.com/news/article/mohd-shami-and-m-siddharth-traded-to-rajasthan-royals-sam-curran-traded-to-lucknow-super-giants'),
('IPL official - Impact Player 2025-27 cycle','https://www.iplt20.com/news/article/ipl-governing-council-announces-tata-ipl-player-regulations-2025-27'),
('IPL 2026 playing conditions - overseas 4-player limit','https://documents.iplt20.com/bcci/documents/1774265031558_TATA_IPL_2026_Match_Playing_Conditions.pdf'),
('Cricbuzz - IPL 2027 other clubs releases','https://www.cricbuzz.com/cricket-news/140949/ipl-2027-all-retentions-and-releases'),
('Wisden - 2027 all-team retained/released lists','https://www.wisden.com/series/ipl-2027/cricket-news/ipl-2027-retention-list-full-list-retained-released'),
('Cricbuzz - CSA 2026 Pretorius batting','https://www.cricbuzz.com/cricket-series/13180/csa-t20-challenge-2026/stats'),
('Cricbuzz - Sher-e-Punjab 2026 Sanvir','https://m.cricbuzz.com/cricket-series/13073/sher-e-punjab-t20-league-2026/stats'),
('CricTracker - Kerala Cricket League Salman','https://www.crictracker.com/kerala-cricket-league/stats/batting-most-runs/'),
('myKhel - SMAT 2025-26 Chama Milind','https://www.mykhel.com/cricket/x-stats-s9792/')]
for i,(name,url) in enumerate(sources):
 y=357-i*29
 text(44,y,f'[{i+1:02d}]  {name}',12,'Semi',AQUA if i<4 else BLUE)
 c.linkURL(url,(43,y-3,918,y+13),relative=0)
caption(44,44,'OTHER PRIMARY EVIDENCE: USER-SUPPLIED UPDATED BALL-BY-BALL DATA, PRESSURE MODEL OUTPUTS, RETENTION CHECKS + REPRODUCIBLE TARGET CSVS.')
end()

# 28 final
page_count+=1
rect(0,0,W,H,NAV)
for x in range(400,1070,23):ln(x,0,x-230,540,'#FCE3ED',1)
rect(52,468,199,28,PINK,14);text(151,477,'THE 2027 WINNING SYSTEM',10,'Bold',ONPINK,'center')
text(52,406,'KEEP THE CORE.',45,'Black',WHITE)
text(52,330,'BUY THE GAPS.',57,'Black',PINK)
text(52,251,'WIN THE MOMENTS.',51,'Black',WHITE)
ln(52,218,763,218,PINK,4)
para(54,178,'A confirmed roster. A six-slot plan. A phase-specific bowling attack. An Impact Player advantage. Fifteen players do not win a title by name alone - the correct twelve must win the right overs.',735,17,'Semi',BLUE,24,4)
rect(0,0,W,47,PINK)
text(52,17,'THIS IS HOW RAJASTHAN ROYALS GIVE THEMSELVES THE BEST SHOT AT IPL 2027.',12,'Bold',ONPINK)
end()
c.save()
print('wrote',OUT,'pages',page_count, 'bytes',OUT.stat().st_size)
