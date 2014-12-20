import uuid

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Survey, Question, Answers
from .forms import SurveyForm
from .results import Results

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
	form = SurveyForm( request.POST or None, questions=questions )

	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		
		# check whether it's valid:
		if form.is_valid():
			answers = []
			for question in questions:
				answer = Answers( )
				answer.survey = survey
				answer.question = question

				answers = form.cleaned_data[ str( question.pk ) ]

				if type( answers ) is list:
					for individualAnswer in answers:
						answer.text = answer.text + individualAnswer + ", "
					answer.text = answer.text[:-2]
					answer.text = answer.text.replace("  ", "").replace(", ", "")

				else:
					answer.text = answers

				answer.session_id = uuid.uuid1( ) 
				answer.save()

			# redirect to a new URL:
			#return HttpResponseRedirect('/thanks/')


	context = {
		"survey" : survey,
		"page_title": survey.title,
		"form": form,
	}

	return render( request, template_name, context )

def survey_results( request, pk, *args, **kwargs ):
	survey = Survey.objects.get( pk = pk, published = True )
	questions = Question.objects.filter( survey__exact = survey )
	template_name = "survey_results.html"

	results = Results( )
	answers = results.render_results( questions, survey )
	output = ''

	charts = []
	chart_ids = ""

	for input_type, answer, input_id in answers:
		if input_type == "text" or input_type == "textarea":

			question = Question.objects.get( pk = input_id )
			output += """
						<table>
							<tr>
								<th> %s </th>
							</tr>
					  """ % ( question.text )

 			for indiv_answer in answer:
 				output += """
							<tr>
								<td> %s </td>
							</tr>
						  """ % ( indiv_answer )

 			output += """
						</table>
					   """
		else:
			charts.append( answer )
			chart_ids += "container_" + str( input_id ) + ","
			output += " \n <div id='container_" + str( input_id ) + "'> Chart </div>"

	context = {
		"page_title": survey.title + " Results",
		"answers": answers,
		"output": output,
		"charts": charts,
		"chart_ids": chart_ids
	}

	return render( request, template_name, context )


