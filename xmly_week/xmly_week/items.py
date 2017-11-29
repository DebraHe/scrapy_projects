import scrapy


class XmlyInfoItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    cover_pic = scrapy.Field()
    play_count = scrapy.Field()
    first_level = scrapy.Field()
    second_level = scrapy.Field()
    xmly_uploader_id = scrapy.Field()
    xmly_album_id = scrapy.Field()
    last_track = scrapy.Field()
    intro = scrapy.Field()


class XmlyDetailItem(scrapy.Item):
    url = scrapy.Field()
    uploader = scrapy.Field()
    uploader_cover = scrapy.Field()
    title = scrapy.Field()
    xmly_uploader_id = scrapy.Field()
    xmly_album_id = scrapy.Field()
    xmly_sound_id = scrapy.Field()
    track_in_album = scrapy.Field()
    track_play_count = scrapy.Field()
    track_upload_date = scrapy.Field()
    track_title = scrapy.Field()
    labels = scrapy.Field()
    row_number = scrapy.Field()
    first_level = scrapy.Field()
    second_level = scrapy.Field()
