from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from joblib import load
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plotly.tools import mpl_to_plotly
import seaborn as sns
import xlrd

from app import app

pipeline = load('model/pipeline.joblib')
history = pd.read_csv('model/n_alltime.csv')




# Assign to X, y to avoid data leakage
features = ['CaseMembers',
       '3.2_Social_Security_Quality', '3.3_Birthdate_Quality',
       'Age_at_Enrollment', '3.4_Race', '3.5_Ethnicity', '3.6_Gender',
       '3.7_Veteran_Status', '3.8_Disabling_Condition_at_Entry',
       '3.917_Living_Situation', 'length_homeless',
       '3.917_Times_Homeless_Last_3_Years', '3.917_Total_Months_Homeless_Last_3_Years', 
       'V5_Last_Permanent_Address', 'V5_State', 'V5_Zip', 'Municipality_(City_or_County)',
       '4.1_Housing_Status', '4.4_Covered_by_Health_Insurance', '4.11_Domestic_Violence',
       '4.11_Domestic_Violence_-_Currently_Fleeing_DV?', 'Household_Type', 
       'R4_Last_Grade_Completed', 'R5_School_Status',
       'R6_Employed_Status', 'R6_Why_Not_Employed', 'R6_Type_of_Employment',
       'R6_Looking_for_Work', 'entry_income',
       '4.3_Non-Cash_Benefit_Count', 'Barrier_Count_at_Entry',
       'Chronic_Homeless_Status', 'Under_25_Years_Old',
       '4.10_Alcohol_Abuse_(Substance_Abuse)', '4.07_Chronic_Health_Condition',
       '4.06_Developmental_Disability', '4.10_Drug_Abuse_(Substance_Abuse)',
       '4.08_HIV/AIDS', '4.09_Mental_Health_Problem',
       '4.05_Physical_Disability', 'perm_leaver'
          ]


X = history[features]
X = X.drop(columns='perm_leaver')



y_pred = pipeline.predict(X)


fig, ax = plt.subplots()
sns.distplot(history['perm_leaver'], hist=False, kde=True, ax=ax, label='Actual')
sns.distplot(y_pred, hist=False, kde=True, ax=ax, label='Predicted')
ax.set_title('Distribution of Actual Exit compared to prediction')
ax.legend().set_visible(False)
plotly_fig = mpl_to_plotly(fig)
plotly_fig['layout']['showlegend'] = True


layout = [dcc.Markdown("""
### Evaluate

This graph displays the actual outcomes of previous guests and the predicted outcomes of those same guests.  
The model proved to be more accurate in predicting non-permanent exits versus predicting permanent exits, which is tailored
pretty well to the purpose of this webapp: predicting households not likely to exit to permanent housing to provide more 
case management to them in an effort to ensure they do end up leaving for permanent housing.  

"""), 

dcc.Graph(id='evaluate-graph', figure=plotly_fig)
]
