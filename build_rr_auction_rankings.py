from pathlib import Path
import pandas as pd, numpy as np
O=Path('/mnt/data/rr_2027_latest')
# Verified team releases from 17 Nov reports; all participation contingent on official auction register.
# Scores are a transparent scenario decision rubric (not pressure statistics), 40/30/20/10.
# fields: player,last_2026_team,origin,role,role_score,recent_score,pressure_score,confidence_score,fit_rationale,warning,impact_plan
bats=[
('M Shahrukh Khan','GT','Released','Indian No.5-7 power finisher',5,4,2,4,'Direct Indian late-overs backup to Ferreira; 2025 SR 184.0 in 94 balls.','2026: 43 from 33; historical pressure impact -9.45/120 despite adequate sample.','Bat first: keep as No.6; bowl first: Indian batting Impact for a specialist seamer.'),
('Nitish Rana','DC','Released','LHB middle-order stability',4,4,3,4,'2025/26 sample totals 391 runs; No.3-5 left-hand option if Parag/Jurel shift.','Not a like-for-like No.7 hitter; 95 pressure balls is under our 150-ball benchmark.','Chase: Indian No.3/4 replacement for a bowler; only if lineup contains another finisher.'),
('Nehal Wadhera','PBKS','Released','Indian LHB No.4-6 depth',5,3,2,4,'289 combined 2025/26 balls; left-hand balance and No.4-6 flexibility.','2026 batting SR 114.0 from 57 balls; pressure impact -9.35/120.','Bat first: No.5/6; chase: batting Impact on surfaces where extra middle-order cover matters.'),
('Abishek Porel','DC','Released','Indian wicketkeeper and LH batting cover',4,4,2,4,'2025: 244 at SR 154.4; backup to Jurel without using an overseas slot.','2026 SR fell to 122.7; better top-order than late finisher; 50 HP balls only.','Chase: keeper-batter Impact if selected substitute; use as No.3-5 rather than No.7.'),
('Pathum Nissanka','DC','Released','Overseas high-tempo opener backup',3,5,2,4,'2026 IPL: 277 at SR 160.1 from 173 balls; strong top-order cover.','Duplicates Jaiswal/Sooryavanshi opening role; occupies an overseas spot.','Condition-specific chase batting Impact only when RR start fewer than four overseas players.'),
('Sanvir Singh','Unattached / unconfirmed','Unattached; registration pending','Uncapped Indian lower-order power upside',5,3,2,1,'2026 Sher-e-Punjab T20: 377 at SR 183.90 (8 matches); attractive Indian upside.','No IPL 2025/26 batting sample; lower-standard domestic league and auction registration unverified.','Indian batting Impact for No.6/7 as a development pick, conditional on signing.'),
('Prashant Veer','CSK','Released','Indian spin all-rounder project',4,3,2,2,'2026 IPL 90 in 67 balls; offers batting plus reserve spin for conditions.','Only 67 IPL 2026 balls and 12 bowling deliveries; no proven specialist-level bowling.','Bowl first: spin matchup then middle-order batting option if retained in XI; Indian flexibility.'),
('Karun Nair','DC','Released','Experienced Indian top/middle-order reserve',3,4,1,2,'2025: 198 at SR 180.0 from 110 balls; experienced batting insurance.','Only 18 balls in 2026 at SR 100; historical pressure impact heavily negative on small sample.','Bowl first: situational top/middle-order batting Impact; not first-choice finisher.'),
('Rachin Ravindra','KKR','Released','Overseas left-handed batting/spin cover',2,3,2,3,'2025: 190 from 147 balls; secondary spin option and top-order batting.','No IPL batting in 2026 clean sample; overseas top-order already crowded.','Only if overseas top-order injuries; could be batting Impact with three overseas starters.'),
('Mitchell Owen','PBKS','Released','Overseas power-hitting project',3,1,2,1,'Potential finisher profile with batting and seam-bowling flexibility.','IPL 2025/26 total only two faced balls, scoring zero; no reliable IPL measure.','Speculative No.6 overseas batting Impact; require stronger domestic scouting and availability checks.')
]
bowls=[
('Matheesha Pathirana','KKR','Released','Overseas death-overs wicket-taker',5,3,5,4,'2025: 13 wickets in 251 legal balls; historical high-pressure impact +35.33/120 (593 events).','Only 8 clean IPL balls in 2026; medical, recent form and cost are crucial.','Bat first: overseas bowling Impact only if initial XI has three or fewer overseas players.'),
('Avesh Khan','LSG','Released','Indian death/seam bowling rotation',5,3,2,5,'19 wickets across 432 legal IPL balls in 2025/26; Indian strike-bowling role.','2025/26 combined economy above 10.5; historical pressure impact -11.44/120.','Bat first: Indian seamer Impact, used for overs 16-20 depending economy risk.'),
('Jaydev Unadkat','SRH','Released','Indian left-arm angle and bowling rotation',4,4,2,4,'2025: 10 wickets at 8.17 econ (119 balls); changes angle without foreign slot.','2026: 4 wickets at 10.91; declining consistency and age-related workload questions.','Bat first: Indian left-arm bowling Impact where early movement or variation is valued.'),
('Blessing Muzarabani','KKR','Released','Overseas hit-the-deck seam alternative',4,3,3,2,'2026: 4 wickets in just 42 legal balls, Zimbabwe pace/height option; 214 HP events overall.','Very small IPL sample; competition-adjusted IPL translation and fitness uncertain.','Overseas bowling Impact in seam-friendly conditions with max three overseas starters.'),
('Deepak Chahar','MI','Released','Indian powerplay swing and injury cover',3,4,2,5,'2025-26 IPL: 18 wickets in 375 legal balls; 2025 econ 9.05.','Duplicates Shami/Sandeep new-ball role; 2026 econ 9.92 and pressure -25.01.','Bat first: Indian bowling Impact for swing conditions or Shami fitness cover.'),
('Tushar Deshpande','RR','Released','Indian pace depth / conditional buyback',3,3,2,4,'RR familiarity; 2025 took 9 wickets in 174 legal balls.','2026: 3 wickets from 126 legal balls at 11.71; only if auction price falls.','Bat first: Indian pace Impact backup; do not automatically replace Brijesh at the death.'),
('Trent Boult','MI','Released','Overseas swing/new-ball strike bowler',2,4,2,5,'2025: 20 wickets in 322 balls; proven early-over wicket threat.','2026: 2 wickets in 91 balls and 10.95 econ; foreign slot, price and Shami overlap.','Powerplay conditions only; overseas bowling Impact requires <=3 overseas XI.'),
('Akash Madhwal','CSK','Released','Indian yorker/death bowling project',4,2,2,2,'2025 4 wickets from 90 legal balls; developmental Indian death-role prospect.','No clean IPL 2026 bowling sample; 2025 economy 11.07; unproven consistency.','Bat first: Indian bowling Impact option after training/role validation.'),
('Allah Ghazanfar','MI','Released','Overseas off-spin matchup insurance',2,4,2,3,'2026: 13 IPL wickets in 221 legal balls; alternate to existing spin options.','RR already has Jadeja, Bishnoi, Siddharth; overseas-slot and role redundancy.','Only on strong matchup spin pitch with three or fewer overseas starters.'),
('Akash Deep','KKR','Released','Indian pace depth contingency',2,1,1,2,'Experienced Indian pace reserve; possible inexpensive injury cover.','2025: only 3 wickets/114 balls, 12.05 econ; no clean IPL 2026 sample.','Indian bowling Impact only if fit, in form and bought at depth price.')
]
cols=['player','released_by','release_status','role','role_1to5','recent_1to5','pressure_1to5','evidence_1to5','reason','risk','impact_scenario']
all=[]
for group,rows in [('BATTER',bats),('BOWLER',bowls)]:
 df=pd.DataFrame(rows,columns=cols);df['discipline']=group;df['rr_fit_score_100']=8*df.role_1to5+6*df.recent_1to5+4*df.pressure_1to5+2*df.evidence_1to5
 df=df.sort_values(['rr_fit_score_100','role_1to5'],ascending=False).reset_index(drop=True);df['rr_shortlist_rank']=df.index+1
 all.append(df)
rank=pd.concat(all,ignore_index=True)
perf=pd.read_csv(O/'rr_acquirable_targets_ipl_2025_26_and_pressure.csv')
agg=[]
for name,ds in [(r.player,r.discipline) for r in rank.itertuples()]:
 g=perf[(perf.player==name)&(perf.discipline==('BAT' if ds=='BATTER' else 'BOWL'))]
 if len(g):
  bb=int(g.bat_balls.sum());br=int(g.bat_runs.sum());bl=int(g.bowl_legal.sum());wr=int(g.bowl_wickets.sum());bowr=int(g.bowl_runs.sum())
  agg.append(dict(player=name,discipline=ds,ipl_2025_26_bat_balls=bb,ipl_2025_26_bat_runs=br,ipl_2025_26_bat_sr=round(br*100/bb,1) if bb else np.nan,ipl_2025_26_bowl_legal=bl,ipl_2025_26_bowl_wickets=wr,ipl_2025_26_bowl_econ=round(6*bowr/bl,2) if bl else np.nan,hp_balls=int(g.hp_balls.iloc[0]),hp_matches=int(g.hp_matches.iloc[0]),pressure_impact_per120=float(g.hp_impact_per_120.iloc[0]) if pd.notna(g.hp_impact_per_120.iloc[0]) else np.nan,pressure_eligibility=bool(g.hp_eligible.iloc[0])))
stat=pd.DataFrame(agg)
rank=rank.merge(stat,on=['player','discipline'],how='left')
rank=rank[['discipline','rr_shortlist_rank','player','released_by','release_status','role','rr_fit_score_100','role_1to5','recent_1to5','pressure_1to5','evidence_1to5','ipl_2025_26_bat_balls','ipl_2025_26_bat_runs','ipl_2025_26_bat_sr','ipl_2025_26_bowl_legal','ipl_2025_26_bowl_wickets','ipl_2025_26_bowl_econ','hp_balls','hp_matches','pressure_impact_per120','pressure_eligibility','reason','risk','impact_scenario']]
rank.to_csv(O/'rr_2027_acquirable_top10_batters_and_bowlers.csv',index=False)
print(rank[['discipline','rr_shortlist_rank','player','rr_fit_score_100','release_status','ipl_2025_26_bat_sr','ipl_2025_26_bowl_wickets']].to_string(index=False))
