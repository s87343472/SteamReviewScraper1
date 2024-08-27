import pandas as pd

def save_to_csv(json_file):
    data = pd.read_json(json_file)
    csv_file = json_file.replace('.json', '.csv')
    data.to_csv(csv_file, index=False, encoding='utf-8-sig')
    return csv_file

def save_to_excel(json_file):
    data = pd.read_json(json_file)
    excel_file = json_file.replace('.json', '.xlsx')
    data.to_excel(excel_file, index=False)
    return excel_file