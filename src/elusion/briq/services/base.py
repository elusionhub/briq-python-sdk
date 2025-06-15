"""Base service class for all Briq SDK services."""

from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, ValidationError

from elusion.briq.config import BriqConfig
from elusion.briq.exceptions import BriqValidationError
from elusion.briq.http import HTTPClient
from elusion.briq.models.common import APIResponse, PaginatedResponse

# Type variable for generic model types
T = TypeVar("T", bound=BaseModel)


class BaseService:
    """Base class for all API services."""

    def __init__(self, http_client: HTTPClient, config: BriqConfig) -> None:
        """Initialize the service.

        Args:
            http_client: HTTP client instance.
            config: Briq configuration.
        """
        self.http_client = http_client
        self.config = config

    def _build_url(self, endpoint: str, resource_id: Optional[str] = None) -> str:
        """Build a full URL for an API endpoint.

        Args:
            endpoint: The endpoint name from config.ENDPOINTS.
            resource_id: Optional resource ID to append to the URL.

        Returns:
            Full URL for the endpoint.
        """
        url = self.config.get_endpoint_url(endpoint)
        if resource_id:
            url = f"{url}/{resource_id}"
        return url

    def _validate_and_serialize(
        self, data: Union[BaseModel, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate and serialize data for API requests.

        Args:
            data: Data to validate and serialize.

        Returns:
            Serialized data dictionary.

        Raises:
            BriqValidationError: If validation fails.
        """
        if isinstance(data, BaseModel):
            return data.model_dump(exclude_unset=True, by_alias=True)
        return data

    def _parse_response(
        self,
        response_data: Dict[str, Any],
        model_class: Type[T],
        is_list: bool = False,
        is_paginated: bool = False,
    ) -> Any:
        """Parse API response into typed models.

        Args:
            response_data: Raw response data from API.
            model_class: Pydantic model class to parse data into.
            is_list: Whether the response data is a list.
            is_paginated: Whether the response is paginated.

        Returns:
            Parsed response with typed data.

        Raises:
            BriqValidationError: If response parsing fails.
        """
        try:
            if is_paginated:
                return PaginatedResponse[model_class].model_validate(response_data)
            elif is_list:
                if "data" in response_data:
                    parsed_data = [
                        model_class.model_validate(item)
                        for item in response_data["data"]
                    ]
                    return APIResponse[List[model_class]](
                        success=response_data.get("success", True),
                        data=parsed_data,
                        message=response_data.get("message"),
                        error=response_data.get("error"),
                    )
                else:
                    parsed_data = [
                        model_class.model_validate(item) for item in response_data
                    ]
                    return APIResponse[List[model_class]](
                        success=True,
                        data=parsed_data,
                        message=None,
                        error=None,
                    )
            else:
                if "data" in response_data:
                    parsed_data = model_class.model_validate(response_data["data"])
                    return APIResponse[model_class](
                        success=response_data.get("success", True),
                        data=parsed_data,
                        message=response_data.get("message"),
                        error=response_data.get("error"),
                    )
                else:
                    parsed_data = model_class.model_validate(response_data)
                    return APIResponse[model_class](
                        success=True,
                        data=parsed_data,
                        message=None,
                        error=None,
                    )

        except ValidationError as e:
            raise BriqValidationError(
                f"Failed to parse response: {str(e)}",
                validation_errors={"errors": e.errors()},
            ) from e

    def _build_query_params(
        self, params: Optional[BaseModel]
    ) -> Optional[Dict[str, Any]]:
        """Build query parameters from a Pydantic model.

        Args:
            params: Pydantic model with query parameters.

        Returns:
            Dictionary of query parameters, or None if params is None.
        """
        if params is None:
            return None

        # Convert to dict and remove None values
        param_dict = params.model_dump(exclude_unset=True, by_alias=True)

        # Convert datetime objects to ISO strings
        for key, value in param_dict.items():
            if hasattr(value, "isoformat"):
                param_dict[key] = value.isoformat()

        return param_dict

    # Async methods
    async def _get(
        self,
        endpoint: str,
        model_class: Type[T],
        resource_id: Optional[str] = None,
        params: Optional[BaseModel] = None,
    ) -> APIResponse[T]:
        """Make a GET request for a single resource.

        Args:
            endpoint: API endpoint name.
            model_class: Model class to parse response into.
            resource_id: Optional resource ID.
            params: Optional query parameters.

        Returns:
            Parsed API response.
        """
        url = self._build_url(endpoint, resource_id)
        query_params = self._build_query_params(params)

        response_data = await self.http_client.get(url, params=query_params)
        result: APIResponse[T] = self._parse_response(
            response_data, model_class, is_list=False, is_paginated=False
        )
        if not isinstance(result, APIResponse) or isinstance(getattr(result, "data", None), list):  # type: ignore[arg-type]
            raise BriqValidationError(
                "Expected a single APIResponse[T] but got a list or paginated response."
            )
        return result

    async def _list(
        self,
        endpoint: str,
        model_class: Type[T],
        params: Optional[BaseModel] = None,
        is_paginated: bool = False,
    ) -> APIResponse[List[T]]:
        """Make a GET request for a list of resources.

        Args:
            endpoint: API endpoint name.
            model_class: Model class to parse response items into.
            params: Optional query parameters.
            is_paginated: Whether the response is paginated.

        Returns:
            Parsed API response with list data.
        """
        url = self._build_url(endpoint)
        query_params = self._build_query_params(params)

        response_data = await self.http_client.get(url, params=query_params)
        return self._parse_response(
            response_data, model_class, is_list=True, is_paginated=is_paginated
        )

    async def _create(
        self,
        endpoint: str,
        data: Union[BaseModel, Dict[str, Any]],
        model_class: Type[T],
    ) -> APIResponse[T]:
        """Make a POST request to create a resource.

        Args:
            endpoint: API endpoint name.
            data: Data to create the resource with.
            model_class: Model class to parse response into.

        Returns:
            Parsed API response.
        """
        url = self._build_url(endpoint)
        serialized_data = self._validate_and_serialize(data)

        response_data = await self.http_client.post(url, data=serialized_data)
        return self._parse_response(response_data, model_class)

    async def _update(
        self,
        endpoint: str,
        resource_id: str,
        data: Union[BaseModel, Dict[str, Any]],
        model_class: Type[T],
    ) -> APIResponse[T]:
        """Make a PUT request to update a resource.

        Args:
            endpoint: API endpoint name.
            resource_id: ID of the resource to update.
            data: Data to update the resource with.
            model_class: Model class to parse response into.

        Returns:
            Parsed API response.
        """
        url = self._build_url(endpoint, resource_id)
        serialized_data = self._validate_and_serialize(data)

        response_data = await self.http_client.patch(url, data=serialized_data)
        return self._parse_response(response_data, model_class)

    async def _delete(
        self, endpoint: str, resource_id: str
    ) -> APIResponse[Dict[str, Any]]:
        """Make a DELETE request to delete a resource.

        Args:
            endpoint: API endpoint name.
            resource_id: ID of the resource to delete.

        Returns:
            Parsed API response.
        """
        url = self._build_url(endpoint, resource_id)

        response_data = await self.http_client.delete(url)
        return APIResponse[Dict[str, Any]](
            success=response_data.get("success", True),
            data=response_data.get("data", {"deleted": True}),
            message=response_data.get("message"),
            error=response_data.get("error"),
        )

    def _get_sync(
        self,
        endpoint: str,
        model_class: Type[T],
        resource_id: Optional[str] = None,
        params: Optional[BaseModel] = None,
    ) -> APIResponse[T]:
        """Make a sync GET request for a single resource."""
        url = self._build_url(endpoint, resource_id)
        query_params = self._build_query_params(params)

        response_data = self.http_client.get_sync(url, params=query_params)
        return self._parse_response(response_data, model_class)

    def _list_sync(
        self,
        endpoint: str,
        model_class: Type[T],
        params: Optional[BaseModel] = None,
        is_paginated: bool = False,
    ) -> APIResponse[List[T]]:
        """Make a sync GET request for a list of resources."""
        url = self._build_url(endpoint)
        query_params = self._build_query_params(params)

        response_data = self.http_client.get_sync(url, params=query_params)
        return self._parse_response(
            response_data, model_class, is_list=True, is_paginated=is_paginated
        )

    def _create_sync(
        self,
        endpoint: str,
        data: Union[BaseModel, Dict[str, Any]],
        model_class: Type[T],
    ) -> APIResponse[T]:
        """Make a sync POST request to create a resource."""
        url = self._build_url(endpoint)
        serialized_data = self._validate_and_serialize(data)

        response_data = self.http_client.post_sync(url, data=serialized_data)
        return self._parse_response(response_data, model_class)

    def _update_sync(
        self,
        endpoint: str,
        resource_id: str,
        data: Union[BaseModel, Dict[str, Any]],
        model_class: Type[T],
    ) -> APIResponse[T]:
        """Make a sync PUT request to update a resource."""
        url = self._build_url(endpoint, resource_id)
        serialized_data = self._validate_and_serialize(data)

        response_data = self.http_client.put_sync(url, data=serialized_data)
        return self._parse_response(response_data, model_class)

    def _delete_sync(
        self, endpoint: str, resource_id: str
    ) -> APIResponse[Dict[str, Any]]:
        """Make a sync DELETE request to delete a resource."""
        url = self._build_url(endpoint, resource_id)

        response_data = self.http_client.delete_sync(url)
        return APIResponse[Dict[str, Any]](
            success=response_data.get("success", True),
            data=response_data.get("data", {"deleted": True}),
            message=response_data.get("message"),
            error=response_data.get("error"),
        )
