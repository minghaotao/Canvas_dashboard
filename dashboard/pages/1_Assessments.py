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
    data = pd.read_csv(upload_file)


    def submission_due():
        df1 = data.copy()

        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

        df = df1.groupby(['Submission_type']).agg({'Weekday': 'value_counts'})['Weekday'].unstack().fillna(0)

        fig = px.imshow(df, labels=dict(x="Assessment Type", y="Due Date", color="Numbers"),
                        x=df.index, y=df.columns
                        )

        fig.update_xaxes(side="top")

        tab1.subheader("A tab with a chart")
        tab1.plotly_chart(fig, theme="streamlit", use_container_width=True)

        tab2.subheader("A tab with the data")
        tab2.write(df)

        return tab1, tab2

        # return st.plotly_chart(fig, theme="streamlit", use_container_width=True)


    def assignment_due():
        st.write(""" Assessment Due Date """)

        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

        call_days = data['Assignment_due']
        call_days = pd.DatetimeIndex(call_days.values).strftime('%D').value_counts().sort_index()

        data['Assignment_due'] = pd.to_datetime(data['Assignment_due'], format='%Y/%m/%d')

        data.set_index('Assignment_due', inplace=True)

        report = data['Submission_type'].resample('D').agg({'value_counts'})[
            'value_counts'].unstack().fillna(0)
        # fig, ax = plt.subplots()
        #
        fig = report.plot.area(fontsize=9, figsize=(9, 7), rot=0, stacked=False)

        # return fig.figure

        tab1.subheader("A tab with a chart")
        tab1.pyplot(fig.figure)

        tab2.subheader("A tab with the data")
        tab2.write(report)

        return tab1, tab2


    # st.area_chart(report)

    submission_due()
    # st.pyplot(assignment_due())
    assignment_due()
