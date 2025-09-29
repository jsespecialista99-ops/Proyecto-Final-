import json

def load_checklist(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["checklist_contrato"]
