from speed_bot_class import InternetSpeed


def main():
    user = input("Twitter User: ")
    password = input("Twitter Password: ")
    chromedriver_path = "/Users/karlmarx/Documents/development/chromedriver"
    internet_speed_bot = InternetSpeed(chromedriver_path=chromedriver_path)
    internet_speed_bot.send_tweet(twitter_user=user, twitter_password=password)

if __name__ == "__main__":
    main()
