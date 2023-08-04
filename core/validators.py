import jdatetime

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator


@deconstructible
class MaxImageSizeValidator:
    message = _("The maximum size allowed for images is “%(max_size)s” MB.")
    code = "max_image_size"

    def __init__(self, max_size: int, message=None, code=None):
        self.max_size = max_size
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if int(value.size) > self.max_size * 1024 * 1024:
            params = {"max_size": self.max_size}
            raise ValidationError(self.message, code=self.code, params=params)
    
    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.message == other.message
            and self.code == other.code
            and self.max_size == other.max_size
        )


class MaxCurrentYearValidator(MaxValueValidator):
    def __init__(self, message=None):
        limit_value = jdatetime.date.today().year
        super().__init__(limit_value, message)
