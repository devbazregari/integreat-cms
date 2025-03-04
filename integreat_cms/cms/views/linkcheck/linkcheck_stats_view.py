import logging

from django.views.generic import View
from django.http import JsonResponse

from ...utils.linkcheck_utils import get_url_count

logger = logging.getLogger(__name__)


class LinkcheckStatsView(View):
    """
    Return the linkcheck counter stats
    """

    # pylint: disable=unused-argument
    def get(self, request, *args, **kwargs):
        r"""
        Retrieve the stats about valid/invalid/unchecked/ignored links

        :param request: The current request
        :type request: ~django.http.HttpResponse

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        # Link count
        count_dict = get_url_count(kwargs.get("region_slug"))
        return JsonResponse(count_dict)
