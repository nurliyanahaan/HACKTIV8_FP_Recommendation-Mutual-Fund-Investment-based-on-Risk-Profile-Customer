import streamlit as st
from annotated_text import annotated_text
from PIL import Image
import pandas as pd
import numpy as np
import pickle
import time
from plotly import graph_objs as go
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_option_menu import option_menu

# ---- Config & setting page icon and title ----
app_icon = Image.open("app_icon.png")
st.set_page_config(page_title="Anminvesting", page_icon=app_icon, layout="centered")

# ---- Hiding the menu and streamlit footer note ----
hide_menu = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_menu, unsafe_allow_html=True)

# ---- Loading the Model ----
pipeline = pickle.load(open('full_model.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

page_nav = option_menu(
    menu_title="Navigation Bar",
    options=["Find your Risk Profile", "What is Mutual Funds?"],
    icons = ["house","book"],
    orientation="horizontal",
    menu_icon="arrow-down-circle-fill"
    # style = 
)

# ---- Setting the header and tagline -----
if page_nav == "Find your Risk Profile":
    st.title("Anminve$ting")
    title_alignment= """
    <style>
    #Amninve$ting {
    text-align: center
    }
    </style>
    """
    st.markdown(title_alignment, unsafe_allow_html=True)
    st.write('''
            ## How are you investing today?
            ''')
    logo = Image.open('Logo.png')
            
    # test_logo = """
    #     <h1>test</h1>
    #     <img src="Logo.png" alt="Logo" style="width:500px;height:600px;">
    #     """
    st.image(logo)
    # st.image(logo)

# ---- Setting up the questionnaire Form ----
    with st.form(key='form1'):

        st.write('''
            ### Please choose the following questions so we could recommend the best Mutual Fund investations for you.
            ''')

        name = st.text_input(label = "What is your name?")

        st.markdown('''
            #### QUESTION 1
            ''')
        st.write("How old are you?\n 1. Over 55 years\n", "2. 45-55 years\n","3. 35-44 years\n","4. Under 35 years\n")
        age = st.radio(label = "Choose your answer", options = [1,2,3,4], key="age")
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        st.markdown('''
            #### QUESTION 2
            ''')
        salary = st.number_input(label = "What is your salary in one month?")

        st.markdown('''
            #### QUESTION 3
            ''')
        st.write("What are your financial burdens and fixed expenses? (i.e. mortgage payment, personal expensed for individual investor; business operating costs for juristic person investor)\n","1. Over 75% of total income\n","2. Between 50– 75% of total income\n","3. Between 25– 50% of total income\n","4. Less than 25% of total income\n")
        expenses = st.radio(label = "Choose your answer", options = [1,2,3,4], key="expenses")
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        st.markdown('''
        #### QUESTION 4
        ''')
        st.write("What is your current financial status?\n","1. Less assets than debts\n","2. Assets equal to debts\n","3. More assets than debts\n","4. I will have adequate savings/investments throughout my retirement\n")
        financial_status = st.radio(key="financial_status", label = "Choose your answer", options = [1,2,3,4])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        st.markdown('''
            #### QUESTION 5
            ''')
        st.write("Which of the following assets do you have investment experience with or knowledge about? (You can choose more than one answer.)\n","1. Bank Deposit\n","2. Government Bond or Government Bond Fund\n","3. Debentures or Fixed Income Fund\n","4. Equity Equity or Equity Fund or other High-Risk Assets\n")
        st.write("Choose your answer")

        checkbox_labels = ["Option 1", "Option 2", "Option 3", "Option 4"]
        checkbox_values = [1, 2, 3, 4]
        total_value = 0

        for label, value in zip(checkbox_labels, checkbox_values):
            if st.checkbox(label, value=value):
                total_value += value
        
        st.markdown('''
            #### QUESTION 6
            ''')
        st.write("The estimated period that you will not need to use your invested funds\n","1. Less than 1 year\n","2. 1 – 3 years\n","3. 3 – 5 years\n","4. More than 5 years\n")
        estimated_period = st.radio(key="estimated_period", label = "Choose your answer", options = [1,2,3,4])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        st.markdown('''
            #### QUESTION 7
            ''')
        st.write("Which of the following investment scenarios are you willing to be engaged in?\n","1. Scenario 1: returns of perhaps 2.5%, and 0% loss\n","2. Scenario 2: maximum returns of perhaps 7%, and 1% possible loss\n","3. Scenario 3: maximum returns of perhaps 15%, and 5% possible loss\n","4. Scenario 4: maximum returns of perhaps 25%, and 15% possible loss\n")
        scenario = st.selectbox(label = "Choose your answer", options=[1,2,3,4])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        st.markdown('''
            #### QUESTION 8
            ''')
        st.write("You would be worried or unwilling to accept a scenario where your investment diminishes by:\n","1. 5% or less\n","2. Around 5% - 10%\n","3. Around 10% - 20%\n","4. Over 20%\n")
        unwilling_toAccept = st.radio(key="unwilling_toAccept", label = "Choose your answer", options = [1,2,3,4])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        
        submit_button = st.form_submit_button(label = "find out your risk scores")

    # ---- PRICE PREDICTION PROCESS ----

    # convert into dataframe
    data = pd.DataFrame({
                    'age': age,
                    'expenses': expenses,
                    'financial_status': financial_status,
                    'experience':total_value,
                    'estimated_period': estimated_period,
                    'unwilling_toAccept': unwilling_toAccept,
                    'scenario': scenario,
                    'salary': salary
                        }, index=[0])
    #pipelining
    X = pipeline.transform(data)

    # model predict
    clas = model.predict(X).tolist()[0]
    result = str(clas)

    # ---- SUBMIT BUTTON ACTION ----
    if submit_button:
        # --- showing progress bar ---
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i+1)
    
        st.success('Your Risk Score is asessed!')
        st.write('Hello there `{}` ! Your Risk Profile Assesment Score is : '.format(name), result)

    # ---- FORECASTING PLOTS ----
        def plot_forecast_high(df_high):
            fig = go.Figure(
                            data = [
                            go.Scatter(
                                x = df_high['Date'], 
                                y = df_high.Forecast,
                                mode = 'lines', 
                                name = 'Forecasting ',
                                line = {'color': 'red'}
                            )
                        ]
                    )
            fig.update_layout(title_text = "",width = 600, height = 600, title_x=0.5, xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)

        def plot_forecast_low(df_low):
                fig = go.Figure(
                                data = [
                                go.Scatter(
                                    x = df_low['Date'], 
                                    y = df_low.Forcast,
                                    mode = 'lines', 
                                    name = 'Forecasting ',
                                    line = {'color': 'red'}
                                )
                            ]
                        )
                fig.update_layout(title_text = "",width = 600, height = 600, title_x=0.5, xaxis_rangeslider_visible=True)
                st.plotly_chart(fig)

    # ---- SHOWING MUTUAL FUNDS OPTIONS----
        def money_market():
                # ---- SHOWING THE FULL GRAPH ----
                df_1 = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Pasar Uang/MNC Dana Lancar_HL.csv')
                df_high = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Pasar Uang/MNC High Forecast.csv')
                df_low = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Pasar Uang/MNC Low Forecast.csv')
                def plot_raw_data():
                    fig = go.Figure(
                            data = [
                            go.Scatter(
                                x = df_1['Date'], 
                                y = df_1.Low,
                                mode = 'lines', 
                                name = 'Low',
                                line = {'color': 'yellow'}
                            ),
                            go.Scatter(
                                x = df_1['Date'], 
                                y = df_1.High,
                                mode = 'lines', 
                                name = 'High',
                                line = {'color': 'red'}
                            )
                        ]
                    )
                    fig.update_layout(title_text="Product : MNC Dana Lancar Money Market Fund", width = 600, height = 600, title_x=0.5, xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
                plot_raw_data()
                # ---- SHOWING THE HIGH LOW TABLE ---
                st.write("MNC Dana Lancar Money Market Fund Data")
                gd = GridOptionsBuilder.from_dataframe(df_1)
                gd.configure_pagination(enabled=True, paginationPageSize=10)
                AgGrid(df_1, gridOptions=gd.build(), height=250, key='result1')
                st.write("")
                st.markdown('''
                            ## WEEKLY PRICE FORECASTING
                            ''')
                st.markdown('''
                    ### HIGH PRICE FORECASTING
                    ''')
                plot_forecast_high(df_high)
                st.markdown('''
                    ### LOW PRICE FORECASTING
                    ''')
                plot_forecast_low(df_low)
                
                
                # st.markdown('''
                #             ## Weekly Money Market Forecasting 
                #             ''')
                # high_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/Pasar Uang/MNC High.png'
                # low_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/Pasar Uang/MNC Low.png'
                # st.markdown('''
                # #### HIGH PRICE PREDICTION
                # ''')
                # st.image(high_path)
                # st.markdown('''
                # #### LOW PRICE PREDICTION
                # ''')
                # st.image(low_path)

        def fixed_income_1():
                        # ---- SHOWING THE FULL GRAPH ----
                df_2 = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Pendapatan Tetap/Ashmore Dana Obligasi Nusantara/Ashmore Dana Obligasi Nusantara_HL.csv')
                df_high = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Pendapatan Tetap/Ashmore Dana Obligasi Nusantara/ADON High Forecast.csv')
                df_low = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Pendapatan Tetap/Ashmore Dana Obligasi Nusantara/ADON Low Forecast.csv')
                
                def plot_raw_data():
                    fig = go.Figure(
                            data = [
                            go.Scatter(
                                x = df_2['Date'], 
                                y = df_2.Low,
                                mode = 'lines', 
                                name = 'Low',
                                line = {'color': 'yellow'}
                            ),
                            go.Scatter(
                                x = df_2['Date'], 
                                y = df_2.High,
                                mode = 'lines', 
                                name = 'High',
                                line = {'color': 'red'}
                            )
                        ]
                    )
                    fig.update_layout(title_text="Product : Ashmore Dana Obligasi Nusantara Fixed Income Fund", width = 600, height = 600, title_x=0.5, xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
                plot_raw_data()

                # ---- SHOWING THE HIGH LOW TABLE ---
                st.write("Ashmore Dana Obligasi Nusantara Fixed Income Fund Data")
                gd = GridOptionsBuilder.from_dataframe(df_2)
                gd.configure_pagination(enabled=True, paginationPageSize=10)
                AgGrid(df_2, gridOptions=gd.build(), height=250,key='result2_1')
                st.write("")
                st.markdown('''
                            ## WEEKLY PRICE FORECASTING
                            ''')
                st.markdown('''
                    ### HIGH PRICE FORECASTING
                    ''')
                plot_forecast_high(df_high)
                st.markdown('''
                    ### LOW PRICE FORECASTING
                    ''')
                plot_forecast_low(df_low)
                # st.markdown('''
                #             ## Weekly Ashmore Dana Obligasi Nusantara Fixed Income Forecasting 
                #             ''')
                # high_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/Pendapatan Tetap/Ashmore Dana Obligasi Nusantara/ADPN High.png'
                # low_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/Pendapatan Tetap/Ashmore Dana Obligasi Nusantara/ADON Low.png'
                # st.markdown('''
                # #### HIGH PRICE PREDICTION
                # ''')
                # st.image(high_path)
                # st.markdown('''
                # #### LOW PRICE PREDICTION
                # ''')
                # st.image(low_path)


        def fixed_income_2():
        # ---- SHOWING THE FULL GRAPH ----
                df_3 = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Pendapatan Tetap/Schroder Dana Mantap II/Schroder Dana Mantap II_HL.csv')
                df_high = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Pendapatan Tetap/Schroder Dana Mantap II/SDM High Forecast.csv')
                df_low = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Pendapatan Tetap/Schroder Dana Mantap II/SDM Low Forecast.csv')
                def plot_raw_data():
                    fig = go.Figure(
                            data = [
                            go.Scatter(
                                x = df_3['Date'], 
                                y = df_3.Low,
                                mode = 'lines', 
                                name = 'Low',
                                line = {'color': 'yellow'}
                            ),
                            go.Scatter(
                                x = df_3['Date'], 
                                y = df_3.High,
                                mode = 'lines', 
                                name = 'High',
                                line = {'color': 'red'}
                            )
                        ]
                    )
                    fig.update_layout(title_text="Product : Schroder Dana Mantap II Fixed Income Fund", width = 600, height = 600, title_x=0.5, xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
                plot_raw_data()

                # ---- SHOWING THE HIGH LOW TABLE ---
                st.write("Schroder Dana Mantap II Fixed Income Fund Data")
                gd = GridOptionsBuilder.from_dataframe(df_3)
                gd.configure_pagination(enabled=True, paginationPageSize=10)
                AgGrid(df_3, gridOptions=gd.build(), height=250,key='result2_2')
                st.write("")
                st.markdown('''
                            ## WEEKLY PRICE FORECASTING
                            ''')
                st.markdown('''
                ### HIGH PRICE FORECASTING
                ''')
                plot_forecast_high(df_high)
                st.markdown('''
                    ### LOW PRICE FORECASTING
                    ''')
                plot_forecast_low(df_low)
                # st.markdown('''
                #             ## Weekly Schroder Dana Mantap II Fixed Income Forecasting 
                #             ''')
                # high_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/Pendapatan Tetap/Schroder Dana Mantap II/SDM high.png'
                # low_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/Pendapatan Tetap/Schroder Dana Mantap II/SDM Low.png'
                # st.markdown('''
                # #### HIGH PRICE PREDICTION
                # ''')
                # st.image(high_path)
                # st.markdown('''
                # #### LOW PRICE PREDICTION
                # ''')
                # st.image(low_path)
        
        def mixed_fund():
            df_4 = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Campuran/Schroder Dana Terpadu II.csv')
            df_high = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Campuran/SDT High Forecast.csv')
            df_low = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/Campuran/SDT Low Forecast.csv')
            def plot_raw_data():
                    fig = go.Figure(
                            data = [
                            go.Scatter(
                                x = df_4['Date'], 
                                y = df_4.Low,
                                mode = 'lines', 
                                name = 'Low',
                                line = {'color': 'yellow'}
                            ),
                            go.Scatter(
                                x = df_4['Date'], 
                                y = df_4.High,
                                mode = 'lines', 
                                name = 'High',
                                line = {'color': 'red'}
                            )
                        ]
                    )
                    fig.update_layout(title_text="Product : Schroder Dana Terpadu II Balanced Fund", width = 600, height = 600, title_x=0.5, xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
            plot_raw_data()

            # ---- SHOWING THE HIGH LOW TABLE ---
            st.write("Schroder Dana Terpadu II Balanced Fund Data")
            gd = GridOptionsBuilder.from_dataframe(df_4)
            gd.configure_pagination(enabled=True, paginationPageSize=10)
            AgGrid(df_4, gridOptions=gd.build(), height=250,key='result3')
            st.write("")
            st.markdown('''
                        ## WEEKLY PRICE FORECASTING
                        ''')
            st.markdown('''
            ### HIGH PRICE FORECASTING
            ''')
            plot_forecast_high(df_high)
            st.markdown('''
                ### LOW PRICE FORECASTING
                ''')
            plot_forecast_low(df_low)
            # st.markdown('''
            #             ## Weekly Schroder Dana Terpadu II Balanced Fund Forecasting 
            #             ''')
            # high_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/Campuran/SDT High.png'
            # low_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/Campuran/SDT Low.png'
            # st.markdown('''
            # #### HIGH PRICE PREDICTION
            # ''')
            # st.image(high_path)
            # st.markdown('''
            # #### LOW PRICE PREDICTION
            # ''')
            # st.image(low_path)
        
        def stock1():
            df_5 = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Ashmore_Dana_Ekuitas_Nusantara/Ashmore_Dana_Ekuitas_Nusantara_HL.csv')
            df_high = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Ashmore_Dana_Ekuitas_Nusantara/ADEN High Forecast.csv')
            df_low = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Ashmore_Dana_Ekuitas_Nusantara/ADEN Low Forecast.csv')
            def plot_raw_data():
                    fig = go.Figure(
                            data = [
                            go.Scatter(
                                x = df_5['Date'], 
                                y = df_5.Low,
                                mode = 'lines', 
                                name = 'Low',
                                line = {'color': 'yellow'}
                            ),
                            go.Scatter(
                                x = df_5['Date'], 
                                y = df_5.High,
                                mode = 'lines', 
                                name = 'High',
                                line = {'color': 'red'}
                            )
                        ]
                    )
                    fig.update_layout(title_text="Product : Ashmore Dana Ekuitas Nusantara Equity Fund", width = 600, height = 600, title_x=0.5, xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
            plot_raw_data()

            # ---- SHOWING THE HIGH LOW TABLE ---
            st.write("Ashmore Dana Ekuitas Nusantara Equity Fund Data")
            gd = GridOptionsBuilder.from_dataframe(df_5)
            gd.configure_pagination(enabled=True, paginationPageSize=10)
            AgGrid(df_5, gridOptions=gd.build(), height=250,key='result4_1')
            st.write("")
            st.markdown('''
                        ## WEEKLY PRICE FORECASTING
                        ''')
            st.markdown('''
            ### HIGH PRICE FORECASTING
            ''')
            plot_forecast_high(df_high)
            st.markdown('''
                ### LOW PRICE FORECASTING
                ''')
            plot_forecast_low(df_low)
            # st.markdown('''
            #             ## Weekly Ashmore Dana Ekuitas Nusantara Equity Fund Forecasting 
            #             ''')
            # high_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Ashmore_Dana_Ekuitas_Nusantara/ADEN High.png'
            # low_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Ashmore_Dana_Ekuitas_Nusantara/ADEN Low.png'
            # st.markdown('''
            # #### HIGH PRICE PREDICTION
            # ''')
            # st.image(high_path)
            # st.markdown('''
            # #### LOW PRICE PREDICTION
            # ''')
            # st.image(low_path)

        def stock2():
            df_6 = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Ashmore_Dana_Progresif_Nusantara/Ashmore Dana Progresif Nusantara_HL.csv')
            df_high = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Ashmore_Dana_Progresif_Nusantara/ADPN High Forecast.csv')
            df_low = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Ashmore_Dana_Progresif_Nusantara/ADPN Low Forecast.csv')
            def plot_raw_data():
                    fig = go.Figure(
                            data = [
                            go.Scatter(
                                x = df_6['Date'], 
                                y = df_6.Low,
                                mode = 'lines', 
                                name = 'Low',
                                line = {'color': 'yellow'}
                            ),
                            go.Scatter(
                                x = df_6['Date'], 
                                y = df_6.High,
                                mode = 'lines', 
                                name = 'High',
                                line = {'color': 'red'}
                            )
                        ]
                    )
                    fig.update_layout(title_text="Product : Ashmore Dana Progresif Nusantara Equity Fund", width = 600, height = 600, title_x=0.5, xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
            plot_raw_data()

            # ---- SHOWING THE HIGH LOW TABLE ---
            st.write("Ashmore Dana Progresif Nusantara Equity Fund Data")
            gd = GridOptionsBuilder.from_dataframe(df_6)
            gd.configure_pagination(enabled=True, paginationPageSize=10)
            AgGrid(df_6, gridOptions=gd.build(), height=250,key='result4_2')
            st.write("")
            st.markdown('''
                        ## WEEKLY PRICE FORECASTING
                        ''')
            st.markdown('''
            ### HIGH PRICE FORECASTING
            ''')
            plot_forecast_high(df_high)
            st.markdown('''
                ### LOW PRICE FORECASTING
                ''')
            plot_forecast_low(df_low)
            # st.markdown('''
            #             ## Weekly Ashmore Dana Progresif Nusantara Equity Fund Forecasting 
            #             ''')
            # high_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Ashmore_Dana_Progresif_Nusantara/ADPN High.png'
            # low_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Ashmore_Dana_Progresif_Nusantara/ADPN Low.png'
            # st.markdown('''
            # #### HIGH PRICE PREDICTION
            # ''')
            # st.image(high_path)
            # st.markdown('''
            # #### LOW PRICE PREDICTION
            # ''')
            # st.image(low_path)

        def stock3():
            df_7 = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Schroder_Dana_Prestasi/Schroder Dana Prestasi_HL.csv')
            df_high = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Schroder_Dana_Prestasi/SDP High Forecast.csv')
            df_low = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Schroder_Dana_Prestasi/SDP Low Forecast.csv')
            def plot_raw_data():
                    fig = go.Figure(
                            data = [
                            go.Scatter(
                                x = df_7['Date'], 
                                y = df_7.Low,
                                mode = 'lines', 
                                name = 'Low',
                                line = {'color': 'yellow'}
                            ),
                            go.Scatter(
                                x = df_7['Date'], 
                                y = df_7.High,
                                mode = 'lines', 
                                name = 'High',
                                line = {'color': 'red'}
                            )
                        ]
                    )
                    fig.update_layout(title_text="Product : Schroder Dana Prestasi Equity Fund", width = 600, height = 600, title_x=0.5, xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
            plot_raw_data()

            # ---- SHOWING THE HIGH LOW TABLE ---
            st.write("Schroder Dana Prestasi Equity Fund Data")
            gd = GridOptionsBuilder.from_dataframe(df_7)
            gd.configure_pagination(enabled=True, paginationPageSize=10)
            AgGrid(df_7, gridOptions=gd.build(), height=250,key='result4_3')
            st.write("")
            st.markdown('''
                        ## WEEKLY PRICE FORECASTING
                        ''')
            st.markdown('''
            ### HIGH PRICE FORECASTING
            ''')
            plot_forecast_high(df_high)
            st.markdown('''
                ### LOW PRICE FORECASTING
                ''')
            plot_forecast_low(df_low)
            # st.markdown('''
            #             ## Weekly Schroder Dana Prestasi Equity Fund Forecasting 
            #             ''')
            # high_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Schroder_Dana_Prestasi/SDP High.png'
            # low_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Schroder_Dana_Prestasi/SDP Low.png'
            # st.markdown('''
            # #### HIGH PRICE PREDICTION
            # ''')
            # st.image(high_path)
            # st.markdown('''
            # #### LOW PRICE PREDICTION
            # ''')
            # st.image(low_path)

        def stock4():
            df_8 = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Schroder_Dana_Prestasi_Plus/Schroder Dana Prestasi Plus_HL.csv')
            df_high = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Schroder_Dana_Prestasi_Plus/SDPP High Forecast.csv')
            df_low = pd.read_csv('/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Schroder_Dana_Prestasi_Plus/SDPP Low Forecast.csv')
            def plot_raw_data():
                    fig = go.Figure(
                            data = [
                            go.Scatter(
                                x = df_8['Date'], 
                                y = df_8.Low,
                                mode = 'lines', 
                                name = 'Low',
                                line = {'color': 'yellow'}
                            ),
                            go.Scatter(
                                x = df_8['Date'], 
                                y = df_8.High,
                                mode = 'lines', 
                                name = 'High',
                                line = {'color': 'red'}
                            )
                        ]
                    )
                    fig.update_layout(title_text="Product : Schroder Dana Prestasi Plus Equity Fund", width = 600, height = 600, title_x=0.5, xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
            plot_raw_data()

            # ---- SHOWING THE HIGH LOW TABLE ---
            st.write("Schroder Dana Prestasi Plus Equity Fund Data")
            gd = GridOptionsBuilder.from_dataframe(df_8)
            gd.configure_pagination(enabled=True, paginationPageSize=10)
            AgGrid(df_8, gridOptions=gd.build(), height=250,key='result4_4')
            st.write("")
            st.markdown('''
                        ## WEEKLY PRICE FORECASTING
                        ''')
            st.markdown('''
            ### HIGH PRICE FORECASTING
            ''')
            plot_forecast_high(df_high)
            st.markdown('''
                ### LOW PRICE FORECASTING
                ''')
            plot_forecast_low(df_low)
            # st.markdown('''
            #             ## Weekly Schroder Dana Prestasi Plus Equity Fund Forecasting 
            #             ''')
            # high_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Schroder_Dana_Prestasi_Plus/SDPP High.png'
            # low_path = '/Users/zow/Desktop/FINAL PROJECT/FinProData/SAHAM/Schroder_Dana_Prestasi_Plus/SDPP Low.png'
            # st.markdown('''
            # #### HIGH PRICE PREDICTION
            # ''')
            # st.image(high_path)
            # st.markdown('''
            # #### LOW PRICE PREDICTION
            # ''')
            # st.image(low_path)


    # ---- RESULTS CONDITION ----
        if result == "1": 
            st.markdown('''
                ### From your risk profile assesment we recommend the Mutual Funds products of :''')
            with st.expander('MNC Dana Lancar Money Market Fund'):
                money_market()
            
        if result == "2":
            st.markdown('''
                ### From your risk profile assesment we recommend the Mutual Funds products of :''')
            with st.expander('MNC Dana Lancar Money Market Fund'):
                money_market()
            with st.expander('Ashmore Dana Obligasi Nusantara Fixed Income Fund'):
                fixed_income_1()
            with st.expander('Schroder Dana Mantap II Fixed Income Fund'):
                fixed_income_2()

        if result == "3":
            st.markdown('''
                ### From your risk profile assesment we recommend the Mutual Funds products of :''')
            with st.expander('MNC Dana Lancar Money Market Fund'):
                money_market()
            with st.expander('Ashmore Dana Obligasi Nusantara Fixed Income Fund'):
                fixed_income_1()
            with st.expander('Schroder Dana Mantap II Fixed Income Fund'):
                fixed_income_2()
            with st.expander('Schroder Dana Terpadu II Balanced Fund'):
                mixed_fund()

        if result == "4":
            st.markdown('''
                ### From your risk profile assesment we recommend the Mutual Funds products of :''')
            with st.expander('MNC Dana Lancar Money Market Fund'):
                money_market()
            with st.expander('Ashmore Dana Obligasi Nusantara Fixed Income Fund'):
                fixed_income_1()
            with st.expander('Schroder Dana Mantap II Fixed Income Fund'):
                fixed_income_2()
            with st.expander('Schroder Dana Terpadu II Balanced Fund'):
                mixed_fund()
            with st.expander('Ashmore Dana Ekuitas Nusantara Equity Fund'):
                stock1()
            with st.expander('Ashmore Dana Progresif Nusantara Equity Fund'):
                stock2()
            with st.expander('Schroder Dana Prestasi Equity Fund'):
                stock3()
            with st.expander('Schroder Dana Prestasi Plus Equity Fund'):
                stock4()
            
        if result == "5":
            st.markdown('''
                ### From your risk profile assesment we recommend the Mutual Funds products of :''')
            with st.expander('MNC Dana Lancar Money Market Fund'):
                money_market()
            with st.expander('Ashmore Dana Obligasi Nusantara Fixed Income Fund'):
                fixed_income_1()
            with st.expander('Schroder Dana Mantap II Fixed Income Fund'):
                fixed_income_2()
            with st.expander('Schroder Dana Terpadu II Balanced Fund'):
                mixed_fund()
            with st.expander('Ashmore Dana Ekuitas Nusantara Equity Fund'):
                stock1()
            with st.expander('Ashmore Dana Progresif Nusantara Equity Fund'):
                stock2()
            with st.expander('Schroder Dana Prestasi Equity Fund'):
                stock3()
            with st.expander('Schroder Dana Prestasi Plus Equity Fund'):
                stock4()

if page_nav == "What is Mutual Funds?":
    st.markdown("""
            Mutual Fund is one of the investment alternatives for financial assets. Mutual Fund is known as “Reksa Dana” in Indonesia.

Mutual fund is a collective investment scheme pooled by a Fund Manager from institutions or individual investors to be managed professionally. This type of fund management is aimed at providing capital gains to investors over a period of time. Mutual Fund is regulated under Law of Capital Market Year 1995.

Investment portfolio of mutual fund can consist of securities such as stocks, bonds, money market instruments, or a combination of these securities.
            """)

    st.markdown("""
            ## Here Are the types of Mutual Funds Available in this system :
            1. Money Market Fund\n
            \tThis type of mutual fund has a 100% investment policy in money market instruments or securities with a maturity of less than 1 year. the lowest risk and the return is relatively smaller.\n
            2. Fixed Income Fund\n
            \tAllocation (minimum 80%) is placed in securities that provide a fixed income, such as debentures or bonds. Suitable for meeting financial goals with a maturity of between 1-3 years.\n
            3. Equity Fund\n
            \tMixed mutual funds have a maximum investment policy of 79% in money market instruments, bonds and stocks. Suitable for meeting financial goals with a maturity of between 3-5 years.\n
            4. Stock Fund\n
            \tThis mutual fund type has an investment policy of minimum 80% in 1 instrument of stocks. Suitable to fullfill long term financial needs for more than 5 years. High risk, high returns.
    """)  
    logo = Image.open('Logo.png')  
    st.image(logo)