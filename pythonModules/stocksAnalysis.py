equirements:
#Python
#matplotlib : visualization library
#Pandas : data manipulation
###############

#Import Modules
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

import plotly
import plotly.graph_objects as graph_obj
from plotly.subplots import make_subplots

import re


import matplotlib.pyplot as plt
import datetime
import pytz
eastern_tz = pytz.timezone('US/Eastern')
india_tz = pytz.timezone('Asia/Kolkata')
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

config = {
        'io':{
            'graphReportFile':'stocks_graph_%s.html',
            'dataFile':'data_%s_%s.xls',
            'log':'log_%s'
        },
        'alphaVantageKey':'T5LTL1MIRCFHBKRF',
        'currentDate':datetime.datetime.now().strftime('%Y%m%d'),
        'portfolioStocks':['NSE:INFY','NSE:HDFC','NSE:M%26M'],
        'dataInterval':'1min',
        'graphsPerRow':['table','scatter','pie','heatmap'],
        'colors': ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    }

class StockDataUtil:
    def __init__(self):
        self.settings=config

    def load_excel_into_pandas(self,inputfile):
        try:
            # Script
            dataframe = pd.read_excel(inputfile)

            # Test to make sure data is loaded
            print(dataframe.head())

            # Pull out columns for graph
            # Unneccesary for final graph, but good indication if all your data is being read in.
            values = pd[['Locations', 'Profit']]
            print(values)

            # Bar Chart
            ax = values.plot.bar(x='Locations', y='Profit', rot=0)
            plt.show()
        except Exception as e:
            print(e)
            sys.exit()


    def load_stock_daily_data(self):
        try:
            ts = TimeSeries(key=self.settings['alphaVantageKey'], output_format='pandas')
            data, meta_data = ts.get_intraday(symbol=self.settings['portfolioStocks'][2], interval='1min', outputsize='full')
            print("Stock timeseries datadrame head is \n", data.head())
            print("-----------")
            i = 1
            # while i==1:
            #    data, meta_data = ts.get_intraday(symbol='MSFT', interval = '1min', outputsize = 'full')
            #    data.to_excel("output.xlsx")
            #    time.sleep(60)

            close_data = data['4. close']
            percentage_change = close_data.pct_change()

            # print("total percentage change \n",percentage_change)

            last_change = percentage_change[-1]

            print("latest percentage change \n", last_change)

            if abs(last_change) > 0.0004:
                print("Alert ["+str(self.settings['portfolioStocks'][2])+ "] increased:" + str(last_change))
                print("-----------")
            self.plot_graph(data)
        except Exception as e:
            print(e)
            sys.exit()

    def plot_graph(self,dataframe):
        try:
            # excel_file = 'ProductSales.xlsx'
            # pd = pd.read_excel(excel_file)
            dataframe.index = pd.to_datetime(dataframe.index)
            dataframe.index = dataframe.index.tz_localize(pytz.utc).tz_convert(india_tz)
            print(dataframe.head())
            print("-----------")

            data = [graph_obj.Scatter(x=dataframe.index, y=dataframe['2. high'])]

            fig = graph_obj.Figure(data)
            # fig.show()

            # plotly.offline.plot(fig, filename=self.settings['io']['graphReportFile']%(re.sub('[^A-Za-z0-9]+', '', self.settings['portfolioStocks'][2]),self.settings['currentDate']))
            plotly.offline.plot(graph_obj.Figure(data), filename=self.settings['io']['graphReportFile']%(self.settings['currentDate']))
        except Exception as e:
            print(e)
            sys.exit()

    def graph_all_stocks_of_portfolio(self):
        print("@graph_all_stocks_of_portfolio.")
        try:
            # Create subplots, using 'domain' type for pie charts
            # ['histogram', 'line', 'scatter', 'boxplot', 'dotplot', 'area', 'density', 'bar', 'barh',
            #               'heatmap', 'contour', 'hexbin', 'imshow']
            fig = make_subplots(rows=len(self.settings['portfolioStocks']),
                                cols=len(self.settings['graphsPerRow']),
                                shared_xaxes=False,
                                vertical_spacing=0.03,
                                specs=[[{"type": "table"},{"type": "scatter"},{"type": "domain"},{"type": "heatmap"}],
                                       [{"type": "table"}, {"type": "scatter"},{"type": "domain"},{"type": "heatmap"}],
                                       [{"type": "table"}, {"type": "scatter"},{"type": "domain"},{"type": "heatmap"}]]
                                )

            ts = TimeSeries(key=self.settings['alphaVantageKey'], output_format='pandas')
            stock_index = 0
            for stock_symbol in self.settings['portfolioStocks']:
                print("stock_symbol ["+stock_symbol+"]")
                stock_index += 1
                data, meta_data = ts.get_intraday(symbol=stock_symbol, interval=self.settings['dataInterval'],
                                                  outputsize='full')
                data.index = pd.to_datetime(data.index)
                data.index = data.index.tz_localize(pytz.utc).tz_convert(india_tz)
                print(data.head())
                print("----- creating ["+stock_symbol+"] Graph Row "+str(stock_index)+"------")
                fig.add_trace(
                    graph_obj.Table(
                        header=dict(
                            values=data.columns,
                            font=dict(size=12),
                            align="left"
                        ),
                        cells=dict(
                            values=[data[k].tolist() for k in data.columns],
                            align="left"),
                        name=stock_symbol
                    ),
                    row=stock_index, col=1
                )
                fig.add_trace(graph_obj.Scatter(x=data.index, y=data['2. high'],
                                                name=stock_symbol),
                              row=stock_index, col=2)
                # fig.add_trace(graph_obj.Pie(labels= data.index,values=data['2. high'],
                #                             name=stock_symbol),
                #               row=stock_index, col=3)
                fig.add_trace(graph_obj.Heatmap(
                                            z=[data[k].tolist() for k in data.columns],
                                            x=data.index,
                                            y=data.columns,
                                            colorscale='Viridis'),
                              row=stock_index, col=4)
                # time.sleep(60)

            # style all the traces
            fig.update_layout(title="Stocks data",height=700, showlegend=False)


            fig.show()
            # plotly.offline.plot(graph_obj.Figure(data), filename=self.settings['io']['graphReportFile'] % (self.settings['currentDate']))
        except Exception as e:
            print(e)
            sys.exit()

    # def predict_price(self,dataframe):


StockDataUtil().graph_all_stocks_of_portfolio()
