---
title: Blog
permalink: /blog/
---

# Blog

日々学んだことや考えたことをまとめていくブログです．

## シリーズ

{% assign visible_series = site.series | where: 'published', true | sort: 'title' %}

{% for series in visible_series %}
- [{{ series.title }}]({{ series.url | relative_url }})
{% else %}
準備中
{% endfor %}

## 単発記事

{% assign standalone_articles = site.articles | where: 'published', true | where_exp: 'article', 'article.series_id == nil' | sort: 'date' | reverse %}

{% for article in standalone_articles %}
- [{{ article.title }}]({{ article.url | relative_url }})
{% else %}
準備中
{% endfor %}
