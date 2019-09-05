class TweetInfo:
    def __init__(self, time, user_name, message):
        self.__time = time
        self.__use_name = user_name
        self.__message = message


    def to_string(self):
        string = "{0}\n{1}\n{2}\n\n".format(self.__use_name, self.__time, self.__message)
        return string

