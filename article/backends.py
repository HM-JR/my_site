# -*- coding: utf-8 -*-

import json
import random
from django.core.cache import cache
from models import Tag, Music, Article, Classification, Links, CarouselImg
from constants import BlogStatus, CarouselImgType

CACHE_TIME = 600  # second


def get_articles(key):
    articles = []
    if key in cache:
        articles = cache.get(key)
    else:
        articles = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by("-publish_time")
        cache.set(key, articles, CACHE_TIME)
    return articles


def get_tags_and_musics(tag_key, music_key):
    color_array, music_list, tag_list = [
        '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'
    ], [], []
    if tag_key in cache:
        tag_list = cache.get(tag_key)
    else:
        tag_list = list(Tag.objects.all())
        for tag in tag_list:
            tag.color = '#' + ''.join(random.sample(color_array, 6))  # 为每个标签随机生成颜色
        random.shuffle(tag_list)  # random.shuffle()的返回值是none，改变的是原来的元素
        cache.set(tag_key, tag_list, CACHE_TIME)
    if music_key in cache:
        music_list = cache.get(music_key)
    else:
        musics = Music.objects.all()
        for item in musics:
            music_list.append({
                "name": item.name,
                "url": item.url,
                "cover": item.cover,
                "artist": item.artist,
                "lrc": item.lrc,
            })
        random.shuffle(music_list)
        cache.set(music_key, json.dumps(music_list[:3]), CACHE_TIME)

    return tag_list, music_list


def get_popular_top10_blogs(key):
    new_post = []
    if key in cache:
        new_post = cache.get(key)
    else:
        new_post = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-count')[:10]
        cache.set(key, list(new_post), 24 * CACHE_TIME)
    return new_post


def get_classifications(key):
    classification = []
    if key in cache:
        classification = cache.get(key)
    else:
        classification = Classification.class_list.get_classify_list()
        cache.set(key, classification, CACHE_TIME)
    return classification


def get_date_list(key):
    date_list = []
    if key in cache:
        date_list = cache.get(key)
    else:
        date_list = Article.date_list.get_article_by_date()
        cache.set(key, date_list, CACHE_TIME)
    return date_list


def get_archieve(key):
    archieve = []
    if key in cache:
        archieve = cache.get(key)
    else:
        archieve = Article.date_list.get_article_by_archive()
        cache.set(key, archieve, CACHE_TIME)
    return archieve


def get_links(key):
    links = []
    if key in cache:
        links = cache.get(key)
    else:
        links = list(Links.objects.all())
        cache.set(key, links, CACHE_TIME)
    return links


def get_carousel_imgs(key):
    carouse_imgs = []
    if key in cache:
        carouse_imgs = cache.get(key)
    else:
        carouse_imgs = CarouselImg.objects.filter(img_type=CarouselImgType.BANNER).order_by("-weights", "id")
        cache.set(key, carouse_imgs, CACHE_TIME)
    return carouse_imgs
