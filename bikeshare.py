import time
import pandas as pd
import numpy as np
import traceback
import matplotlib.pyplot as plt

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    time.sleep(1)
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:

        city = input('What City would you like to explore?[Chicago, New York City, Washington] ').title()

        month = input('What Month would you like to explore?[January,February,March ... or All] ').capitalize()

        day = input('What Day of the week would you like to explore? [Monday, Tuesday ... or All] ').capitalize()

        if month == "All" and day != 'All':
            print('You are about to analyze data from {} on every {} for all months'.format(city,day))
        elif month != 'All' and day =='All':
            print('You are about to analyze data from {} for all days in the month of {}'.format(city, month))
        else :
            print('You are about to analyze data from {} on every {} in the month of {}'.format(city,day,month))

        time.sleep(1)

        while True:
            mistakes = input("Is this correct? ['Yes','No']")
            if mistakes.lower() == 'yes':
                print('-'*40)
                return city, month, day
            elif mistakes.lower() == 'no':
                break
            else:
                print("\nI don't know how to interpret {} I'll ask again (please type 'yes or 'no')".format(mistakes))
                continue




def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour
    df['end_hour'] = df['End Time'].dt.hour

    #print(df.head())
    # filter by month if applicable
    if month != 'All':

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()

    # TO DO: display the most common start hour
    common_start_hour = df['start_hour'].mode()

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

    print("\nThe most common month: {}".format(common_month[0]))
    print("\nThe most common day of the week: {}".format(common_day[0]))

    if common_start_hour[0] > 12 :
        print("\nThe most common hour to start a trip: {} PM".format(common_start_hour[0] - 12 ))
        print('-'*40)
        return
    print("\nThe most common hour to start a trip:  {} AM".format(common_start_hour[0]))
    print('-'*40)
    return

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()

    # TO DO: display most frequent combination of start station and end station trip
    df['combo'] = df['Start Station'] + ", " + df['End Station']
    station_combo = df['combo'].mode()[0]


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    print("\nThe most common starting station: {}".format(common_start_station[0]))
    print("\nThe most common ending station: {}".format(common_end_station[0]))
    print("\nThe most common station combination 'Start, End': {}".format(station_combo))
    print('-'*40)
    return

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()/3600

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    print("\nThe total trip time for the period: {} hours".format(total_travel_time))
    print("\nThe mean trip time for the period specified: {} minutes".format(mean_travel_time))
    print('-'*40)
    return

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # TO DO: Display counts of user types
    num_subs = df['User Type'].value_counts()['Subscriber']
    num_customers = df['User Type'].value_counts()['Customer']

    # TO DO: Display earliest, most recent, and most common year of birth
    oldest_patron = int(df['Birth Year'].min())

    youngest_patron = int(df['Birth Year'].max())

    mean_patron = int(df['Birth Year'].mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    # TO DO: Display counts of gender
    print("\nThe number of Subscribers that rode: {}".format(num_subs))
    print("\nThe number of Customers that rode: {}".format(num_customers))
    print("\nThe oldest patron has a stated Birth Year : {}".format(oldest_patron))
    print("\nThe youngest patron has a stated Birth Year : {}".format(youngest_patron))
    print("\nThe mean stated Birth year for all patron during this period : {}".format(mean_patron))
    print('-'*40)

def sample(df):
    """User input Yes or No

    Prints 5 rows of data as long as the user keeps inputing yes"""
    a=0
    b=5
    while True:
        try:
            sample = input("\n Would you like to see a sample of your selection ['Yes' or 'No']").lower()
            if sample == 'yes':
                print(df.iloc[a:b])
                a += 5
                b += 5
                continue
            if sample == 'no':
                return
        except Exception as e:
            print("An unexpected {} error occured".format(Exception,e))
            traceback.print_exc()

def plots(df):
    while True:
        viz = input("\nWould you like to see a distribution of start times for users? ['Yes','No']")
        try :
            if viz.lower() == 'yes':
                (df.hist(column='start_hour')

                return
        except Exception as e:
            print("An unexpected {} error occured".format(Exception,e))
            traceback.print_exc()


def main():
    """ Main program to execute the functions defined above"""
    # Promt user to filter the data by month, day, or not at all?

    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            plots(df)
            sample(df)
            time_stats(df)
            time.sleep(2.25)
            station_stats(df)
            time.sleep(2.5)
            trip_duration_stats(df)
            time.sleep(2.75)
            user_stats(df)

        except Exception as e:
            print("An unexpected {} error occured".format(Exception,e))
            traceback.print_exc()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
