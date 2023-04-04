"""
    This module handles the creation, 
    deletion, and updating of categories.
"""
from rest_framework.decorators import api_view
from accounts.com_lib import (
    is_admin, invalid_response, 
    required_data, success_response,
    paginate
)

from events.models import Category
from django.db.models import Q

sorts = ['updated', 'created', 'name', 'description', 'color']
orders = ['asc', 'desc']



@api_view(['GET', 'POST'])
@is_admin()
@paginate(
    page_size=10,
    search_fields=['name', 'description', 'hex_color'],
    order_fields=['updated', 'created', 'name', 'description', 'hex_color'],
    model=Category
)
def categorys(request, models, total_pages, page):
    return success_response(
        'Successfully retrieved categorys', {
            'categorys': [category.serialize() for category in models],
            'page': page,
            'per_page': 10,
            'total': len(models),
            'pages': total_pages,
        })



@api_view(['POST'])
@is_admin()
@required_data(['name', 'description', 'color', 'image'])
def create_category(request, data):
    """
        This view creates a new category.
    """

    # -- Check if the category already exists
    if Category.objects.filter(name=data['name']).exists():
        return invalid_response('Category already exists')

    # -- Create the category
    category = Category.objects.create(
        name=data['name'],
        description=data['description'],
        hex_color=data['color']
    )
    category.save()
    category.add_pic_from_base64(data['image'])

    return success_response(
        'Successfully created category',
        category.serialize()
    )



@api_view(['POST'])
@is_admin()
@required_data(['id', 'name', 'description', 'color'])
def update_category(request, data):
    """
        This view updates a category.
    """

    # -- Get the category
    try: category = Category.objects.get(id=data['id'])
    except Category.DoesNotExist: return invalid_response('Category does not exist')

    # -- Update the category
    category.name = data['name']
    category.description = data['description']
    category.hex_color = data['color']
    category.save()

    print(data)
    return success_response(
        'Successfully updated category',
        category.serialize()
    )



@api_view(['GET'])
@is_admin()
@required_data(['id'])
def get_category(request, data):
    """
        This view returns a category.
    """

    # -- Get the category
    try: category = Category.objects.get(id=data['id'])
    except Category.DoesNotExist: return invalid_response('Category does not exist')

    return success_response(
        'Successfully retrieved category',
        category.serialize()
    )



@api_view(['DELETE'])
@is_admin()
@required_data(['id'])
def delete_category(request, data):
    """
        This view deletes a category.
    """

    # -- Get the category
    try: category = Category.objects.get(id=data['id'])
    except Category.DoesNotExist: return invalid_response('Category does not exist')

    # -- Delete the category
    category.delete()

    return success_response('Successfully deleted category')



@api_view(['POST'])
@is_admin()
@required_data(['id', 'image'])
def upload_category_image(request, data):
    """
        This view uploads a category image.
    """

    # -- Get the category
    try: category = Category.objects.get(id=data['id'])
    except Category.DoesNotExist: return invalid_response('Category does not exist')

    # -- Upload the image
    res = category.add_pic_from_base64(data['image'])

    if res == False: return invalid_response('Invalid image')
    else: return success_response('Successfully uploaded category image')