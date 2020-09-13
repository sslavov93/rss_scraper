# from pytest import raises
#
# from celery.exceptions import Retry
#
# # for python 2: use mock.patch from `pip install mock`.
# from unittest.mock import patch
#
# # from feed.models import Product
# from feed.celery_periodic.tasks import scrape_single
#
#
# # class TestScrapeSingleFeed:

    # @patch('feed.celery_periodic.tasks.DefaultParser.persist')
    # def test_success(self, product_order):
    #     test_url = "http://www."
    #     scrape_single(test_url)
        # ______________________________________
        # product = Product.objects.create(
        #     name='Foo',
        # )
        # send_order(product.pk, 3, Decimal(30.3))
        # product_order.assert_called_with(3, Decimal(30.3))

    # @patch('proj.tasks.Product.order')
    # @patch('proj.tasks.send_order.retry')
    # def test_failure(self, send_order_retry, product_order):
    #     product = Product.objects.create(
    #         name='Foo',
    #     )
    #
    #     # Set a side effect on the patched methods
    #     # so that they raise the errors we want.
    #     send_order_retry.side_effect = Retry()
    #     product_order.side_effect = OperationalError()
    #
    #     with raises(Retry):
    #         send_order(product.pk, 3, Decimal(30.6))