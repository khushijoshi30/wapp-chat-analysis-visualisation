import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    #fetch unique users
    user_list = df['User Name'].unique().tolist()
    user_list.remove('Unofficial Panel 2 ✅🥹')
    #user_list.remove('OCR')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt ",user_list)

    if st.sidebar.button("Show analysis"):
        num_messages, words, num_media_msgs,num_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media ")
            st.title(num_media_msgs)
        with col4:
            st.header("Total   Links")
            st.title(num_links)

#timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'], timeline['User Messages'],color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

#activity map
        st.title("Activity Map")
        col1, col2= st.columns(2)

        with col1:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        activity_hmap = helper.activity_heat_map(selected_user, df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(activity_hmap)
        st.title("Most Busy Time")
        st.pyplot(fig)

#sentiment analysis
        x,y,z=helper.sentiment_analysis(selected_user, df)
        fig, ax = plt.subplots()
        labels1 = ["Positive", "Negative", "Neutral"]
        sizes = [x, y, z]
        ax.pie(sizes, labels=labels1)
        ax.axis('equal')
        st.title("Sentiment Analysis")
        st.pyplot(fig)


#most busy users
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        st.title("WordCloud")
        df_wc = helper.create_word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

#most common words
    df_word_counts = helper.most_common_words(selected_user,df)

    fig, ax = plt.subplots()
    ax.barh(df_word_counts['Word'], df_word_counts['Count'],color='green')
    plt.xticks(rotation='vertical')
    st.title("Most Common Words")
    st.pyplot(fig)
    #st.dataframe(df_word_counts)

#emoji analysis
    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")
    col1,col2=st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(),autopct='%0.2f')
        ax.axis('equal')
        st.title("Top 5 Emojis")
        st.pyplot(fig)

