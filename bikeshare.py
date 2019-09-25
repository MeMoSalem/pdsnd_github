import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
months = {0:'all', 1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun' }
#months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some U.S.A bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input = input('which city you want Chicago, New York City or Washington ?\n').lower().title()
    
    while city_input:
        if city_input in CITY_DATA.keys():
            city = CITY_DATA[city_input]
            break
        else:
            city_input = input('invalid city ! please choose from {Chicago, New York City and Washington} \n').lower().title()
    
    #print(city_choice)
    
  
    # TO DO: get user input for month (all, january, february, ... , june)
    month_input = input('\nEnter "Jan", "Feb", "Mar", "Apr", "May" or "Jun" if you want to filter data by month? or "all" for all months\n').lower()
    
    while month_input:
        if month_input in months.values():
            month = month_input
            break
        else:
            month_input = input('invalid month ! please try again.... (Hint: apr)\n').lower()
            
      
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    day_input = input('\nEnter a day of week by which you want to filter data? if you want data for all days type "all"\n').lower()
            
    while day_input:
        if day_input in days:
            day = day_input
            break
        else:
            day_input = input('invalid day ! please try again ... (Hint: sunday)\n').lower()

    
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

    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    if month != 'all':
        df = df[df['month'] == dict((v,k) for k,v in months.items())[month]]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    print('The most common month is {}'.format(months[df['month'].mode()[0]].title()))
   
    # TO DO: display the most common day of week
    print('\nThe most common day of week is {}'.format(df['day_of_week'].mode()[0]))
    #print(months[df['month'].mode()[0]].title())

    # TO DO: display the most common start hour
    print('\nThe most common hour is {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most common start station is:-')
    #print(df['Start Station'].mode()[0])
    print(df['Start Station'].value_counts().head(1))
    
    # TO DO: display most commonly used end station
    print('\nThe most common end station is:-')
    #print(df['End Station'].mode()[0])
    print(df['End Station'].value_counts().head(1))

    # TO DO: display most frequent combination of start station and end station trip
    df['Combined Stations'] = (df['Start Station']) +' ---> '+ (df['End Station'])
    print('\nThe most frequent combination of start station and end station trip is:-')
    
    print(df['Combined Stations'].value_counts().head(1))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time is {} Mins'.format(df['Trip Duration'].sum()/60))

    # TO DO: display mean travel time
    print('\nMean travel time is {} Mins'.format(df['Trip Duration'].mean()/60))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User Count:-\n{}'.format(df['User Type'].value_counts()))
    
   
    
    # TO DO: Display earliest, most recent, and most common year of birth
    if(city != 'washington.csv'):
        print('\nGender Count:-\n{}'.format(df['Gender'].value_counts()))
        print('\nEarliest year of birth is {}'.format(int(df['Birth Year'].min())))
        print('\nMost recent year of birth is {}'.format(int(df['Birth Year'].max())))
        print('\nMost common year of birth {}'.format(df['Birth Year'].value_counts().head(1)))            
        
    # Giving the user the choice of looking at the raw data
    start_index = 0
    end_index = 5 
    while True:
        display_data = input('\nWould you like to see individual trip data? Enter "yes" or "no"\n')
        if display_data.lower() != 'yes':
            break 
        with pd.option_context('display.max_rows',None, 'display.max_columns',None):
            #df2 = pd.read_csv(city,nrows=end_index)
            #print(df2.iloc[start_index:end_index])
            if city != 'washington.csv':
                print('\n{}'.format(df[['Start Time','Start Station','End Time', 'End Station','Trip Duration',
                                        'User Type','Gender','Birth Year']].iloc[start_index:end_index]))    
            else:
                print('\n{}'.format(df[['Start Time','Start Station','End Time', 'End Station','Trip Duration',
                                        'User Type']].iloc[start_index:end_index]))
        start_index +=5
        end_index +=5   
    
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
