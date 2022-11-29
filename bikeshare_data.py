from calendar import WEDNESDAY
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# a list of the cities, months and days for refrence
CITICES = ['chicago', 'new york city', 'washington']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # check if the user input is correct and ask them to try again.
    while True:
        city = input("Would you like to see data for chicago, new york ciry or washington? ").lower()
        if city not in CITICES:
             print("oops seems like you entered the wrong city! \nlets try again")
        else:
            break;

    #  get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to filter for? type 'all' to fillter by all months: ").lower()
        if month not in MONTHS:
             print("oops seems like you entered the wrong month! \nlets try again")
        else:
            break;

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day of the week would you like to filter for? type 'all' to fillter by all days: ").lower()
        if day not in DAYS:
             print("oops seems like you entered the wrong day! \nlets try again")
        else:
            break;


    print('-'*40)
    return city, month, day


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

    # load data into a pandas dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # get the month and day of week to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month and check if the fillter is applicable
    if month != 'all':
        # get the integer that represents the month from list of MONTHS
        month = MONTHS.index(month) + 1

        # create the new filtered dataframe
        df = df[month == df['month']]

    # filter by day of week and check if the fillter is applicable
    if day != 'all':
        # create the new filtered dataframe
        df = df[day.title() == df['day_of_week']]
           
    # return a refrence to the dataframe      
    return df

def convert_to_12h(hour):
    '''Takes 24H time and conver it to 12H time to ease readability
        retruns a string of the converted hour'''

    # handle 00 and 12 hour first
    if hour == 0:
        return '12 AM'
    elif hour == 12:
        return '12 PM'
    # convert from 24h to 12h 
    else:
        if hour < 12:
            return f'{hour} AM'
        else:
            return f'{hour - 12} PM'


def time_stats(df, day, month):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # check if user is filltring by all months, if not this stat is not important
    if(month == 'all'):
        # get the most common month from the data frame
        common_month = df['month'].mode()[0]
        # display the most common month
        print(f"The most common month to travel is: {MONTHS[common_month - 1]}")

    # check if user is filltring by all days, if not this stat is not important
    if(day == 'all'):
        #get the most common day of the week in data frame
        common_DOE = df['day_of_week'].mode()[0]
        # display the most common day of week
        print(f"The most common day of the week to travel is: {common_DOE}")

        # display the least common day of the week
        least_common_DOE = df['day_of_week'].value_counts().index[-1]
        print(f"The least common day of the week to travel is: {least_common_DOE}")

    # create a new column 'hour' in the data frame
    df['hour'] = df['Start Time'].dt.hour
    # get the most common hour from the 'hour' column
    common_hour = df['hour'].mode()[0]
    # display the most common start hour
    print(f"The most common start hour to travel is: {convert_to_12h(common_hour)}")

    # display the least common start hour
    least_common_hour = df['hour'].value_counts().index[-1]
    print(f"The least common start hour to travel is {convert_to_12h(least_common_hour)}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # get the most common start station form the data frame
    common_start_station = df['Start Station'].value_counts().idxmax()
    # display most commonly used start station
    print(f"The most common start station is: {common_start_station}")


    # get the most common end station form the data frame
    common_end_station = df['End Station'].value_counts().idxmax()
    # display most commonly used end station
    print(f"The most common end station is: {common_end_station}")

    # display most frequent combination of start station and end station trip
    common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print(f"Most frequent combination of start and end station trips are: {common_start_end_station[0]} and {common_start_end_station[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print(f"The total time traveled in bikeshare is: {total_time}")


    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print(f"The mean travel time in bikeshare is: {mean_time}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print(f"There are {len(user_types)} user types:")
        for i in range(len(user_types)):
            count = user_types[i]
            user_type = user_types.index[i]
            print(f"{user_type}s : {count}")
    except KeyError:
        print("Sorry seems like user types are not availabe for applied filter!")
    

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print("Gender counts are as follows:")
        for i in range(len(gender_counts)):
            count = gender_counts[i]
            gender = gender_counts.index[i]
            print(f"{gender}s : {count}")
    except KeyError:
        print("\nSorry seems like gender is not availabe for applied filter!")


    # Display earliest, most recent, and most common year of birth
    try:
        earliest_DOB = df['Birth Year'].min()
        recent_DOB = df['Birth Year'].max()
        common_DOB = df['Birth Year'].mode()[0]
        print("Date of birth stats are as follows:")
        print(f"Earlies date of birth: {earliest_DOB}\nMost recent date of birth: {recent_DOB}\n"+
        f"Most common date of birth: {common_DOB}")
    except KeyError:
        print("\nSorry seems like date of birth is not availabe for applied filter!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    print('\n+=============/\=======================================================+\n'+
'|            /  \         /\       /\                     -            |\n'+
'|           /    \      _/  \/\   /  \ /\                / \           |\n'+
'|          /      \  _-~       \_/    \  \    _   /\    /   \          |\n'+
'|         /        \/         _           \  / \_/  \  /     \         |\n'+
'|  Bike Share Data    ____ __ __o       __  ,__o     \/       \        |\n'+
'| Welcome abroad         ___ -\<,      __ _-\_<,               \       |\n'+
'|____________________________O/_O________(*)/\'(*)______________________|\n'+
'========================================================================\n')

    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # ask user if they want to view 5 rows of data
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
        start_loc = 0
        while (view_data == 'yes'):
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_data = input("Do you wish to continue?: ").lower()

        time_stats(df, day, month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thank you for using BikeShare data, goodbye ;)")
            break


if __name__ == "__main__":
	main()
