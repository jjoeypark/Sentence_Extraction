import msoffcrypto
import io
import pandas as pd
import datetime

datapath = "220405goutdata"
dtypes = ['dx', 'med', 'lab', 'firsts', 'afters']
dtypes_use_date = {'dx': '진단일자', 'med': '약품처방일'}
dtypes_to_revise_date = {'lab': '검사시행일', 'firsts': '서식작성일', 'afters': '서식작성일'}
pw = '1357decaf$'
dfs = []

def datetimestr_to_datestr(dtstr):
    dt = datetime.datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S")
    dstr = dt.strftime("%Y-%m-%d")
    return dstr

for gid in range(1, 7):
    print(gid)
    for dtype in dtypes:
        decrypted = io.BytesIO()
        filename = f"{datapath}/{gid}/id_{gid}_{dtype}.xlsx"
        with open(filename, "rb") as f:
            file = msoffcrypto.OfficeFile(f)
            file.load_key(pw)
            file.decrypt(decrypted)
        
        df = pd.read_excel(decrypted)
        df['dtype'] = dtype
        
        # print(dtype)
        
        if dtype in dtypes_to_revise_date:
            datecol = dtypes_to_revise_date[dtype]
            df["Date"] = df[datecol].apply(datetimestr_to_datestr)
        else:
            datecol = dtypes_use_date[dtype]
            df["Date"] = df[datecol]
        

        if dtype == "dx":
            df["firstDate"] = df["첫 진단일자"]

        dfs.append(df)

datecols = ['진단일자', '약품처방일', '첫 진단일자', '검사시행일', '서식작성일']
entire_cases = pd.concat(dfs, ignore_index=True)
entire_cases.drop(columns=datecols, inplace=True)
entire_cases.to_csv(f"{datapath}/entire_cases.csv")

