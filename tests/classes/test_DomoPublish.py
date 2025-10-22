"""
Test file generated from DomoPublish.ipynb
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
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN"),
    )

    PUBLICATION_ID = "6a6a4dcc-4561-4ef3-b351-904403bc9c6a"

    publication = (
        await publish_routes.get_publication_by_id(auth=auth, publication_id=PUBLICATION_ID)
    ).response

    publication

    # publication

    # subscriber_ls = publication["subscriptionAuthorizations"]
    # subscriber = subscriber_ls[0]
    # print(subscriber)


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN"),
    )

    PUBLICATION_ID = "6a6a4dcc-4561-4ef3-b351-904403bc9c6a"

    publication = (
        await publish_routes.get_publication_by_id(auth=auth, publication_id=PUBLICATION_ID)
    ).response
    publication

    subscriber_ls = publication["subscriptionAuthorizations"]
    subscriber = subscriber_ls[0]
    print(subscriber)


    domo_pub = await DomoPublication.get_by_id(publication_id=publication["id"], auth=auth)

    print(domo_pub.display_url())
    await domo_pub.get_content_details(
        subscriber_domain="crystalballers-ai-partner-christian"
    )


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    pub_subscribers = [
        DomoSubscription._from_dict(subscriber, auth=auth) for subscriber in subscriber_ls
    ]

    parent_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN"),
    )

    child_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_CHILD_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_CHILD_ACCESS_TOKEN"),
    )

    test = await pub_subscribers[0].get_content_details(parent_auth=parent_auth)

    print(test)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    domo_publication = await DomoPublication.get_by_id(
        publication_id=publication["id"], auth=auth, return_raw=False
    )

    domo_publication.__dict__


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    lineage = await domo_publication.Lineage.get(debug_api=False, return_raw=True)

    lineage


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    domo_pub = await DomoPublication.get_by_id(
        publication_id=publication["id"], auth=parent_auth
    )

    print(domo_pub.display_url())
    domo_publication_content = await domo_pub.get_content()

    domo_publication_content[0]


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    domo_sub = domo_publication.subscriptions[0]


    def retrieval_fn(sub: DomoSubscription):
        print(sub)

        if sub.id:
            return auth

        return auth


    test_publis = await domo_sub.get_content_details(
        debug_api=False, parent_auth=parent_auth
    )

    test_publis[0].__dict__


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    domo_everywhere = DomoEverywhere(auth=child_auth)
    print(domo_everywhere)

    (await domo_everywhere.get_subscriptions())[0:9]


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    domo_everywhere_parent = DomoEverywhere(auth=parent_auth)
    domo_everywhere_child = DomoEverywhere(auth=child_auth)

    await domo_everywhere_child.get_subscriptions(debug_api=False, return_raw=False)


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    await domo_everywhere_parent.get_publications()
    # await domo_everywhere_parent.publications[0].report_content_as_dataframe(return_raw=False)
    # await domo_everywhere_parent.publications[0].report_lineage_as_dataframe()


async def test_cell_11(token_auth=token_auth):
    """Test case from cell 11"""
    content_ls = []
    content_item = DomoPublication_Content(
        content_id="",
        entity_type="DATASET",
        entity_id="905fa986-fb88-412c-8a27-bc37b4c06617",
        entity_domain="crystalballers-ai-partner-christian.domo.com",
        is_v2=True,
        is_direct_content=True,
        auth=auth,
        created_dt=dt.datetime.now(),
    )
    content_ls.append(content_item)

    sub_ls = []
    sub_item = DomoSubscription(
        id="",
        publication_id="",
        subscriber_domain="crystalballers-ai-partner.domo.com",
        auth=auth,
        created_dt=dt.datetime.now(),
        parent_publication=None,

        raw=None,
        publisher_domain=None,
    )
    sub_ls.append(sub_item)

    # await DomoPublication.create_publication(auth = token_auth, name="Test OZ",
    #                                  content_ls=content_ls,
    #                                  subscription_ls=sub_ls)


async def test_cell_12(token_auth=token_auth):
    """Test case from cell 12"""
    publication_id = PUBLICATION_ID

    domo_publication = await DomoPublication.get_by_id(
        publication_id=publication_id, auth=auth
    )
    domo_publication.subscriptions

    await domo_publication.update_publication(
        name="Test OZ - updated",
        content_ls=domo_publication.content,
        subscription_ls=domo_publication.subscriptions,
    )


async def test_cell_13(token_auth=token_auth):
    """Test case from cell 13"""
    await domo_everywhere.get_subscription_invitations()
