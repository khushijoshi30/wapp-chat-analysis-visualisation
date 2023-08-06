import re
import pandas as pd
def preprocess(data):

    pattern = r'\[(\d{2}/\d{2}/\d{2}), (\d{2}:\d{2}:\d{2})\] (.+)'

    # Extract dates, times, names, and messages
    matches = re.findall(pattern, data)
    dates = [match[0] for match in matches]
    times = [match[1] for match in matches]
    names = [re.search('^(.*?):', match[2]).group(1) for match in matches]
    msgs = [re.sub('^(.*?):\s*', '', match[2]) for match in matches]

    dates = pd.to_datetime(dates)
    times = pd.to_datetime(times)
    df = pd.DataFrame({"User Name": names, "User Messages": msgs, "Message Date": dates, "Message Time": times})
    df['Year'] = df['Message Date'].dt.year
    df['Month number'] = df['Message Date'].dt.month
    df['Month name'] = df['Message Date'].dt.month_name()
    df['Day Name'] = df['Message Date'].dt.day_name()
    df['Day Number'] = df['Message Date'].dt.day
    df['Hour'] = df['Message Time'].dt.hour
    df['Minute'] = df['Message Time'].dt.minute

    period = []
    for hour in df[['Day Name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df
