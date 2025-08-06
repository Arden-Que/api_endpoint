from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

progs = pd.read_csv("./data/fy26_program_rules.csv")
ops = pd.read_csv("./data/opportunities.csv")

def find_programs(op_id):
    op = ops[ops['Opportunity ID'] == op_id]
    if op.empty:
        raise HTTPException(status_code=404, detail="Opportunity ID not found")

    stage_str = str(op['Sales Stage'].iloc[0]).strip().split('-')[0].strip()
    stage = int(stage_str)

    progs_stage_col_name = f'MCEM Stage {stage}'
    matching_programs = progs[progs[progs_stage_col_name].fillna('') == 'x']
    potential_progs = [
        {row['FY26 Program Name']: [row['Owner'], row['Eligibility Criteria']] }
        for _, row in matching_programs.iterrows()
    ]
    return potential_progs

'''
if __name__ == '__main__':
    find_programs("7-3AYWFQUCEN")
'''

@app.get("/")
def test():
    return {"test":"item"}

@app.get("/opportunities/{op_id}")
async def read_item(op_id):
    programs = find_programs(op_id)
    return programs 
