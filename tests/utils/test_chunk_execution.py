"""
Test file generated from chunk_execution.ipynb
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
    class e(Exception):
        pass

    class b(Exception):
        pass



    if ():
        print('hi')


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    async def sleeper(duration):
        print(duration)
        await asyncio.sleep(duration)


    await gather_with_concurrency(
        *[sleeper(random.randint(0, 3)) for index in list(range(1, 20))], n=5
    )


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    async def t1():
        print("running t1")
        await asyncio.sleep(1)
        print("done running t1")


    async def t2():
        print("running t2 next")
        await asyncio.sleep(3)
        print("done running t2")


    async def t3():
        print("running t3 next")
        await asyncio.sleep(2)
        print("done running t3")


    await_ls = [t1(), t2(), t3()]

    await run_sequence(*await_ls)

    # run_sequence uses the same syntax as asyncio.gather().  the following code sample is the same
    # await run_sequence( t1(),t2(),t3())

    # run_sequence forces sequential code execution as opposed to asyncio.gather
    # await asyncio.gather(*await_ls)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    num_ls = list(range(50))

    # each list contains six elements
    chunk_list(num_ls, 6)
