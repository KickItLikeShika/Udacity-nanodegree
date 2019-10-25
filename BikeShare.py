import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
monthList = ['jan', 'feb', 'mar', 'apr', 
             'may', 'jun', 'jul', 'aug', 'sep', 
             'oct', 'nov', 'dec']
dayList = ['monday', 'tuesday', 'wednesday', 'thursday', 
             'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    strTmp = ''
    for item in CITY_DATA:
        if strTmp == '': 
            strTmp += item.title() 
        else: 
            strTmp += ', ' + item.title()
            
    city = input("\nPlease select data from one of the following cities \n({})\n".format(strTmp)).lower()
    while city not in CITY_DATA:
        city = input("\nInvalid selection. " +
                     "Please select data from one of the following cities ({})\n".format(strTmp)).lower()

    #Get user input for month (all, january, february, ... , june)
    strTmp = ''
    for item in monthList:
        if strTmp == '': 
            strTmp += item.title() 
        else: 
            strTmp += ', ' + item.title()
            
    month = input("\nPlease enter one of the following options to filter by month.\n(All, {})\n".format(strTmp)).lower()
    while month not in monthList and month != 'all':
        month = input("\nInvalid selection. " +
                      "Please enter one of the following options to filter by month. " +
                      "\n(All, {})\n".format(strTmp)).lower()
            
    #Get user input for day of week (all, monday, tuesday, ... sunday)
    strTmp = ''
    for item in dayList:
        if strTmp == '': 
            strTmp += item.title() 
        else: 
            strTmp += ', ' + item.title()
            
    day = input("\nPlease enter one of the following options to filter by day.\n(All, {})\n".format(strTmp)).lower()
    while day not in dayList and day != 'all':
        day = input("\nInvalid selection. " +
                    "Please enter one of the following options to filter by day." +
                    "\n(All, {})\n".format(strTmp)).lower()

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
    
    df = pd.read_csv(CITY_DATA.get(city))

    if 'Start Time' in df.columns:
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        if month != 'all':
            df = df[df['month'] == (monthList.index(month) + 1) ]

        if day != 'all':
            df = df[df['day_of_week'] == day.title()]
    
    if 'End Time' in df.columns:
        df['End Time'] = pd.to_datetime(df['End Time'])
    
    print('\nFilter Selection:\nCity - {},  Month - {},  Day - {}'.format(city,month,day))
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month
    print('Most common month: ', monthList[df['month'].mode()[0] - 1].title())
    
    #Display the most common day of week
    print('Most common day of week: ', df['day_of_week'].mode()[0])

    #Display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print('Most common start hour: ', df['start_hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    #Display most commonly used start station
    df2 = df[df['start_hour'] == df['start_hour'].mode()[0]]
    print('Most commonly used start station: ', df2['Start Station'].mode()[0])

    #Display most commonly used end station
    print('Most commonly used end station: ', df['End Station'].mode()[0])

    #Display most frequent combination of start station and end station trip    
    strTmp = str(df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1).index[0])
    strTmp = strTmp.replace('(', '').replace(')', '').replace("'", '')
    print("Most frequent combination of start and end station: ",strTmp.strip()) 
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def seconds_to_datestamp(seconds):
    """Format seconds to days, hours, minutes, seconds"""
    
    seconds_in_day = 86400
    seconds_in_hour = 3600
    seconds_in_minute = 60
    
    days = seconds // seconds_in_day
    seconds = seconds - (days * seconds_in_day)

    hours = seconds // seconds_in_hour
    seconds = seconds - (hours * seconds_in_hour)

    minutes = seconds // seconds_in_minute
    seconds = seconds - (minutes * seconds_in_minute)
    return '{0:.0f} days, {1:.0f} hours, {2:.0f} minutes, {3:.0f} seconds'.format(days, hours, minutes, seconds)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    #Display total travel time    
    print('Total travel time: ', seconds_to_datestamp(df['Trip Duration'].sum()))
    
    #Display mean travel time
    print('Mean travel time: ', seconds_to_datestamp(df['Trip Duration'].mean()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    if 'User Type' in df.columns:
        strTmp = '\n' + df['User Type'].value_counts().to_string()
    else:
        strTmp = 'N/A'
    print('Count of user types: {}'.format(strTmp))
    
    #Display counts of gender
    if 'Gender' in df.columns:
        strTmp = '\n' + df['Gender'].value_counts().to_string()
    else:
        strTmp = 'N/A'
    print('\nCount of genders: {}'.format(strTmp))

    #Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        strTmp = int(df['Birth Year'].min())
    else:
        strTmp = 'N/A'
    print('\nEarliest birth Year: {}'.format(strTmp))
    
    if 'Birth Year' in df.columns:
        strTmp = int(df['Birth Year'].max())
    else:
        strTmp = 'N/A'
    print('\nRecent birth Year: {}'.format(strTmp))
    
    if 'Birth Year' in df.columns:
        strTmp = int(df['Birth Year'].mode()[0])
    else:
        strTmp = 'N/A'
    print('\nCommon birth year: {}'.format(strTmp))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        counter = 1
        for i,(index,row) in enumerate(df.iterrows()):
            print('\n', row)
            if counter%5 == 0:
                if input('\nWould you like to view more records? (Yes or No) ').lower() == 'no':
                    break
            elif (i == df.shape[0]):
                break
            counter += 1
            
        restart = input('\nWould you like to restart? (Yes or No) ').lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
