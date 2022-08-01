from msilib.schema import CheckBox
from platform import release
from importlib_metadata import version
import pandas as pd
import openpyxl
import numpy as np
from soupsieve import select
import streamlit as st
import streamlit.components.v1 as components
from cmath import inf, nan
import re 
import string
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title='SOUCS QMA CLIENT DASHBOARD', page_icon='bar_chart', layout='wide')
st.title('SOUCS CLIENT DASHBOARD')
col1,col2 = st.columns(2)

class Release:
    def __init__(self,data):
        self.data=data
        self.data=data.fillna(0)
        

    def release_version(self):
        version = self.data['Fix versions']
        new = []
        for i in version:
            if str(i)!= nan:
                new.append(i)
        release_id = list(set(new))
        return release_id
            

class effort:
    def __init__(self,data):
        self.data=data
        self.data=data.fillna(0)
    
    def rework(self):
        Status=self.data['Status']
        data_filter=self.data[(Status!='To Do') & (Status!='Invalid') & (Status!='On Hold') & (Status!='Duplicate')]
        Issue_type=data_filter['Issue Type']
        try:
            data_Issue_filtered=data_filter[(Issue_type=='Bug') | (Issue_type=='Bug SubTask')]
            rework_effort=data_Issue_filtered['Time Spent'].sum()
        except:
            rework_effort=0.0    

        return rework_effort 

    def development_timespent(self):
        Status=self.data['Status']
        data_filter=self.data[(Status!='To Do') & (Status!='Invalid') & (Status!='On Hold') & (Status!='Duplicate')]
        Issue_type=data_filter['Issue Type']
        data_bug_filter=data_filter[(Issue_type!='Bug') & (Issue_type!='Bug SubTask')]
        dev_effort=data_bug_filter['Time Spent'].sum()
        return round(dev_effort,2)

    def development_estimated(self):
        Status=self.data['Status']
        data_filter=self.data[(Status!='To Do') & (Status!='Invalid') & (Status!='On Hold') & (Status!='Duplicate')]
        Issue_type=data_filter['Issue Type']
        data_bug_filter=data_filter[(Issue_type!='Bug') & (Issue_type!='Bug SubTask')]
        dev_effort=data_bug_filter['Original Estimate'].sum()
        return round(dev_effort,2)

project = st.selectbox('PROJECT NAME', ('Select', 'SOUCS'))
activities = st.selectbox('METRIC NAME', ('Select', 'NEW DEFECT', 'REOPEN RATE'))

if activities=='NEW DEFECT':  
    st.write('**The volatility report of project:** '+project)
    try:
        uploaded=st.file_uploader("Please upload file of type .xlsx", type=['xlsx'],key="filuploader")
        if uploaded is not None:
            st.success('File successfully upload')
            data=pd.read_excel(uploaded)
            data['Story_points']=data['Custom field (Story point estimate)']
            data['affect Version']=data['Custom field (Affect Version)']
            FIELDS = ['Issue key','Issue Type','Status',"Created","Updated","Fix versions",'Story_points','affect Version']
            data = data[FIELDS]
            rel = Release(data)
            id = []
            for i in rel.release_version():
                id.append(i)
            values = st.selectbox('release version',id)
            st.write(values)
            if len(values)>= 0:
                try:

                    total_issue_delivered = data.loc[data['Fix versions'] == values].count()
                    issue_delivered = total_issue_delivered['Issue key']
                    bug_reported = data.loc[data['affect Version'] == values].count()
                    bu_reported = bug_reported['Issue key']
                    new_defect = bu_reported/issue_delivered*100
                    if new_defect == inf:
                        print('NA')
                    nnn = {'Release ID' : [values],
                    'Total Number of Jira Issues Delivered':[issue_delivered],
                    'Total Number of Bugs Reported':[bu_reported],
                    'New Defect %':[new_defect]}
                    cod = pd.DataFrame.from_dict(nnn)
                    st.table(cod)


                except:
                    st.error('Please check the code')

        
 

            # if st.checkbox('Display data'):
            #     st.write(rel.release_version())

    except:
        st.error('The file uploaded is not in correct format .. Deepali pleasse refresh page')     
