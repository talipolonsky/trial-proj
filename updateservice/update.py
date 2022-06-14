import subprocess, sys
from django.shortcuts import render
from plus500.models import Plus500
import requests
from urllib.parse import urlparse
import translators as ts
import cloudscraper
from bs4 import BeautifulSoup
#for reaching contact details from a website
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
# for text pre-processing
import re
import string
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
# for model-building
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
# bag of words
from sklearn.feature_extraction.text import TfidfVectorizer

def get_contact(url):
    if "blog" in url:
        return "The website is a blog"
    if "article" in url:
        return "The website is a blog"
    # a queue of urls to be crawled
    new_urls = deque([url])

    # a set of urls that we have already crawled
    processed_urls = set()

    # a set of crawled emails
    emails = set()

    # process urls one by one until we exhaust the queue
    while len(new_urls):
        # move next url from the queue to the set of processed urls
        url = new_urls.popleft()
        processed_urls.add(url)

        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        # get url's content
        #print("Processing %s" % url)
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # ignore pages with errors
            continue

        # extract all email addresses and add them into the resulting set
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)

        # create a beutiful soup for the html document
        soup = BeautifulSoup(response.text, 'lxml')

        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        # resolve relative links
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link
        # add the new url to the queue if it was not enqueued nor processed yet
        if not link in new_urls and not link in processed_urls:
            new_urls.append(link)
    new = str(emails)
    if len(emails) ==0:
        return "No emails were found"
    else:
        return new



def train():
    global lr
    global vectorizer
        # Creating train set
    dict_train = {
        'text': ['Search This Blog', 'nSearch This Blog', 'blog', 'posts', ' Posts ', 'Posts', 'Popular posts from this blog', 'Alexa Top Sites', 'commodities', 'goods',
                 'raw materials', 'oil', 'metal', 'barrel', 'gold', 'Commodity prices', 'silver', 'commodities trading', 'trade commodities',
                 'Commodity news',
                 'Commodities Exchange', 'Gas', 'energy', 'agricultural', 'Gasoline', 'Crude Oil', 'Import', 'export', 'Brent', 'oil price',
                 'gold price',
                 'bitcoin', 'crypto.com', 'Cryptocurrency', 'Digital', 'Mining', 'cryptocurrency news', 'Cryptocurrencies',
                 'Cryptocurrency Exchange to Buy Bitcoin and Ether | Gemini Gemini is a regulated cryptocurrency exchange, wallet, and custodian that makes it simple and secure to buy bitcoin, ether, and other cryptocurrencies. Sign up for Gemini and get $7 in ETH Earn Up to 8.05% APY. The premier',
                 'Crypto News',
                 'Coindoo - Latest Cryptocurrency Prices & Articles Latest Cryptocurrency Prices & Articles  Latest Cryptocurrency Prices & Articles',
                 'World news about cryptocurrency and blockchain technology from different sources Crypto News is a platform with most important news, articles and other content about cryptocurrencies and blockchain today. We provide forecasts, analytics and more. All news  News. About us. Editori',
                 'Cryptocurrency, Blockchain And NFT News Portal - E-Crypto News E-Crypto News was developed to assist all Cryptocurrency, Blockchain and Technology followers to learn about the creators of all of these new technologies.  Privacy settings Arran Stewart of Job.com Explains Technolog',
                 'Blockchain', 'E-Crypto', 'NFT', 'cryptocurrency guides', 'cryptocurrency industry', 'cryptocurrency exchange', 'ether',
                 'Cryptocurrency Prices',
                 'investments', 'trading', 'Online Stock', 'online broker', 'Market trading', 'CFD',
                 'finance news of wild Investing and hope all is ok.',
                 'finance', 'Attention Required! etoro.com', 'Finance', 'Trading', 'Trade', 'trade', 'Stock', 'Investing', 'broker', 'financial decisions', 'stock trading',
                 'Commission-free Stock', 'Brokerage', 'financial information', 'finance advice',
                 "Globes of Israel's business arena \n  Business and financial information is updated in a variety of topics: the Tel Aviv Stock Exchange, Wall Street and world markets, insurance and finance, high -tech, consumer, sentence, sports, environment and other new management tools :. What interests you. Whenever you read you. . . 4% with asterisk: What is the real inflation rate in Israel?",
                 'financial news', 'Stock Market News',
                 'Start Entrepreneur Online - Starting Home Business Dummies Start entrepreneur online is dedicated to creating better information and guides for new or old entrepreneurs. Entrepreneur! enjoy the online business world! Best advice Start Entrepreneur Online, just when you need it! s',
                 'MarketWatch: Stock Market News - Financial News - MarketWatch MarketWatch provides the latest stock market, financial and business news. Get stock market quotes, personal finance advice, company news and more. \nMarketWatch Logo\nGo to the homepage.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n \nLATEST PODCAS',
                 'Exchange Rates', 'Currency Converter', 'Foreign exchange', 'forex', 'Forex', 'Foreign Currency Exchange', 'X-Rates',
                 'Foreign Exchange Rates',
                 'Xe Currency', 'dollar', 'euro', 'Dollars',
                 'Learn How To Trade Forex • Best Forex Trading Course • AFM Learn How to Trade Forex from a Professional Forex Trader who makes 6 figures a trade. The Best Forex Trading Course 2021 - by Investopedia. We train banks. Singapore, United States, United Kingdom, Europe. Who am I?. SO',
                 'Forex Signals - Best Forex Trading Signals and Strategies Join the biggest forex trading community and learn proven strategies from experienced mentors. Best forex signals, live streams and education. Try for free. Forex trading signals alone are not enough Over 83,000 Forex trad',
                 'The Forex Trading Coach | Online Trading Course The Forex Trading Coach by Andrew Mitchem, from a dairy farmer to a successful forex trader will share his success stories in forex trading. Want to break free of your 9-5 and achieve financial freedom?. Here’s what some of our 3500',
                 'Trade Forex', 'Forex Trading', 'Forex Trader', 'Forex Trading Signals', 'Forex Signals', 'Foreign Exchange Market', 'Forex Brokers',
                 'Trade Forex', 'Betting', 'Betting Sport', 'Bet', 'Casino',
                 'Mail Order Brides 2022: Answers To All Questions About Foreign Wives Looking for a mail order brides or foreign woman for marriage, but don’t know where to start? Here, you can find everything you need about how to find a foreign bride. All about best nationalities to marry, best',
                 'Minimalist wooden house ', 'Shobet', 'Chat Rooms', 'love chat mobile chat sites', 'My Love Home Chat', 'Chat',
                 'love chat mobile chat sites',
                 'love', 'University', 'UHAMKA', 'Graduation', 'rebelmouse',
                 '7 Reasons Why RebelMouse Is Better Than WordPress in 2022 - RebelMouse Understand why RebelMouse is the best CMS in 2022. \n\n        7 Reasons Why RebelMouse Is Better Than WordPress in 2022\n    \n. \n\n        RebelMouse Q1 2021 Platform Updates\n    \n. \n\n        The RebelMouse Appro',
                 'Welcome to Ranking Web of Universities: Webometrics ranks 30000 institutions | Ranking Web of Universities: Webometrics ranks 30000 institutions   Search form. title. \nNew edition: January 2022 . \nTRANSPARENT RANKING: Top Universities by Citations in Top Google Scholar profiles .',
                 'Ynet - News, Economy, Sports and Health - Regular reports from Israel and the world the leading news site in Israel from Yedioth Ahronoth. Full coverage of news from Israel and the world, sports, economics, culture, food, science and nature, everything that is happening and everything interesting in Ynet "Delicate person, a family man - who knew Noam would not imagine he was a warrior',
                 'The New York Times - Breaking News, US News, World News and Videos Live news, investigations, opinion, photos and video by the journalists of The New York Times from more than 150 countries around the world. Subscribe for coverage of U.S. and international news, politics, busines',
                 "News, sport and opinion from the Guardian's global edition | The Guardian Latest international news, sport and comment from the Guardian News, sport and opinion from the Guardian's global edition.  Welcome to Ontario  Palette styles new do not delete. Ukraine invasion. Ukraine in",
                 'UK Home | Daily Mail Online MailOnline - get the latest breaking news, showbiz & celebrity photos, sport news & rumours, viral videos and top stories from MailOnline, Daily Mail and Mail on Sunday newspapers. Home \n          Putin continues brutal assault on Azovstal steelworks:',
                 'HuffPost - Breaking News, U.S. and World News | HuffPost Read the latest headlines, news stories, and opinion from Politics, Entertainment, Life, Perspectives, and more.  Main Menu. News. Politics. Opinion. Entertainment. Life. Communities. Special Projects. HuffPost Personal. Vi',
                 'News from California, the nation and world  - Los Angeles Times The L.A. Times is a leading source of breaking news, entertainment, sports, politics, and more for Southern California and the world.    May 15, 2022.  Gunman kills 10 at Buffalo supermarket in attack called a racial',
                 'New York Post – Breaking News, Top Headlines, Photos & Videos Your source for breaking news, photos, and videos about New York, sports, business, entertainment, opinion, real estate, culture, fashion, and more.  \nBeloved security guard, ex-cop killed while firing at Buffalo shoot',
                 'Walla! - The leading site in Israel - updates around the Walla watch! - The popular site in Israel. Recent news 24/7, dozens of leading content and information channels, unlimited e -mail service, shopping and tourism services on the Walla website! Walla!. Vod. Vod. Vod. Vod. Vod. Vod. Vod. Vod. Vod. VOD Fighter Warrior who fell in activity',
                 'News, opinions, culture, sports, economics from Israel and the world | Israel today Israel today: The Newspaper Newspaper News Website. News from Israel and around the world, culture, sports, economics, lifestyle, technology, culture and more. The IDF Fighter in Jenin, the late Noam Raz, is brought to rest on Mount Herzl. Clashes between students at Tel Aviv University',
                 'BBC - Homepage Breaking news, sport, TV, radio and a whole lot more.\n        The BBC informs, educates and entertains - wherever you are, whatever your age. BBC Homepage Accessibility links. \xa0. \nNews\n. \nSport\n. \nWeekend Reads\n. London Weather. \nEditor’s Picks\n. Latest Business Ne',
                 'Latest news from the United States, Latin America and the world | CNN in Spanish the latest news of the world. News from the United States, Mexico, Colombia, Argentina, other Latin American countries and the world in CNN. International information, videos and news about politics',
                 'Spanish News - Spanish.News EPANOL NEWS \n\n The Phoenix Suns were not supposed to be pushed to game 7 \n  Editorial. Health. \n\n The Phoenix Suns were not supposed to be pushed to game 7 \n . \n\n How Hollywood and the media promoted the political rise of JD Vance \n . Deal. Fo',
                 "The mirror | Online messages Germany's leading news site. Everything important from politics, economy, sport, culture, science, technology and more. \n\n 21 injuries in Milwaukee: public viewing in the NBA can be canceled for shootings \n\n 18 min \n\n\n\n . \n\n Follow high Stromp",
                 'ZEIT ONLINE | News, backgrounds and debates Current news, comments, analyzes and background reports from politics, economy, society, knowledge, culture and sport read you online. Latest news, comments, analyzes and background reports AU',
                 'ABC News – Breaking News, Latest News, Headlines & Videos - ABC News Your trusted source for breaking news, analysis, exclusive interviews, headlines, and videos at ABCNews.com  More Top Stories. Governor seeks more US aid for wildfire response. Finland pres. to Putin: we will ap',
                 'NBC News - Breaking News & Top Stories - Latest World, US & Local News | NBC News Go to NBCNews.com for breaking news, videos, and the latest top stories in world news, business, politics, health and pop culture.  U.S. news. 10 killed in racist shooting at Buffalo supermarket, of',
                 'CBS News - Breaking news, 24/7 live streaming news & top stories Watch CBS News live and get the latest, breaking news headlines of the day for national news and world news today.   Latest News. War in Ukraine. More Top Stories. MoneyWatch. Coronavirus Crisis. CBS Weekend News. C',
                 "N12 - Israel's news site N12 from News 12, with the leading reporter team in Israel. We have been updated all day from the reporters in the field and also in the reporters, where they update all day in all events as soon as they happen. The eye that sees everything. N12 magazine. N12 magazine \n\n Lieberman: Need to change the law of nationality \n\n Against the backdrop of the name of the name",
                 'Breaking International News & Views | Reuters   Ukraine Latest. Latest Stories. Talking Points. Asia Pacific. China. UK. United States. Middle East. Africa. Americas. Sports. . The Last Read. My View Reuters. Site Index. Information you can trust. Follow Us. Thomson Reuters Produ',
                 'The Wall Street Journal & Breaking News, Business, Financial and Economic News, World News and Video WSJ online coverage of breaking news and current headlines from the US and around the world. Top stories, photos, videos, detailed analysis and in-depth reporting.  Elon Musk Says',
                 'Google ads, digital marketing, SEO, and raising the arrangement of websites, electronic marketing and codes, and campaigns in Google and Siu ads to upload a site in Google 0544800262 Google ads and electronic digital market \n\n E -marketing and Google ads \n \n\n On this page, you will find content on digital and electronic marketing',
                 "Abydos SEO - Learn SEO for FREE | SEO In 5 Minutes Abydos SEO Beginner's Guide to SEO | Learn SEO for FREE - SEO Course SEO In 5 Minutes - Quick SEO Tips Learn SEO for FREE\u200b \n\t\t\t\t\tSnip your Way\n. \n\t\t\t\t\tWe handle everything for you!\n\t\t\t\t. \n\t\t\t\t\tWhy Choose Us\n\t\t\t\t. \n\t\t\t\t\tGet a call",
                 'SEO', 'digital marketing', 'backlinks', 'Rank', 'Backlink', 'Google Search Results', 'Google Search', 'Page Rank',
                 'SEO Optimization',
                 'Premium Domain', 'website ranking', 'Domain', 'Google ads ', 'Ranking Factors', 'organic traffic', 'Attention Required! moz.com',
                 'Attention Required!', 'Attention Required!', 'Access Denied'],
        'target': ['Blogspot', 'Blogspot', 'Blogspot', 'Blogspot', 'Blogspot', 'Blogspot', 'Blogspot', 'Blogspot', 'Commodities', 'Commodities', 'Commodities',
                   'Commodities',
                   'Commodities', 'Commodities', 'Commodities', 'Commodities', 'Commodities', 'Commodities', 'Commodities', 'Commodities',
                   'Commodities',
                   'Commodities', 'Commodities', 'Commodities', 'Commodities', 'Commodities', 'Commodities', 'Commodities', 'Commodities',
                   'Commodities',
                   'Commodities', 'Crypto', 'Crypto', 'Crypto', 'Crypto', 'Crypto', 'Crypto', 'Crypto', 'Crypto', 'Crypto', 'Crypto', 'Crypto',
                   'Crypto', 'Crypto', 'Crypto',
                   'Crypto', 'Crypto', 'Crypto', 'Crypto', 'Crypto', 'Crypto', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance',
                   'Finance',
                   'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance',
                   'Finance',
                   'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex',
                   'Forex',
                   'Forex', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex', 'Forex',
                   'Forex', 'Leisure',
                   'Leisure', 'Leisure', 'Leisure', 'Leisure', 'Leisure', 'Leisure', 'Leisure', 'Leisure', 'Leisure', 'Leisure', 'Leisure', 'Leisure',
                   'Leisure',
                   'Leisure', 'Leisure', 'Leisure', 'Leisure', 'Leisure', 'News', 'News', 'News', 'News', 'News', 'News', 'News', 'News', 'News', 'News', 'News',
                   'News',
                   'News', 'News', 'News', 'News', 'News', 'News', 'News', 'News', 'SEO', 'SEO', 'SEO', 'SEO', 'SEO', 'SEO', 'SEO',
                   'SEO', 'SEO',
                   'SEO', 'SEO', 'SEO', 'SEO', 'SEO', 'SEO', 'SEO', 'SEO', 'SEO', 'Unable to Categorize', 'Unable to Categorize', 'Unable to Categorize']}

    clean_text_train = []
    for val in dict_train['text']:
        clean_text_train.append(final_pre_process(val))
    dict_train['clean_text'] = clean_text_train

    # SPLITTING THE TRAINING DATA SET INTO TRAINING AND VALIDATION
    x_train, x_val, y_train, y_val = train_test_split(dict_train["clean_text"], dict_train["target"], test_size=0.001, shuffle=True)

    # TF-IDF
    # Convert x_train to vector since model can only run on numbers and not words- Fit and transform
    # Only transform x_test (not fit and transform)
    vectorizer = TfidfVectorizer(use_idf=True)
    x_train_vectors = vectorizer.fit_transform(x_train)  # tf-idf runs on non-tokenized sentences unlike word2vec

    # FITTING THE CLASSIFICATION MODEL using Logistic Regression(tf-idf)
    lr = LogisticRegression(solver='liblinear', C=10, penalty='l2')
    lr.fit(x_train_vectors, y_train)  # model

def get_text(url_link):
    scraper = cloudscraper.create_scraper()
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

    try:
        r = scraper.get(url_link, headers=headers)

        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('title').text
        description = soup.find('meta', attrs={'name': 'description'})

        if "content" in str(description):
            description = description.get("content")
        else:
            description = ""

        h1 = soup.find_all('h1')
        h1_all = ""
        for x in range(len(h1)):
            if x == len(h1) - 1:
                h1_all = h1_all + h1[x].text
            else:
                h1_all = h1_all + h1[x].text + ". "

        paragraphs_all = ""
        paragraphs = soup.find_all('p')
        for x in range(len(paragraphs)):
            if x == len(paragraphs) - 1:
                paragraphs_all = paragraphs_all + paragraphs[x].text
            else:
                paragraphs_all = paragraphs_all + paragraphs[x].text + ". "

        h2 = soup.find_all('h2')
        h2_all = ""
        for x in range(len(h2)):
            if x == len(h2) - 1:
                h2_all = h2_all + h2[x].text
            else:
                h2_all = h2_all + h2[x].text + ". "

        h3 = soup.find_all('h3')
        h3_all = ""
        for x in range(len(h3)):
            if x == len(h3) - 1:
                h3_all = h3_all + h3[x].text
            else:
                h3_all = h3_all + h3[x].text + ". "

        all_the_content = str(title) + " " + str(description) + " " + str(h1_all) + " " + str(h2_all) + " " + str(h3_all) + " " + str(paragraphs_all)
        all_the_content = str(all_the_content)[0:280]

    except:
        all_the_content = "Attention Required!"

    try:
        all_the_content = ts.google(all_the_content, to_language='en')

    except:
        all_the_content = "Attention Required!"

    return all_the_content


# convert to lowercase and remove punctuations and characters and then strip
def pre_process(text):
    text = text.lower()  # lowercase text
    text = text.strip()  # get rid of leading/trailing whitespace
    text = re.compile('<.*?>').sub('', text)  # Remove HTML tags/markups
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)  # Replace punctuation with space
    text = re.sub('\s+', ' ', text)  # Remove extra space and tabs
    text = re.sub(r'\[[0-9]*\]', ' ', text)  # [0-9] matches any digit (0 to 10000...)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
    text = re.sub(r'\d', ' ', text)  # matches any digit from 0 to 100000..., \D matches non-digits
    text = re.sub(r'\s+', ' ', text)  # \s matches any whitespace, \s+ matches multiple whitespace, \S matches non-whitespace
    return text


# STOPWORDS REMOVAL
def remove_stopwords(string_stop):
    a = [i for i in string_stop.split() if i not in stopwords.words('english')]
    return ' '.join(a)


# Initialize the lemmatizer
wl = WordNetLemmatizer()


# This is a helper function to map NTLK position tags
# Full list is available here: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
def get_word_net_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


# Tokenize the sentence
def lemmatizer(string_lemma):
    word_pos_tags = nltk.pos_tag(word_tokenize(string_lemma)) # Get position tags
    a = [wl.lemmatize(tag[0], get_word_net_pos(tag[1])) for idx, tag in enumerate(word_pos_tags)] # Map the position tag and lemmatize the word/token
    return " ".join(a)


# FINAL PRE PROCESSING
def final_pre_process(string_final):
    return lemmatizer(remove_stopwords(pre_process(string_final)))


def get_category(site_url):
    # Creating test set
    dict_test = {'url': site_url}
    text = list()
    text.append(get_text(dict_test['url'][0]))
    dict_test['text'] = text

    # Pre process the data
    clean_text_test = list()
    clean_text_test.append(final_pre_process(dict_test['text'][0]))
    dict_test['clean_text'] = clean_text_test
    x_test = dict_test['clean_text']

    # converting X_test to vector
    x_vector = vectorizer.transform(x_test)

    # use the trained model on X_vector
    y_test_predict = lr.predict(x_vector)
    y_prob = lr.predict_proba(x_vector)[:, 1]
    dict_test['predict_prob'] = y_prob
    dict_test['target'] = y_test_predict
    final = dict_test['target']
    return final[0]


def traffic_for_url(url_from):
    domain = urlparse(url_from).netloc
    domain = 'ahrefs.com'
    traffic_url = 'https://apiv2.ahrefs.com?from=positions_metrics&target=' + domain + '&mode=subdomains&output=json&token=082c4afc97f7348b730e5fc0b861a2ebd9ce522a'
    try:
        traffic_response = requests.get(traffic_url)
        traffic_data = traffic_response.json()
        traffics = traffic_data['metrics']
        traffic = traffics['traffic']
    except Exception as e: print(e)
    return traffic

def refdomain_for_url(url_from):
    domain = urlparse(url_from).netloc
    domain = 'ahrefs.com'
    refdomain_url = 'https://apiv2.ahrefs.com?from=refdomains_by_type&target=' + domain + '&mode=subdomains&limit=1&where=dofollow%3Dtrue&output=json&token=082c4afc97f7348b730e5fc0b861a2ebd9ce522a'
    try:
        refdomain_response = requests.get(refdomain_url)
        refdomain_data = refdomain_response.json()
        all_refdomains_backlinks = refdomain_data['stats']
        refdomain = all_refdomains_backlinks['refdomains']
        all_backlinks = all_refdomains_backlinks['total_backlinks']
    except Exception as e: print(e)
    return refdomain, all_backlinks


def get_data():
    all_links = {}
    Plus500.objects.all().delete()
    target_list=['ahrefs.com']
    train() # the train of the category model
    for target in target_list:
        url = 'https://apiv2.ahrefs.com?from=backlinks&target=' + target + '&mode=subdomains&limit=50&order_by=domain_rating%3Adesc&select=url_from,domain_rating,url_to,title&where=nofollow%3Dfalse&output=json&token=082c4afc97f7348b730e5fc0b861a2ebd9ce522a'
        try:
            response = requests.get(url)
            data = response.json()
            links = data['refpages']
            url_from_list = []
            for i in links:
                url_from_1 = i['url_from']
                url_from_list.append(url_from_1)
                link_data = Plus500(
                    url_from = i['url_from'],
                    url_to = i['url_to'],
                    domain_rating = i['domain_rating'],
                    title = i['title'],
                    competitor = target
                )
                link_data.save()
            for url in url_from_list:
                url_list = [url]
                category_pred = get_category(url_list)
                Plus500.objects.filter(url_from=url,competitor=target).update(category=category_pred)
                url_domain_value=urlparse(url).netloc
                Plus500.objects.filter(url_from=url,competitor=target).update(url_domain=url_domain_value)
                refdomain_value, backlinks_value =refdomain_for_url(url)
                ratio = round(float(refdomain_value/backlinks_value), 8)*100
                Plus500.objects.filter(url_from=url,competitor=target).update(refdomains=refdomain_value)
                Plus500.objects.filter(url_from=url,competitor=target).update(refdomains_backlinks_ratio=ratio)
                traffic_value =traffic_for_url(url)
                Plus500.objects.filter(url_from=url,competitor=target).update(traffic=traffic_value)
                contact_value = get_contact(url)
                Plus500.objects.filter(url_from=url,competitor=target).update(contact_email=contact_value)
        except Exception as e: print(e)
    all_links = Plus500.objects.all()
    return (all_links)
