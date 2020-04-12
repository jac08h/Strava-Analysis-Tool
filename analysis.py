"""analysis.py

Processes and analyses Strava athlete and activity data.

Functions:
create_activity_dataframe()
display_summary_statistics()
display_commute_statistics()
display_commute_plots()
display_activity_count_plot()
display_mean_distance_plot()

Felix van Oost 2020
"""

# Standard library imports
import datetime

# Third-party imports
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#sns.set(rc={'axes.facecolor':'#1d1d1d', 'figure.facecolor':'#1d1d1d'})

# Universal colour palette for generating plots
universal_colour_palette = ["#2C3E50", "#E74C3C", "#ECF0F1", "#3498DB", "#2980B9", "#195962", "#F56F6C", "#FFFFFF", "#252932", "#191C21"]

def _generate_mean_distance_plot(activity_data: pd.DataFrame, ax: mpl.axes.Axes, colour_palette: list):
    """
    Generate a bar plot of mean activity distance over time (by type).

    Arguments:
    activity data - A pandas DataFrame containing the activity data.
    ax - A set of matplotlib axes to generate the plot on.
    colour_palette - The colour palette to generate the plot with.
    """

    # Group the activity data by month and calculate the mean distance of each activity type
    data = activity_data.groupby([activity_data.index.to_period('Y'), 'type']).mean().reset_index()

    # Generate and format the bar plot
    sns.barplot(x='start_date_local',
                y='distance',
                hue='type',
                data=data,
                palette=colour_palette,
                ax=ax)
    ax.set(title='Mean activity distance over time', ylabel='Mean distance (km)', xlabel='Year')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.grid(b=True, which='major', linewidth=1.0)
    ax.yaxis.grid(b=True, which='minor', linewidth=0.5)
    ax.set_axisbelow(True)


def _generate_activity_count_plot(activity_data: pd.DataFrame, ax: mpl.axes.Axes, colour_palette: list):
    """
    Generate a bar plot of activity counts over time (by type).

    Arguments:
    activity data - A pandas DataFrame containing the activity data.
    ax - A set of matplotlib axes to generate the plot on.
    colour_palette - The colour palette to generate the plot with.
    """

    # Group the activity data by month and calculate the count of each activity type
    data = (activity_data.groupby([activity_data.index.to_period('M'), 'type'])
                         .size().to_frame('count').reset_index())

    # Generate and format the bar plot
    sns.barplot(x='start_date_local',
                y='count',
                hue='type',
                data=data,
                palette=colour_palette,
                ax=ax)
    ax.set(title='Activities over time', ylabel='Number of activities', xlabel='Month')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.grid(b=True, which='major', linewidth=1.0)
    ax.yaxis.grid(b=True, which='minor', linewidth=0.5)
    ax.set_axisbelow(True)


def _generate_commute_count_plot(commute_data: pd.DataFrame, ax: mpl.axes.Axes, colour_palette: list):
    """
    Generate a bar plot of number of commutes per month.

    Arguments:
    commute_data - A pandas DataFrame containing the commute activity data.
    ax - A set of matplotlib axes to generate the plot on.
    colour_palette - The colour palette to generate the plot with.
    """

    # Group the commute data by month
    data = commute_data.resample('M').count()

    # Generate and format the bar plot
    sns.barplot(x=data.index.to_period('M'),
                y=data['distance'],
                color=colour_palette[0],
                ax=ax)
    ax.set(ylabel='Number of commutes', xlabel='Month')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.grid(b=True, which='major', linewidth=1.0)
    ax.yaxis.grid(b=True, which='minor', linewidth=0.5)
    ax.set_axisbelow(True)


def _generate_commute_distance_plot(commute_data: pd.DataFrame, ax: mpl.axes.Axes, colour_palette: list):
    """
    Generate a line plot of total and mean commute distance per year.

    Arguments:
    commute_data - A pandas DataFrame containing the commute activity data.
    ax - A set of matplotlib axes to generate the plot on.
    colour_palette - The colour palette to generate the plot with.
    """

    # Group the commute data by year
    data = commute_data.resample('Y').agg({'distance': ['sum', 'mean']})

    # Generate and format the total distance line plot
    sns.lineplot(x=data.index.year,
                 y=data['distance', 'sum'],
                 color=colour_palette[0],
                 marker='o',
                 ax=ax)
    ax.set_xlabel('Year')
    ax.set_ylabel('Total commute distance (km)', color=colour_palette[0])
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.grid(b=True, which='major', linewidth=1.0)
    ax.yaxis.grid(b=True, which='minor', linewidth=0.5)

    # Generate and format the mean distance line plot
    ax_mean = ax.twinx()
    sns.lineplot(x=data.index.year,
                 y=data['distance', 'mean'],
                 color=colour_palette[1],
                 marker='o',
                 ax=ax_mean)
    ax_mean.set_ylabel('Average commute distance (km)', color=colour_palette[1])


def _generate_commute_days_plot(commute_data: pd.DataFrame, ax: mpl.axes.Axes, colour_palette: list):
    """
    Generate a line plot of commute days per year.

    Arguments:
    commute_data - A pandas DataFrame containing the commute activity data.
    ax - A set of matplotlib axes to generate the plot on.
    colour_palette - The colour palette to generate the plot with.
    """
    
    # Group the commute data by day
    data = commute_data.groupby(commute_data.index.to_period('D')).agg({'distance': 'mean'})

    # Generate and format the line plot
    sns.lineplot(x=data.index.year.value_counts().index,
                 y=data.index.year.value_counts(),
                 palette=colour_palette,
                 marker='o',
                 ax=ax)
    ax.set(ylabel='Commute days', xlabel='Year')
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.grid(b=True, which='major', linewidth=1.0)
    ax.yaxis.grid(b=True, which='minor', linewidth=0.5)


def _generate_commute_statistics(x: pd.Series) -> pd.Series:
    """
    Generate basic commute statistics from a given pandas Series.

    Arguments:
    x - The Series to generate basic commute statistics from. 

    Return:
    A Series containing the following commute statistics:
    - Number of commutes
    - Total and average commute distance
    - Total and average commute time
    """

    rows = {'Number of commutes': x['type'].count(),
            'Total commute distance (km)': x['distance'].sum() / 1000,
            'Average commute distance (km)': x['distance'].mean() / 1000,
            'Total commute moving time (hours)': x['moving_time'].sum() / 3600,
            'Average commute moving time (mins)': x['moving_time'].mean() / 60}

    series = pd.Series(rows, index=['Number of commutes',
                                        'Total commute distance (km)',
                                        'Average commute distance (km)',
                                        'Total commute moving time (hours)',
                                        'Average commute moving time (mins)'])

    return series


def _generate_summary_statistics(x: pd.Series) -> pd.Series:
    """
    Generate basic statistics from a given pandas Series.

    Arguments:
    x - The Series to generate basic commute statistics from. 

    Return:
    A Series containing the following statistics:
    - Total and average distance
    - Total and average moving time
    - Total and average elevation gain
    - Average speed
    """

    rows = {'Number of activities': x['type'].count(),
            'Total distance (km)': x['distance'].sum() / 1000,
            'Average distance (km)': x['distance'].mean() / 1000,
            'Total moving time (hours)': x['moving_time'].sum() / 3600,
            'Average moving time (mins)': x['moving_time'].mean() / 60,
            'Total elevation gain (km)': x['total_elevation_gain'].sum() / 1000,
            'Average elevation gain (m)': x['total_elevation_gain'].mean(),
            'Average speed (km/h)': x['average_speed'].mean() * 3.6}

    series = pd.Series(rows, index=['Number of activities',
                                    'Total distance (km)',
                                    'Average distance (km)',
                                    'Total moving time (hours)',
                                    'Average moving time (mins)',
                                    'Total elevation gain (km)',
                                    'Average elevation gain (m)',
                                    'Average speed (km/h)'])

    return series


def display_mean_distance_plot(activity_dataframe: pd.DataFrame):
    """
    Generate and display a bar plot of mean activity distance over time (by type).

    Arguments:
    activity_dataframe - A pandas DataFrame containing the activity data.
    """

    # Create a list of stationary activities to exclude from the plot
    exclude_list = ['Crossfit', 'RockClimbing', 'WeightTraining', 'Workout', 'Yoga']

    # Get only the activity distances, types, and start dates
    activity_data = (activity_dataframe[~activity_dataframe['type'].isin(exclude_list)]
                                       [['distance', 'type', 'start_date_local']])
    activity_data = activity_data.set_index('start_date_local')

    # Convert the activity distances from m to km
    activity_data.loc[:, 'distance'] = activity_data.loc[:, 'distance'] / 1000

    # Create an empty set of axes
    fig = plt.figure()
    fig.set_tight_layout(True)
    ax = fig.add_subplot(1, 1, 1)

    # Generate and display the plot
    _generate_mean_distance_plot(activity_data, ax, universal_colour_palette)
    plt.show()


def display_activity_count_plot(activity_dataframe: pd.DataFrame):
    """
    Generate and display a bar plot of activity counts over time (by type).

    Arguments:
    activity_dataframe - A pandas DataFrame containing the activity data.
    """

    # Get only the activity types and start dates
    activity_data = activity_dataframe[['type', 'start_date_local']]
    activity_data = activity_data.set_index('start_date_local')

    # Create an empty set of axes
    fig = plt.figure()
    fig.set_tight_layout(True)
    ax = fig.add_subplot(1, 1, 1)

    # Generate and display the plot
    _generate_activity_count_plot(activity_data, ax, universal_colour_palette)
    plt.show()


def display_commute_plots(activity_dataframe: pd.DataFrame):
    """
    Generate and display the following plots using data from activities
    marked as commutes:

    - Number of commute days per year (line plot)
    - Total and average commute distance per year (line plot)
    - Number of commutes per month (bar plot)

    Arguments:
    activity_dataframe - A pandas DataFrame containing the activity data.
    """

    # Get only commute data
    commute_data = (activity_dataframe[activity_dataframe['commute'] == True]
                   [['distance', 'start_date_local']])
    commute_data = commute_data.set_index('start_date_local')

    # Convert the activity distances from m to km
    commute_data.loc[:, 'distance'] = commute_data.loc[:, 'distance'] / 1000

    # Create a new grid of subplots
    ax1 = plt.subplot2grid((2, 2), (0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid((2, 2), (0, 1), rowspan=1, colspan=1)
    ax3 = plt.subplot2grid((2, 2), (1, 0), rowspan=1, colspan=2)

    # Format the global plot
    plt.suptitle('Commutes', size=16)

    # Generate and display the plots
    _generate_commute_days_plot(commute_data, ax1, universal_colour_palette)
    _generate_commute_distance_plot(commute_data, ax2, universal_colour_palette)
    _generate_commute_count_plot(commute_data, ax3, universal_colour_palette)
    plt.show()


def display_commute_statistics(activity_dataframe: pd.DataFrame):
    """
    Display basic commute statistics for each activity type.

    Arguments:
    activity_dataframe - A pandas DataFrame containing the activity data.
    """

    commute_dataframe = activity_dataframe[activity_dataframe['commute'] == True]

    if not commute_dataframe.empty:
        commute_statistics = commute_dataframe.groupby('type').apply(_generate_commute_statistics)

        print('Commute statistics:')
        print()
        print(commute_statistics.T)
        print()
    else:
        print('Analysis: No commutes found')


def display_summary_statistics(activity_dataframe: pd.DataFrame):
    """
    Display basic statistics for each activity type.

    Arguments:
    activity_dataframe - A pandas DataFrame containing the activity data.
    """

    if not activity_dataframe.empty:
        summary_statistics = activity_dataframe.groupby('type').apply(_generate_summary_statistics)

        print()
        print('Summary statistics:')
        print()
        print(summary_statistics.T)
        print()
    else:
        print('Analysis: No activities found')


def create_activity_dataframe(activity_data: list) -> pd.DataFrame:
    """
    Create and return a pandas DataFrame from the activity data list and
    format the dates / times to simplify visual interpretation.

    Arguments:
    activity_data - A list of detailed activity data

    Return:
    A pandas DataFrame of formatted detailed activity data
    """

    # Configure pandas to display data to 2 decimal places
    pd.set_option('precision', 2)

    # Create a pandas data frame from the Strava activities list
    activity_dataframe = pd.DataFrame.from_records(activity_data)

    # Format the activity start dates and moving / elapsed times
    activity_dataframe.loc[:, 'start_date_local_formatted'] = (activity_dataframe['start_date_local']
        .apply(lambda x: x.strftime('%e %B %Y, %H:%M:%S').strip()))
    activity_dataframe.loc[:, 'moving_time_formatted'] = (activity_dataframe['moving_time']
        .apply(lambda x: str(datetime.timedelta(seconds=x))))
    activity_dataframe.loc[:, 'elapsed_time_formatted'] = (activity_dataframe['elapsed_time']
        .apply(lambda x: str(datetime.timedelta(seconds=x))))

    return activity_dataframe
