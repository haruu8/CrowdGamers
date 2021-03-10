from django.db import models



class Game(models.Model):
    """
    ゲームの選択肢を追加する
    """
    class Meta():
        db_table = 't_game'
        verbose_name = 'ゲーム'
        verbose_name_plural = 'ゲーム'

    id = models.AutoField(editable=False, primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title
