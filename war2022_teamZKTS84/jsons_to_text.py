import codecs
import json
import os.path
import re


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def main():
    articles_folder = "../articles/"
    text_folder = "../texts/"
    os.mkdir(text_folder)

    articles_files_names = ["kp-articles.json", 'lenta-articles.json', 'pravda-articles.json',
                  'svoboda-articles.json']

    data = []

    for file_name in articles_files_names:
        with open(articles_folder + file_name) as json_open_file:
            json_data = json.load(json_open_file)
            data.append(json_data)

    for json_data in data:
        for article in json_data:
            if len(article['article_title']) >= 1:
                article_text = article['article_title'][0] + "\n\n" + article['article_text'].replace("\xa0", " ")
                article_uuid = article['article_uuid']

                with codecs.open(text_folder + article_uuid + ".txt", "w", "utf-8-sig") as temp:
                    temp.write(article_text)


if __name__ == "__main__":
    main()
