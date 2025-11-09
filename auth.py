"""
Authentication and API request handling for MyBillBook
"""

import requests
import time
from typing import Optional, Dict, Any
from config import get_headers, BASE_URL, REQUEST_TIMEOUT, RETRY_ATTEMPTS, RETRY_DELAY


class MyBillBookAPI:
    """Handles API requests to MyBillBook"""

    def __init__(self):
        self.base_url = BASE_URL
        self.headers = get_headers()
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        retry_count: int = 0,
    ) -> Optional[Dict[str, Any]]:
        """
        Make an API request with retry logic

        Args:
            endpoint: API endpoint path
            method: HTTP method (GET, POST, etc.)
            params: Query parameters
            data: Request body data
            retry_count: Current retry attempt

        Returns:
            Response JSON or None if failed
        """
        url = f"{self.base_url}{endpoint}"

        try:
            if method == "GET":
                response = self.session.get(
                    url, params=params, timeout=REQUEST_TIMEOUT
                )
            elif method == "POST":
                response = self.session.post(
                    url, json=data, params=params, timeout=REQUEST_TIMEOUT
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Check if request was successful
            response.raise_for_status()

            # Return JSON response
            return response.json()

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            if response.status_code == 401:
                print("Authentication failed. Please check your credentials.")
                return None
            elif response.status_code == 429:
                print("Rate limit exceeded. Waiting before retry...")
                if retry_count < RETRY_ATTEMPTS:
                    time.sleep(RETRY_DELAY * (retry_count + 1))
                    return self._make_request(
                        endpoint, method, params, data, retry_count + 1
                    )
            else:
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text}")

        except requests.exceptions.ConnectionError:
            print("Connection error. Please check your internet connection.")
            if retry_count < RETRY_ATTEMPTS:
                print(f"Retrying... (Attempt {retry_count + 1}/{RETRY_ATTEMPTS})")
                time.sleep(RETRY_DELAY)
                return self._make_request(
                    endpoint, method, params, data, retry_count + 1
                )

        except requests.exceptions.Timeout:
            print("Request timed out.")
            if retry_count < RETRY_ATTEMPTS:
                print(f"Retrying... (Attempt {retry_count + 1}/{RETRY_ATTEMPTS})")
                time.sleep(RETRY_DELAY)
                return self._make_request(
                    endpoint, method, params, data, retry_count + 1
                )

        except Exception as e:
            print(f"Unexpected error: {e}")

        return None

    def get_bulk_upload_status(self) -> Optional[Dict[str, Any]]:
        """
        Fetch the bulk upload status which contains all inventory items

        Returns:
            Dictionary containing all uploaded items or None if failed
        """
        print("Fetching inventory data from bulk upload status...")
        # Try with query parameters
        params = {
            "upload_type": "item"
        }
        return self._make_request("/bulk_upload/status", params=params)

    def get_items_stats(self) -> Optional[Dict[str, Any]]:
        """
        Fetch items statistics

        Returns:
            Dictionary containing item statistics or None if failed
        """
        print("Fetching items statistics...")
        return self._make_request("/items/stats")

    def get_all_items(self, per_page: int = 500) -> Optional[Dict[str, Any]]:
        """
        Fetch all inventory items from the items API

        Args:
            per_page: Number of items to fetch per page (default 500)

        Returns:
            Dictionary containing all items or None if failed
        """
        print("Fetching all inventory items...")
        params = {
            "page": 1,
            "per_page": per_page
        }
        return self._make_request("/items", params=params)

    def test_connection(self) -> bool:
        """
        Test if the API connection and authentication are working

        Returns:
            True if connection successful, False otherwise
        """
        print("Testing API connection...")
        # Use bulk_upload_status as the test endpoint since it doesn't require params
        result = self._make_request("/bulk_upload/status")
        if result:
            print("[OK] Connection successful!")
            return True
        else:
            print("[FAIL] Connection failed. Please check your credentials.")
            return False
