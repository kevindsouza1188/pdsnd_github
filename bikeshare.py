import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_flag = True

    while city_flag:
        try:
            city = input("\nEnter the city you want to analyze the bikeshare data for (valid options are chicago, new york city and washington): ").lower()
            if CITY_DATA[city]:
                print("\nYou have entered the correct city name: {}\n-----\n".format(city))
                city_flag=False
        except Exception:
            print("\nYou have entered wrong city name. Please enter a valid city name from the list.\n-----\n")          
               

    # Get user input for month (all, january, february, ... , june)
    month_flag = True            # Set the month flag boolean variable to True

    months=['january','february','march','april','may','june','july','august','september','october','november','december','all']			# Valid list of entries for month

    while month_flag:            # While loop to ensure that the user enters the correct month name or all
        try:
            month = input("\nEnter the month you want to analyze the bikeshare data for (valid options are january,february,march,april,may,june,all): ").lower()  # Check for correct month name (or all) and convert to lower to match the months list
            if months.index(month)+1:         # If the month name exists in the months list, set flag to False and continue with the execution              
                print("\nYou have entered the correct month name: {}\n-----\n".format(month))
                month_flag=False
        except Exception:               # If the month doesn't exist in the list, the if statement will throw a ValueError. When the exception is raised print a friendly message to the user to enter the correct month name from the list
            print("\nYou have entered wrong month. Please enter a valid month from the list.\n-----\n")   

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week_flag = True            # Set the day_of_week flag boolean variable to True

    days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']			# Valid list of entries for days

    while day_of_week_flag:            # While loop to ensure that the user enters the correct day name or all
        try:
            day = input("\nEnter the day of the week you want to analyze the bikeshare data for (valid options are monday,tuesday,wednesday,thursday,friday,saturday,sunday,all): ").lower() # Check for correct day of the week name (or all) and convert to lower to match the days list
            if days.index(day)+1:         # If the day name exists in the days list, set flag to False and continue with the execution              
                print("\nYou have entered the correct day name: {}\n-----\n".format(day))
                day_of_week_flag=False
        except Exception:               # If the day doesn't exist in the list, the if statement will throw a ValueError. When the exception is raised print a friendly message to the user to enter the correct day name from the list
            print("\nYou have entered wrong day of the week. Please enter a valid day of the week from the list.\n-----\n")   
    

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
    df = pd.read_csv(CITY_DATA[city], index_col=0)           # Load data for the user provided city

    # Replace missing values in the dataset if the column exsits
    if 'Birth Year' in df: 
        df['Birth Year'].fillna(value=df['Birth Year'].mode().astype(int).tolist()[0], inplace=True)        # Replace empty cells for Birth Year with the mode value across the column 
    if 'Gender' in df:
        df['Gender'].fillna('Unknown', inplace=True)                                                        # Replace empty cells for Gender with Unknown to avoid skewing the data in either direction 'M' or 'F'
    
    df['User Type'].fillna('Unknown', inplace=True)                                                     # Replace empty cells for User Type with Unknown to avoid skewing the data for any of the existing values
    
    # Fetch month and day of the week from Start Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # Filter by month if a specific month is provided
    if month != 'all':                          
        months=['january','february','march','april','may','june']            # Months list
        month = months.index(month)+1
        df = df[df['month']==month]             # Filter the dataframe for the specified month
    
    # Filter by day of the week if a specific day is provided
    if day != 'all':                            
        df = df[df['day_of_week']==day.title()]     # Filter the dataframe for the specified day
           
    return df






def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Create the months list for displaying the monthname to the end user
    months=['January','February','March','April','May','June','July','August','September','October','November','December']
    
    # Display the most common month
    most_common_month = df['month'].value_counts(sort=True, ascending=False).keys().tolist()[0]
    print("Most common month is:",months[most_common_month-1])

    # Display the most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts(sort=True, ascending=False).keys().tolist()[0]
    print("Most common day of the week is:",most_common_day_of_week)

    # Display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.value_counts(sort=True, ascending=False).keys().tolist()[0]
    print("Most common start hour is:",most_common_start_hour)

    # Display the most common end hour
    most_common_end_hour = pd.to_datetime(df['End Time']).dt.hour.value_counts(sort=True, ascending=False).keys().tolist()[0]
    print("Most common end hour is:",most_common_end_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    
    
    
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        df - dataframe to compute time statistics on
    Returns:
        Nothing. Displays the output to the console."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station=df['Start Station'].value_counts(sort=True, ascending=False).keys().tolist()[0]
    print("Most common start station is:",most_common_start_station)

    # Display most commonly used end station
    most_common_end_station=df['End Station'].value_counts(sort=True, ascending=False).keys().tolist()[0]
    print("Most common end station is:",most_common_end_station)

    # Display most frequent combination of start station and end station trip
    most_common_start_and_end_combination=df.groupby(['Start Station','End Station'], axis=0)['Start Station','End Station'].size().reset_index().max().tolist()
    print("Most common start station is '{}' and end station '{}' with {} trips".format(most_common_start_and_end_combination[0],most_common_start_and_end_combination[1],most_common_start_and_end_combination[2]))    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    
    
    
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print("Total travel time across all trips is {} seconds or approximately {} days".format(total_travel_time,total_travel_time/60/60/24))

    # Display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print("Mean travel time across all trips is {} seconds or approximately {} hours".format(mean_travel_time,mean_travel_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    
    
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type=df['User Type'].value_counts()
    print("Types of users:\n {}\n".format(user_type))

    # Display counts of gender if gender column exists
    if 'Gender' in df:
        gender=df['Gender'].value_counts()
        print("Gender breakdown:\n {}\n".format(gender))


    # Display earliest, most recent, and most common year of birth if Birth Year column exists
    if 'Birth Year' in df:
        earliest_birth_year=df['Birth Year'].astype(int).min()                                      # Get the earliest birth year aka the oldest rider
        latest_birth_year=df['Birth Year'].astype(int).max()                                        # Get the latest birth year aka the youngest rider
        most_common_birth_year=df['Birth Year'].astype(int).mode().tolist()[0]                      # Get the most common birth year 
        print("The earliest birth year of a rider is {}\n".format(earliest_birth_year))
        print("The most recent birth year of a rider is {}\n".format(latest_birth_year))
        print("The most common year of birth is {}\n".format(most_common_birth_year))
        
        # Group the users into bins based on their age
        df['Current Age']=int(time.strftime("%Y")) - df['Birth Year']                               # Get the present age of the rider
        labels = ["{0} - {1}".format(i, i + 9) for i in range(0, 150, 10)]                          # Create labels for the bins
        df['Age Group'] = pd.cut(df['Current Age'], range(0, 160, 10), right=False, labels=labels)  # Use the labels on the Current Age column to assign the appropriate bin
        print("The Age Group breakdown for all users is as follows:\n{}".format(df['Age Group'].value_counts(sort=True,ascending=False)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
    
    
    
    
def get_raw_data(df):
    """
    Check if user wishes to look at 5 lines of raw data.
    Returns the 5 lines of raw data if user inputs 'yes'. Iterate until user responds with a 'no'.

    """
    line = 0

    while True:
        response = input('Do you want to see 5 lines of the raw data that will be used to display the descriptive statistics? Enter yes or no: ')
        if response.lower() == 'yes':
            print(df[line : line+5])
            line += 5
        else:
            break    
    
    
    
    

def main():
    while True:        
        city, month, day = get_filters()
        df = load_data(city, month, day)
        get_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


            
            
            
            
if __name__ == "__main__":
	main()
