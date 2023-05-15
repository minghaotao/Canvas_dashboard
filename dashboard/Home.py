import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib

matplotlib.style.use('fivethirtyeight')

if "shared" not in st.session_state:
    st.session_state["shared"] = True

st.write(""" Tool Usage Report """)

upload_file = st.file_uploader("Choose a CSV file")

if upload_file is not None:

    df = pd.read_csv(upload_file)
    df = df.fillna(0).set_index('Course Name')


    def get_value(column):
        return df[column].value_counts().drop(0)


    def tool_usage():

        df1 = pd.Series([], dtype='int64')
        for column in df.columns:
            column = get_value(column)

            df1 = pd.concat([df1, column])
        df1 = df1.to_frame().reset_index()
        df1 = df1.rename(columns={0: 'Usage', 'index': 'Tool Name'})
        ax = df1.sort_values('Usage').plot.barh(x='Tool Name', y='Usage', fontsize=9, figsize=(10, 4), rot=0)

        for patch in ax.patches:
            ax.text(
                patch.get_width(),
                patch.get_y(),
                " {:,}".format(patch.get_width()),
                fontsize=10,
                color='dimgrey'
            )
        plt.tight_layout()

        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
        tab1.subheader("Tool Usage")
        tab1.pyplot(ax.figure)

        tab2.subheader("Raw Data")
        tab2.write(df1)

        return tab1, tab2


    tool_usage()

    # df = df.sort_values(by='number', ascending=False)

    # fig = px.funnel(df, x='number', y='Tool_Name')

# st.plotly_chart(fig, theme=None, use_container_width=True)
