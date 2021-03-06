""" strava_analysis_tool.py

Main module for the Strava Analysis Tool.

Felix van Oost 2020
"""

# Standard library imports
import argparse

# Local imports
import analysis
import here_xyz
import geo
import strava_data

# File paths
STRAVA_ACTIVITY_DATA_FILE = 'Data/StravaActivityData.json'
STRAVA_GEO_DATA_FILE = 'Data/StravaGeoData.geojson'


def main():
    """
    Main method for the Strava Analysis Tool.
    """

    # Parse the command line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', '--activity_count_plot',
                        action='store_const',
                        const=True,
                        default=False,
                        required=False,
                        help='Generate and display a plot of activity counts over time')
    parser.add_argument('-c', '--commute_plots',
                        action='store_const',
                        const=True,
                        default=False,
                        required=False,
                        help='Generate and display plots of the commute data')
    parser.add_argument('-d', '--mean_distance_plot',
                        action='store_const',
                        const=True,
                        default=False,
                        required=False,
                        help='Generate and display a plot of the mean activity distance over time')
    parser.add_argument('-g', '--export_geo_data',
                        action='store_const',
                        const=True,
                        default=False,
                        required=False,
                        help='Export the geospatial activity data in GeoJSON format')
    parser.add_argument('-gu', '--export_upload_geo_data',
                        action='store_const',
                        const=True,
                        default=False,
                        required=False,
                        help=('Export the geospatial activity data in GeoJSON format and upload it'
                              ' to the HERE XYZ mapping platform'))
    parser.add_argument('-r', '--refresh_data',
                        action='store_const',
                        const=True,
                        default=False,
                        required=False,
                        help='Get and store a fresh copy of the activity data')
    args = parser.parse_args()

    # Get a list of detailed activity data for all Strava activities
    activity_data = strava_data.get_activity_data(STRAVA_ACTIVITY_DATA_FILE, args.refresh_data)

    # Create a pandas DataFrame from the activity data
    activity_dataframe = analysis.create_activity_dataframe(activity_data)

    # Display summary and commute statistics
    analysis.display_summary_statistics(activity_dataframe)
    analysis.display_commute_statistics(activity_dataframe)

    if args.export_geo_data or args.export_upload_geo_data:
        # Export the geospatial data from all activities in GeoJSON
        # format
        geo.export_geo_data_file(STRAVA_GEO_DATA_FILE, activity_dataframe)

        if args.export_upload_geo_data:
            # Upload the geospatial data to HERE XYZ
            here_xyz.upload_geo_data(STRAVA_GEO_DATA_FILE)

    if args.activity_count_plot:
        # Generate and display a plot of activity counts over time
        analysis.display_activity_count_plot(activity_dataframe)

    if args.commute_plots:
        # Generate and display plots of the commute data
        analysis.display_commute_plots(activity_dataframe)

    if args.mean_distance_plot:
        # Generate and display a plot of the mean activity distance over time
        analysis.display_mean_distance_plot(activity_dataframe)


if __name__ == "__main__":
    main()
