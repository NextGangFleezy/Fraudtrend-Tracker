# Custom/Gerenated Merge Bugs Overview

This note summarises the two regression bugs that existed in the previous
implementation of `merge_with_generated_data` and what practical issues they
caused for the FraudLens demo.

## 1. Ratio bounds were not enforced

The legacy implementation blindly multiplied the total number of available rows
(custom + generated) by the user supplied ratio and used that figure as the
number of custom rows to keep. When a caller accidentally passed a ratio outside
`[0.0, 1.0]`, the intermediate counts became negative because pandas interprets
`df.iloc[:negative_number]` as "all but the last N rows". In practice that meant
that a ratio above 100% discarded most of the generated dataset, and a negative
ratio produced an empty merge. The hardened implementation now clamps the ratio
before any calculations so that accidental misconfiguration no longer drops or
silently truncates data. 【F:utils/custom_data_loader.py†L108-L133】

This bug effectively blocked FraudLens from loading a realistic blended dataset
whenever the UI slider or an environment variable fed an unexpected ratio. The
merge would succeed technically, but it produced a mangled dataset with whole
sections missing, which in turn stopped downstream dashboards from populating.

## 2. The requested mix was not achievable when one source was small

Previously the function always tried to keep the full generated dataset and only
trimmed the custom rows. If the generated dataset was much larger than the
custom dataset, the final share of custom records plummeted well below the
requested ratio. For example, combining 10 custom rows with 100 generated rows
at a 60% target still yielded 10 custom vs. 100 generated rows (≈9% custom). The
reworked logic now computes a feasible merged size, rebalances any rounding
errors, and tops up from whichever source still has capacity so the final share
stays as close as possible to what the caller asked for. 【F:utils/custom_data_loader.py†L135-L191】

This bug prevented risk analysts from running controlled demonstrations. They
would configure the tool to showcase a "mostly real" dataset, but the generated
records swamped the small custom sample, undermining the narrative they were
trying to present during demos and stakeholder reviews.
