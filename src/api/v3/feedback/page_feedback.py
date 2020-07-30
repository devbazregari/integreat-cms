import json

from django.http import HttpResponse

from cms.models import Page, PageFeedback, PageTranslation


class FeedbackData:
    """
    This class is a generic api representation of cms feedback incl. its meta information stored in the database.
    It is used to examine feedback sent to the feedback api endpoint.

    :param page_id: The id of the page this feedback is referring to, if empty the permalink is required, defaults to ``None``
    :type page_id: int, optional

    :param permalink: The permalink of the page this feedback is referring to, is empty the page_id is required, defaults to ``''``
    :type permalink: str, optional

    :param comment: The descriptive feedback string, defaults to ``''``
    :type comment: int, optional

    :param emotion: The emotion of the feedback, can be one of ``['Pos', 'Neg', 'NA']``, defaults to ``'NA'``
    :type emotion: int, optional
    """

    def __init__(self, page_id, permalink, comment, emotion):
        self.page_id = page_id
        self.permalink = permalink
        self.comment = comment
        self.emotion = emotion

    @classmethod
    def from_dict(cls, feedback_dict):
        return cls(
            feedback_dict.get("id", None),
            feedback_dict.get("permalink", None),
            feedback_dict.get("comment", None),
            feedback_dict.get("emotion", None),
        )

    def has_id(self):
        return self.__is_either_exist(self.page_id, self.permalink)

    def has_content(self):
        return self.__is_either_exist(self.comment, self.emotion)

    def get_comment(self):
        return self.comment if self.comment else ""

    def get_emotion(self):
        return self.emotion if self.emotion else "NA"

    @staticmethod
    def __is_either_exist(one, two):
        return one or two


# pylint: disable=unused-argument
def feedback(req, region_slug, languages):
    if req.method != "POST":
        return HttpResponse("Invalid request method.", status=405)

    data = json.loads(req.body)
    feedback_data = FeedbackData.from_dict(data)

    if not feedback_data.has_id():
        return HttpResponse(
            f'No page found for region "{region_slug}" with permalink "{feedback_data.permalink}".',
            content_type="text/plain",
            status=404,
        )

    if not feedback_data.has_content():
        return HttpResponse(
            "Please enter a valid rating/comment.",
            content_type="text/plain",
            status=400,
        )

    page = Page.objects.get(id=feedback_data.page_id)
    if not page:
        page_translation = PageTranslation.objects.get(
            permalink=feedback_data.permalink
        )
        page = page_translation.page

    try:
        page_feedback = PageFeedback(
            page=page,
            emotion=feedback_data.get_emotion(),
            comment=feedback_data.get_comment(),
        )
        page_feedback.save()
        return HttpResponse(status=200)
    except ValueError:
        return HttpResponse("Bad request.", content_type="text/plain", status=400)
