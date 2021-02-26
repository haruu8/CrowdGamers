from django.db import models



""" タグモデル """

class Feature(models.Model):
    class Meta():
        db_table = 't_feature'
        verbose_name = '特徴'
        verbose_name_plural = '特徴'

    id = models.AutoField(editable=False, primary_key=True)
    feature = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.feature
