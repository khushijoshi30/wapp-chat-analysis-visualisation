from urlextract import URLExtract
from wordcloud import WordCloud
import re
import pandas as pd
from collections import Counter
import emoji
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentiments = SentimentIntensityAnalyzer()

extract = URLExtract()
def fetch_stats(selected_user,df ):
    if selected_user!='Overall':
        df = df[df['User Name'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for msgs in df['User Messages']:
        words.extend(msgs.split())

    num_media_msgs = df[df['User Messages'] == 'image omitted\n'].shape[0]

    from urlextract import URLExtract

    extractor = URLExtract()
    links = []

    for msgs in df['User Messages']:
        extracted_links = extractor.find_urls(msgs)
        links.extend(extracted_links)



    return num_messages, len(words), num_media_msgs,len(links)

def most_busy_users(df):
    x = df['User Name'].value_counts().head()
    df = round((df['User Name'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'User Name': 'Percent'})
    return x, df

def create_word_cloud(selected_user, df):
    if selected_user!='Overall':
        df = df[df['User Name'] == selected_user]

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['User Messages'].str.cat(sep=" "))
    return  df_wc

def most_common_words(selected_user, df):
    stop_words_file = 'stop_hinglish.txt'

    with open(stop_words_file, 'r') as f:
        stop_words = set(f.read().splitlines())

    if selected_user != 'Overall':
        df = df[df['User Name'] == selected_user]
    temp = df[df['User Name'] != 'Unofficial Panel 2 ✅🥹']
    temp = temp[temp['User Messages'] != 'This message was deleted.']
    temp = temp[temp['User Messages'] != 'sticker omitted']
    #temp = df[df['User Name'] != 'OCR']
    #temp = temp[temp['User Messages'] != 'image omitted']

    words = []
    for msgs in temp['User Messages']:
        for word in msgs.lower().split():
            word = re.sub(r'[^A-Za-z0-9]', '', word)  # Remove special characters
            word = word.strip()  # Remove leading/trailing whitespace
            if word and word not in stop_words:  # Check if word is non-empty and not in stop words
                words.append(word)
    word_counts = Counter(words)
    top_words = word_counts.most_common(30)
    df_word_counts = pd.DataFrame(top_words, columns=['Word', 'Count'])
    return df_word_counts

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User Name'] == selected_user]

    emojis = []
    for msgs in df['User Messages']:
        emojis.extend([c for c in msgs if emoji.is_emoji(c)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User Name'] == selected_user]
    timeline = df.groupby(['Year', 'Month number', 'Month name']).count()['User Messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month name'][i] + "-" + str(timeline['Year'][i]))
    timeline['time'] = time

    return timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User Name'] == selected_user]
    return df['Day Name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User Name'] == selected_user]
    return df['Month name'].value_counts()

def activity_heat_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User Name'] == selected_user]
    activity_hmap = df.pivot_table(index='Day Name',columns='period',values='User Messages',aggfunc='count').fillna(0)
    return activity_hmap

def sentiment_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User Name'] == selected_user]
    data123=df.dropna()
    data123 = data123[data123['User Name'] != 'Unofficial Panel 2 ✅🥹']
    data123.loc[:, "positive"] = [sentiments.polarity_scores(i)["pos"] for i in data123["User Messages"]]
    data123.loc[:, "negative"] = [sentiments.polarity_scores(i)["neg"] for i in data123["User Messages"]]
    data123.loc[:, "neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data123["User Messages"]]
    x = sum(data123["positive"])
    y = sum(data123["negative"])
    z = sum(data123["neutral"])

    return x,y,z




