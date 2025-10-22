"""
Test file generated from 95_Logger.ipynb
Auto-generated - excludes cells starting with #
Generated on: C:\GitHub\domolibrary
"""

import os
import domolibrary.client.DomoAuth as dmda

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ['DOMO_INSTANCE'],
    domo_access_token=os.environ['DOMO_ACCESS_TOKEN'],
)


async def test_cell_1(token_auth=token_auth):
    """Test case from cell 1"""
    class Foo:
        def __init__(self):
            pass

        def test_get_traceback_details(self, debug_traceback: bool = False):
            return get_traceback(parent_class=self.__class__.__name__, debug_traceback=debug_traceback)


    # # print traceback details for test_get_details function
    test_foo = Foo()

    test_foo.test_get_traceback_details(debug_traceback=True).to_dict()


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    show_doc(Logger.get_traceback)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    logger = Logger(
        app_name="test",
    )


    def test_log():
        return logger.log_info("test the error returns type Info", debug_log=False)


    test_log()


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    import pandas as pd


    def custom_write_logs_fn(logs):
        print("printing logs")
        return pd.DataFrame(logs)


    logger = Logger(app_name="test", output_fn=custom_write_logs_fn)


    def test_error():
        try:
            if 1 == 1:
                raise Exception("random error")

        except Exception as e:
            logger.log_error(e)


    def double_test():
        test_error()


    # record first error
    test_error()

    # records second error nested inside double_test()
    double_test()

    logger.output_log()
