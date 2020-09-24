import pandas as pd

title_file = pd.read_csv("lda_output_head_agri.csv")
body_file = pd.read_csv("lda_output_agri.csv")

final_lda_output = pd.merge(body_file, title_file, how='inner', on='Id')
final_lda_output = final_lda_output.drop(['Date_y', 'Url_y'], axis=1)
final_lda_output = final_lda_output.rename(columns={'Date_x':'Date', 'Url_x':'Url'})

final_lda_output.to_csv(r"lda_output_agri_final.csv",index=None, header=True)