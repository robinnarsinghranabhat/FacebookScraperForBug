#this scrape will scrape post TEXT and reactions for upto 24 posts in a day


#import dependencies
import json
import requests
import pandas as pd

# please continously update this  from facebook graph api ..
#go to :  https://developers.facebook.com/tools/explorer/145634995501895/
#LOG IN to facebook as said in the page
#copy the access token you get and paste below !
access_key = 'EAACEdEose0cBAF5QiCVzdOW2b1zsS2T5feSF822yoKlEykH2oQ6XOIE5X7obhNyQFwTc1nWZC61gXflWCLnPmnPzArNNTyAIWGgA8AQB6hOTJrZCNAnJx9ZCY7nCWWw49Ham5i1LVoed2EWYX9PL2vT1bAaja41MbjzotjUAZAl8Y2OW8n1FJMtEEcoKsaa9n4acWcsznAZDZD'

# this is the list of days for which you want to scrape
# the days are not in dd/mm/yy format but in unixtimestamp format
# because facebook will let you scrape just 24 post for each day , thanks to it's bug
# each number in array below is unixtimestamps value from date 08/12/2017 to 12/12/2017 (dd/mm/yy)
unixtimeStamps = [1512677592, 1512763992, 1512850392, 1512936792, 1513023192, 1513109592]


#if you just want to use the scraper , go to line 71 and read the instrucitons . don't mess with functions below

# this function scrapes reactions from a post of a page..
def makeReactionsTableFromPost(pagename, access_token=access_key):
    reactionFrames = []
    reactionString = '{reactions.type(LIKE).summary(total_count).limit(0).as(like),reactions.type(LOVE).summary(total_count).limit(0).as(love),reactions.type(WOW).summary(total_count).limit(0).as(wow),reactions.type(HAHA).summary(total_count).limit(0).as(haha),reactions.type(SAD).summary(total_count).limit(0).as(sad),reactions.type(ANGRY).summary(total_count).limit(0).as(angry)}'
    for i in unixtimeStamps:
        stringUrl = 'https://graph.facebook.com/v2.11/{}?fields=feed.until({}){}&access_token={}'.format(pagename, i,
                                                                                                         reactionString,
                                                                                                         access_token)
        r = requests.get(url=stringUrl)
        data = r.json()
        rawFrame = pd.DataFrame.from_dict(data['feed']['data'])
        words = ['like', 'love', 'haha', 'angry', 'sad', 'wow']
        for word in words:
            for i in range(len(rawFrame)):
                rawFrame[word][i] = rawFrame[word][i]['summary']['total_count']

        reactionFrames.append(rawFrame)
    return pd.concat(reactionFrames)


# gives back the pandas dataframe for list of post messages(TEXT's)

def createPostTextfromURL(pagename, access_token=access_key):
    # stores post Text
    dataframes = []
    for i in unixtimeStamps:
        # exra
        stringUrl = 'https://graph.facebook.com/v2.11/{}?fields=feed.until({})&access_token={}'.format(pagename, i,
                                                                                                       access_token)
        r = requests.get(url=stringUrl)
        data = r.json()
        # don't supply data dirictly into code below. supply data['data]['message]
        dataframes.append(pd.DataFrame.from_dict(data['feed']['data'])['message'])
    final = pd.concat(dataframes)
    return final


# returns pandas dataframe containing reactions and post Text

def getPostTextandReactions(pagename):
    pd1 = createPostTextfromURL(pagename, access_token= access_key)
    pd2 = makeReactionsTableFromPost(pagename, access_token= access_key)
    cols_to_elect = ['like', 'love', 'sad', 'haha', 'wow', 'angry', 'message']
    return pd.concat([pd1, pd2], axis=1)[cols_to_elect]



#SCRAPING PART IS HERE
#place the pagename you want to scrape data from in this code below
pagenametoscrape = 'CNN'

dataCNN = getPostTextandReactions(pagename=pagenametoscrape)


#store in csv format in computer

dataCNN.to_csv()
