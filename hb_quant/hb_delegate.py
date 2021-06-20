#coding: utf8 
from huobi.client.generic import GenericClient
from huobi.client.market import MarketClient
from huobi.client.account import AccountClient
from huobi.client.trade import TradeClient
from huobi.constant.definition import OrderType

class General(object):
    '''
        不涉及交易，不需要账户信息
    '''

    def __init__(self, symbols, url="https://api.huobi.pro"):
        self._symbol_list = symbols
        self._market = MarketClient(url = url)
        self.symbolInfo = {}
        self._getSymbolInfo()

    def getSymbolInfo(self):
        '''
            获取关心的交易对信息，如报价精度等
        '''
        gc = GenericClient()
        lst = gc.get_exchange_symbols()
        for sym in lst:
            if sym.symbol not in self._symbol_list:
                continue
            tmp = {}
            tmp['price_precision'] = sym.price_precision
            tmp['amount_precision'] = sym.amount_precision
            tmp['value_precision'] = sym.value_precision
            tmp['symbol'] = sym.symbol
            self.symbolInfo[sym.symbol] = tmp

    def getTickers(self):
        '''
            获取关心的交易对的最新价格
        '''
        ret = {}
        lst = self._market.get_market_tickers()
        for mt in lst:
            if mt.symbol not in self._symbol_list:
                continue
            tmp = {}
            tmp['symbol'] = mt.symbol
            tmp['price'] = mt.close
            ret[mt.symbol] = tmp
        return ret


class Trade(object):

    def __init__(self, apiKey, secretKey, url="https://api.huobi.pro"):
        self._account_id = None
        self._api_key = apiKey
        self._secret_key = secretKey
        self._trade = TradeClient(api_key=apiKey, secret_key=secretKey,url=url)
        accs = self.getAccounts()
        for a in accs:
            if a['type'] == 'spot':
                self._account_id = a['id']
                break

    def getAccounts(self):
        ret = []
        ac = AccountClient(api_key=self._api_key, secret_key=self._secret_key)
        aList = ac.get_accounts()
        for a in aList:
            tmp = {}
            tmp['id'] = a.id
            tmp['type'] = a.type
            tmp['state'] = a.state
            tmp['subtype'] = a.subtype
            ret.append(tmp)
        return ret

    def marketBuy(self, symbol, amount, clientOrderId = None):
        orderId = self._trade.create_spot_order(symbol, self._account_id, OrderType.BUY_MARKET, amount, 0.0, client_order_id = clientOrderId)
        return orderId

    def limitBuy(self, symbol, amount, price, clientOrderId = None):
        orderId = self._trade.create_spot_order(symbol, self._account_id, OrderType.BUY_LIMIT, amount, price, client_order_id = clientOrderId)
        return orderId

    def marketSell(self, symbol, amount, clientOrderId = None):
        orderId = self._trade.create_spot_order(symbol, self._account_id, OrderType.SELL_MARKET, amount, 0.0, client_order_id = clientOrderId)
        return orderId

    def limitSell(self, symbol, amount, price, clientOrderId = None):
        orderId = self._trade.create_spot_order(symbol, self._account_id, OrderType.SELL_LIMIT, amount, price, client_order_id = clientOrderId)
        return orderId

    def getOrderStatus(self, orderId):
#        info = self._trade.get_match_results_by_order_id(orderId)
        info = self._trade.get_order(orderId)
        ret = {}
        ret['id'] = info.id
        ret['symbol'] = info.symbol
        ret['account_id'] = info.account_id
        ret['amount'] = info.amount
        ret['price'] = info.price
        ret['created_at'] = info.created_at
        ret['canceled_at'] = info.canceled_at
        ret['finished_at'] = info.finished_at
        ret['type'] = info.type
        ret['filled_amount'] = info.filled_amount
        ret['filled_cash_amount'] = info.filled_cash_amount
        ret['filled_fees'] = info.filled_fees
        ret['source'] = info.source
        ret['state'] = info.state
        ret['client_order_id'] = info.client_order_id
        return ret
        
            
if __name__ == '__main__':
    symbols = ['btcusdt','ethusdt']
    gTest = General(symbols)            
    print("{}".format(gTest.symbolInfo))
    tickers = gTest.getTickers()
    print("{}".format(tickers))

    tTest = Trade("378d5374-fb9614ee-7090ffa3-qv2d5ctgbn","c4b92159-7651d5bb-ca376cab-7145d")
    x = tTest.getAccounts()
    print("{}".format(x))
#    oId = tTest.limitBuy('btcusdt', 0.003, 30000, 1)
#    print("{}".format(oId))
    oId = 296301522690604
    x = tTest.getOrderStatus(oId)
    print("{}".format(x))
#    o = tTest._trade.get_order(oId)
#    o.print_object()
    o = tTest.getOrderStatus(oId)
    print("{}".format(o))
    
        
        


