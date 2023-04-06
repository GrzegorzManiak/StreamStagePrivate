from rest_framework.decorators import api_view
from django.shortcuts import render
from ..models import FAQ
from accounts.com_lib import (
    is_admin,
    invalid_response,
    success_response,
    required_data,
    paginate
)

#     question = models.CharField(max_length=100)
#     answer = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     section 
@api_view(['GET'])
def render_faq(request):
    # -- Get all FAQ's
    faq = FAQ.objects.all()

    # -- Filter them down into their sections
    sections = {}
    for f in faq:
        if f.section not in sections: sections[f.section.lower()] = []
        sections[f.section.lower()].append(f.serialize())

    # -- Render the page
    return render(
        request, 'faq.html',
        { 'sections': sections }
    )
    
@api_view(['POST'])
@is_admin()
@required_data(['answer', 'question', 'section'])
def create_faq(request, data):
    # -- Create the faq
    try: faq = FAQ.objects.create(answer=data['answer'], question=data['question'], section=data['section'])
    except Exception as e: return invalid_response(str(e))
    return success_response('faq', faq.serialize())



@api_view(['GET'])
@is_admin()
@paginate(
    page_size=10,
    search_fields=['question', 'answer', 'section'],
    order_fields=['created', 'updated', 'question', 'answer', 'section'],
    model=FAQ
)
def filter_faq(request, models, total_pages, page):

    # -- Return the response
    return success_response('faq', {
        'faq': [faq.serialize() for faq in models],
        'page': page,
        'per_page': 10,
        'total': len(models),
        'pages': total_pages,
    })



@api_view(['DELETE'])
@is_admin()
def delete_faq(request, faq_id):
    # -- Get the faq
    try: faq = FAQ.objects.get(id=faq_id)
    except FAQ.DoesNotExist: return invalid_response('FAQ not found', status=404)

    # -- Delete the faq
    faq.delete()
    return success_response('faq', faq.serialize())



@api_view(['PUT'])
@is_admin()
@required_data(['answer', 'question', 'section'])
def update_faq(request, data, faq_id):
    # -- Get the faq
    try: faq = FAQ.objects.get(id=faq_id)
    except FAQ.DoesNotExist: return invalid_response('FAQ not found', status=404)

    # -- Update the faq
    faq.answer = data['answer']
    faq.question = data['question']
    faq.section = data['section']
    faq.save()
    return success_response('faq', faq.serialize())