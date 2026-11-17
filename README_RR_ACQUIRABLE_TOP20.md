# Rajasthan Royals 2027 – acquirable top 10 batters and 10 bowlers

**Cutoff:** 17 November 2026.  **PDF:** `Rajasthan_Royals_2027_Pink_RR_Acquirable_Top10_Batters_Bowlers.pdf` (41 pages).

This is the **user-requested RR recruitment shortlist**, NOT the original SupeRR Selector competition's unrestricted overall pressure-performance leaderboard. The original contest calls for global data-only lists; the RR shortlist additionally gates on recruitment feasibility and role fit. Do not submit this RR-only shortlist in lieu of those lists unless contest rules permit.

## Eligibility gate

- Candidates must not be retained at another IPL franchise. Every ranked player except Sanvir Singh is confirmed **released by their previous club on 17 November 2026**, cross-checked against all-franchise release reports. A release does not establish that a player registered for the December auction.
- Sanvir Singh is a separately flagged domestic prospect: no team-retention confirmation found, but his participation in the 2027 auction remains UNCONFIRMED. Verify once the auction register is published; delete him from the shortlist if absent.
- Exclude retired/opted-out players (e.g. MS Dhoni, Travis Head, Mitchell Starc, Jacob Bethell), Pakistan players, and players retained by rivals.
- RR official squad: 19 players, ₹27.05 crore budget, six slots and three unfilled overseas slots.

## Scoring rubric

`RR Suitability / 100 = 8*role_fit + 6*recent_form + 4*pressure_signal + 2*evidence_strength`

Each four component grades is an **auditable analyst score from 1 to 5**, not a calibrated win-probability prediction. The pillars correspond to 40% role, 30% form, 20% pressure, 10% confidence. Source worksheet gives each player's grade, reasoning, and source data. Recent form is based on **68 eligible matches in IPL 2025 and 70 eligible matches in IPL 2026**, 33,167 delivery events in the updated CSV, filtered with the original inclusion audit. The provided IPL/T20I pressure model adds historical pressure impact and pressure sample flags. Where the pressure sample fails the original threshold (150 HP events/15 matches) we mark LOW N and do not treat it as a firm ranking claim.

The ratings reflect RR recruitment decisions, **not** global batting/bowling pressure ranks. A player can be a strong tactical fit without positive measured pressure uplift. Famous star power alone earns nothing.

## Outputs

- PDF – complete pink theme with original RR logo, squad/venue analysis, top-10 batters and bowlers, 2025–26 evidence, reasoning, Impact Player plans, acquisition priorities and risks.
- `rr_2027_acquirable_top10_batters_and_bowlers.csv` – ranked shortlist with full score breakdown and evidence.
- `rr_acquirable_targets_ipl_2025_26_and_pressure.csv` – 2025/26 stats by year for broader evaluation pool including all 20.
- `rr_acquirable_targets_phase_splits.csv` – recent batting/bowling phase splits.
- `build_rr_auction_rankings.py`, `build_realistic_target_evidence.py` – data preparation and ranking generation.
- `build_pink_rr_only.py` – PDF source; depends on earlier prepared RR squad and venue evidence files.

## Core sources

Official RR 2027 roster and released list:
https://www.rajasthanroyals.com/latest-news/ipl-2027-rr-players-retention-list-retained-released

Other clubs' 2027 releases:
https://www.cricbuzz.com/cricket-news/140949/ipl-2027-all-retentions-and-releases
https://www.wisden.com/series/ipl-2027/cricket-news/ipl-2027-retention-list-full-list-retained-released

Sanvir 2026 domestic form:
https://m.cricbuzz.com/cricket-series/13073/sher-e-punjab-t20-league-2026/stats

Auction register is not finalized as of the report date; verify registration, medical availability and any late trades before bidding.
