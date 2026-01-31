import pandas as pd
from decision_engine.risk_assessment import calculate_risk
from decision_engine.action_selector import select_action

df = pd.read_csv("data/human_presence_logs.csv")

df["risk"] = df.apply(lambda r: calculate_risk(
    r["human_distance"], r["human_motion"], r["environment_type"]), axis=1)

df["action"] = df["risk"].apply(select_action)

print(df)
