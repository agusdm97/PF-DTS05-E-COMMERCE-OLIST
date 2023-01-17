import os
import pandas as pd
from dataprep.eda import create_report
from warnings import simplefilter

simplefilter(action="ignore", category=FutureWarning)

datasets = os.listdir("./datasets")
os.mkdir("eda_reports")

for dataset in datasets:
    df = pd.read_csv(os.path.join("datasets", dataset))
    name = os.path.splitext(dataset)[0]
    report = create_report(df, title=name, display=["Overview", "Variables"])
    path = f"{os.getcwd()}/eda_reports/{name}_report.html"
    with open(path, "x", encoding="utf-8") as file:
        file.write(report.report)
