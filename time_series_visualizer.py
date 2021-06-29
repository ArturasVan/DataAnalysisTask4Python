import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.dates import  DateFormatter

months = ['January','February','March','April','May','June','July','August','September','October','November','December']

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'],index_col=['date'])

# Clean data

df = df[(df['value'] > df['value'].quantile(0.025)) &
        (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot

    fig, ax = plt.subplots()
    fig.set_figheight(6)
    fig.set_figwidth(14)

    ax.plot_date(df.index, df['value'], linestyle="solid", marker=None, color="red")
    ax.set_ylabel('Page Views')
    ax.set_xlabel('Date')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))




    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['Month'] = df_bar.index.strftime('%B')
    df_grp = df_bar.groupby(['year', 'Month'])
    df_grp['value'].apply(lambda x: x.mean())
    # Draw bar plot
    sns.set_style("ticks")
    g = sns.catplot(x="year", kind="bar", hue="Month", y="value", data=df_bar, hue_order=months, ci=None, legend=False, palette="hls")

    fig = g.fig
    ax = g.ax    
    ax.set_ylabel('Average Page Views')
    ax.set_xlabel('Years')
    plt.xticks(rotation=90)
    plt.legend(loc='upper left', title="Month")
    plt.setp(ax.get_legend().get_texts(), fontsize='8')
    plt.setp(ax.get_legend().get_title(), fontsize='8')
    plt.tight_layout()




    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig



def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    df_box.sort_values(by=['year','date'], ascending=[False, True], inplace=True)

    # Draw box plots (using Seaborn)
    
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')
    
    fig, axes= plt.subplots(nrows=1, ncols=2, figsize=(16,6))
    axes[0] = sns.boxplot(x=df_box['year'], y=df_box['value'], ax= axes[0])
    axes[1] = sns.boxplot(x=df_box['month'], y=df_box['value'], ax= axes[1])

    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_ylabel('Page Views')
    axes[0].set_xlabel('Year')

    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_ylabel('Page Views')
    axes[1].set_xlabel('Month')



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
