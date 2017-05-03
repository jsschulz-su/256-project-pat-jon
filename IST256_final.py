from tkinter import *
import tweepy
import sys

consumer_key = 'AlfLQVBsQ30vcoaey1scPkzk7' #consumer_key
consumer_secret = '5Xru2iNdY3lhxE7WzgL3UWHStQzVdZDFXppFUu8zZq1FfJBRPL' #consumer_secret
access_token = '2994712059-BxdCYDbjfkkYBnEC1uxUzOvTWC1puUckrRyyC1B' #access_token
access_token_secret = 'gjw7cxCJs5kNbWrdHnxsk6cwxi4W7huefnQXqWxXXcrga' #token_secret


class TweepyHandler: #Twitter class
    def __init__(self): #Init tweepy function, referenced from tweepy docs, prints 'Init complete' when finished
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        global api
        api = tweepy.API(auth)
        print('Init Complete')
    def get_user_tweets(self, a, b): #function getting tweets of inputted user_name
        twitter_user = a
        twitter_user_amount = b
        results = api.user_timeline(screen_name = twitter_user, count = twitter_user_amount)
        i = 0
        user_tweet_list=[]
        while (i < int(twitter_user_amount)):
            try:
                user_tweet_list.append(results[i].text.translate(non_bmp_map))
            except:
                print('Error, please enter another twitter handle!')
            i+=1
        return user_tweet_list
    def get_input_hashtag(self, d, e): #function getting tweets with inputted hashtag
        user_input_hashtag = d
        user_input_amount = e
        results = api.search(user_input_hashtag,rpp=user_input_amount)
        i = 0
        hashtag_list=[]
        while (i < int(user_input_amount)):
            try:
                hashtag_list.append(results[i].text.translate(non_bmp_map))#resolve error with utf-8 encoding
            except:
                print('Error, please enter another hashtag!')
            i+=1
        return hashtag_list
class MainProgram(object):
    masterwindow = None
    subwindow = None
    stop_prog = False
    
    twitter_username = ''
    num_of_tweets_user = 0
    twitter_hashtag = ''
    num_of_tweets_hash = 0
    
    def search_input_user(self):
        string_siu = self.a.get()
        self.twitter_username = string_siu
        
        string_siu = self.b.get()
        self.num_of_tweets_user = int(string_siu)
            

    def search_input_hashtag(self):
        string_sih = self.d.get()
        self.twitter_hashtag = string_sih
        
        string_sih = self.e.get()
        self.num_of_tweets_hash = int(string_sih)

    def close_window(self):
        self.masterwindow.destroy()
        
    def restart_prog(self):
        self.subwindow.destroy()

    def stop_prog_handler(self):
        self.stop_prog = True
        self.subwindow.destroy()
        print('quit')

    #gui window
    def init_main_window(self):
        self.masterwindow = Tk()

        self.masterwindow.title('Twitter Search')
        self.masterwindow.geometry("260x260+500+220")
        #row0
        la = Label(self.masterwindow,text='Username')
        la.grid(row=0)

        a = Entry(self.masterwindow)
        a.grid(row=0,column=1)
        a.focus_set()
        self.a = a
        #row1
        lb = Label(self.masterwindow,text='# of tweets')
        lb.grid(row=1)

        b = Entry(self.masterwindow)
        b.grid(row=1,column=1)
        self.b = b
        #row2
        c = Button(self.masterwindow,text='Save input',command=self.search_input_user)
        c.grid(row=2,column=1)
        #row3
        ld = Label(self.masterwindow,text='Hashtag')
        ld.grid(row=3)

        d = Entry(self.masterwindow)
        d.grid(row=3,column=1)
        self.d = d
        #row4
        le = Label(self.masterwindow,text='# of tweets')
        le.grid(row=4)

        e = Entry(self.masterwindow)
        e.grid(row=4,column=1)
        self.e = e
        #row5
        f = Button(self.masterwindow,text='Save input',command=self.search_input_hashtag)
        f.grid(row=5,column=1)
        #row6
        g = Button(self.masterwindow,text='Close Window & Get Results')
        g.grid(row=6)
        g['command'] = self.close_window

        self.masterwindow.mainloop()

    def init_results_window(self,formatted_str):
        self.subwindow = Tk()
        self.subwindow.title('Results Window')
        h = Text(self.subwindow)
        h.insert(INSERT,formatted_str)
        h.grid(row=0)
        h_reset = Button(self.subwindow,text='Restart')
        h_reset.grid(row=1,column=0)
        h_reset['command'] = self.restart_prog
        h_stop = Button(self.subwindow,text='Quit')
        h_stop.grid(row=1,column=1)
        h_stop['command'] = self.stop_prog_handler
        self.subwindow.mainloop()

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd) #resolve error with utf-8 encoding

#main program
def main():
    m = MainProgram()
    m.init_main_window()
    try:
        x = TweepyHandler()
        ret_val_user = x.get_user_tweets(m.twitter_username, m.num_of_tweets_user)
        #m.
        ret_val_hash = x.get_input_hashtag(m.twitter_hashtag, m.num_of_tweets_hash)

        #results formatting
        title_username = 'tweets by user'
        user_tweet_str=''
        for tweet1 in ret_val_user:
            user_tweet_str+='\n'+tweet1

        title_hashtag = 'tweets by hashtag'
        hashtag_tweet_str=''
        for tweet2 in ret_val_hash:
            hashtag_tweet_str+='\n'+tweet2

        formatted_str = title_username+user_tweet_str+'\n\n'+title_hashtag+hashtag_tweet_str
    except:
        print('That is not valid input!')
        formatted_str='That is not valid input!'
    m.init_results_window(formatted_str)
    return m

stop_prog = False
while True:
    if not stop_prog:
       m = main()
       stop_prog = m.stop_prog
       print(m.stop_prog)
    else:
        print("Quit Program")
        break







