r"""
Test file generated from 50_DomoPublish.ipynb
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
        domo_instance=os.environ['DOMO_DOJO_INSTANCE'],
        domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    )

    publications = (await publish_routes.search_publications(auth = auth)).response
    publication = publications[0]

    publication = (await publish_routes.get_publication_by_id(auth = auth, publication_id = publication['id'])).response
    publication

    subscriber_ls = publication["subscriptionAuthorizations"]
    subscriber_ls[0]


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    pub_subscribers = [
        DomoPublication_Subscription._from_json(subscriber, auth=auth)
        for subscriber in subscriber_ls
    ]

    pub_subscribers[0:5]


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    domo_publication = await DomoPublication.get_by_id(
        publication_id=publication['id'],
        auth=auth,
        return_raw = False
    )

    domo_publication


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    await domo_publication.get_content(return_raw = False)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    await domo_publication.Lineage.get(debug_api = True, return_raw = True)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    domo_sub = domo_publication.subscription_authorizations[0]

    await domo_sub.get_content_details(debug_api = False)


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    domo_publications = DomoPublications(auth = auth)

    (await domo_publications.get())[0:5]


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    domo_publications = DomoPublications(auth = auth)

    await domo_publications.get_subscribers(debug_api = False, return_raw=False)


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    (await domo_publications.search_publications())[0:5]


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    await domo_publications.publications[0].report_content_as_dataframe( return_raw = False)


async def test_cell_11(token_auth=token_auth):
    """Test case from cell 11"""
    publication_id = "438731a1-7e4e-4863-967f-fcfad22c9247"

    domo_publication = await DomoPublication.get_by_id(
        publication_id=publication_id, auth=auth
    )

    await domo_publication.update_publication(
        name="Test OZ - updated",
        content_ls=domo_publication.content,
        subscription_ls=domo_publication.subscription_authorizations,
    )


async def test_cell_12(token_auth=token_auth):
    """Test case from cell 12"""
    await DomoPublication.get_subscription_invites_list(auth=auth)
