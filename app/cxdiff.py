import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import io



def is_different(row):
        return row[0] if row[0] == row[1] or row[0] is None or row[0] is None  else f'"{row[0]}"  |  "{row[1]}"'

def common_field(df1: pd.DataFrame, df2: pd.DataFrame) -> list:
    return df2.columns.intersection(df1.columns).to_list()

def compare_sheets(sheet1: tuple, sheet2: tuple, unique_identifier: list) -> any:
    # Merge the two DataFrames on the 'Name' column
    df1 = pd.read_excel(sheet1[0], sheet_name=sheet1[1])
    df2 = pd.read_excel(sheet2[0], sheet_name=sheet2[1])
    suffixes=('_df1', '_df2')
    merged_df = df1.merge(df2, on=unique_identifier, how='outer', suffixes=suffixes)
    # Function to check if values are different
    # unique_identifier_suffixes = [f'{iden}{suf}' for iden, suf in zip(unique_identifier, list(suffixes))]
    # Apply the function across the rows for selected columns
    merged_df = merged_df.replace({np.nan: None})
    for col in set(common_field(df1, df2)).difference(set(unique_identifier)):
        merged_df[col] = merged_df[[f'{col}_df1', f'{col}_df2']].apply(is_different, axis=1)
        merged_df.drop([f'{col}_df1', f'{col}_df2'], axis=1, inplace=True)

    # Define a styling function to highlight differences
    def highlight_diffs(val):
        if ' | ' in str(val):
            return f'color: red;'
            
        else:
            return f'background-color: #f5f5f5;' 

    # Apply the styling
    styles = merged_df.style.map(highlight_diffs).highlight_null(props="color: transparent;")
    return styles


def compare_dfs(df1: pd.DataFrame, df2: pd.DataFrame, unique_identifier: list) -> any:
    # Merge the two DataFrames on the 'Name' column
    suffixes=('_df1', '_df2')
    merged_df = df1.merge(df2, on=unique_identifier, how='outer', suffixes=suffixes)
    # Function to check if values are different
    # unique_identifier_suffixes = [f'{iden}{suf}' for iden, suf in zip(unique_identifier, list(suffixes))]
    # Apply the function across the rows for selected columns
    try:
        merged_df = merged_df.replace({np.nan: None})
        print()
        for col in set(common_field(df1, df2)).difference(set(unique_identifier)):
            merged_df[col] = merged_df[[f'{col}_df1', f'{col}_df2']].apply(is_different, axis=1)
            merged_df.drop([f'{col}_df1', f'{col}_df2'], axis=1, inplace=True)
    except Exception as e:
        raise  e

    # Define a styling function to highlight differences
    def highlight_diffs(val):
        if '|' in str(val):
            return f'color: red;'
            
        else:
            return f'background-color: #f5f5f5;' 

    # Apply the styling
    styles = merged_df.style.map(highlight_diffs).highlight_null(props="color: transparent;")
    return styles

# Other parts of your Streamlit app should work as before ...

# Set up the Streamlit app layout
st.title('Document Comparison App (Excel, CSV)')
file_type = st.selectbox('Select :', ['CSV', 'Excel'], key='file_type')

st.write("You selected:", file_type)
    # File upload section for the two Excel files
sheet_name_1 = None
if file_type is not None:
    if file_type == 'Excel':
        uploaded_file_1 = st.file_uploader("Choose first Excel file", type=['xlsx'], key='file_1')
        if uploaded_file_1 is not None:
            sheet_names_1 = pd.ExcelFile(uploaded_file_1).sheet_names
            sheet_name_1 = st.selectbox('Select a sheet:', sheet_names_1, key='file_1_select_sheet')
            unique_identifiers = list(pd.read_excel(uploaded_file_1, sheet_name_1).columns)
            df1 = pd.read_excel(uploaded_file_1, sheet_name=sheet_name_1)
            if sheet_name_1 is not None:
                try:
                    selected_join = st.multiselect('Select unique common column(s) for join field:', unique_identifiers, key='file_1_unique_identifiers')
                except Exception as e:
                    st.error(f'Please select common column(s) in the files')
        try:
            uploaded_file_2 = st.file_uploader("Choose second Excel file", type=['xlsx'], key='file_2')
            if uploaded_file_2 is not None:
                sheet_names_2 = pd.ExcelFile(uploaded_file_2).sheet_names
                sheet_name_2 = st.selectbox('Select a sheet:', sheet_names_2, key='file_2_select_sheet')
                df2 = pd.read_excel(uploaded_file_2, sheet_name=sheet_name_2)
        except Exception as e:
            st.error(f'Please upload another file')

    elif file_type == 'CSV':
        uploaded_file_1 = st.file_uploader("Choose first CSV file", type=['csv'])
        if uploaded_file_1 is not None:
            try:
                df1 = pd.read_csv(uploaded_file_1, header=0)
                unique_identifiers = list(df1.columns)
                selected_join = st.multiselect('Select unique common column(s) for join field:', unique_identifiers, key='file_1')
            except Exception as e:
                st.error(f'Please select common column(s) in the files')
            try:
                uploaded_file_2 = st.file_uploader("Choose second CSV file", type=['csv'])
                if uploaded_file_2 is not None:
                    df2 = pd.read_csv(uploaded_file_2, header=0)
            except Exception as e:
                st.error(f'Please upload another file')

# Button to trigger the comparison
if st.button('Compare Documents'):
    # Check if the files were uploaded and sheet names were provided
    # and sheet_name_1 and sheet_name_2
    if uploaded_file_1 is not None and uploaded_file_2 is not None:
        try:
            # Perform the comparison
            result = compare_dfs(df1, df2, selected_join)
            styled_html = result.to_html()
            # Display the differences
            st.write('Differences (Light Red: Content differs seperated by (|), light Green: content match:')
            # components.html(styled_html, width=1000, height=600, scrolling=True)
            st.dataframe(result)
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine="openpyxl")
            result.to_excel(writer, index=False, sheet_name="sheet1")
            writer.close()
            data_bytes = output.getvalue()
            st.download_button(label='Download Comparison Excel', data=data_bytes, file_name='comparison_result.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        except Exception as e:
            st.error(f'An error occurred: {e}')
    else:
        st.error('Please upload both Excel files and provide corresponding sheet names.')