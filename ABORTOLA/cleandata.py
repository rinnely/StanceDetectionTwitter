import re
import pandas as pd

def getUrls(text):
    find = re.findall(r'(http\S+|pic\S+)', text)
    return find

def replaceUrls(text, r):
    urls = getUrls(text)
    if urls:
        for url in urls:
            text = text.replace(url,r)
    text = re.sub(r'\s+',' ',text)
    text = re.sub(r'[\s]*$','',text)
    return text

def getHashtags(text):
    find = re.findall(r'#\w*',text)
    
    return [re.sub('http\w*|pic\w*', '', find[i]) for i in range(len(find))]

def removeLastHT(text):
    hastags = getHashtags(text)
    for hs in hastags[::-1]:
        if re.findall(r'[.?\-",|\W|\b\w*]*\s*'+hs+'\s*(URL|"pic|pic|$|http|\W+$)',text):
            text = text.replace(hs, ' ')
    text = re.sub(r'\s+',' ',text)
    text = re.sub(r'[\s]*$','',text)
    
    return text

def removeEmoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = re.sub(r'\s+',' ',text)
    text = re.sub(r'[\s]*$','',text)

    return text

def replaceUsers(text,r):
    text = re.sub(r'[@]\w*',r,text)
    text = re.sub(r'\s+',' ',text)
    text = re.sub(r'[\s]*$','',text)
    return text

def cleanData(df, label, hashtags=False, urls=None, emojis=False, users=None):
    '''
        df:= Dataframe con los tweets
        hashtags:= True si se desea elminar los ultimos
        ulrs:= reemplaza las url por un string especificado
        emojis:= elimina los emojis si es True
        users:= reemplaza los usuarios por un string especificado
    '''
    for i, row in df.iterrows():
        text = row[label]
        if emojis:
            text = removeEmoji(text)
            
        if urls or urls=='':
            text = replaceUrls(text, urls)

        if hashtags:
            text = removeLastHT(text)
        if users or  users=='':
            text = replaceUsers(text,users)
        
        df.loc[i, label] = text
        
    return df.replace('\n',' ', regex=True)