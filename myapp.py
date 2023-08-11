import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')
len(gss_clean)

mystring = "While women, in general, earn approximately 82 cents to every dollar that men earn  <a href=\"https://www.pewresearch.org/short-reads/2023/03/01/gender-pay-gap-facts\">Pew Research</a>, the specific disparities in women's pay depends on occupation, age, race, education, among other variables. According to <a href=\"https://www.pewresearch.org/short-reads/2023/03/01/gender-pay-gap-facts\">Pew Research</a>, women ages 25 to 34 earn 92 cents to every dollar that mean earn, while the women of all other ages groups earn 82 cents to every dollar. <a href=\"https://www.gao.gov/products/gao-23-106041\">The Government Accountability Office</a> found further differences. Hispanic women earn 58 cents for every dollar that white men earn and black women earn 63 cents for every dollar that white men earn. The pay gap is greatest for those with only a high school education and smallest for those with a bachelors. Finally, the pay gap also depends on occupation with women in private industry earning 78 cents for every dollar that men earn and women in management earning 77 cents for every dollar that men earn. \n To assess the pay gap, we will be using the <a href=\"https://gss.norc.org/About-The-GSS\">General Social Survey</a> data, a nationally representative survery of American adults collected since 1972. The survery aims to collect contemporary opinions, attitudes, and behaviors via demographic, behavioral, and attitudinal questions. The clean data presented here represent 2348 individuals in 2019."


gss_table = gss_clean.groupby("sex")[["income", "job_prestige", "socioeconomic_index", "education"]].mean()
gss_bar = gss_clean.groupby("sex")[["income", "job_prestige", "socioeconomic_index", "education"]].mean()
gss_bar['Income'] = round(gss_bar['income'],2)
gss_bar['Job Prestige'] = round(gss_bar['job_prestige'],2)
gss_bar['SES'] = round(gss_bar['socioeconomic_index'],2)
gss_bar['Years of Education'] = round(gss_bar['education'],2)
gss_bar = gss_bar.reset_index()
gss_bar


variables=['Income']

fig1 = go.Figure(data=[
    go.Bar(name='female', x=variables, y=gss_bar.loc[0,variables]),
    go.Bar(name='male', x=variables, y=gss_bar.loc[1,variables])])
# Change the bar mode
fig1.update_layout(barmode='group')
fig1.show()

variables=['Job Prestige', 'SES', 'Years of Education']

fig2 = go.Figure(data=[
    go.Bar(name='female', x=variables, y=gss_bar.loc[0,variables]),
    go.Bar(name='male', x=variables, y=gss_bar.loc[1,variables])])
# Change the bar mode
fig2.update_layout(barmode='group')
fig2.show()

gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].astype('category')
gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].cat.reorder_categories(['strongly disagree', 'disagree', 'agree', 'strongly agree'])


gss_bar = gss_clean.groupby('sex', sort=False).agg({'male_breadwinner':'value_counts'})
gss_bar = gss_bar.rename({'male_breadwinner':'Patriarchy'}, axis=1) #needed to avoid the same name as the index
gss_bar['Sex'] =  gss_bar.index.get_level_values('sex')
gss_bar['Male Breadwinner'] =  gss_bar.index.get_level_values('male_breadwinner')


fig3 = px.bar(gss_bar, x= 'Male Breadwinner', y = 'Patriarchy', color = 'Sex', 
            labels={'Male Breadwinner':'Endorse Patriarchy', 'Patriarchy': 'Count'},
            hover_data = ['Patriarchy', 'Sex'],
            barmode = 'group')
fig3.update_layout(showlegend=True)
fig3.update(layout=dict(title=dict(x=0.5)))
fig3.show()

gss_scatter = gss_clean[~gss_clean.isnull()]
fig4 = px.scatter(gss_scatter.head(200), x='job_prestige', y='income', 
                 trendline='ols',
                 color = 'sex', 
                 height=600, width=600,
                 labels={'job_prestige':'Occupational Prestige', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'])
fig4.update(layout=dict(title=dict(x=0.5)))
fig4.show()

fig5 = px.box(gss_clean, x='income', y = 'sex', color = 'sex',
                   labels={'income':'Income', 'sex':''})
fig5.update_layout(showlegend=False)
fig5.update(layout=dict(title=dict(x=0.5)))
fig5.show()

fig6 = px.box(gss_clean, x='job_prestige', y = 'sex', color = 'sex',
                   labels={'job_prestige':'Occupational Prestige', 'sex':''})
fig6.update_layout(showlegend=False)
fig6.update(layout=dict(title=dict(x=0.5)))
fig6.show()

cols = ['income', 'sex', 'job_prestige']
gss_sub = gss_clean[cols].dropna()
gss_sub['job_cat'] = pd.cut(gss_sub['job_prestige'],
                            bins=[16, 27, 38, 49, 60, 71, float('Inf')],
                            labels=['lowest', 'low', 'mid-low', 'mid-high', 'high', 'highest'])

fig7 = px.box(gss_sub, x='sex', y = 'income', color = 'sex', facet_col='job_cat',
              facet_col_wrap=2,
              hover_data=['income', 'sex', 'job_cat'], 
              labels={'income':'Income', 'sex':''},
              width=1000, height=800)
fig7.update(layout=dict(title=dict(x=0.5)))
fig7.update_layout(showlegend=False)
fig7.for_each_annotation(lambda a: a.update(text=a.text.replace("job_cat=", "")))
fig7.show()

table = ff.create_table(gss_table)
table.show()