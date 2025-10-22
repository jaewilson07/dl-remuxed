__all__ = [
    "PDP_Parameter",
    "PDP_Policy",
    "Dataset_PDP_Policies",
    # Route exceptions
    "PDP_GET_Error",
    "SearchPDP_NotFound",
    "PDP_CRUD_Error",
]

from dataclasses import dataclass, field
from typing import Optional, List, Union
import datetime as dt

import httpx

from ...client.auth import DomoAuth
from ...client.entities import DomoEntity, DomoSubEntity
from ...routes import pdp as pdp_routes
from ...routes.pdp import (
    PDP_GET_Error,
    SearchPDP_NotFound,
    PDP_CRUD_Error,
)
from ...utils import DictDot as util_dd, chunk_execution as ce


@dataclass
class PDP_Parameter:
    """PDP policy parameter defining filter conditions.
    
    Parameters specify which column values users can see based on
    filter conditions like EQUALS, GREATER_THAN, etc.
    
    Attributes:
        column_name: Name of the column to filter on
        column_values_ls: List of column values to filter
        operator: Comparison operator (default: "EQUALS")
        ignore_case: Whether to ignore case when comparing (default: True)
        type: Parameter type - "COLUMN" or "DYNAMIC" (default: "COLUMN")
    """
    column_name: str
    column_values_ls: list
    operator: str = "EQUALS"  # EQUALS, GREATER_THAN, LESS_THAN, etc.
    ignore_case: bool = True
    type: str = "COLUMN"  # COLUMN or DYNAMIC
    
    def to_dict(self) -> dict:
        """Convert parameter to API request format.
        
        Returns:
            Dictionary representation for API requests
        """
        return pdp_routes.generate_policy_parameter_simple(
            column_name=self.column_name,
            type=self.type,
            column_values_ls=self.column_values_ls,
            operator=self.operator,
            ignore_case=self.ignore_case,
        )
    
    @classmethod
    def from_dict(cls, obj: dict) -> "PDP_Parameter":
        """Create parameter from API response dictionary.
        
        Args:
            obj: Dictionary from API response
            
        Returns:
            PDP_Parameter instance
        """
        return cls(
            column_name=obj.get("name", ""),
            column_values_ls=obj.get("values", []),
            operator=obj.get("operator", "EQUALS"),
            ignore_case=obj.get("ignoreCase", True),
            type=obj.get("type", "COLUMN"),
        )


@dataclass
class PDP_Policy(DomoEntity):
    """A PDP (Personalized Data Permissions) policy for a dataset.
    
    PDP policies control row-level data access based on user, group,
    or virtual user assignments with column-based filter parameters.
    
    Attributes:
        id: Policy ID (filter_group_id)
        auth: Authentication object
        raw: Raw API response data
        dataset_id: ID of the dataset this policy applies to
        name: Policy name
        parameters_ls: List of filter parameters (PDP_Parameter objects or dicts)
        user_ls: List of user IDs or DomoUser objects assigned to policy
        group_ls: List of group IDs or DomoGroup objects assigned to policy
        virtual_user_ls: List of virtual user IDs assigned to policy
    """
    
    # Required DomoEntity attributes
    id: str  # This is the filter_group_id
    auth: DomoAuth = field(repr=False)
    raw: dict = field(default_factory=dict, repr=False)
    
    # PDP-specific attributes
    dataset_id: str = ""
    name: str = ""
    parameters_ls: List[dict] = field(default_factory=list)
    user_ls: List[str] = field(default_factory=list)
    group_ls: List[str] = field(default_factory=list)
    virtual_user_ls: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Ensure ID is string type."""
        self.id = str(self.id)
    
    @property
    def display_url(self) -> str:
        """Return the Domo web URL for this PDP policy.
        
        Returns:
            URL to view the dataset with PDP policies
        """
        return f"https://{self.auth.domo_instance}.domo.com/datasources/{self.dataset_id}/details/data-settings/policies"

    @classmethod
    def from_dict(cls, auth: DomoAuth, obj: dict) -> "PDP_Policy":
        """Convert API response dictionary to PDP_Policy instance.
        
        Args:
            auth: Authentication object
            obj: Dictionary from API response
            
        Returns:
            PDP_Policy instance
        """
        dd = util_dd.DictDot(obj)
        
        return cls(
            auth=auth,
            id=str(dd.filterGroupId or ""),
            dataset_id=str(dd.dataSourceId or ""),
            name=dd.name or "",
            parameters_ls=dd.parameters or [],
            user_ls=dd.userIds or [],
            group_ls=dd.groupIds or [],
            virtual_user_ls=dd.virtualUserIds or [],
            raw=obj,
        )
    
    @classmethod
    async def get_by_id(
        cls,
        auth: DomoAuth,
        dataset_id: str,
        policy_id: str,
        return_raw: bool = False,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> "PDP_Policy":
        """Retrieve a PDP policy by its ID.
        
        Args:
            auth: Authentication object
            dataset_id: ID of the dataset
            policy_id: ID of the policy to retrieve
            return_raw: Return raw response without processing
            debug_api: Enable API debugging
            session: Optional HTTP client session
            
        Returns:
            PDP_Policy instance or ResponseGetData if return_raw=True
            
        Raises:
            PDP_GET_Error: If policy retrieval fails
        """
        # Get all policies and search for the specific one
        res = await pdp_routes.get_pdp_policies(
            auth=auth,
            dataset_id=dataset_id,
            debug_api=debug_api,
            session=session,
            return_raw=return_raw,
        )
        
        if return_raw:
            return res
        
        # Find the policy with matching ID
        policy_obj = next(
            (p for p in res.response if p.get("filterGroupId") == policy_id),
            None
        )
        
        if not policy_obj:
            raise SearchPDP_NotFound(
                search_criteria=f"policy_id: {policy_id}",
            )
        
        return cls.from_dict(auth=auth, obj=policy_obj)

    @classmethod
    async def create(
        cls,
        auth: DomoAuth,
        dataset_id: str,
        name: str,
        parameters_ls: List[dict],
        user_ids: Optional[List[str]] = None,
        group_ids: Optional[List[str]] = None,
        virtual_user_ids: Optional[List[str]] = None,
        override_same_name: bool = False,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> "PDP_Policy":
        """Create a new PDP policy.
        
        Args:
            auth: Authentication object
            dataset_id: ID of the dataset
            name: Policy name
            parameters_ls: List of parameter dictionaries
            user_ids: List of user IDs to assign
            group_ids: List of group IDs to assign
            virtual_user_ids: List of virtual user IDs to assign
            override_same_name: Allow duplicate policy names
            debug_api: Enable API debugging
            session: Optional HTTP client session
            
        Returns:
            PDP_Policy instance
            
        Raises:
            PDP_CRUD_Error: If policy creation fails
        """
        body = pdp_routes.generate_policy_body(
            policy_name=name,
            dataset_id=dataset_id,
            parameters_ls=parameters_ls,
            user_ids=user_ids,
            group_ids=group_ids,
            virtual_user_ids=virtual_user_ids,
        )
        
        res = await pdp_routes.create_policy(
            auth=auth,
            dataset_id=dataset_id,
            body=body,
            override_same_name=override_same_name,
            debug_api=debug_api,
            session=session,
        )
        
        return cls.from_dict(auth=auth, obj=res.response)
    
    async def update(
        self,
        name: Optional[str] = None,
        parameters_ls: Optional[List[dict]] = None,
        user_ids: Optional[List[str]] = None,
        group_ids: Optional[List[str]] = None,
        virtual_user_ids: Optional[List[str]] = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> "PDP_Policy":
        """Update this PDP policy.
        
        Args:
            name: New policy name (optional)
            parameters_ls: New parameter list (optional)
            user_ids: New user ID list (optional)
            group_ids: New group ID list (optional)
            virtual_user_ids: New virtual user ID list (optional)
            debug_api: Enable API debugging
            session: Optional HTTP client session
            
        Returns:
            Updated PDP_Policy instance
            
        Raises:
            PDP_CRUD_Error: If policy update fails
        """
        body = pdp_routes.generate_policy_body(
            policy_name=name or self.name,
            dataset_id=self.dataset_id,
            parameters_ls=parameters_ls or self.parameters_ls,
            policy_id=self.id,
            user_ids=user_ids if user_ids is not None else self.user_ls,
            group_ids=group_ids if group_ids is not None else self.group_ls,
            virtual_user_ids=virtual_user_ids if virtual_user_ids is not None else self.virtual_user_ls,
        )
        
        res = await pdp_routes.update_policy(
            auth=self.auth,
            dataset_id=self.dataset_id,
            policy_id=self.id,
            body=body,
            debug_api=debug_api,
            session=session,
        )
        
        # Update instance with new values
        updated_policy = self.from_dict(auth=self.auth, obj=res.response)
        self.name = updated_policy.name
        self.parameters_ls = updated_policy.parameters_ls
        self.user_ls = updated_policy.user_ls
        self.group_ls = updated_policy.group_ls
        self.virtual_user_ls = updated_policy.virtual_user_ls
        self.raw = updated_policy.raw
        
        return self
    
    async def delete(
        self,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ):
        """Delete this PDP policy.
        
        Args:
            debug_api: Enable API debugging
            session: Optional HTTP client session
            
        Raises:
            PDP_CRUD_Error: If policy deletion fails
        """
        await pdp_routes.delete_policy(
            auth=self.auth,
            dataset_id=self.dataset_id,
            policy_id=self.id,
            debug_api=debug_api,
            session=session,
        )


@dataclass
class Dataset_PDP_Policies(DomoSubEntity):
    """Manager for PDP policies belonging to a dataset.
    
    This class manages the collection of PDP policies for a specific dataset,
    providing methods to retrieve, search, create, and manage policies.
    
    Attributes:
        auth: Authentication object (inherited from parent)
        parent: Parent DomoDataset object
        parent_id: Dataset ID
        policies: List of PDP_Policy objects (cached)
    """
    
    auth: DomoAuth = field(repr=False)
    parent: any = None  # DomoDataset
    parent_id: str = ""
    policies: List[PDP_Policy] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize with parent's auth and ID."""
        if self.parent:
            self.auth = self.parent.auth
            self.parent_id = self.parent.id
    
    async def get(
        self,
        include_all_rows: bool = True,
        return_raw: bool = False,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> List[PDP_Policy]:
        """Get all PDP policies for this dataset.
        
        Args:
            include_all_rows: Include policy associations and filters
            return_raw: Return raw response without processing
            debug_api: Enable API debugging
            session: Optional HTTP client session
            
        Returns:
            List of PDP_Policy instances or ResponseGetData if return_raw=True
            
        Raises:
            PDP_GET_Error: If policy retrieval fails
        """
        res = await pdp_routes.get_pdp_policies(
            auth=self.auth,
            dataset_id=self.parent_id,
            include_all_rows=include_all_rows,
            debug_api=debug_api,
            session=session,
            return_raw=return_raw,
        )
        
        if return_raw:
            return res
        
        # Convert to PDP_Policy objects
        self.policies = [
            PDP_Policy.from_dict(auth=self.auth, obj=policy_obj)
            for policy_obj in res.response
        ]
        
        return self.policies
    
    async def search(
        self,
        search: str,
        search_method: str = "name",
        is_exact_match: bool = True,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> Union[PDP_Policy, List[PDP_Policy]]:
        """Search for PDP policies by name or ID.
        
        Args:
            search: Search term (policy name or ID)
            search_method: Search by "name" or "id"
            is_exact_match: Use exact matching for names
            debug_api: Enable API debugging
            session: Optional HTTP client session
            
        Returns:
            Single PDP_Policy (exact match) or list of PDP_Policy (partial match)
            
        Raises:
            SearchPDP_NotFound: If no policies match the search criteria
        """
        # Get all policies if not already cached
        if not self.policies:
            await self.get(debug_api=debug_api, session=session)
        
        if search_method == "name":
            if is_exact_match:
                policy = next(
                    (p for p in self.policies if p.name == search),
                    None
                )
                
                if not policy:
                    raise SearchPDP_NotFound(
                        search_criteria=f'name: "{search}" (exact match)',
                    )
                
                return policy
            else:
                matching_policies = [
                    p for p in self.policies
                    if search.lower() in p.name.lower()
                ]
                
                if not matching_policies:
                    raise SearchPDP_NotFound(
                        search_criteria=f'name containing: "{search}"',
                    )
                
                return matching_policies
        else:  # search by ID
            policy = next(
                (p for p in self.policies if p.id == search),
                None
            )
            
            if not policy:
                raise SearchPDP_NotFound(
                    search_criteria=f'policy_id: "{search}"',
                )
            
            return policy
    
    async def create_policy(
        self,
        name: str,
        parameters_ls: List[dict],
        user_ids: Optional[List[str]] = None,
        group_ids: Optional[List[str]] = None,
        virtual_user_ids: Optional[List[str]] = None,
        override_same_name: bool = False,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> PDP_Policy:
        """Create a new PDP policy for this dataset.
        
        Args:
            name: Policy name
            parameters_ls: List of parameter dictionaries
            user_ids: List of user IDs to assign
            group_ids: List of group IDs to assign
            virtual_user_ids: List of virtual user IDs to assign
            override_same_name: Allow duplicate policy names
            debug_api: Enable API debugging
            session: Optional HTTP client session
            
        Returns:
            Created PDP_Policy instance
            
        Raises:
            PDP_CRUD_Error: If policy creation fails
        """
        policy = await PDP_Policy.create(
            auth=self.auth,
            dataset_id=self.parent_id,
            name=name,
            parameters_ls=parameters_ls,
            user_ids=user_ids,
            group_ids=group_ids,
            virtual_user_ids=virtual_user_ids,
            override_same_name=override_same_name,
            debug_api=debug_api,
            session=session,
        )
        
        # Add to cached policies
        self.policies.append(policy)
        
        return policy
    
    async def toggle_pdp(
        self,
        is_enable: bool = True,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ):
        """Enable or disable PDP for this dataset.
        
        Args:
            is_enable: True to enable PDP, False to disable
            debug_api: Enable API debugging
            session: Optional HTTP client session
            
        Raises:
            PDP_CRUD_Error: If toggle operation fails
        """
        await pdp_routes.toggle_pdp(
            auth=self.auth,
            dataset_id=self.parent_id,
            is_enable=is_enable,
            debug_api=debug_api,
            session=session,
        )
