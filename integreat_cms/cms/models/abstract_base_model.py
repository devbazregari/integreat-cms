import logging

from django.db import models

from debug_toolbar.panels.sql.tracking import SQLQueryTriggered


logger = logging.getLogger(__name__)


class AbstractBaseModel(models.Model):
    """
    Abstract base class for all models
    """

    def get_repr(self):
        """
        Returns the canonical string representation of the content object

        To be implemented in the inheriting model
        """
        raise NotImplementedError

    def __repr__(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return
        ``<AbstractContentModel: AbstractContentModel object (id)>``.
        It tries to get the representation of the inheriting model, but falls back to a minimal representation in case
        the fields used in the ``get_repr()`` method do not exist yet (e.g. because other errors occurred)

        :return: The canonical string representation of the content object
        :rtype: str
        """
        try:
            return self.get_repr()
        # pylint: disable=broad-except
        except Exception as e:
            fallback_repr = f"<{type(self).__name__} (id: {self.id})>"
            if not isinstance(e, SQLQueryTriggered):
                logger.debug(
                    "repr() for object %s failed because of %s: %s",
                    fallback_repr,
                    type(e),
                    e,
                    exc_info=e,
                )
            return fallback_repr

    class Meta:
        #: This model is an abstract base class
        abstract = True
