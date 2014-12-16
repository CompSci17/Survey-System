from django import forms
from .models import Question


class SurveyForm( forms.Form ):
	def __init__(self, *args, **kwargs):
		super(SurveyForm, self).__init__(*args, **kwargs)


	def add_questions( self, questions ):
		for question in questions:
			required = question.required

			if question.input_type == 'text':
				self.fields['%s' % question.id] = forms.CharField(max_length=255, label= question.text, required = required)

			elif question.input_type == 'textarea':
				self.fields['%s' % question.id] = forms.CharField(label= question.text, required = required, widget = forms.Textarea() )

			elif question.input_type == 'radio':
				CHOICES=[]

				choices_delimited = question.choices.split( ',' )

				for choice in choices_delimited:
					CHOICES.append((choice, choice))

				self.fields['%s' % question.id] = forms.ChoiceField(label= question.text, choices=CHOICES, widget=forms.RadioSelect(), required = required)

			elif question.input_type == 'select':
				CHOICES=[]

				choices_delimited = question.choices.split( ',' )

				for choice in choices_delimited:
					CHOICES.append((choice, choice))

				self.fields['%s' % question.id] = forms.ChoiceField(label= question.text, choices = CHOICES)

			elif question.input_type == 'checkbox':
				self.fields['%s' % question.id] = forms.BooleanField(label= question.text, required = required)