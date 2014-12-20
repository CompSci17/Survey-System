from .models import Answers, RadioResults, SelectResults
from chartit import DataPool, Chart

class Results( ):
	def render_results( self, questions, survey ):
		output = []
		for question in questions:
			if question.input_type == 'text':
				results = self.get_results( question )
				combined_results = []
				for result in results:
					combined_results.append( str( result.text ) )

				output.append( ( "text", combined_results, question.pk ) ) 

			elif question.input_type == 'textarea':
				results = self.get_results( question )
				combined_results = []
				for result in results:
					combined_results.append( str( result.text ) )

				output.append( ( "textarea", combined_results, question.pk ) ) 

			elif question.input_type == 'radio':
				options = self.get_choices( question.choices )

				counter = {}

				answers = self.get_results( question )


				for option in options:
					counter.update( { option.strip().replace( ",", "" ) : 0 } )

				for answer in answers:
					counter[ str( answer.text ).strip().replace( ",", "" ) ] += 1

				for option in options:

					existence_check = RadioResults.objects.filter( 
										survey__exact = survey, 
										question__exact = question, 
										answer__exact = option.strip().replace( ",", "" ) 
									)

					if existence_check.exists( ):
						result = RadioResults( 
									pk = existence_check[0].pk,
									survey = survey,
									question = question,
									answer = option.strip().replace( ",", "" ),
									answer_count = counter[ str( option ).strip().replace( ",", "" ) ]
								)
					else: 
						result = RadioResults( 
									survey = survey,
									question = question,
									answer = option.strip().replace( ",", "" ),
									answer_count = counter[ str( option ).strip().replace( ",", "" ) ]
								)

					result.save()
				piechart = self.radio_pie_chart( question )
				output.append( ( "radio", piechart, question.pk ) )
					

			elif question.input_type == 'select':
				options = self.get_choices( question.choices )

				counter = {}

				answers = self.get_results( question )


				for option in options:
					counter.update( { option.strip().replace( ",", "" ) : 0 } )

				for answer in answers:
					counter[ str( answer.text ).strip().replace( ",", "" ) ] += 1

				for option in options:

					existence_check = SelectResults.objects.filter( 
										survey__exact = survey, 
										question__exact = question, 
										answer__exact = option.strip().replace( ",", "" ) 
									)

					if existence_check.exists( ):
						result = SelectResults( 
									pk = existence_check[0].pk,
									survey = survey,
									question = question,
									answer = option.strip().replace( ",", "" ),
									answer_count = counter[ str( option ).strip().replace( ",", "" ) ]
								)
					else: 
						result = SelectResults( 
									survey = survey,
									question = question,
									answer = option.strip().replace( ",", "" ),
									answer_count = counter[ str( option ).strip().replace( ",", "" ) ]
								)

					result.save()
				piechart = self.select_pie_chart( question )
				output.append( ( "select", piechart, question.pk ) )

				

			elif question.input_type == 'checkbox':
				options = self.get_choices( question.choices )

				

			elif question.input_type == 'order':
				options = self.get_choices( question.choices )

		return output

	def get_choices( self, choices ):
		CHOICES=[]

		choices_delimited = choices.split( ',' )

		for choice in choices_delimited:
			CHOICES.append( str( choice ) )

		return CHOICES

	def get_results( self, question ):
		answers = Answers.objects.filter( question__exact = question )

		return answers

	def radio_pie_chart( request, question ):

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