from lxml import html
import json, urllib, time

def run():
    queryString = raw_input("Please enter something (example: \"knife\"): ")
    clearFiles()
    count = 100
    start = 0
    counter = 0;
    total_count = 0
    while(counter <= total_count):
        total_count = runBatch(count, start, queryString)
        start += count
        counter += count
        time.sleep(1)
    parseIdsFromUrlFile()

def clearFiles():
    open('data_names.txt', 'w+').close()
    open('data_urls.txt', 'w+').close()
    open('data_item_ids.txt', 'w+').close()

def parseNamesFromHTML(resultHTML):
    tree = html.fromstring(resultHTML)
    items = tree.xpath('//span[@class="market_listing_item_name"]/text()')
    #print 'Items: ', items
    fileObject = open('data_names.txt', 'a+')
    for item in items:
        fileObject.write( item + "\n");
    fileObject.close()

def parseUrlsFromHTML(resultHTML):
    tree = html.fromstring(resultHTML)
    items = tree.xpath('//a[@class="market_listing_row_link"]/@href')
    #print 'Items: ', items
    fileObject = open('data_urls.txt', 'a+')
    for item in items:
        fileObject.write( item + "\n");
    fileObject.close()

def parseIdsFromUrlFile():
    urlFileObject = open('data_urls.txt')
    idsFileObject = open('data_item_ids.txt', 'w+')
    for line in urlFileObject:
        terms = line.split("/")
        # Last term might contain extra query filters.
        terms2 = terms[-1].split("?")
        # Write the last term, which should be the id
        idsFileObject.write( terms2[0] + "\n");
    urlFileObject.close()
    idsFileObject.close()

def runBatch(count, start, queryString):
    url = makeUrl(count, start, queryString)
    response = urllib.urlopen(url);
    data = json.loads(response.read())
    print url
    print data["success"]
    print data["start"]
    #print data["pagesize"]
    print data["total_count"]
    #print data["results_html"]
    parseNamesFromHTML(data["results_html"].encode('ascii', 'ignore'))
    parseUrlsFromHTML(data["results_html"])
    return data["total_count"]

# appid=440: Team Fortress 2
# appid=570: Dota 2
# appid=730: Counter-Strike: Global Offensive
# appid=753: Steam
# appid=214190: Minimum
# appid=230410: Warframe
# appid=238460: BattleBlock Theater
# appid=238960: Path of Exile
# appid=239220: The Mighty Quest For Epic Loot
# appid=251970: Sins of a Dark Age
# appid=308080: Altitude0: Lower & Faster
# appid=321360: Primal Carnage: Extinction
def makeUrl(count, start, queryString):
    return "http://steamcommunity.com/market/search/render/?appid=730&query=" + queryString + "&count=" + str(count) + "&start=" + str(start) + "#p1_price_desc"

if __name__ == "__main__":
    run()
    #parseIdsFromUrlFile()
