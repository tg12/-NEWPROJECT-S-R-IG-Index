'''THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd

# contact :- github@jamessawyer.co.uk



import traceback #errors
import pytz
import datetime
import random
import time
import json
import requests
import math
import pandas
import numpy
from time import localtime, strftime
import sys #better errors
from matplotlib.pyplot import * #graphs and stuff
import re #dates and such
import uuid #filenames, figure a better way to do this

spread_check = -3


def midpoint(p1, p2):
    return (p1 + p2) / 2     # or *0.


def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d' % (hours, mins, secs)


def all_same(items):
    return all(x == items[0] for x in items)


def debug_info(err_str):
    # Standard debugging function, pass it a string
    # print("-----------------DEBUG-----------------")
    print("#################DEBUG##################")
    print(str(time.strftime("%H:%M:%S")) + ":!!!DEBUG!!!:" + str(err_str))
    print("#################DEBUG##################")
    # print("-----------------DEBUG-----------------")


def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]


def tradeable_epic(epic_id, status):

    try:

        if str(status) == "TRADEABLE":
            base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
            auth_r = requests.get(
                base_url, headers=authenticated_headers)
            d = json.loads(auth_r.text)

            current_bid = d['snapshot']['bid']
            ask_price = d['snapshot']['offer']
            spread = float(current_bid) - float(ask_price)

            if float(spread) >= spread_check:
                print(
                    "!!INFO!!...FOUND GOOD EPIC..., passing to trade function ..." +
                    str(epic_id))
                time.sleep(1)
                return True
            else:
                print(
                    "!!INFO!!...skipping, NO GOOD EPIC....Checking next epic spreads...")
                time.sleep(1)
                pass
        else:
            print(
                "!!INFO!!...skipping, not tradeable):" +
                str(epic_id))
            time.sleep(0.5)

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print(sys.exc_info()[0])
        debug_info("bid/ask probably returned NoneType!!!")
        pass


market_close_tm = "00:00"
market_open_tm = "00:01"

# remember to change these for DEMO/LIVE!!!
types = {
    # 'Cryptocurrency': ['', 'Europe/London']}
    # 'Options (Australia 200)': '',
    # 'Weekend Indices': '',
    # 'Indices': '',
    # 'Forex': ['', 'Europe/London']}
    # 'Commodities Metals Energies': '',
    # 'Bonds and Moneymarket': '',
    # 'ETFs, ETCs & Trackers': '',
    'Shares - UK': ['180500', 'Europe/London'],
    'Shares - UK International (IOB)': ['97695', 'Europe/London'],
    # 'Shares - US (All Sessions)': '',
    # 'Shares - US': '',
    # 'Shares - Austria': '',
    # 'Shares - Belgium': '',
    'Shares - LSE (UK)': ['172904', 'Europe/London']}
# 'Shares - Finland': '',
# 'Shares - Canada': '',
# 'Shares - France': '',
# 'Shares - Denmark': '',
# 'Shares - Germany': '',
# 'Shares - Greece': '',
# 'Shares - Hong Kong': '',
# 'Shares - Ireland (ISEQ)': '',
# 'Shares - Ireland (LSE)': '',
# 'Shares - Netherlands': '',
# 'Shares - Norway': '',
# 'Shares - Portugal': '',
# 'Shares - Singapore': '',
# 'Shares - South Africa': '',
# 'Shares - Sweden': '',
# 'Shares - Switzerland': '',
# 'Options (Eu Stocks 50)': '',
# 'Options (France 40)': '',
# 'Options (FTSE)': '',
# 'Options (Germany)': '',
# 'Options (Italy 40)': '',
# 'Options (Spain 35)': '',
# 'Options (Sweden 30)': '',
# 'Options (US 500)': '',
# 'Options (Wall St)': '',
# 'Options on FX Majors': '',
# 'Options on Metals, Energies': ''}

###########################################################################
###########################################################################
###########################################################################
############################CONFIG VARIABLES###############################
############################CONFIG VARIABLES###############################
############################CONFIG VARIABLES###############################
###########################################################################
###########################################################################
###########################################################################

b_REAL = False

#CREDS###################################################################
LIVE_API_KEY = ''
LIVE_USERNAME = ""
LIVE_PASSWORD = ""
LIVE_ACC_ID = ""
##########################################################################
DEMO_API_KEY = ''
DEMO_USERNAME = ""
DEMO_PASSWORD = ""
DEMO_ACC_ID = ""
###########################################################################

if b_REAL:
    REAL_OR_NO_REAL = 'https://api.ig.com/gateway/deal'
    API_ENDPOINT = "https://api.ig.com/gateway/deal/session"
    API_KEY = LIVE_API_KEY
    data = {"identifier": LIVE_USERNAME, "password": LIVE_PASSWORD}
else:
    REAL_OR_NO_REAL = 'https://demo-api.ig.com/gateway/deal'
    API_ENDPOINT = "https://demo-api.ig.com/gateway/deal/session"
    API_KEY = DEMO_API_KEY
    data = {"identifier": DEMO_USERNAME, "password": DEMO_PASSWORD}

headers = {'Content-Type': 'application/json; charset=utf-8',
           'Accept': 'application/json; charset=utf-8',
           'X-IG-API-KEY': API_KEY,
           'Version': '2'
           }

r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)

headers_json = dict(r.headers)
CST_token = headers_json["CST"]
print(R"CST : " + CST_token)
x_sec_token = headers_json["X-SECURITY-TOKEN"]
print(R"X-SECURITY-TOKEN : " + x_sec_token)

# GET ACCOUNTS
base_url = REAL_OR_NO_REAL + '/accounts'
authenticated_headers = {'Content-Type': 'application/json; charset=utf-8',
                         'Accept': 'application/json; charset=utf-8',
                         'X-IG-API-KEY': API_KEY,
                         'CST': CST_token,
                         'X-SECURITY-TOKEN': x_sec_token}

auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)

base_url = REAL_OR_NO_REAL + '/session'

if b_REAL:
    data = {
        "accountId": LIVE_ACC_ID,
        "defaultAccount": "True"}  # Main Live acc
else:
    data = {
        "accountId": DEMO_ACC_ID,
        "defaultAccount": "True"}  # Main Demo acc

auth_r = requests.put(
    base_url,
    data=json.dumps(data),
    headers=authenticated_headers)

# print("-----------------DEBUG-----------------")
# print("#################DEBUG#################")
# print(auth_r.status_code)
# print(auth_r.reason)
# print(auth_r.text)
# print("-----------------DEBUG-----------------")
# print("#################DEBUG#################")


##########################################################################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################################################################


def supres(
        low,
        high,
        min_touches=2,
        stat_likeness_percent=1.5,
        bounce_percent=5):
    """Support and Resistance Testing

    Identifies support and resistance levels of provided price action data.

    Args:
        low(pandas.Series): A pandas Series of lows from price action data.
        high(pandas.Series): A pandas Series of highs from price action data.
        min_touches(int): Minimum # of touches for established S&R.
        stat_likeness_percent(int/float): Acceptable margin of error for level.
        bounce_percent(int/float): Percent of price action for established bounce.

    ** Note **
        If you want to calculate support and resistance without regard for
        candle shadows, pass close values for both low and high.

    Returns:
        sup(float): Established level of support or None (if no level)
        res(float): Established level of resistance or None (if no level)
    """
    # Setting default values for support and resistance to None
    sup = None
    res = None

    # Identifying local high and local low
    maxima = high.max()
    minima = low.min()

    # Calculating distance between max and min (total price movement)
    move_range = maxima - minima

    # Calculating bounce distance and allowable margin of error for likeness
    move_allowance = move_range * (stat_likeness_percent / 100)
    bounce_distance = move_range * (bounce_percent / 100)

    # Test resistance by iterating through data to check for touches delimited
    # by bounces
    touchdown = 0
    awaiting_bounce = False
    for x in range(0, len(high)):
        if abs(maxima - high[x]) < move_allowance and not awaiting_bounce:
            touchdown = touchdown + 1
            awaiting_bounce = True
        elif abs(maxima - high[x]) > bounce_distance:
            awaiting_bounce = False
    if touchdown >= min_touches:
        res = maxima

    # Test support by iterating through data to check for touches delimited by
    # bounces
    touchdown = 0
    awaiting_bounce = False
    for x in range(0, len(low)):
        if abs(low[x] - minima) < move_allowance and not awaiting_bounce:
            touchdown = touchdown + 1
            awaiting_bounce = True
        elif abs(low[x] - minima) > bounce_distance:
            awaiting_bounce = False
    if touchdown >= min_touches:
        sup = minima
    return sup, res


def exploreNode(nodeID):
    base_url = REAL_OR_NO_REAL + '/marketnavigation/' + nodeID
    r = requests.get(base_url, headers=authenticated_headers)

    if isinstance(r.json()['nodes'], list):
        for node in r.json()['nodes']:
            time.sleep(2)
            exploreNode(node['id'])
    if isinstance(r.json()['markets'], list):
        for market in r.json()['markets']:

            dfb_today_daily_checks = [
                "DFB" in str(
                    market['epic']), "TODAY" in str(
                    market['epic']), "DAILY" in str(
                    market['epic'])]

            if any(dfb_today_daily_checks):
                if tradeable_epic(market['epic'], market['marketStatus']):
                    print("trading.... " + str(market['epic']))
                    main_trade_function(market['epic'])


def main_trade_function(epic_id):

    position_base_url = REAL_OR_NO_REAL + "/positions"
    position_auth_r = requests.get(
        position_base_url, headers=authenticated_headers)
    position_json = json.loads(position_auth_r.text)

    positionMap = {}

    # print("-------------Position Info-------------")
    # print("#################DEBUG#################")
    # print(position_auth_r.status_code)
    # print(position_auth_r.reason)
    # print(position_auth_r.text)
    # print("-----------------DEBUG-----------------")
    # print("#################DEBUG#################")

    for item in position_json['positions']:
        direction = item['position']['direction']
        dealSize = item['position']['dealSize']
        ccypair = item['market']['epic']
        key = ccypair + '-' + direction
        if(key in positionMap):
            positionMap[key] = dealSize + positionMap[key]
        else:
            positionMap[key] = dealSize
    # print('current position summary:')
    # print(positionMap)

    try:

        # obligatory sleep, gets round IG 60 per min limit
        time.sleep(2)

        base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
        auth_r = requests.get(
            base_url, headers=authenticated_headers)
        d = json.loads(auth_r.text)

        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")
        # print(auth_r.status_code)
        # print(auth_r.reason)
        # print(auth_r.text)
        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")

        current_bid = d['snapshot']['bid']
        current_offer = d['snapshot']['offer']
        ######################################
        current_mid = float(midpoint(current_bid, current_offer))
        ######################################
        instrument_name = str(d['instrument']['name'])

        base_url = REAL_OR_NO_REAL + "/prices/" + epic_id + "/DAY/30"
        # Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5,
        # MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3,
        # HOUR_4, DAY, WEEK, MONTH)
        auth_r = requests.get(base_url, headers=authenticated_headers)
        d = json.loads(auth_r.text)

        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")
        # print(auth_r.status_code)
        # print(auth_r.reason)
        # print(auth_r.text)
        # print("-----------------DEBUG-----------------")
        # print("#################DEBUG#################")

        remaining_allowance = d['allowance']['remainingAllowance']
        reset_time = humanize_time(
            int(d['allowance']['allowanceExpiry']))
        # debug_info("Remaining API Calls left: " + str(remaining_allowance))
        # debug_info("Time to API Key reset: " + str(reset_time))

        high_prices = []
        low_prices = []
        snap_tm = []

        for i in d['prices']:

            if i['highPrice']['bid'] is not None:
                highPrice = i['highPrice']['bid']
                high_prices.append(highPrice)
            ########################################
            if i['lowPrice']['bid'] is not None:
                lowPrice = i['lowPrice']['bid']
                low_prices.append(lowPrice)
            ########################################
            snap_time = str(i['snapshotTime'])
            match = re.search(r'\d{4}:\d{2}:\d{2}', snap_time)
            date = datetime.datetime.strptime(
                match.group(), '%Y:%m:%d').date()
            snap_tm.append(str(date))

        array_len_check = []
        array_len_check.append(len(high_prices))
        array_len_check.append(len(low_prices))
        xa = range(0, len(low_prices))
        if all_same(array_len_check) == False:
            print("Fuck this! Incomplete dataset from IG")
            return None

        sup, res = supres(pandas.Series(low_prices),
                          pandas.Series(high_prices))

        if any(elem is None for elem in [sup,res]):
            debug_info("no sup/res value")
            return None

        # print(sup)
        # print(res)
        if sup is not None:
            sup_a = numpy.empty(len(xa))
            sup_a.fill(sup)
            plot(xa, sup_a, label='Support')
        if res is not None:
            res_a = numpy.empty(len(xa))
            res_a.fill(res)
            plot(xa, res_a, label='Resistance')
        
        plot(xa, high_prices, label='High Prices')
        plot(xa, low_prices, label='Low Prices')
        xticks(xa, snap_tm, rotation='vertical')
        tight_layout()
        rcParams.update({'figure.autolayout': True})
        rcParams.update({'font.size': 8})
        ylabel('Price')
        legend(loc='best')
        legend()
        grid(True)
        title("Daily Analysis for " + str(instrument_name))
        draw()
        build_file_name = str(uuid.uuid4().hex)
        savefig(str(build_file_name) + ".jpg", dpi=100)
        # show()
        clf()

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print(sys.exc_info()[0])
        debug_info(
            "Something fucked up with the order, or the pricing or whatever!!, Try again!!")
        time.sleep(2)
        pass


if __name__ == '__main__':

    debug_info("Program Starting...")

    while True:

        try:
            for t in types.keys():
                try:
                    id, time_zone = types[t]
                    tz = pytz.timezone(time_zone)
                    now_time = datetime.datetime.now(tz=tz).strftime("%H:%M")
                    if is_between(
                        str(now_time),
                        (str(market_close_tm),
                         str(market_open_tm))):
                        print("!!INFO!!...Market Closed, waiting....")
                        timeDelay = random.randrange(0, 90)
                        time.sleep(timeDelay)
                    else:
                        print("!!INFO!!...Market Likely Open")
                        # as not to start again from the start
                        exploreNode(id)
                except Exception as e:
                    print(e)
                    print(traceback.format_exc())
                    print(sys.exc_info()[0])
                    debug_info("!!ERROR!!...Nothing to see here moving on....")
                    continue

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(sys.exc_info()[0])
            debug_info("!!ERROR!!...Generic Program Error...Moving on!!")
            continue
