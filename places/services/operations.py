class PlaceOperations:
    """
    Operations for filtering mapped place-like responses by range or category.
    """

    @staticmethod
    def range_query(resource_response, search_radious):
        """
        Range query by proximity using the search_radious parameter as base.

        :param resource_response: List of items from the main response.
        :param search_radious: Integer parameter.

        :return: Filtered list of objects.
        """

        return [
            item for item in resource_response
            if item["distance"] <= search_radious
        ]

    @staticmethod
    def filter_by_category(resource_response, category):
        """
        Filter items by category parameter.

        :param resource_response: List of items from the main response.
        :param category: Integer ID for category from main response.

        :return: Filtered list of objects.
        """

        filtered_response = []

        for place in resource_response:
            for category_item in place.get("categories", []):
                if category_item.get("id") == category:
                    filtered_response.append(place)

        return filtered_response

    @staticmethod
    def get_categories(resource_response):
        """
        Get non repeated categories from original response.

        :param resource_response: List of items from the main response.

        :return: List of category objects.
        """

        all_categories = []

        for place in resource_response:
            for category_item in place.get("categories", []):
                all_categories.append(category_item)

        return [
            item for counter, item in enumerate(all_categories)
            if item not in all_categories[counter + 1:]
        ]
