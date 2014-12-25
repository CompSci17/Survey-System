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
	survey = Survey.objects.get( pk = pk, published = True )
	questions = Question.objects.filter( survey__exact = survey ).order_by( "order" )
	template_name = "survey_detail.html"
	form = SurveyForm( request.POST or None, questions=questions )

	if survey.single_vote and request.COOKIES.has_key( "survey_" + hashlib.sha256( str( survey.pk ) ).hexdigest() ):
		template_name = "thanks.html"
	else:
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

	response = HttpResponse()
	response = render( request, template_name, context )
	if request.method == 'POST':
		if form.is_valid():
			if survey.single_vote:
				response.set_cookie( "survey_" + hashlib.sha256( str( survey.pk ) ).hexdigest(), hashlib.sha256( str( survey.pk ) + ( survey.title ) ).hexdigest() , max_age = 30 * 24 * 60 * 60, httponly = True )

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

			output += """
						<table class="importance">
							<tr>
								<th colspan="%d"> %s </th>
							</tr>
							<tr>
								<th></th>
					  """ % ( len( choices ) + 1, question.text )

			for i, option in enumerate( choices ):
				output += """
								<th> %d </th>
						  """ % ( i + 1 )

			output += " </tr>"

			for choice in choices:
				output += """
							<tr>
								<td> %s </td>
						  """ % ( choice )

				for column in xrange( 1, len( choices ) + 1 ):
					output += """
								<td> %s </td>
							  """ % ( answer[ column ][ choice.strip().replace( ",", "" ) ] )

				output += """
							</tr>
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
		"chart_ids": chart_ids,
	}

	return render( request, template_name, context )


