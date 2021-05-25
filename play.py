#%%
import pandas as pd
import time
from joblib import Parallel

from src.parsing.parsing_controller import ParsingController


# %%

df_test = pd.read_csv('data/adresy_dla_studentow.csv', encoding='UTF-8', header=None,  names=['Address'], delimiter=";")
adresy_dla_studentow = df_test['Address'].tolist()

def address_parser(parsing_controller: ParsingController, ad: str):
    records = parsing_controller.parse_address(ad)

    print(ad)
    print('#####')
    for i, r in enumerate(records):
        if i < 3:            
            print(f"score: {r.score} - {r.street} {r.building_number} {r.postal_code} {r.city.name}. errors: {' '.join(r.errors)}")
        else:
            break
    print("##### \n")
    return records

startTime = time.perf_counter()
parsing_controller = ParsingController()

address_parser(parsing_controller, 'al. Tysiąclecia 22, 26-110')

for i in adresy_dla_studentow:
    address_parser(parsing_controller, i)

# results = Parallel(n_jobs=2)(delayed(address_parser)(i) for i in adresy_dla_studentow)

print(time.perf_counter() - startTime)

# %%




