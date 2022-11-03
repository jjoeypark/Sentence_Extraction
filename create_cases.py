import pandas as pd
import json
import numpy as np

datapath = "220405goutdata"
casepath = 'cases_new'
df_cases = pd.read_csv(f"{datapath}/entire_cases.csv")

cases = {}

for idx, row in df_cases.iterrows():
    caseNum = row["케이스번호"]
    gender = row["성별"]
    birthDate = row["생년월일"]

    p_info = {
        "caseNum": caseNum,
        "gender": gender,
        "birthDate": birthDate,
        "events": {},
        "event_dates": set()
    }
    cases.setdefault(caseNum, p_info)
    
    dtype = row["dtype"]
    date = row["Date"]
    dtypes = ['dx', 'med', 'lab', 'firsts', 'afters']
    
    event_default = {
        "dx": [],
        "lab": [],
        "med": [],
        "firsts": [],
        "afters": []
    }
    cases[caseNum]["event_dates"].add(date)
    cases[caseNum]["events"].setdefault(date, event_default)

    row_data = {}
    if dtype == "dx":
        row_data["first_date"] = row["firstDate"]
        row_data["diag_code"] = row["진단코드"]
        row_data["diag_name"] = row["진단명"]
        row_data["ICD10_code"] = row["ICD10코드"]
    elif dtype == "med":
        med_name_ingr = row["약품명(성분명)"]
        ingr_names, *rest = med_name_ingr.split(' ')
        for inge in rest:
            finge = inge[0]
            if '0' <= finge <= '9':
                ingr_amounts = inge
                break
        if not ingr_amounts:
            print(f"Error {caseNum} - Ingredient Amount Parse Failed. (rest: {rest})")
        ingr_name_list = ingr_names.split('/')
        ingr_amount_list = ingr_amounts.split('/')
        med_name_norm = row["약품명(일반명)"]
        # duration = row["투약일수"]
        if ' ' in med_name_norm:
            drug_name = med_name_norm.split(' ')[0]
        else:
            dni = len(med_name_norm)
            for i in range(len(med_name_norm)):
                mc = med_name_norm[i]
                if ('0' <= mc <= '9') or ('(' == mc):
                    dni = i
                    break
            drug_name = med_name_norm[:dni]
        if len(ingr_amount_list) < len(ingr_name_list):
            print(f"Error {caseNum} - Ingredient Size Different. (Ingr_names: {ingr_names})")
            print(row["Date"])
        ingredients = []
        for i in range(len(ingr_name_list)):
            ingr_name = ingr_name_list[i]
            ingr_amount_mg = ingr_amount_list[i]
            ingr_amount = ingr_amount_mg[:-2]
            ingr_unit = ingr_amount_mg[-2:]
            ingredient = {
                "ingr_name": ingr_name,
                "ingr_amount": ingr_amount,
                "ingr_unit": ingr_unit,
            }
            ingredients.append(ingredient)
        
        dosage, number_of_doses_per_day = row["1회처방량"].split("*")
        if dosage[0] == '.':
            dosage = '0' + dosage
        row_data["med_name_ingr"] = med_name_ingr
        row_data["med_name_norm"] = med_name_norm
        row_data["med_unit"] = row["처방단위"]
        row_data["dosage"] = dosage
        row_data["number_of_doses_per_day"] = number_of_doses_per_day
        row_data["drug_name"] = drug_name
        # row_data["duration"] = row["투약일수"]
    elif dtype == "lab":
        row_data["lab_name"] = row["검사명"]
        lab_num = row["검사결과-수치값"]
        lab_pn = row["검사결과-음성양성"]
        lab_text = row["검사결과"]
        lab_type = "Text"
        if np.isnan(lab_num):
            lab_num = ""
        try:
            if np.isnan(lab_pn):
                lab_pn = ""
        except:
            print(lab_pn)
        if lab_num:
            lab_type = "Number"
        elif lab_pn:
            lab_type = "PN"
        row_data["lab_type"] = lab_type
        row_data["lab_num"] = lab_num
        row_data["lab_pn"] = lab_pn
        row_data["lab_text"] = lab_text
    elif dtype == "firsts":
        row_data = row["서식내용"]
    elif dtype == "afters":
        row_data = row["서식내용"]
    else:
        print(f"Error {caseNum} - dtype doesn't exist. (dtype: {dtype})")
    cases[caseNum]["events"][date][dtype].append(row_data)



for case_num, case_info in cases.items():
    event_dates = list(case_info["event_dates"])
    event_dates.sort()
    case_info["event_dates"] = event_dates

    prevEvent = False
    events = case_info["events"]
    events_new = {}
    event_new_dates = []

    for date in event_dates:
        event = events[date]
        if event["dx"]:
            events_new[date] = event
            if prevEvent:
                for k, v in prevEvent.items():
                    if v:
                        events_new[date][k] = v
                prevEvent = False
            event_new_dates.append(date)
        elif prevEvent:
            for k, v in event.items():
                if v:
                    prevEvent[k] = v
        else:
            prevEvent = event
    case_info["events"] = events_new

    # event_new_dates = list(case_info["event_new_dates"])
    event_new_dates.sort()
    case_info["event_dates"] = event_new_dates
    
    with open(f"{datapath}/{casepath}/{case_num}.json", 'w') as f:
        json.dump(case_info, f)