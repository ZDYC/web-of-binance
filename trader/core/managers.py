from django.db.models import Manager, Q
from decimal import Decimal


class OrderManager(Manager):
    """订单管理者
    """
    def create_order(self, user, account,
                     symbol, quantity, price,
                     side, buy, sell,
                     order_type, time_in_force,
                     stop_price=None, iceberg_qty=None):
        """create order
        """
        order = self.model(
            user=user,
            account=account,
            symbol=symbol,
            quantity=quantity,
            price=price,
            side=side,
            order_type=order_type,
            buy=buy,
            sell=sell,
            time_in_force=time_in_force,
            stop_price=stop_price)
        order.save()
        return order

    def get_orders(self, symbol=None, trader=None, account=None):
        query = self.get_queryset()
        if symbol:
            query = query.filter(symbol=symbol)

        if trader:
            query = query.filter(user=trader)



class AssetManager(Manager):
    """资产管理者
    """

    def _create_log(self, coin, quantity, type, account, effect_account=True,
                    user=True, related_object=None, usdt_value=0, save=True):
        if not isinstance(quantity, Deciaml):
            quantity = Decimal(quantity)
        if isinstance(coin, str):
            from core.models import CryptoCoin
            coin = CryptoCoin.objects.get(pk=coin)
        log = self.model(
            account=account,
            user=user,
            coin=coin,
            quantity=quantity,
            effect_account=effect_account,
            related_object=related_object,
            type=type,
            usdt_value=usdt_value)
        if save:
            log.save()
        return log

    def log_transfer_to_account(self, coin, quantity, account):
        """记录一条交易账户转入
        """
        return self._create_log(
            coin, quantity,
        )