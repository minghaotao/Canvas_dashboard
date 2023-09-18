import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.style.use('fivethirtyeight')

if "shared" not in st.session_state:
    st.session_state["shared"] = True

st.write(""" Assessment Usage Report """)

upload_file = st.file_uploader("Choose a CSV file")

if upload_file is not None:
    data = pd.read_csv(upload_file)

    # data = data.replace(to_replace='None',value=np.NaN).dropna()

    # Convert Assignment_due column to datetime format
    data['Assignment_due'] = pd.to_datetime(data['Assignment_due'])
    # Extract weekday names and assign to a new column
    data['Weekday'] = data['Assignment_due'].dt.strftime('%A')
    # Drop the original Assignment_due column
    data.drop('Assignment_due', axis=1, inplace=True)

    # Replace 'None' with NaN and drop NaN values
    data = data.replace(to_replace='None', value=np.NaN).dropna()


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


    def scatter_():

        pass


    def assignment_due():
        st.write(""" Assessment Due Date """)

        # Add dynamic columns
        columns = st.sidebar.multiselect("Select columns", data['Course_code'].unique().tolist())
        if columns:
            # report = data[columns]
            # selected_course_codes = st.multiselect("Select Course Code(s)", list(course_codes))
            filtered_data = data[data["Course_code"].isin(columns)]
        else:
            #
            #     selected_course_codes = st.multiselect("Select Course Code(s)", list(course_codes))
            #
            #     # Filter the data based on the selected course codes
            filtered_data = data

        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

        filtered_data['Assignment_due'] = pd.to_datetime(data['Assignment_due'], format='%Y/%m/%d')
        filtered_data.set_index('Assignment_due', inplace=True)
        report = filtered_data['Submission_type'].resample('D').agg({'value_counts'})[
            'value_counts'].unstack().fillna(0)

        # Add dynamic filters
        filters = st.sidebar.multiselect("Select assessment types", data['Submission_type'].unique().tolist())
        if filters:
            report = report[filters]

        # Create the chart
        fig, ax = plt.subplots()
        report.plot.area(fontsize=9, figsize=(9, 7), rot=0, stacked=False, ax=ax)

        # fig = report.plot.area(fontsize=9, figsize=(9, 7), rot=0, stacked=False)

        tab1.subheader("Filter by Course")
        tab1.pyplot(fig.figure)

        tab2.subheader("Assignment Due Dates")
        tab2.write(report)

        tab3, tab4 = st.tabs(["📈 Chart", "🗃 Data"])

        bar_chart = filtered_data['Submission_type'].value_counts()

        tab3.subheader("Filter by Course")
        tab3.bar_chart(bar_chart)

        tab4.subheader("Number of Submission Types")
        tab4.write(bar_chart)

        return tab1, tab2, tab3, tab4


    # st.area_chart(report)

    submission_due()
    # st.pyplot(assignment_due())
    assignment_due()
