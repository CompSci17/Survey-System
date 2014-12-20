from .models import Answers, RadioResults, SelectResults
from chartit import DataPool, Chart

class Results( ):

	def render_results( self, questions, survey ):
		"""
		Sorts out logic behind how we present our answers.

		@param questions 	QuerySet 	Questions we're working with
		@param survey 		Object 		The survey we're rendering results for 


		@return Returns a tuple of answers to be utilised in the view.

		Text/Textarea are of the form: ( input_type, list_of_answers, survey_object )
		Every other input is of the form: ( input_type, chart_object, survey_object )
		"""

		# A list to hold our output tuples
		output = []
		for question in questions:
			# For every question in the QuerySet, we're going to check and process
			# it dependent on input type

			if question.input_type == 'text':

				# get question's results
				results = self.get_results( question )

				combined_results = []
				for result in results:
					# For every answer we have, put it inside a list
					combined_results.append( str( result.text ) )

				# Add our input type, list and primary key to our output list
				output.append( ( "text", combined_results, question.pk ) ) 

			elif question.input_type == 'textarea':
				# get question's results
				results = self.get_results( question )

				combined_results = []
				for result in results:
					# For every answer we have, put it inside a list
					combined_results.append( str( result.text ) )

				# Add our input type, list and primary key to our output list
				output.append( ( "textarea", combined_results, question.pk ) )  

			elif question.input_type == 'radio':

				# Get all the options offered by the question
				options = self.get_choices( question.choices )

				# Dictionary for counting the occurrences of a selection
				counter = {}

				# Get our question's results
				answers = self.get_results( question )


				for option in options:
					# For every option, add it to our dictionary; starting with 0
					counter.update( { option.strip().replace( ",", "" ) : 0 } )

				for answer in answers:
					# For every answer, increment the answer in the dictionary
					counter[ str( answer.text ).strip().replace( ",", "" ) ] += 1

				for option in options:

					# Check if the count for this question already exists
					existence_check = RadioResults.objects.filter( 
										survey__exact = survey, 
										question__exact = question, 
										answer__exact = option.strip().replace( ",", "" ) 
									)

					if existence_check.exists( ):
						# If it exists, pass in the primary key
						result = RadioResults( 
									pk = existence_check[0].pk,
									survey = survey,
									question = question,
									answer = option.strip().replace( ",", "" ),
									answer_count = counter[ str( option ).strip().replace( ",", "" ) ]
								)
					else: 
						# If it doesn't exist, leave out the primary key
						result = RadioResults( 
									survey = survey,
									question = question,
									answer = option.strip().replace( ",", "" ),
									answer_count = counter[ str( option ).strip().replace( ",", "" ) ]
								)

					# Save our set of results
					result.save()

				# Get our chart object for the list
				piechart = self.radio_pie_chart( question )

				# Add our input type, chart object and primary key to our output list
				output.append( ( "radio", piechart, question.pk ) )
					

			elif question.input_type == 'select':
				
				# Get all the options offered by the question
				options = self.get_choices( question.choices )

				# Dictionary for counting the occurrences of a selection
				counter = {}

				# Get our question's results
				answers = self.get_results( question )


				for option in options:
					# For every option, add it to our dictionary; starting with 0
					counter.update( { option.strip().replace( ",", "" ) : 0 } )

				for answer in answers:
					# For every answer, increment the answer in the dictionary
					counter[ str( answer.text ).strip().replace( ",", "" ) ] += 1

				for option in options:

					# Check if the count for this question already exists
					existence_check = SelectResults.objects.filter( 
										survey__exact = survey, 
										question__exact = question, 
										answer__exact = option.strip().replace( ",", "" ) 
									)

					if existence_check.exists( ):
						# If it exists, pass in the primary key
						result = SelectResults( 
									pk = existence_check[0].pk,
									survey = survey,
									question = question,
									answer = option.strip().replace( ",", "" ),
									answer_count = counter[ str( option ).strip().replace( ",", "" ) ]
								)
					else: 
						# If it doesn't exist, leave out the primary key
						result = SelectResults( 
									survey = survey,
									question = question,
									answer = option.strip().replace( ",", "" ),
									answer_count = counter[ str( option ).strip().replace( ",", "" ) ]
								)

					# Save our set of results
					result.save()

				# Get our chart object for the list
				piechart = self.select_pie_chart( question )

				# Add our input type, chart object and primary key to our output list
				output.append( ( "select", piechart, question.pk ) )

				

			elif question.input_type == 'checkbox':
				# TODO
				options = self.get_choices( question.choices )

				

			elif question.input_type == 'order':
				# TODO
				options = self.get_choices( question.choices )

		return output

	def get_choices( self, choices ):
		"""
		Get all the chocies/options for a question, delimiting them 
		by comma.

		@param choices 	String 	String of choices from the question model

		@return A list of choices/options
		"""
		CHOICES=[]

		# Delimit our choices
		choices_delimited = choices.split( ',' )

		for choice in choices_delimited:
			# For every choice, append the value to a list
			CHOICES.append( str( choice ) )

		# Return a list of choices/options
		return CHOICES

	def get_results( self, question ):
		"""
		Get all the answers for a question

		@return QuerySet with all the answers for a question
		"""

		answers = Answers.objects.filter( question__exact = question )

		return answers

	def radio_pie_chart( request, question ):
		"""
		@return Piechart object for radio results
		"""

		ds = DataPool(
	   series=
		[{'options': {
			'source': RadioResults.objects.filter( question__exact = question )},
		  'terms': [
			'answer',
			'answer_count']}
		 ])

		chart = Chart(
				datasource = ds, 
				series_options = 
				  [{'options':{
					  'type': 'pie',
					  'stacking': False},
					'terms':{
					  'answer': [
						'answer_count']
					  }}],
				chart_options = 
				{
					'title': {
						'text': question.text
					}
				}
			)
		return chart

	def select_pie_chart( request, question ):
		"""
		@return Piechart object for select results
		"""

		ds = DataPool(
	   series=
		[{'options': {
			'source': SelectResults.objects.filter( question__exact = question )},
		  'terms': [
			'answer',
			'answer_count']}
		 ])

		chart = Chart(
				datasource = ds, 
				series_options = 
				  [{'options':{
					  'type': 'pie',
					  'stacking': False},
					'terms':{
					  'answer': [
						'answer_count']
					  }}],
				chart_options = 
				{
					'title': {
						'text': question.text
					}
				}
			)
		return chart