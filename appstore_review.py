import pandas as pd
import requests
import os
import xmltodict

# petdoc_id = 1059558618
# https://itunes.apple.com/kr/rss/customerreviews/page=10/id=1059558618/xml


PETDOC_ID = 1059558618
URL = 'https://itunes.apple.com/kr/rss/customerreviews/id=1059558618/xml'
result = list()


def get_url_index():
    response = requests.get(URL).content.decode('UTF-8')
    xml = xmltodict.parse(response)

    last_url = [l['@href'] for l in xml['feed']['link'] if (l['@rel'] == 'last')][0]
    last_index = [int(s.replace('page=', '')) for s in last_url.split('/') if ('page=' in s)][0]

    return last_index


def append_result(data):
    result.append(data)


def appstore_crawler():
    url = 'https://itunes.apple.com/kr/rss/customerreviews/page=1/id=%i/xml' % PETDOC_ID
    try:
        last_index = get_url_index()
    except Exception as e:
        print(url)
        print(PETDOC_ID)
        print(e)
        return

    for idx in range(1, last_index + 1):
        url = 'https://itunes.apple.com/kr/rss/customerreviews/page=%i/id=%i/xml' % (idx, PETDOC_ID)
        print(url)

        response = requests.get(url).content.decode('utf-8')
        try:
            xml = xmltodict.parse(response)
        except Exception as e:
            print('\tXml parse Error %s\n\tSkip %s : ' % (e, url))
            continue

        try:
            num_reviews = len(xml['feed']['entry'])
        except Exception as e:
            print('\tNo entry', e)
            continue

        try:
            xml['feed']['entry'][0]['author']['name']
            single_reviews = False
        except:
            single_reviews = True
            pass

        if single_reviews:
            append_result({
                'USER': xml['feed']['entry']['author']['name'],
                'DATE': xml['feed']['entry']['updated'],
                'STAR': int(xml['feed']['entry']['im:rating']),
                'LIKE': int(xml['feed']['entry']['im:voteSum']),
                'TITLE': xml['feed']['entry']['title'],
                'REVIEW': xml['feed']['entry']['content'][0]['#text']
            })
        else:
            for i in range(len(xml['feed']['entry'])):
                append_result({
                    'USER': xml['feed']['entry'][i]['author']['name'],
                    'DATE': xml['feed']['entry'][i]['updated'],
                    'STAR': int(xml['feed']['entry'][i]['im:rating']),
                    'LIKE': int(xml['feed']['entry'][i]['im:voteSum']),
                    'TITLE': xml['feed']['entry'][i]['title'],
                    'REVIEW': xml['feed']['entry'][i]['content'][0]['#text']
                })
        res_df = pd.DataFrame(result)
        # res_df['DATE'] = pd.to_datetime(res_df['DATE'], format="%Y-%m-%dT%H:%M:%S")
        res_df['DATE'].apply(lambda a: pd.to_datetime(a).date())
        import datetime
        today = datetime.datetime.today().date()
        today_str = str(today)
        outfile = './appstore_review_%s.xlsx' % today_str
        # res_df.to_csv(outfile, encoding='utf-8-sig', index=False)
        res_df.to_excel(outfile, sheet_name='Sheet1',
                        na_rep='NaN',
                        float_format="%.2f",
                        header=True,
                        index=True,
                        index_label="id",
                        startrow=1,
                        startcol=1,
                        freeze_panes=(2, 0)
                        )


if __name__ == '__main__':
    # print(get_url_index())
    appstore_crawler()
