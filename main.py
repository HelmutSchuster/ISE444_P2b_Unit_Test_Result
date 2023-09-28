import streamlit as st
import pandas as pd

CORRECT_FILE_NAME = 'unit_test_result.csv'

st.set_page_config(layout="wide", page_title="Verify Unit Test")

st.write("## Verification of the format of the unit test file (P2B ISE444)")

# ----------------------------------------------------------------------
def verify_unit_test_file(csv_file):
    if csv_file.name != CORRECT_FILE_NAME:
        st.warning(f'File name is wrong.  Should be {CORRECT_FILE_NAME} .')
        return False
    
    df = pd.read_csv(csv_file)
    rowCount, colCount = df.shape
    if (colCount != 11) or (rowCount != 261):
        st.warning('File should have 10 columns and 261 rows.')
        return False
    
    firstDT = df.iloc[0, 0]
    # st.write(firstDT)
    if firstDT != '2023-09-01 07:40:00':
        st.warning('The sensor_time value in row zero should be 1 Sep 2023 @ 7:40 in  YYYY-MM-DD HH:mm:ss format.')
        return False
    
    valid_set = {0, 1}
    error_msg = ''
    if set(df['hvac_is_active'].unique()) != valid_set:
        error_msg += 'Field hvac_is_active must consist of 0 and 1. '
    if set(df['room_is_occupied'].unique()) != valid_set:
        error_msg += 'Field room_is_occupied must consist of 0 and 1. '
    if set(df['temperature_warning'].unique()) != valid_set:
        error_msg += 'Field temperature_warning must consist of 0 and 1. '
    if error_msg != '':
        st.warning(error_msg)
        return False
    
    col_names = ','.join(df.columns)
    if col_names != 'sensor_time,u_t,ui_t,e,T1,T2,T_feedback,T_Setpoint,hvac_is_active,room_is_occupied,temperature_warning':
       st.warning('Check your column names and sequence of fields.') 
       return False
    
    st.success('Format of CSV file looks fine.')


uploaded_file = st.file_uploader('Upload your unit test file [csv]')
if uploaded_file is not None:
    try:
        verify_unit_test_file(uploaded_file)
    except Exception as e:
        st.error(e.args)        
else:
    st.warning('you need to upload a csv file.')
