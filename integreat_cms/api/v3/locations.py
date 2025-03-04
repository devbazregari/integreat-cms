"""
This module includes functions related to the locations/POIs API endpoint.
"""
from distutils.util import strtobool
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from ..decorators import json_response


def transform_poi(poi):
    """
    Function to create a JSON from a single poi object.

    :param poi: The poi object which should be converted
    :type poi: ~integreat_cms.cms.models.pois.poi.POI

    :return: data necessary for API
    :rtype: dict
    """
    if not poi:
        return {
            "id": None,
            "name": None,
            "address": None,
            "town": None,
            "state": None,
            "postcode": None,
            "region": None,
            "country": None,
            "latitude": None,
            "longitude": None,
        }
    return {
        "id": poi.id,
        "name": poi.default_translation.title,
        "address": poi.address,
        "town": poi.city,
        "state": None,
        "postcode": poi.postcode,
        "region": None,
        "country": poi.country,
        "latitude": poi.latitude,
        "longitude": poi.longitude,
    }


def transform_poi_translation(poi_translation):
    """
    Function to create a JSON from a single poi_translation object.

    :param poi_translation: The poi translation object which should be converted
    :type poi_translation: ~integreat_cms.cms.models.pois.poi_translation.POITranslation

    :return: data necessary for API
    :rtype: dict
    """

    poi = poi_translation.poi
    return {
        "id": poi_translation.id,
        "url": settings.BASE_URL + poi_translation.get_absolute_url(),
        "path": poi_translation.get_absolute_url(),
        "title": poi.default_translation.title,
        "modified_gmt": poi_translation.last_updated,  # deprecated field in the future
        "last_updated": timezone.localtime(poi_translation.last_updated),
        "excerpt": poi_translation.short_description,
        "content": poi_translation.content,
        "available_languages": poi_translation.available_languages_dict,
        "icon": poi.icon.url if poi.icon else None,
        "thumbnail": poi.icon.thumbnail_url if poi.icon else None,
        "website": poi.website if poi.website else None,
        "email": poi.email if poi.email else None,
        "phone_number": poi.phone_number if poi.phone_number else None,
        "location": transform_poi(poi),
        "hash": None,
    }


@json_response
# pylint: disable=unused-argument
def locations(request, region_slug, language_slug):
    """
    List all POIs of the region and transform result into JSON

    :param request: The current request
    :type request: ~django.http.HttpRequest

    :param region_slug: The slug of the requested region
    :type region_slug: str

    :param language_slug: The slug of the requested language
    :type language_slug: str

    :return: JSON object according to APIv3 locations endpoint definition
    :rtype: ~django.http.JsonResponse
    """
    region = request.region
    # Throw a 404 error when the language does not exist or is disabled
    region.get_language_or_404(language_slug, only_active=True)
    result = []
    pois = region.pois.prefetch_public_translations().filter(archived=False)
    if "on_map" in request.GET:
        try:
            location_on_map = strtobool(request.GET["on_map"])
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        pois = pois.filter(location_on_map=location_on_map)
    for poi in pois:
        translation = poi.get_public_translation(language_slug)
        if translation:
            result.append(transform_poi_translation(translation))

    return JsonResponse(
        result, safe=False
    )  # Turn off Safe-Mode to allow serializing arrays
