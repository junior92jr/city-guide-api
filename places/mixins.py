
class FourSquareUtilsMixin:
    """
    Utils class to process the main response from FourSquare Service.
    """
    
    @staticmethod
    def range_query(resource_response, search_radious):
        """
        Range Query by proximity using the search_radious parameter as base.
        
        :param resource_response: List of Items from the main response
        :param search_radious: Integer parameter

        :return: List of objects, Filtered Data
        """

        return [item for item in resource_response if item['distance'] <= search_radious]

    @staticmethod
    def filter_by_category(resource_response, category):
        """
        Filter items by category parameter.
        
        :param resource_response: List of Items from the main response
        :param category: Interger ID for category from main response

        :return: List of objects, Filtered Data
        """

        filtered_response = []

        for place in resource_response:
            for category_item in place.get('categories'):
                if category_item.get('id') == category:
                    filtered_response.append(place)

        return filtered_response

    @staticmethod
    def get_categories(resource_response):
        """
        Get Not Repeated Categories from Original Response.
        
        :param resource_response: List of Items from the main response

        :return: List of objects
        """

        all_categories = []

        for place in resource_response:
            for catefory in place.get('categories'):
                all_categories.append(catefory)
        
        all_categories = [
            item for counter, item in enumerate(
                all_categories) if item not in all_categories[counter + 1:]]

        return all_categories
