from django.core.exceptions import ValidationError



def user_directory_path(instance, filename):
    """
    user ごとにディレクトリを分ける。
    """
    return 'user_{0}/{1}'.format(instance.user.id, filename)



def team_directory_path(instance, filename):
    """
    チームごとにディレクトリを分ける。
    """
    return 'team_{0}/{1}'.format(instance.id, filename)



def validate_icon_image(fieldfile_obj):
    """
    アイコンの画像サイズに上限を設ける。
    """
    image_size = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if image_size > megabyte_limit*1024*1024:
        raise ValidationError("ファイルのサイズを%sMBより小さくしてください" % str(megabyte_limit))



def validate_header_image(fieldfile_obj):
    """
    ヘッダー画像のサイズに条件を設ける。
    """
    image_size = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if image_size > megabyte_limit*1024*1024:
        raise ValidationError("ファイルのサイズを%sMBより小さくしてください" % str(megabyte_limit))
