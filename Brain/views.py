from django.shortcuts import render
from .clean_slate.qpsvc import QuestionClassifier
from .clean_slate.api import FileProcessor 
# from .clean_slate.genprocess import Brain
from home.models import Forms, Questions, QuestionAnswers
from django.http import JsonResponse

def output(request):
    form_data = get_form_data(9)
    
    if 'error' in form_data:
        print(form_data)
        return JsonResponse({'error': form_data['error']}, status=404)
    
    return render(request, 'Brain/output.html')


from home.models import Forms, Questions, QuestionAnswers

def get_form_data(form_identifier):
    try:
        form = Forms.objects.get(form_id=form_identifier)  # form_identifier can be form id or name
    except Forms.DoesNotExist:
        try:
            form = Forms.objects.get(title=form_identifier)  # If it's a name, fetch form by title
        except Forms.DoesNotExist:
            return {'error': 'Form not found'}

    questions = Questions.objects.filter(form=form)
    
    form_data = {
        'name': 'jordan',  # Example name, replace with actual logic if needed
        'questions': []
    }

    for question in questions:
        answers = QuestionAnswers.objects.filter(question=question)
        answer_texts = [answer.answer_text for answer in answers]

        form_data['questions'].append({
            'question': question.question_text,
            'answers': answer_texts
        })
    print(f"Form Data: {form_data}")

    return form_data

def another_view(request, form_identifier):
    form_data = get_form_data(9)
    
    if 'error' in form_data:
        print(form_data)
        return JsonResponse({'error': form_data['error']}, status=404)

    return JsonResponse(form_data)