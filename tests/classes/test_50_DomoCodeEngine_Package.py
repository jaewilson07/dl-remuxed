"""
Test file for DomoCodeEngine_Package class.

Tests the refactored CodeEngine entity classes following domolibrary2 standards.
"""

import os
from dotenv import load_dotenv

import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoCodeEngine as dmce

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

# Test constants - add these to your .env file
TEST_PACKAGE_ID = os.environ.get("TEST_CODEENGINE_PACKAGE_ID", "")
TEST_PACKAGE_VERSION = os.environ.get("TEST_CODEENGINE_VERSION", "1.0.0")


async def test_cell_0(token_auth=token_auth):
    """Setup test - verify authentication works."""
    assert token_auth is not None
    assert token_auth.domo_instance
    assert token_auth.domo_access_token
    print(f"✓ Authentication configured for instance: {token_auth.domo_instance}")
    return token_auth


async def test_cell_1(token_auth=token_auth):
    """Test DomoCodeEngine_Package.get_by_id() method."""
    if not TEST_PACKAGE_ID:
        print("⚠ TEST_PACKAGE_ID not set in environment, skipping test")
        return None

    package = await dmce.DomoCodeEngine_Package.get_by_id(
        auth=token_auth,
        package_id=TEST_PACKAGE_ID,
        debug_api=False,
    )

    assert package is not None, "Package should not be None"
    assert package.id == TEST_PACKAGE_ID, "Package ID should match"
    assert package.auth == token_auth, "Auth should be set"
    assert isinstance(package.raw, dict), "Raw should be a dictionary"
    assert package.name, "Package should have a name"
    
    print(f"✓ Retrieved package: {package.name} (ID: {package.id})")
    print(f"  Language: {package.language}")
    print(f"  Current Version: {package.current_version}")
    print(f"  Display URL: {package.display_url}")
    
    return package


async def test_cell_2(token_auth=token_auth):
    """Test DomoCodeEngine_Package.from_dict() method."""
    # Sample API response format
    sample_response = {
        "id": "test-package-123",
        "name": "Test Package",
        "description": "A test package",
        "language": "PYTHON",
        "environment": "PROD",
        "availability": "PUBLIC",
        "owner": 12345,
        "createdOn": "2024-01-01T00:00:00Z",
        "updatedOn": "2024-01-02T00:00:00Z",
        "functions": [],
        "versions": [],
    }

    package = dmce.DomoCodeEngine_Package.from_dict(
        auth=token_auth,
        obj=sample_response,
    )

    assert package.id == "test-package-123"
    assert package.name == "Test Package"
    assert package.language == "PYTHON"
    assert package.auth == token_auth
    
    print("✓ from_dict() creates package correctly")
    print(f"  Package: {package.name}")
    print(f"  Display URL: {package.display_url}")
    
    return package


async def test_cell_3(token_auth=token_auth):
    """Test DomoCodeEngine_Packages manager class - get all packages."""
    packages_manager = dmce.DomoCodeEngine_Packages(auth=token_auth)
    
    packages = await packages_manager.get(debug_api=False)
    
    assert isinstance(packages, list), "Should return a list of packages"
    print(f"✓ Retrieved {len(packages)} CodeEngine packages")
    
    if packages:
        sample_pkg = packages[0]
        print(f"  Sample package: {sample_pkg.name} (ID: {sample_pkg.id})")
        print(f"  Language: {sample_pkg.language}")
    
    return packages


async def test_cell_4(token_auth=token_auth):
    """Test DomoCodeEngine_Packages.search_by_name() method."""
    packages_manager = dmce.DomoCodeEngine_Packages(auth=token_auth)
    
    # Get all packages first to find a name to search for
    all_packages = await packages_manager.get(debug_api=False)
    
    if not all_packages:
        print("⚠ No packages found to test search")
        return None
    
    # Search for the first package by partial name
    search_term = all_packages[0].name[:5] if all_packages[0].name else "test"
    
    try:
        matches = await packages_manager.search_by_name(
            name=search_term,
            debug_api=False,
        )
        
        assert len(matches) > 0, "Should find at least one match"
        print(f"✓ Search for '{search_term}' found {len(matches)} package(s)")
        
        for pkg in matches[:3]:  # Show first 3 matches
            print(f"  - {pkg.name}")
        
        return matches
        
    except dmce.SearchCodeEngine_NotFound as e:
        print(f"⚠ No packages found matching '{search_term}'")
        print(f"  Error: {e}")
        return []


async def test_cell_5(token_auth=token_auth):
    """Test DomoCodeEngine_PackageVersion.get_by_id_and_version() method."""
    if not TEST_PACKAGE_ID or not TEST_PACKAGE_VERSION:
        print("⚠ TEST_PACKAGE_ID or TEST_PACKAGE_VERSION not set, skipping test")
        return None

    version = await dmce.DomoCodeEngine_PackageVersion.get_by_id_and_version(
        auth=token_auth,
        package_id=TEST_PACKAGE_ID,
        version=TEST_PACKAGE_VERSION,
        debug_api=False,
    )

    assert version is not None, "Version should not be None"
    assert version.package_id == TEST_PACKAGE_ID
    assert version.version == TEST_PACKAGE_VERSION
    assert version.auth == token_auth
    
    print(f"✓ Retrieved version: {version.version}")
    print(f"  Package ID: {version.package_id}")
    print(f"  Language: {version.language}")
    print(f"  Description: {version.description}")
    print(f"  Has code: {version.code is not None}")
    print(f"  Has Manifest: {version.Manifest is not None}")
    
    return version


async def test_cell_6(token_auth=token_auth):
    """Test DomoCodeEngine_Package.get_current_version() method."""
    if not TEST_PACKAGE_ID:
        print("⚠ TEST_PACKAGE_ID not set, skipping test")
        return None

    package = await dmce.DomoCodeEngine_Package.get_by_id(
        auth=token_auth,
        package_id=TEST_PACKAGE_ID,
        debug_api=False,
    )

    current_version = await package.get_current_version(debug_api=False)
    
    assert current_version is not None, "Current version should not be None"
    assert current_version.version == package.current_version
    
    print(f"✓ Current version: {current_version.version}")
    print(f"  Package: {package.name}")
    print(f"  Language: {current_version.language}")
    
    return current_version


async def test_cell_7(token_auth=token_auth):
    """Test DomoCodeEngine_Package.get_owner() method."""
    if not TEST_PACKAGE_ID:
        print("⚠ TEST_PACKAGE_ID not set, skipping test")
        return None

    package = await dmce.DomoCodeEngine_Package.get_by_id(
        auth=token_auth,
        package_id=TEST_PACKAGE_ID,
        debug_api=False,
    )

    if package.owner_id:
        owner = await package.get_owner(debug_api=False)
        
        assert owner is not None, "Owner should not be None"
        print(f"✓ Package owner: {owner.display_name}")
        print(f"  Email: {owner.email_address}")
        
        return owner
    else:
        print("⚠ Package has no owner_id set")
        return None


async def test_cell_8(token_auth=token_auth):
    """Test DomoCodeEngine_PackageVersion.download_source_code() method."""
    if not TEST_PACKAGE_ID or not TEST_PACKAGE_VERSION:
        print("⚠ TEST_PACKAGE_ID or TEST_PACKAGE_VERSION not set, skipping test")
        return None

    version = await dmce.DomoCodeEngine_PackageVersion.get_by_id_and_version(
        auth=token_auth,
        package_id=TEST_PACKAGE_ID,
        version=TEST_PACKAGE_VERSION,
        debug_api=False,
    )

    if version.code:
        file_path = await version.download_source_code(
            download_folder="/tmp/codeengine_test",
            debug_api=False,
        )
        
        print(f"✓ Downloaded source code to: {file_path}")
        print(f"  Code length: {len(version.code)} characters")
        
        # Show first few lines of code
        code_lines = version.code.split('\n')[:5]
        print("  First few lines:")
        for line in code_lines:
            print(f"    {line}")
        
        return file_path
    else:
        print("⚠ Version has no code to download")
        return None


async def test_cell_9(token_auth=token_auth):
    """Test DomoCodeEngine_PackageVersion equality comparison."""
    if not TEST_PACKAGE_ID or not TEST_PACKAGE_VERSION:
        print("⚠ TEST_PACKAGE_ID or TEST_PACKAGE_VERSION not set, skipping test")
        return None

    version1 = await dmce.DomoCodeEngine_PackageVersion.get_by_id_and_version(
        auth=token_auth,
        package_id=TEST_PACKAGE_ID,
        version=TEST_PACKAGE_VERSION,
        debug_api=False,
    )

    version2 = await dmce.DomoCodeEngine_PackageVersion.get_by_id_and_version(
        auth=token_auth,
        package_id=TEST_PACKAGE_ID,
        version=TEST_PACKAGE_VERSION,
        debug_api=False,
    )

    assert version1 == version2, "Same package versions should be equal"
    print(f"✓ Version equality works correctly")
    print(f"  {version1.package_id} v{version1.version} == {version2.package_id} v{version2.version}")
    
    return True


async def test_cell_10(token_auth=token_auth):
    """Test return_raw parameter on get_by_id()."""
    if not TEST_PACKAGE_ID:
        print("⚠ TEST_PACKAGE_ID not set, skipping test")
        return None

    raw_response = await dmce.DomoCodeEngine_Package.get_by_id(
        auth=token_auth,
        package_id=TEST_PACKAGE_ID,
        return_raw=True,
        debug_api=False,
    )

    assert hasattr(raw_response, 'response'), "Should return ResponseGetData object"
    assert hasattr(raw_response, 'is_success'), "Should have is_success attribute"
    assert raw_response.is_success, "Response should be successful"
    
    print("✓ return_raw parameter works correctly")
    print(f"  Response type: {type(raw_response)}")
    print(f"  Has response data: {raw_response.response is not None}")
    
    return raw_response


# Run all tests
async def run_all_tests():
    """Run all test functions in sequence."""
    print("=" * 60)
    print("Running DomoCodeEngine_Package Tests")
    print("=" * 60)
    
    tests = [
        ("Setup Authentication", test_cell_0),
        ("Get Package By ID", test_cell_1),
        ("Create Package from Dict", test_cell_2),
        ("Get All Packages", test_cell_3),
        ("Search Packages by Name", test_cell_4),
        ("Get Package Version", test_cell_5),
        ("Get Current Version", test_cell_6),
        ("Get Package Owner", test_cell_7),
        ("Download Source Code", test_cell_8),
        ("Version Equality", test_cell_9),
        ("Return Raw Response", test_cell_10),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 60)
        try:
            result = await test_func(token_auth)
            results.append((test_name, True, result))
        except Exception as e:
            print(f"✗ Test failed: {e}")
            results.append((test_name, False, str(e)))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    return results


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_all_tests())
