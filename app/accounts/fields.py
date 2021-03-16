from django.db import models



class LowerCharField(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()
