import json
import tweepy
from tweepy import Cursor
import csv
import os  # Used to show where the new files were stored.
from StreamCaptureAsList import StreamParser

# Your Twitter app authentication for Tweepy.
consumer_key = "tR1mg68SP6qSk4lpLc5kgJipI"
consumer_secret = "CWNK2PLZkqafYoMT6AIdR0vYDMazpGFVCxMppANywTPI4YVKfq"

access_token = "3063995561-OG8YNTGsEoouSdSinxycWaK4W1PlbGIN6oPk1mn"
access_token_secret = "96qKNDzkITjwvquIuxnY5l11Lm5g5eNEfSzbInfoZo7H3"

if consumer_key == '' or consumer_secret == '' or access_token == '' or access_token_secret == '':
    print("Error: Please set your Twitter app authentiction for Tweepy in the source code!")
    quit()

# Tweepy will log into the Twitter API with our credentials.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#this function will go through all the tweets collected in the csv and get information to print which user tweeted exactly what
def run(object):
    with open (object, 'r') as my_file:
        my_file_csv = csv.reader(my_file)
        headings=next(my_file_csv)
        for row in my_file_csv:
            print('User name', row[0], 'tweeted', row[1])
            print()

#this function will calculate the total status updates done by all of the twitter accounts in the queery that were collected.
# That is if account A had 50 status updates and account B had 100 then this function will show total that is 150.
def total_statuses(object):
    sum = 0
    for status in statuses:
        sum = sum+status
    print ("The total statuses among all users in this query is", sum)

#this function will calculate the total number of tweets all of the twitter accounts in the query have favourtied
def total_favourites(object):
    sum = 0
    for i in fav_count:
        sum = sum+i
    print ("The total number of tweets all the users in this query have favorited are", sum)

#this function will calculate the total number of people all the of the twitter accounts collected in the query are following
def total_following(object):
    sum = 0
    for i in following:
        sum = sum+i
    print ("The total number of people all the useers are following in this query is", sum)

#this function will calculate the total no of people that follow all of the twitter accounts collected in the query
def total_friends(object):
    sum = 0
    for i in friends_list:
        sum = sum+i
    print ("The total number of friends (people following the users) all the users has in this query is", sum)

# Filenames to use for output (they will be either ".json" or ".csv" depending on usage need).
output_historical_file = "historical_tweets"
output_livestream_file = "live_streamed_tweets"

#parameter that asks the user the maximum number of tweets to collect
while True:
    try:
        max_tweets = int(input("Maximum number of tweets to gather? "))
        break  # This exits the while-loop if there were no problems from the int() above.

    except ValueError:
        print("Error: Please only input a number.\n")

#a for loop to give users the option of either collecting historial tweets or live tweets and which word(s) to perform the query on
check = ""
while check == "":
    activity=input("Do you want to search historical tweets or live tweets?\n 1 - Historial Tweets \n 2 - Live tweets \n 3 - Quit")
    if activity == '1':
        historical_search_filter = input("What do you want to create historical search for?")
        tweets_collected = tweepy.Cursor(api.search, q= historical_search_filter).items(max_tweets)

        # Parses the historical JSON file.
        print("\nAttempting to create your historical JSON file...")
        tweets_collected_list = []  # Blank list that we'll later fill up.
        with open(output_historical_file + ".json", 'w') as json_output_file:
            for tweet in tweets_collected:
                tweets_collected_list.append(json.dumps(tweet._json))  # Corrects the line-ending problem.

            json.dump(tweets_collected_list, json_output_file)  # Finally creates the JSON file.

            print("Success! The JSON file was saved correctly.\n")

            # Cross-platform way to show where the file was stored on the disk.
            print("File Name:", output_historical_file + ".json")
            print("Full Path: {}".format(os.path.join(os.getcwd(), output_historical_file + ".json")))

        files_to_convert = [
            output_historical_file
        ]

        # Loops according to how many files we need to convert.
        for i in range(0, len(files_to_convert)):

            print("Input File: {}".format(files_to_convert[i] + ".json"))

            with open(files_to_convert[i] + ".csv", 'w', newline='', encoding='utf-8') as csvfile:
                tweetwriter = csv.writer(csvfile)
                tweetwriter.writerow(["Twitter_Username", "Tweet_Text", "Language", "Location", "No. of favourties", "No. of statuses", "No. of people follwoing", "No. of friends"])

                with open(files_to_convert[i] + ".json", 'r') as json_file:
                    # Reads the entire JSON content, which can be one or more tweets.
                    # Notice how it is json.load() and not json.loads() [with an 's']
                    json_data = json.load(json_file)


                    fav_count=[] #empty to list to count the total number of tweets all the accounts in the query have favorited
                    statuses=[] #empty to list to count the total number of status updated by all the accounts in the query
                    following=[] #empty to list to count the total number of followers all the accounts in the query have
                    friends_list=[] #empty to list to count the total number of people that are following all the accounts in the query

                    # Each tweet is stored as a JSON-like string, such as: json_data[0]
                    for one_element in json_data:
                        # But, we need to reload even the json_data[0] again via json.loads() [notice the 's' on .loads()]
                        # The difference between .load() and .loads() is that .loads() is for ONE string, not an entire file.
                        tweet = json.loads(one_element)

                        # The Twitter data fields we care about.
                        name = tweet['user']['screen_name']
                        username = tweet['user']['screen_name']
                        tweet_text = tweet['text']
                        language = tweet['user']['lang']
                        place = tweet['user']['location']
                        favourties_count = tweet['user']['favourites_count']
                        statuses_count = tweet['user']['statuses_count']
                        followers_count = tweet['user']['followers_count']
                        friends_count = tweet['user']['friends_count']

                        fav_count.append(favourties_count)
                        statuses.append(statuses_count)
                        following.append(followers_count)
                        friends_list.append(friends_count)

                        # Removes newline characters from the tweet_text to avoid accidentally creating new CSV rows in the wrong places.
                        tweet_text = tweet_text.replace("\n", " ")

                        # Writes the data fields to the CSV file.
                        tweetwriter.writerow([name, tweet_text, language, place, favourties_count, statuses_count, followers_count, friends_count])

                # print(tweets)

            print("Success! The CSV file was saved correctly.")

            # Cross-platform way to show where the file was stored on the disk.
            print("File Name:", files_to_convert[i] + ".csv")
            print("Full Path: {}\n".format(os.path.join(os.getcwd(), files_to_convert[i] + ".csv")))

            #calling all the functions defined above
            run('historical_tweets.csv')
            total_statuses('historical_tweets.csv')
            total_favourites('historial_tweets_csv')
            total_following('historical_tweets_csv')
            total_friends('historical_tweets_csv')

            print()


    elif activity =='2':

        #this will ask the user to create a time limit i.e. how many seconds should the function run before discarding it
        max_seconds = int(input("How long (in seconds) would you want to check for the data?"))
        print("Note: Maximum time the live stream query will last is: {} seconds.\n".format(max_seconds))

        print()  # Blank line for whitespace.

        # We'll send a blank List to the StreamParser to fill up with tweets!
        tweets_list = []
        listener = StreamParser(tweets_list, max_tweets, max_seconds)
        stream = tweepy.Stream(auth, listener)

        # This line will filter Twitter streams to capture data by the keywords, which can be a List.

        print(stream.filter(track=livestream_search_filter))

        with open(output_livestream_file + ".json", 'w') as json_output_file:
            # Writes all of the tweets that were stored in the List (from StreamParser) as a proper JSON file.
            json.dump(tweets_list, json_output_file)

        print("Success! The JSON file was saved correctly.\n")

        # Cross-platform way to show where the file was stored on the disk.
        print("File Name:", output_livestream_file + ".json")
        print("Full Path: {}".format(os.path.join(os.getcwd(), output_livestream_file + ".json")))

        files_to_convert1 = [
            output_livestream_file
        ]

        # Loops according to how many files we need to convert.
        for i in range(0, len(files_to_convert1)):

            print("Input File: {}".format(files_to_convert1[i] + ".json"))

            with open(files_to_convert1[i] + ".csv", 'w', newline='', encoding='utf-8') as csvfile:
                tweetwriter = csv.writer(csvfile)
                tweetwriter.writerow(["Twitter_Username", "Tweet_Text", "Language", "Location", "No. of favourties", "No. of statuses", "No. of people follwoing", "No. of friends"])

                with open(files_to_convert1[i] + ".json", 'r') as json_file:
                    # Reads the entire JSON content, which can be one or more tweets.
                    # Notice how it is json.load() and not json.loads() [with an 's']
                    json_data = json.load(json_file)

                    fav_count = [] #empty to list to count the total number of tweets all the accounts in the query have favorited
                    statuses = [] #empty to list to count the total number of status updated by all the accounts in the query
                    following = [] #empty to list to count the total number of followers all the accounts in the query have
                    friends_list = [] #empty to list to count the total number of people that are following all the accounts in the query

                        # Each tweet is stored as a JSON-like string, such as: json_data[0]
                    for one_element in json_data:
                        # But, we need to reload even the json_data[0] again via json.loads() [notice the 's' on .loads()]
                        # The difference between .load() and .loads() is that .loads() is for ONE string, not an entire file.
                        tweet = json.loads(one_element)

                        # The Twitter data fields we care about.
                        name = tweet['user']['screen_name']
                        username = tweet['user']['screen_name']
                        tweet_text = tweet['text']
                        language = tweet['user']['lang']
                        place = tweet['user']['location']
                        favourties_count = tweet['user']['favourites_count']
                        statuses_count = tweet['user']['statuses_count']
                        followers_count = tweet['user']['followers_count']
                        friends_count = tweet['user']['friends_count']

                        fav_count.append(favourties_count)
                        statuses.append(statuses_count)
                        following.append(followers_count)
                        friends_list.append(friends_count)

                        # Removes newline characters from the tweet_text to avoid accidentally creating new CSV rows in the wrong places.
                        tweet_text = tweet_text.replace("\n", " ")

                        # Writes the data fields to the CSV file.
                        tweetwriter.writerow([name, tweet_text, language, place, favourties_count, statuses_count, followers_count, friends_count])

            print("Success! The CSV file was saved correctly.")

            # Cross-platform way to show where the file was stored on the disk.
            print("File Name:", files_to_convert1[i] + ".csv")
            print("Full Path: {}\n".format(os.path.join(os.getcwd(), files_to_convert1[i] + ".csv")))

            run('live_streamed_tweets.csv')
            total_statuses('live_streamed_tweets.csv')
            total_favourites('live_streamed_tweets.csv')
            total_following('live_streamed_tweets.csv')
            total_friends('live_streamed_tweets.csv')

            print()

    elif activity=='3':
        print("Have a nice day")
        break

    else:
        print ("Please enter '1' for Historical tweets and '2' for Live tweets")






