import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import japanize_matplotlib


class GenerateLineGraph:
        def __init__(self, file_name): 
                self.file_name = file_name  

        def Execute(self):
                fig = plt.figure()
                rcParams['figure.figsize'] = (35.0, 12.0)
                df = pd.read_csv('app/csv_files/%s.csv' % self.file_name, parse_dates=["落札年月"])
                plt.plot(df["落札年月"],df["月内平均落札価格"],color="blue",linestyle="solid", linewidth = 1.0)
                plt.ylabel("月内平均落札価格",size=14)
                plt.xlabel("落札年月日",size=13)
                plt.grid()
                fig.savefig('app/csv_files/%s.png' % self.file_name)

