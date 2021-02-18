from django.db import models



""" Game モデル """

class Game(models.Model):
    class Meta():
        db_table = 't_game'
        verbose_name = 'ゲーム'
        verbose_name_plural = 'ゲーム'

    id = models.AutoField(editable=False, primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title
