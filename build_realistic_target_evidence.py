from pathlib import Path
import pandas as pd, numpy as np
R=Path('/mnt/data');O=R/'rr_2027_latest'
BATS=['M Shahrukh Khan','Nehal Wadhera','Abishek Porel','Nitish Rana','Prashant Veer','Rahul Tripathi','Karun Nair','Rachin Ravindra','Mitchell Owen','Aman Khan','Ben Duckett','Pathum Nissanka','Matthew Breetzke','Connor Esterhuizen','Jacob Bethell','Mahipal Lomror','Sanvir Singh','Luvnith Sisodia','Pyla Avinash']
BOWLS=['Avesh Khan','Akash Madhwal','Matheesha Pathirana','Deepak Chahar','Tushar Deshpande','Akash Deep','Mayank Markande','Gerald Coetzee','Umran Malik','Navdeep Saini','Matt Henry','Trent Boult','Lockie Ferguson','Anrich Nortje','Jaydev Unadkat','Shivam Mavi','Praveen Dubey','Blessing Muzarabani','Luke Wood','Dushmantha Chameera','Rehan Ahmed','Spencer Johnson','Adam Milne','Keshav Maharaj','Allah Ghazanfar']
raw=pd.read_csv(R/'6af855c0e8386_ball_by_ball (1).csv',low_memory=False)
m=pd.read_csv(R/'matches.csv').merge(pd.read_csv(R/'competitions.csv'),on='comp_id',validate='many_to_one')
a=pd.read_csv(R/'superr_selector_outputs/match_inclusion_audit.csv')[['match_id','eligible','exclude_reason']]
m=m.merge(a,on='match_id',how='left',validate='one_to_one')
ms=m[(m.comp_name.isin(['IPL 2025','IPL 2026'])) & m.eligible.eq(True)].copy()
x=raw[raw.match_id.isin(ms.match_id)].copy().merge(ms[['match_id','season','venue_id']],on='match_id',validate='many_to_one')
x.season=x.season.astype(int)
x.extras_type=x.extras_type.fillna('')
x['legal_ball']=~x.extras_type.isin(['wide','Overstep','other'])
x['batter_faced']=x.legal_ball
x['bowler_runs']=x.runs+x.extras1_runs.where(x.extras_type.isin(['wide','Overstep','other']),0).fillna(0)+x.extras_2_runs.fillna(0)
x['bowler_wicket']=x.is_wicket.fillna(False)&~x.dismissal_type.fillna('').isin(['RunOut','Retire Out','Obstracting the field','Obstructing the field'])
x['batter_dismissed']=x.is_wicket.fillna(False)&x.dismissed_player_id.eq(x.striker_id)
x['phase']=np.where(x.overid<=6,'Powerplay',np.where(x.overid<=15,'Middle','Death'))
x['boundary']=x.runs.isin([4,6]);x['dot_bat']=x.runs.eq(0);x['dot_bowler']=x.bowler_runs.eq(0)
pres=pd.concat([pd.read_csv(R/'superr_selector_outputs/bat_all_players.csv').assign(discipline='BAT'),pd.read_csv(R/'superr_selector_outputs/bowl_all_players.csv').assign(discipline='BOWL')],ignore_index=True)
recs=[]; phase=[]
for discipline,names in [('BAT',BATS),('BOWL',BOWLS)]:
 for name in names:
  pr=pres[(pres.discipline==discipline)&(pres.player_name==name)]
  pb=pr.iloc[0].to_dict() if len(pr) else {}
  for season in (2025,2026):
   b=x[(x.striker_name==name)&(x.season==season)&(x.batter_faced)];w=x[(x.bowler_name==name)&(x.season==season)]
   l=int(w.legal_ball.sum());o=int(b.batter_dismissed.sum());
   rec=dict(discipline=discipline,player=name,season=season,bat_matches=int(b.match_id.nunique()),bat_balls=len(b),bat_runs=int(b.runs.sum()),bat_outs=o,bat_sr=round(b.runs.sum()*100/len(b),1) if len(b) else None,bat_avg=round(b.runs.sum()/o,1) if o else None,bat_boundary_pct=round(b.boundary.mean()*100,1) if len(b) else None,bowl_matches=int(w.match_id.nunique()),bowl_legal=l,bowl_wickets=int(w.bowler_wicket.sum()),bowl_runs=int(w.bowler_runs.sum()),bowl_econ=round(6*w.bowler_runs.sum()/l,2) if l else None,bowl_dot_pct=round(w.dot_bowler.mean()*100,1) if len(w) else None,hp_balls=int(pb.get('hp_balls') or 0) if pb else 0,hp_matches=int(pb.get('hp_matches') or 0) if pb else 0,hp_impact_per_120=round(float(pb.get('pressure_impact_per_120')),2) if pb and pd.notna(pb.get('pressure_impact_per_120')) else None,hp_uplift_per_120=round(float(pb.get('uplift_per_120')),2) if pb and pd.notna(pb.get('uplift_per_120')) else None,hp_eligible=bool(pb.get('eligible',False)) if pb else False)
   recs.append(rec)
   for ph,g in (('Powerplay',1),('Middle',2),('Death',3)):
    bb=b[b.phase==ph];ww=w[w.phase==ph];le=int(ww.legal_ball.sum())
    phase.append(dict(discipline=discipline,player=name,season=season,phase=ph,bat_balls=len(bb),bat_runs=int(bb.runs.sum()),bat_sr=round(100*bb.runs.sum()/len(bb),1) if len(bb) else None,bowl_legal=le,bowl_wickets=int(ww.bowler_wicket.sum()),bowl_econ=round(6*ww.bowler_runs.sum()/le,2) if le else None))
pd.DataFrame(recs).to_csv(O/'rr_acquirable_targets_ipl_2025_26_and_pressure.csv',index=False)
pd.DataFrame(phase).to_csv(O/'rr_acquirable_targets_phase_splits.csv',index=False)
print('SAMPLE',ms.groupby('season').size().to_dict(),len(x));print(pd.DataFrame(recs).to_string(index=False))
