from django.db import models



class LowerCharField(models.CharField):
    """
    大文字を小文字に自動変換するフィールド。
    ユーザーネームなどに使用している。
    """
    def get_prep_value(self, value):
        return str(value).lower()
