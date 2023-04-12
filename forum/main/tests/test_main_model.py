import pytest


def test_category(blog_category_factory):
    category = blog_category_factory.build()
    print(category.category_name)

    assert category.category_name == 'django'
    assert category.category_slug == 'django'


def test_sub_category(sub_category_factory):
    """
    Tests relationship between table SubCategory
    and table BlogCategory
    """
    sub_category_data = sub_category_factory.build()
    category = str(sub_category_data.category)

    assert sub_category_data.sub_category_name == 'Django models'
    assert sub_category_data.slug == 'django-models'
    assert category == 'django'


def test_post(post_factory):
    """
    Tests if relationship between table Post and
    tables BlogCategory, Author is correct
    """
    post_data = post_factory.build()
    post_cat = str(post_data.category)
    author = str(post_data.author)

    assert post_cat == 'Django models'
    assert author == 'Jonny Depp'





