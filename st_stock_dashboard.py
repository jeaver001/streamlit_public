import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf
import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
from pandas_datareader import data as wb
import requests
from dateutil import parser


st.set_page_config(layout="wide")

st.title("S&P 500 Stock Information")
st.write("As of", datetime.today().date().strftime('%d %B %Y'))

#Gets the list of S&P 500 ticker symbol from Wikipedia
ticker_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']

# Adds a dropdown list of ticker symbols and an update button
ticker = st.selectbox("Select a ticker symbol.", ticker_list, index =26)
update_button = st.button("Update", help = "Click to refresh the data.")

if update_button == "Update":
    main()
    
ticker_data = yf.Ticker(ticker)

tab1, tab2, tab3, tab4, tab5 =  st.tabs(["Summary", "Chart", "Financials", "Monte Carlo", "Headlines"])

#https://github.com/luigibr1/Streamlit-StockSearchWebApp/blob/master/web_app_v3.py
def main():
    with tab1:
    #Summary Tab including stock info, history, profile, description and major holders
        try:
            #creating df for stock info
            stock_df2 = ticker_data.info
            
            #Get the earnings date from the yfinance's calendar
            earnings_date = pd.DataFrame(ticker_data.calendar.iloc[0,:]).reset_index()
            earnings_start = earnings_date.iloc[0,1]
            earnings_start = pd.to_datetime(earnings_start).strftime('%d %b %Y')
            earnings_end = earnings_date.iloc[1,1]
            earnings_end = pd.to_datetime(earnings_end).strftime('%d %b %Y')
              
            #create df for major shareholders
            major_holders = ticker_data.major_holders.rename(columns={0: '', 1:' '})
            major_holders.set_index('', inplace=True)
                    
            insti_holders = ticker_data.institutional_holders
            insti_holders["Date Reported"] = pd.to_datetime(insti_holders["Date Reported"]).apply(lambda t: t.strftime('%d-%b-%Y'))
    
            
            mf_holders = ticker_data.mutualfund_holders
            mf_holders["Date Reported"] = pd.to_datetime(mf_holders["Date Reported"]).apply(lambda t: t.strftime('%d-%b-%Y'))
    
    
            #create df per period for the area chart
            stock_1M = ticker_data.history(period='1mo', interval = '1d', rounding = True)
            stock_3M = ticker_data.history(period='3mo', interval = '1d', rounding = True)
            stock_6M = ticker_data.history(period='6mo', interval = '1d', rounding = True)
            stock_YTD = ticker_data.history(period='ytd', interval = '1d', rounding = True)
            stock_1Y = ticker_data.history(period='1y', interval = '1d', rounding = True)
            stock_3Y = ticker_data.history(period='3y', interval = '1d', rounding = True)
            stock_5Y = ticker_data.history(period='5y', interval = '1d', rounding = True)
            stock_MAX = ticker_data.history(period='max', interval = '1d', rounding = True)
        
            with st.container(): 
                col_summary1, col_summary3, col_summary2, col_summary4, col_chart = st.columns([0.125, 0.125, 0.125, 0.125, 0.5])
                with col_summary1:
                
                    stock_table1 = ['Previous Close', 'Open', 'Bid', 'Ask',"Day's Range", "52-Week Range",
                              'Volume']
                    st.markdown("""---""")
                    for i in stock_table1:
                        st.write(i)
                    st.markdown("""---""")    
                
                with col_summary3:
                    st.markdown("""---""")
                    st.write(f"**{str(round(stock_df2['previousClose'],2))}**")
                    st.write(f"**{str(round(stock_df2['open'],2))}**")
                    st.write(f"**{str(round(stock_df2['bid'],2))}**", "x", f"**{str(round(stock_df2['bidSize'],2))}**")
                    st.write(f"**{str(round(stock_df2['ask'],2))}**", "x", f"**{str(round(stock_df2['askSize'],2))}**")
                    st.write(f"**{str(round(stock_df2['dayLow'],2))}**", "-", f"**{str(round(stock_df2['dayHigh'],2))}**")
                    st.write(f"**{str(round(stock_df2['fiftyTwoWeekLow'],2))}**", "-", f"**{str(round(stock_df2['fiftyTwoWeekHigh'],2))}**")
                    st.write(f"**{str(float(round(stock_df2['volume'],2)))}**")
                    st.markdown("""---""")
                
                with col_summary2:                
                      stock_table2 = ['Average Volume', 'Market Cap', 'Beta (5Y Monthly)', 'PE Ratio (TTM)',
                                      'EPS (TTM)', 'Forward Dividend & Yield', 'Earnings Date']
                      
                      st.markdown("""---""")
                      for i in stock_table2:
                          st.write(i)
                      st.markdown("""---""")   
                
                with col_summary4:
                    st.markdown("""---""")
                    st.write(f"**{str(float(round(stock_df2['averageVolume'],2)))}**")
                    st.write(f"**{str(float(round(stock_df2['marketCap'],2)))}**")                
                    st.write(f"**{str(round(stock_df2['beta'],2))}**")
                    st.write(f"**{str(round(stock_df2['trailingPE'],2))}**")
                    st.write(f"**{str(round(stock_df2['trailingEps'],2))}**")
                    st.write(f"**{str(stock_df2['dividendRate'])}**","(",f"**{str(stock_df2['dividendYield'])}**", ")")
                    st.write(f"**{earnings_start}**", "-", f"**{earnings_end}**")
                    st.markdown("""---""")
                
                with col_chart:
                    
                    #create tabs for each period
                    tab1M, tab3M, tab6M, tabYTD, tab1Y, tab3Y, tab5Y, tabMAX = st.tabs(["1M", "3M", "6M", "YTD", "1Y", "3Y", "5Y", "MAX"])
                
                #create area chart
                tab1M.area_chart(stock_1M.Close) 
                tab3M.area_chart(stock_3M.Close)
                tab6M.area_chart(stock_6M.Close)
                tabYTD.area_chart(stock_YTD.Close)
                tab1Y.area_chart(stock_1Y.Close)
                tab3Y.area_chart(stock_3Y.Close)
                tab5Y.area_chart(stock_5Y.Close)
                tabMAX.area_chart(stock_MAX.Close)
            
                st.subheader("""Company Profile""")
                col_sum, col_profile1, col_profile2, col_empty = st.columns([0.2, 0.2, 0.2, 0.4])
                
                #display ticker profile
                
                with col_sum:
                    st.image(stock_df2['logo_url'])
                    st.caption(f"**{stock_df2['longName']}**")
                    
                with col_profile1:
                    st.write(f"**{stock_df2['address1']}**")
                    st.write(f"**{stock_df2['city']}**", f"**{stock_df2['state']}**", f"**{stock_df2['zip']}**")
                    st.write(f"**{stock_df2['country']}**")    
                    st.write(f"**{stock_df2['phone']}**")
                    st.write(f"**{stock_df2['website']}**") 
    
                with col_profile2:
                    st.write("Sector:", f"**{stock_df2['sector']}**")
                    st.write("Industry:", f"**{stock_df2['industry']}**")
                    st.write("Full Time Employees:", f"**{stock_df2['fullTimeEmployees']}**")
                    
    
                st.markdown(f"**About {stock_df2['longName']}:**")
                st.write(stock_df2['longBusinessSummary'])
                
                #display major holders                
                
                st.subheader("Major Holders")
                st.write("Breakdown")
                st.dataframe(major_holders)
                
                col_insti, col_mf = st.columns(2)
                
                with col_insti:
                    st.write("Top Insitutional Holders")
                    st.dataframe(insti_holders)
                
                with col_mf:
                    st.write("Top Mutual Fund Holders")
                    st.dataframe(mf_holders)
                    
                st.caption("Source: Yahoo! Finance")       
    
        except:
            st.write("Oh no! We encountered an error upon retrieving information for", f"{ticker}", ". Please try another ticker.")
            
    #Chart Tab
    with tab2:
        try:    
            col1, col2, col3, col4, col5 = st.columns([0.6, 0.6, 1.9, 0.6, 0.6])
            
            interval_list = ('1d', '1wk', '1mo')
             	
            plot_list = ("Line", "Candle")
            
            #date input
            start_date = col1.date_input("Start date", datetime.today().date() - timedelta(days=30))
            end_date = col2.date_input("End date", datetime.today().date())
        
            today = date.today()
            
            #create start date variable for each period
            one_month = today - relativedelta(months=+1)
            three_months = today - relativedelta(months=+3)
            six_months = today - relativedelta(months=+6)
            ytd_start = date(today.year, 1, 1)
            one_year = today - relativedelta(months=+12)
            three_years = today - relativedelta(months=+36)
            five_years = today - relativedelta(months=+60)
            
            #create dictionary for the start date per period
            duration_list_dict = {"Date Range": start_date, "1M": one_month, "3M": three_months,
                               "6M": six_months, "YTD": ytd_start, "1Y": one_year,
                               "3Y": three_years, "5Y": five_years, "MAX": date(1960,1,1)}
            
            #create dictionary for the end date per period
            duration_end_dict = {"Date Range": end_date, "1M": today, "3M": today,
                               "6M": today, "YTD": today, "1Y": today,
                               "3Y": today, "5Y": today, "MAX": today}
            
            with col3:
                #create options to select different periods using radio buttons
                select_duration = st.radio("Duration (For a specific date range, select Date Range below.)", duration_list_dict.keys(), horizontal = True)
            
            with col4:
                #create options to select different intervals using select box
                select_interval = st.selectbox("Interval", interval_list)
                
            with col5:
                #create options to select different plots using select box
                select_plot = st.selectbox("Plot", plot_list)
            
            #if Date Range is selected in the radio button
            if select_duration == 'Date Range':
                
                #create df to get stock history based on specified period and interval
                stock_data = pd.DataFrame(yf.Ticker(ticker).history(start=start_date, 
                                                                    end=end_date, 
                                                                    interval = select_interval))
                stock_data.reset_index(inplace=True)
    
                #add rolling column for moving average
                stock_data['rolling'] = stock_data['Close'].rolling(50).mean()
    
                #adjust date column name and format
                stock_data = stock_data.rename(columns = {'index':'Date'})    
                stock_data['Date'] = pd.to_datetime(stock_data['Date'])
                
                #convert date column to numeric to be able to convert entire below df to float
                stock_data['Date'] = stock_data['Date'].apply(mpl_dates.date2num)
                
                #create df for stock open, high, low, close price and limit decimal points
                stock_data_ohlc = stock_data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
                stock_data_ohlc = stock_data_ohlc.astype(float)
                
                
            else:
                stock_data = pd.DataFrame(yf.Ticker(ticker).history(start=duration_list_dict.get(select_duration), 
                                                                    end=duration_end_dict.get(select_duration), 
                                                                    interval = select_interval))
                stock_data.reset_index(inplace=True)
                
                #add rolling column for moving average
                stock_data['rolling'] = stock_data['Close'].rolling(50).mean()
                
                #adjust date column name and format
                stock_data = stock_data.rename(columns = {'index':'Date'})    
                stock_data['Date'] = pd.to_datetime(stock_data['Date'])
                
                #convert date column to numeric to be able to convert entire below df to float
                stock_data['Date'] = stock_data['Date'].apply(mpl_dates.date2num)
    
                #create df for stock open, high, low, close price and limit decimal points
                stock_data_ohlc = stock_data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
                stock_data_ohlc = stock_data_ohlc.astype(float)
                        
            plt.rcParams['font.sans-serif'] = "Franklin Gothic Book"
            plt.rcParams['font.family'] = "sans-serif"
            date_format = mpl_dates.DateFormatter('%d %b %Y')
    
            if select_plot == "Candle":   
        
                fig, ax1 = plt.subplots(figsize=(15, 5))
                fig.tight_layout()
                
                #varying width based on the selected interval
                if select_interval == '1d':
                    candlestick_ohlc(ax1, stock_data_ohlc.values, colorup='green', colordown='red', alpha=0.8, width = 0.5)
                elif select_interval == '1wk':
                    candlestick_ohlc(ax1, stock_data_ohlc.values, colorup='green', colordown='red', alpha=0.8, width = 4.5)
                elif select_interval == '1mo':
                    candlestick_ohlc(ax1, stock_data_ohlc.values, colorup='green', colordown='red', alpha=0.8, width = 8.5)
                
                #format the plot
                ax1.xaxis.set_major_formatter(date_format)
                ax1.tick_params(labelbottom=True, labeltop=False, labelleft=False, labelright=False, right = False, bottom = False)
                ax1.spines['top'].set_visible(False)
                ax1.spines['right'].set_visible(False)
                ax1.spines['bottom'].set_visible(False)
                ax1.spines['left'].set_visible(False)
                ax1.get_yaxis().set_ticks([])
                ax1.set_facecolor('white')
                ax1.grid(False)
                
                #create a second plot for the historical volume
                ax2 = ax1.twinx()
                if select_interval == '1d':
                    ax2.bar(x = stock_data['Date'], height=stock_data['Volume'], color = 'royalblue', alpha=0.8,width = 0.5)
                elif select_interval == '1wk':
                    ax2.bar(x = stock_data['Date'], height=stock_data['Volume'], color = 'royalblue', alpha=0.8, width = 4.5)
                elif select_interval == '1mo':
                    ax2.bar(x = stock_data['Date'], height=stock_data['Volume'], color = 'royalblue', alpha=0.8, width = 8.5)
                
                #apply the same formatting to the second plot
                ax2.tick_params(labelbottom=False, labeltop=False, labelleft=False, labelright=False, right = False, bottom = False)
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.spines['bottom'].set_visible(False)
                ax2.spines['left'].set_visible(False)
                ax2.set_facecolor('white')
                ax2.margins(0,4)
                ax2.grid(False)
                
                #create a third plot for the moving average and apply the same formatting
                ax3 = ax1.twinx()
                ax3.plot(stock_data['Date'], stock_data['rolling'], color='darkviolet', linewidth=0.7)
                ax3.spines['top'].set_visible(False)
                ax3.spines['right'].set_visible(False)
                ax3.spines['bottom'].set_visible(False)
                ax3.spines['left'].set_visible(False)
                ax3.set_facecolor('white')
                ax3.grid(False)
                ax3.tick_params(labelbottom=False, labeltop=False, labelleft=False, labelright=False, right = False, bottom = False)               
                
                #show the plot
                st.pyplot(fig)
        
            elif select_plot == "Line":
                fig1, ax4 = plt.subplots(figsize=(15, 5))
                fig1.tight_layout()
    
                #create a line plot and apply formatting
                ax4.plot(stock_data['Date'], stock_data['Close'], linewidth=0.7, color = 'slategrey')
                ax4.xaxis.set_major_formatter(date_format)
                ax4.tick_params(labelbottom=True, labeltop=False, labelleft=False, labelright=False, right = False, bottom = False) 
                ax4.spines['top'].set_visible(False)
                ax4.spines['right'].set_visible(False)
                ax4.spines['bottom'].set_visible(False)
                ax4.spines['left'].set_visible(False)
                ax4.set_facecolor('white')
                ax4.get_yaxis().set_ticks([])        
                ax4.grid(False)
    
                #create a second plot for the volume
                ax5 = ax4.twinx()
                if select_interval == '1d':
                    ax5.bar(x = stock_data['Date'], height=stock_data['Volume'], color = 'royalblue', alpha=0.8,width = 0.5)
                elif select_interval == '1wk':
                    ax5.bar(x = stock_data['Date'], height=stock_data['Volume'], color = 'royalblue', alpha=0.8, width = 4.5)
                elif select_interval == '1mo':
                    ax5.bar(x = stock_data['Date'], height=stock_data['Volume'], color = 'royalblue', alpha=0.8, width = 8.5)            
                
                #apply formatting
                ax5.set_facecolor('white')
                ax5.margins(0,4)
                ax5.grid(False)
                ax5.spines['top'].set_visible(False)
                ax5.spines['right'].set_visible(False)
                ax5.spines['bottom'].set_visible(False)
                ax5.spines['left'].set_visible(False)
                ax5.get_yaxis().set_ticks([]) 
                ax5.tick_params(labelbottom=False, labeltop=False, labelleft=False, labelright=False, right = False, bottom = False)               
                
                #create a third plot for the moving average and apply the same formatting
                ax6 = ax4.twinx()
                ax6.plot(stock_data['Date'], stock_data['rolling'], color='darkviolet', linewidth=0.7)
                ax6.set_facecolor('white')
                ax6.grid(False)
                ax6.spines['top'].set_visible(False)
                ax6.spines['right'].set_visible(False)
                ax6.spines['bottom'].set_visible(False)
                ax6.spines['left'].set_visible(False)
                ax6.get_yaxis().set_ticks([])        
                ax6.tick_params(labelbottom=False, labeltop=False, labelleft=False, labelright=False, right = False, bottom = False)               
                
                st.pyplot(fig1)        
            st.caption("Source: Yahoo! Finance")
        
        except:
            st.write("Oh no! We encountered an error upon retrieving information for", f"{ticker}", ". Please try another ticker.")
            
    #Creates the annual/quarterly income statement, balance sheet, and cash flow statement
    #Functions were defined for each financial statement     
    with tab3:
        try:
            #needed for timeline selection to come before tabs
            col1,col2 = st.columns(2)
                    
            #create separate tabs for each financial statement
            tab_is, tab_bs, tab_cf = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
                
            with col1:
            #radio button to select between annual and quarterly
                timeline = st.radio('Select Period', ('Annual', 'Quarterly'), horizontal = True)
                    
            with col2:
                
                #create separate dfs and tables for annual and quarterlt statements
                with tab_is:
                    if timeline == 'Annual':
                        annual_is_df = ticker_data.financials.rename(lambda t: t.strftime('%d-%B-%Y'),
                                                                      axis='columns').drop(labels = ["Effect Of Accounting Charges", 
                                                                                                    "Extraordinary Items", "Other Operating Expenses",
                                                                                                    "Non Recurring","Other Items", "Discontinued Operations"],axis=0,inplace=False)
                        st.table(annual_is_df)
                    elif timeline == 'Quarterly':
                        qtrly_is_df = ticker_data.quarterly_financials.rename(lambda t: t.strftime('%d-%B-%Y'),
                                                                              axis='columns').drop(labels = ["Effect Of Accounting Charges",
                                                                                                              "Extraordinary Items", "Other Operating Expenses",
                                                                                                              "Non Recurring","Other Items", "Discontinued Operations"],axis=0,inplace=False)
                        st.table(qtrly_is_df)
                
                with tab_bs:
                    if timeline == 'Annual':
                        annual_bs_df = ticker_data.balancesheet.rename(lambda t: t.strftime('%d-%B-%Y'),axis='columns')
                        st.table(annual_bs_df)  
                                                               
                    elif timeline == 'Quarterly':
                        qtrly_bs_df = ticker_data.quarterly_balancesheet.rename(lambda t: t.strftime('%d-%B-%Y'),axis='columns')
                        st.table(qtrly_bs_df)
                        
                with tab_cf:
                    if timeline == 'Annual':
                        annual_cf_df = ticker_data.cashflow.rename(lambda t: t.strftime('%d-%B-%Y'),axis='columns')
                        st.table(annual_cf_df)
                    elif timeline == 'Quarterly':
                        qtrly_cf_df = ticker_data.quarterly_cashflow.rename(lambda t: t.strftime('%d-%B-%Y'),axis='columns')
                        st.table(qtrly_cf_df)                     
                    
            st.caption("Source: Yahoo! Finance")

        except:
            st.write("Oh no! We encountered an error upon retrieving information for", f"{ticker}", ". Please try another ticker.")

    with tab4:
    #Based on the monte carlo simulation performed in Financial Programming class by Professor Minh Phan.
        try:
            col_sim, col_time = st.columns(2)
                    
            simulation_list = (200, 500, 1000)
            horizon_dict = {"30 days": 30, "60 days": 60, "90 days": 90}
            np.random.seed(123)
            
            
            with col_sim:
                select_simulation = st.selectbox("Simulations", simulation_list)
                
            with col_time:
                select_horizon = st.selectbox("Horizon", horizon_dict.keys())
            
            st.write("A monte carlo simulation for the stock price of", f"{ticker}", "for the next", f"{select_horizon}")
            
            #read historical data
            monte_data = pd.DataFrame(wb.DataReader(ticker, data_source='yahoo', start='2022-01-01'))
            close_price = monte_data['Close']
            
            # The returns ((today price - yesterday price) / yesterday price)
            daily_return = close_price.pct_change()
            daily_volatility = np.std(daily_return)
    
            # Run the simulation
            simulation_df = pd.DataFrame()
    
            for i in range(select_simulation):
        
                # The list to store the next stock price
                next_price = []
                # Create the next stock price
                last_price = close_price[-1]
        
                for j in range(horizon_dict.get(select_horizon)):
                    # Generate the random percentage change around the mean (0) and std (daily_volatility)
                    future_return = np.random.normal(0, daily_volatility)
            
                    # Generate the random future price
                    future_price = last_price * (1 + future_return)
            
                    # Save the price and go next
                    next_price.append(future_price)
                    last_price = future_price
                
                next_price_df = pd.Series(next_price).rename('sim' + str(i))
                simulation_df = pd.concat([simulation_df, next_price_df], axis=1)    
        
            
            #plot the monte carlo simulation
            fig2, ax7 = plt.subplots(figsize=(15, 5))
            plt.plot(simulation_df, linewidth = 0.7)
            plt.grid(False)
            ax7.spines['top'].set_visible(False)
            ax7.spines['right'].set_visible(False)
            ax7.spines['bottom'].set_visible(False)
            ax7.spines['left'].set_visible(False)
            fig2.patch.set_alpha(0) #https://pythonguides.com/matplotlib-change-background-color/
            ax7.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False, left=False, bottom=False, labelsize=8) 
            
            #plot the current stock price
            plt.axhline(y=close_price[-1], color='steelblue')
            plt.legend(['The current stock price is: ' + str(np.round(close_price[-1], 2))], frameon=False)
            st.pyplot(fig2)
            
            # Get the ending price of the 200th day
            ending_price = simulation_df.iloc[-1:, :].values[0, ]
    
            # Price at 95% confidence interval
            future_price_95ci = np.percentile(ending_price, 5)
    
            # Value at Risk
            value_at_risk = close_price.iloc[-1] - future_price_95ci
            st.write('The Value at Risk at 95% confidence interval is: ',str(np.round(value_at_risk, 2)),' USD')
            
            st.caption("This simulation is based on the historical closing price of the stock from 01 Jan 2022 until today.")
            st.caption("Historical Data Source: DataReader")
    
        except:
            st.write("Oh no! We encountered an error upon retrieving information for", f"{ticker}", ". Please try another ticker.")

    
    #Get financial news for the specified ticker using newsapi.org
    #To see full feature, use AMZN as ticker
    with tab5:
        try:
# =============================================================================
#     https://www.youtube.com/watch?v=eJk_ySnVLmU
#     https://newsapi.org/docs/client-libraries/python
#     https://www.machinelearningplus.com/python/datetime-python-examples/
# =============================================================================
            with st.container():
            
                st.caption("Source: NewsAPI.org")
                
                ticker_name_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Security']
            
                #https://stackoverflow.com/questions/209840/how-can-i-make-a-dictionary-dict-from-separate-lists-of-keys-and-values
                #create a ticker dictionary to serve as news query
                ticker_dict = dict(zip(ticker_list, ticker_name_list))
                news_query = ticker_dict.get(ticker)
        
                #create url with varying query(ticker)
                url =  f"https://newsapi.org/v2/top-headlines?q={news_query}&language=en&location=us&apiKey=6bd40922b0e0414aa3dc0e724297cb8c"
                
                #request news based on url and use as json
                r = requests.get(url)
                r = r.json()
                
                articles = r['articles']
                if len(articles) > 0:
                    for article in articles:
                        st.header(article['title'])
                        st.write(article['source']['name'], "|", parser.parse(article['publishedAt']).strftime('%d %b %Y'))
                        if article['author']:
                            st.caption(article['author'])
                        if article['description']:
                            st.subheader(article['description'])
                        st.image(article['urlToImage'])
                else:
                    print(st.markdown(f"Sorry, no news articles were found for **{news_query}**."))             

        except:
            st.write("Oh no! We encountered an error upon retrieving information for", f"{ticker}", ". Please try another ticker.")
    
if __name__ == "__main__":
    main()