import uuid

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Survey, Question, Answers
from .forms import SurveyForm

# Create your views here.

def survey_list( request, *args, **kwargs ):
	survey_list = Survey.objects.filter( published = True )
	template_name = "survey_list.html"

	context = {
		"survey_list": survey_list,
		"page_title": "Surveys"
	}

	return render( request, template_name, context )

def survey_detail( request, pk, *args, **kwargs ):
	survey = Survey.objects.get( pk = pk, published = True )
	questions = Question.objects.filter( survey__exact = survey )
	template_name = "survey_detail.html"

	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		form = SurveyForm( request.POST )
		# check whether it's valid:
		if form.is_valid():
			for question in questions:
				answer = Answers( )
				answer.survey = survey
				answer.question = question
				answers = request.POST.getlist( str(question.pk), "" )

				for individualAnswer in answers:
					answer.text = answer.text + individualAnswer + ", "

				answer.text = answer.text[:-2]
				answer.session_id = uuid.uuid1( ) 
				answer.save()
				output = request.POST.get( str(question.pk), "" )

			# redirect to a new URL:
			#return HttpResponseRedirect('/thanks/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = SurveyForm( )


	form.add_questions( questions )


	context = {
		"survey" : survey,
		"page_title": survey.title,
		"form": form,
	}

	return render( request, template_name, context )

