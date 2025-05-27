from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
app_dir1 = Path(__file__).parent.parent

df = pd.read_csv(app_dir1 / "data/fair_warming.csv")
dfmed = pd.read_csv(app_dir1 / "data/fair_warming_scenario_medians_exceedances.csv")
dfquant = pd.read_csv(app_dir1 / "data/fair_warming_scenario_quantiles.csv")