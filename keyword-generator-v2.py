import pandas as pd
import streamlit as st

st.markdown('# Keyword Generator')
st.markdown("""
    This application aids with the creation of large sets of keyword lists based on a set of Keyword _Seeds_ and Keyword _Phrases_.
""")

st.markdown('### Upload Keyword List File (CSV)')
seed_words = st.file_uploader('Upload Keyword List')

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

if seed_words is not None:
    seed_df = pd.read_csv(seed_words, header=None)

    st.markdown('### Upload Phrase List File (CSV)')
    phrase_words = st.file_uploader('Upload Phrase List')
    
    if phrase_words is not None:
        phrase_df = pd.read_csv(phrase_words, header=None)

        if phrase_df is not None:
            with st.spinner('Computing...'):
                merged = seed_df.merge(phrase_df, how='cross')

                if len(seed_df.columns) == 1:
                    merged['keyword'] = [phrase.replace('{0}', str(keyword1)) for keyword1, phrase in merged.iloc[:, 0:2].to_numpy()]
                    merged.columns=['seed1','phrase','keyword']
                elif len(seed_df.columns) == 2:
                    merged['keyword'] = [phrase.replace('{0}', str(keyword1)).replace('{1}', str(keyword2)) for keyword1, keyword2, phrase in merged.iloc[:, 0:3].to_numpy()]
                    merged.columns=['seed1','seed2','phrase','keyword']
                elif len(seed_df.columns) == 3:
                    merged['keyword'] = [phrase.replace('{0}', str(keyword1)).replace('{1}', str(keyword2)).replace('{2}', str(keyword3)) for keyword1, keyword2, keyword3, phrase in merged.iloc[:, 0:4].to_numpy()]
                    merged.columns=['seed1','seed2','seed3','phrase','keyword']
                elif len(seed_df.columns) == 4:
                    merged['keyword'] = [phrase.replace('{0}', str(keyword1)).replace('{1}', str(keyword2)).replace('{2}', str(keyword3)).replace('{3}', str(keyword4)) for keyword1, keyword2, keyword3, keyword4, phrase in merged.iloc[:, 0:5].to_numpy()]
                    merged.columns=['seed1','seed2','seed3','seed4','phrase','keyword']
                
                st.markdown('### Keywords Generated')
                st.markdown('Showing the top 5 rows generated (column headers will be removed in exported csv file)')

                st.write(merged.head(5))
            
                csv = convert_df(merged)

                st.download_button(label="Download data as CSV", data=csv, file_name='output.csv', mime='text/csv')