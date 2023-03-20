import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('fivethirtyeight')

if "shared" not in st.session_state:
   st.session_state["shared"] = True




st.write(""" Assessment Usage Report """)

upload_file = st.file_uploader("Choose a CSV file")

if upload_file is not None:

    try:
        df = pd.read_csv(upload_file)

        df = df.groupby(['Submission_type']).agg({'Weekday': 'value_counts'})['Weekday'].unstack().fillna(0)


        fig = px.imshow(df,labels=dict(x="Assessment Type", y="Due Date", color="Numbers"),
                        x = df.index, y = df.columns
                        )

        fig.update_xaxes(side="top")
        # fig.show()

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    except:
        pass




