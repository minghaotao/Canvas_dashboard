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


def plotting(df, type):
    if type == 'bar':
        course_tools = ['Item banks', 'Brainfuse Tutoring', 'New Quizzes']
        fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True)

        course_tool = df[df['Tool Name'].isin(course_tools)]

        course_tool.sort_values('Usage').plot.bar(x='Tool Name', y='Usage', fontsize=9, figsize=(10, 4), rot=0,
                                                  ax=axes[0])

        axes[0].legend(['Canvas Tools'])
        axes[0].set(xlabel=None)
        axes[0].get_legend().set_bbox_to_anchor((1.2, 1.2))

        for patch in axes[0].patches:
            axes[0].text(
                patch.get_x(),
                patch.get_height() + 0.1,
                " {:,}".format(int(patch.get_height())),
                fontsize=10,
                color='dimgrey',

            )

        external_tool = df[~df['Tool Name'].isin(course_tools)]
        external_tool.sort_values('Usage').plot.bar(x='Tool Name', y='Usage', fontsize=9, figsize=(10, 4), rot=0,
                                                    ax=axes[1])
        axes[1].set(xlabel=None)
        axes[1].legend(['External Tools'])
        axes[1].get_legend().set_bbox_to_anchor((1.2, 1.2))

        for patch in axes[1].patches:
            axes[1].text(
                patch.get_x(),
                patch.get_height() + 0.1,
                " {:,}".format(int(patch.get_height())),
                fontsize=10,
                color='dimgrey',

            )

        plt.tight_layout()

        return fig

        # ax = df.sort_values('Usage').plot.bar(x='Tool Name', y='Usage', fontsize=9, figsize=(10, 4), rot=0)
        # for patch in ax.patches:
        #     ax.annotate("{:,}".format(patch.get_height()),
        #                 (patch.get_x() + patch.get_width() / 2, patch.get_height()),
        #                 ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=10,
        #                 color='dimgrey')
    if type == 'barh':
        ax = df.sort_values('Usage').plot.barh(x='Tool Name', y='Usage', fontsize=9, figsize=(10, 4), rot=0)
        for patch in ax.patches:
            ax.text(
                patch.get_width(),
                patch.get_y(),
                " {:,}".format(patch.get_width()),
                fontsize=10,
                color='dimgrey'
            )

        plt.tight_layout()

        return ax


if upload_file is not None:

    data = pd.read_csv(upload_file).fillna(0)


    # df = df.fillna(0).set_index('Course Name')

    def tool_usage():
        df1 = data.copy()

        df = df1.fillna(0).set_index('Course Name')

        def get_value(column):
            return df[column].value_counts().drop(0)

        df1 = pd.Series([], dtype='int64')
        for column in df.columns:
            column = get_value(column)

            # column = filtered_data[column].value_counts().drop(0)

            df1 = pd.concat([df1, column])

        df1 = df1.to_frame().reset_index()
        df1 = df1.rename(columns={0: 'Usage', 'index': 'Tool Name'})

        ax = plotting(df1, 'barh')

        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
        tab1.subheader("Tool Usage")
        tab1.pyplot(ax.figure)

        tab2.subheader("Raw Data")
        tab2.write(df1)

        return tab1, tab2


    def course_filter():

        columns = st.sidebar.multiselect("Select course", data['Course Name'].unique().tolist())

        if columns:

            filtered_data = data[data['Course Name'].isin(columns)]

            df = filtered_data.fillna(0).set_index('Course Name')

            def get_value(column):
                return df[column].value_counts()

            df1 = pd.Series([], dtype='int64')
            for column in df.columns:
                column = get_value(column)
                df1 = pd.concat([df1, column])

            df1 = df1.to_frame().reset_index()
            df1 = df1.rename(columns={0: 'Usage', 'index': 'Tool Name'})
            df1 = df1.drop(df1[df1['Tool Name'] == 0].index)

            ax = plotting(df1, 'bar')

            tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
            tab1.subheader("Filtered Tool Usage")
            # tab1.pyplot(ax.figure)
            tab1.pyplot(ax)

            tab2.subheader("Filtered Raw Data")
            tab2.write(df1)

            return tab1, tab2


    def tool_filter():

        # df2 = data.copy()

        filters = st.sidebar.multiselect("Select tool types", data.columns.unique().tolist())
        if filters:
            def filter_columns(course):
                filtered_data = data.loc[data[f'{course}'] != 0, ['Course Name', f'{course}']]

                filtered_data = filtered_data.rename(columns={f'{course}': 'Tool Name'})

                return filtered_data

            report = pd.DataFrame(columns=['Course Name', 'Tool Name'])
            for filter in filters:
                report = pd.concat([report, filter_columns(filter)], ignore_index=True)

            fig, ax = plt.subplots()
            ax = report.value_counts('Tool Name').plot.bar(x='Tool Name', y='Course Name', fontsize=9, figsize=(10, 4),
                                                           rot=0)
            for patch in ax.patches:
                ax.annotate("{:,}".format(patch.get_height()),
                            (patch.get_x() + patch.get_width() / 2, patch.get_height()),
                            ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=10,
                            color='dimgrey')

            tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
            plt.tight_layout()
            tab1.subheader(""" Filtered by Tool Type """)
            tab1.pyplot(fig.figure)
            tab2.write(report)


    tool_usage()
    course_filter()
    tool_filter()

    # df = df.sort_values(by='number', ascending=False)

    # fig = px.funnel(df, x='number', y='Tool_Name')

# st.plotly_chart(fig, theme=None, use_container_width=True)
