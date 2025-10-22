"""
Test file for PDP (Personalized Data Permissions) classes.

Tests PDP_Parameter, PDP_Policy, and Dataset_PDP_Policies classes
following domolibrary2 patterns and standards.
"""

import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoDataset.PDP as pdp

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

# Test constants from environment
TEST_DATASET_ID = os.environ.get("DATASET_ID_1", "")
TEST_PDP_POLICY_ID = os.environ.get("PDP_POLICY_ID_1", "")


async def test_cell_0(token_auth=token_auth) -> str:
    """Helper function to verify authentication setup."""
    if not token_auth.user_id:
        await token_auth.who_am_i()
    return token_auth.user_id


async def test_cell_1_pdp_parameter(token_auth=token_auth):
    """Test PDP_Parameter creation and to_dict conversion."""
    # Create a parameter
    param = pdp.PDP_Parameter(
        column_name="Region",
        column_values_ls=["West", "East"],
        operator="EQUALS",
        ignore_case=True,
        type="COLUMN"
    )
    
    # Test to_dict conversion
    param_dict = param.to_dict()
    
    assert param_dict["name"] == "Region"
    assert param_dict["values"] == ["West", "East"]
    assert param_dict["operator"] == "EQUALS"
    
    # Test from_dict
    param2 = pdp.PDP_Parameter.from_dict(param_dict)
    assert param2.column_name == param.column_name
    assert param2.column_values_ls == param.column_values_ls
    
    return param


async def test_cell_2_pdp_policy_from_dict(token_auth=token_auth):
    """Test PDP_Policy from_dict classmethod."""
    # Sample API response
    sample_policy = {
        "filterGroupId": "policy-123",
        "dataSourceId": "dataset-456",
        "name": "Test Policy",
        "parameters": [
            {
                "name": "Region",
                "values": ["West"],
                "operator": "EQUALS",
                "ignoreCase": True,
                "type": "COLUMN"
            }
        ],
        "userIds": ["user-1", "user-2"],
        "groupIds": ["group-1"],
        "virtualUserIds": []
    }
    
    policy = pdp.PDP_Policy.from_dict(auth=token_auth, obj=sample_policy)
    
    assert policy.id == "policy-123"
    assert policy.dataset_id == "dataset-456"
    assert policy.name == "Test Policy"
    assert len(policy.parameters_ls) == 1
    assert len(policy.user_ls) == 2
    assert policy.auth == token_auth
    
    # Test display_url
    url = policy.display_url
    assert token_auth.domo_instance in url
    assert policy.dataset_id in url
    
    return policy


async def test_cell_3_get_pdp_policies(token_auth=token_auth):
    """Test retrieving PDP policies for a dataset."""
    if not TEST_DATASET_ID:
        print("Skipping test - TEST_DATASET_ID not set in environment")
        return None
    
    # This would normally be accessed through DomoDataset.PDP_Policies
    # but we can test the PDP_Policy class directly
    try:
        # Get a policy by creating a mock Dataset_PDP_Policies
        from dataclasses import dataclass
        
        @dataclass
        class MockDataset:
            id: str
            auth: dmda.DomoAuth
        
        mock_dataset = MockDataset(id=TEST_DATASET_ID, auth=token_auth)
        pdp_policies = pdp.Dataset_PDP_Policies.from_parent(parent=mock_dataset)
        
        # Get all policies
        policies = await pdp_policies.get(debug_api=False)
        
        print(f"Found {len(policies)} PDP policies")
        for policy in policies:
            print(f"  - {policy.name} (ID: {policy.id})")
        
        return policies
    except Exception as e:
        print(f"Error getting PDP policies: {e}")
        return None


async def test_cell_4_get_policy_by_id(token_auth=token_auth):
    """Test retrieving a specific PDP policy by ID."""
    if not TEST_DATASET_ID or not TEST_PDP_POLICY_ID:
        print("Skipping test - TEST_DATASET_ID or TEST_PDP_POLICY_ID not set")
        return None
    
    try:
        policy = await pdp.PDP_Policy.get_by_id(
            auth=token_auth,
            dataset_id=TEST_DATASET_ID,
            policy_id=TEST_PDP_POLICY_ID,
            debug_api=False
        )
        
        print(f"Retrieved policy: {policy.name}")
        print(f"  Dataset ID: {policy.dataset_id}")
        print(f"  Policy ID: {policy.id}")
        print(f"  Parameters: {len(policy.parameters_ls)}")
        print(f"  Users: {len(policy.user_ls)}")
        print(f"  Groups: {len(policy.group_ls)}")
        
        return policy
    except pdp.SearchPDP_NotFound as e:
        print(f"Policy not found: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


async def test_cell_5_search_pdp_policy(token_auth=token_auth):
    """Test searching for PDP policies by name."""
    if not TEST_DATASET_ID:
        print("Skipping test - TEST_DATASET_ID not set")
        return None
    
    try:
        from dataclasses import dataclass
        
        @dataclass
        class MockDataset:
            id: str
            auth: dmda.DomoAuth
        
        mock_dataset = MockDataset(id=TEST_DATASET_ID, auth=token_auth)
        pdp_policies = pdp.Dataset_PDP_Policies.from_parent(parent=mock_dataset)
        
        # Get all policies first
        all_policies = await pdp_policies.get()
        
        if all_policies:
            # Try to search for the first policy by name
            first_policy_name = all_policies[0].name
            found_policy = await pdp_policies.search(
                search=first_policy_name,
                search_method="name",
                is_exact_match=True
            )
            
            print(f"Found policy by name: {found_policy.name}")
            assert found_policy.name == first_policy_name
            
            return found_policy
        else:
            print("No policies found to test search")
            return None
            
    except pdp.SearchPDP_NotFound as e:
        print(f"Search failed: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
