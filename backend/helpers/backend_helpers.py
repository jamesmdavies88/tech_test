@staticmethod
def get_total_pages(last_page):
    """
    Get the total number of pages from the last page link.

    :param last_page: URL of the last page.
    :return: Total number of pages.
    """
    return int(last_page.split("=")[-1])
