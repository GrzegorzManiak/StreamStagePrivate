"""
    This module handles the creation, 
    deletion, and updating of categories.
"""
from rest_framework.decorators import api_view
from accounts.com_lib import (
    is_admin, invalid_response, 
    required_data, success_response,
    authenticated
)

from events.models import Category
from django.db.models import Q

sorts = ['updated', 'created', 'name', 'description', 'color']
orders = ['asc', 'desc']



@api_view(['GET', 'POST'])
@authenticated()
@required_data(['page', 'sort', 'order', 'search'])
def categorys(request, data):
    """
        This view returns all categorys in the database in a formatted list.
        Some data is truncated to save performance.
    """

    # -- Make sure all the data is valid
    try: 
        page = int(data['page'])
        if page < 0: return invalid_response('Page must be greater than 0')
    except ValueError: return invalid_response('Page must be an integer')

    if data['sort'] not in sorts: return invalid_response('Invalid sort')
    if data['order'] not in orders: return invalid_response('Invalid order')

    # -- Get the categorys
    filter = {}

    # -- Sort
    match data['sort']:
        case 'updated': sort = 'updated'
        case 'created': sort = 'created'
        case 'name': sort = 'name'
        case 'description': sort = 'description'
        case 'color': sort = 'color'

    # -- Order
    if data['order'] == 'desc': sort = '-' + sort
    else: sort = sort

    # -- Get the categorys
    categorys = Category.objects.filter(**filter).order_by(sort)

    # -- Search
    if len(data['search']) > 3:
        categorys = categorys.filter(
            Q(name__icontains=data['search']) |
            Q(description__icontains=data['search']) |
            Q(color__icontains=data['search'])
        )

    # -- Pagination
    categorys = categorys[page*10:page*10+10]

    # -- Format the data
    categorys = [{
        'id': category.id,
        'name': category.name,
        'description': category.description,
        'color': category.color,
        'created': category.created,
        'updated': category.updated
    } for category in categorys]


    return success_response(
        'Successfully retrieved categorys', 
        categorys
    )



@api_view(['POST'])
@is_admin()
@required_data(['name', 'description', 'color'])
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
        color=data['color']
    )

    return success_response(
        'Successfully created category',
        {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'color': category.color,
            'created': category.created,
            'updated': category.updated
        }
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
    category.color = data['color']
    category.save()

    return success_response(
        'Successfully updated category',
        {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'color': category.color,
            'created': category.created,
            'updated': category.updated
        }
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
        {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'color': category.color,
            'created': category.created,
            'updated': category.updated
        }
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