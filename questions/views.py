import random

from django.shortcuts import render, redirect
from .models import *
from .form import *

# Create your views here.
def index(request):
    shortQuestions = ShortQuestion.objects.all().order_by('created_at')
    multiChoiceQuestions = MultiChoiceQuestion.objects.all().order_by('created_at')
    essayQuestions = EssayQuestion.objects.all().order_by('created_at')
    context = {
        'shortQuestions' : shortQuestions,
        'essayQuestions' : essayQuestions,
        'multiChoiceQuestions' : multiChoiceQuestions,
    }
    return render(request, 'index.html', context)

def addShortQuestion(request):
    form = AddShortQuestion()

    if request.method == "POST":
        try:
            form = AddShortQuestion(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.save()
                return redirect("/")
        except Exception as e:
            print(e)
            raise
    context = {'form': form}
    return render(request, 'add_short_question.html', context)

def addEssayQuestion(request):
    form = AddEssayQuestion()
    if request.method == "POST":
        try:
            form = AddEssayQuestion(request.POST, request.FILES)
            if form.is_valid():
                question = form.save(commit=False)
                question.save()
                return redirect("/")
        except Exception as e:
            print(e)
            raise
    context = {'form': form}
    return render(request, 'add_essay_question.html', context)

def addMCQuestion(request):
    form = AddMCQuestion()
    if request.method == "POST":
        try:
            form = AddMCQuestion(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.save()
                return redirect('/add_mcq_add_choice/'+str(question.id))
        except Exception as e:
            print(e)
            raise
    context = {
        'form': form,
    }
    return render(request, 'add_mcq.html', context)

def addChoice(request, id):
    choices = Choices.objects.filter(mcq=id)
    multiChoiceQuestions = MultiChoiceQuestion.objects.get(id=id)
    print(choices)
    form = AddChoices()
    if request.method == "POST":
        form = AddChoices(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.mcq = MultiChoiceQuestion(id=id)
            choice.save()
            form = AddChoices()
            return redirect("/add_mcq_add_choice/"+str(id))
    context = {
        'form': form,
        'multiChoiceQuestions': multiChoiceQuestions,
        'choices': choices
    }
    print(choices)
    return render(request, 'add_mcq_add_choice.html', context)

def shortQuestionPage(request, id):
    short_response_form = ShortResponseForm()
    if request == "POST":
        try:
            short_response_form = ShortResponseForm(request.POST)
            if short_response_form.is_valid():
                short_response = short_response_form.save(commit=False)
                short_response.question = ShortQuestion(id=id)
                short_response.save()
                return redirect("/")
        except Exception as e:
            print(e)
            raise
    short_question = ShortQuestion.objects.get(id=id)
    context = {
        'short_question': short_question,
        'short_response_form': short_response_form
    }
    return render(request, 'ShortQuestion.html', context)

def deleteShortQuestion(request, id):
    short_question = ShortQuestion.objects.filter(id=id)
    short_question.delete()
    return redirect("/")
def deleteEssayQuestion(request, id):
    essay_question = EssayQuestion.objects.filter(id=id)
    essay_question.delete()
    return redirect("/")
def deleteChoice(request, id):
    choice = Choices.objects.get(id=id)
    choice.delete()
    return redirect("/mcq-question/"+str(choice.mcq.id))
def deleteMCQ(request, id):
    mcq_question = MultiChoiceQuestion.objects.filter(id=id)
    choice = Choices.objects.filter(id=id)
    mcq_question.delete()
    choice.delete()
    return redirect("/")
def deleteChoice_amcq(request, id):
    choice = Choices.objects.get(id=id)
    choice.delete()
    return redirect("/add_mcq_add_choice/"+str(choice.mcq.id))

def essayQuestionPage(request, id):
    essay_response_form = EssayResponseForm()
    if request.method == "POST":
        try:
            essay_response_form = EssayResponseForm(request.POST)
            if essay_response_form.is_valid():
                essay_response = essay_response_form.save(commit=False)
                essay_response.question = EssayQuestion(id=id)
                essay_response.save()
                return redirect("/")
        except Exception as e:
            print(e)
            raise
    essay_question = EssayQuestion.objects.get(id=id)
    context = {
        'essay_question': essay_question,
        'essay_response_form': essay_response_form
    }
    return render(request, 'EssayQuestion.html', context)
def MCQuestionPage(request, id):
    mcq_question = MultiChoiceQuestion.objects.get(id=id)
    choices = Choices.objects.filter(mcq=id)
    form = AddChoices()
    if request.method == "POST":
        form = AddChoices(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.mcq = MultiChoiceQuestion(id=id)
            choice.save()
            form = AddChoices()
            return redirect("/mcq-question/" + str(id))
    context = {
        'mcq_question': mcq_question,
        'choices': choices,
        'form': form
    }
    return render(request, 'MCQ.html', context)

def createCategory(request):
    form = CreateCategory()
    if request.method == "POST":
        form = CreateCategory(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            form = CreateCategory()
            return redirect("/create-category-add-question/"+ str(question.id))
    context = {
        'form': form,
    }
    return render(request, 'create_category.html', context)
def addQuestionToCategory(request, id):
    shortQuestions = ShortQuestion.objects.all()
    essayQuestions = EssayQuestion.objects.all()
    multiChoiceQuestions = MultiChoiceQuestion.objects.all()
    shortQuestionsCat = ShortQuestion.objects.filter(category=id)
    essayQuestionsCat = EssayQuestion.objects.filter(category=id)
    multiChoiceQuestionsCat = MultiChoiceQuestion.objects.filter(category=id)
    category = Question.objects.get(id=id)
    print(id)
    print(shortQuestionsCat)
    print(shortQuestions.values_list('category'))
    context = {
        'shortQuestions': shortQuestions,
        'essayQuestions': essayQuestions,
        'multiChoiceQuestions': multiChoiceQuestions,
        'shortQuestionsCat':shortQuestionsCat,
        'essayQuestionsCat':essayQuestionsCat,
        'multiChoiceQuestionsCat': multiChoiceQuestionsCat,
        'category': category,
    }
    return render(request, 'create_category_add_question.html', context)

def addShortQuestionToCategory(request, id, id2):
    category = Question.objects.get(id=id)
    question = ShortQuestion.objects.filter(id=id2).update(category=id)
    return redirect("/create-category-add-question/" + str(category.id))
def addEssayQuestionToCategory(request, id, id2):
    category = Question.objects.get(id=id)
    question = EssayQuestion.objects.filter(id=id2).update(category=id)
    return redirect("/create-category-add-question/" + str(category.id))
def addMCQToCategory(request, id, id2):
    category = Question.objects.get(id=id)
    question = MultiChoiceQuestion.objects.filter(id=id2).update(category=id)

    return redirect("/create-category-add-question/" + str(category.id))