import pandas as pd

title_file = pd.read_excel(r'cargill_lda_output.xlsx')
body_file = pd.read_excel(r'lda_output_head_cargill.xlsx')

final_lda_output = pd.merge(body_file, title_file, how='inner', on='Id')
final_lda_output = final_lda_output.drop(['Date_y', 'Url_y'], axis=1)
final_lda_output = final_lda_output.rename(columns={'Date_x':'Date', 'Url_x':'Url'})
final_lda_output = final_lda_output.drop(columns = ['Topic'])

for i in range(len(final_lda_output)):
    inputStr = str(final_lda_output.iloc[i,1]).strip("\n")
    no_of_lines = inputStr.count('\n')
    if no_of_lines>0:
        inputStr = inputStr.split("\n")[no_of_lines]
    print(inputStr)
    print("---------------End-----------------")
    final_lda_output.iloc[i, 1] = inputStr



#final_lda_output.to_csv(r"lda_output_cargill_final.csv",index=None, header=True)
final_lda_output.to_excel(r"lda_output_cargill_final.xlsx",index=None, header=True)