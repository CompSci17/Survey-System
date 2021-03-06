import uuid
import hashlib

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Survey, Question, Answers
from .forms import SurveyForm
from .results import Results

# Create your views here.

def survey_list( request, *args, **kwargs ):
	# Get a list of all the surveys
	survey_list = Survey.objects.filter( published = True )

	template_name = "survey_list.html"
	context = {
		"survey_list": survey_list,
		"page_title": "Surveys"
	}

	return render( request, template_name, context )

def survey_detail( request, pk, *args, **kwargs ):
	# Get the survey we're working with
	survey = Survey.objects.get( pk = pk, published = True )

	# Get all the questions for the survey
	questions = Question.objects.filter( survey__exact = survey ).order_by( "order" )

	template_name = "survey_detail.html"

	#Get the survey form
	form = SurveyForm( request.POST or None, questions=questions )

	if survey.single_vote and request.COOKIES.has_key( "survey_" + hashlib.sha256( str( survey.pk ) ).hexdigest() ):
		# If the survey only allows 1 vote and the user has voted, load the thank you template
		template_name = "thanks.html"
	else:
		# if this is a POST request we need to process the form data
		if request.method == 'POST':
			
			if form.is_valid():
				# If form is valid, process the input
				
				answers = []
				for question in questions:
					# For every question, process the answer and save it to the Answers model
					answer = Answers( )
					answer.survey = survey
					answer.question = question

					answers = form.cleaned_data[ str( question.pk ) ]

					if type( answers ) is list:
						# If the input has multiple answers, concatenate them into a comma separated list
						for individualAnswer in answers:
							answer.text = answer.text + individualAnswer + ", "
						answer.text = answer.text[:-2]

					else:
						answer.text = answers

					answer.session_id = uuid.uuid1( ) 
					answer.save()
				template_name = "thanks.html"

	context = {
		"survey" : survey,
		"page_title": survey.title,
		"form": form,
	}

	# Create blank response
	response = HttpResponse()

	# Fill the response with the template render
	response = render( request, template_name, context )


	if request.method == 'POST' and form.is_valid() and survey.single_vote:
		# If form is submitted, the form is valid and the survey only allows 1 vote:
		# set a cookie to identify the user has voted
		response.set_cookie( "survey_" + hashlib.sha256( str( survey.pk ) ).hexdigest(), hashlib.sha256( str( survey.pk ) + ( survey.title ) ).hexdigest() , max_age = 30 * 24 * 60 * 60, httponly = True )

	# Return the rendered response
	return response

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

			if "email" not in question.text:
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
		elif input_type == "order_of_importance":
			question = Question.objects.get( pk = input_id )
			choices = results.get_choices( question.choices )

			counter = []
			max_score = 0

			output += "<h2>" + question.text + "</h2>"

			for choice in choices:
				answer_score = 0

				for column in xrange( 1, len( choices ) + 1 ):
					answer_score += ( len( choices ) + 1 - column ) * int( answer[ column ][ choice.strip().replace( ",", "" ) ] )

					max_score = answer_score if answer_score > max_score else max_score

				counter.append( ( choice.strip().replace( ",", "" ), answer_score ) )

			counter = sorted( counter, key=lambda answer: answer[1], reverse = True )

			for answer, score in counter:
				output += str( answer ) + '<br /> <meter value="' + str( score ) + '" min="0" max="' + str( max_score ) + '" >' + str( score ) + '</meter> <br /><br />'

		else:
			charts.append( answer )
			chart_ids += "container_" + str( input_id ) + ","
			output += " \n <div id='container_" + str( input_id ) + "'> Chart </div>"

	context = {
		"page_title": survey.title + " Results",
		"answers": answers,
		"output": output,
		"charts": charts,
		"chart_ids": chart_ids,
	}

	return render( request, template_name, context )


