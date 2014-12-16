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
				CHOICES = self.get_choices( question.choices )

				self.fields['%s' % question.id] = forms.ChoiceField(label= question.text, choices=CHOICES, widget=forms.RadioSelect(), required = required)

			elif question.input_type == 'select':
				CHOICES = self.get_choices( question.choices )

				self.fields['%s' % question.id] = forms.ChoiceField(label= question.text, choices = CHOICES,  widget=forms.Select(attrs={'required': required}))

			elif question.input_type == 'checkbox':
				CHOICES = self.get_choices( question.choices )

				self.fields['%s' % question.id] = forms.MultipleChoiceField(label= question.text, choices = CHOICES, widget=forms.CheckboxSelectMultiple(), required = required)

			elif question.input_type == 'order':
				CHOICES = self.get_choices( question.choices )

				self.fields['%s' % question.id] = forms.MultipleChoiceField(label= question.text, 
																	choices=CHOICES, 
																	widget=forms.CheckboxSelectMultiple(attrs={'class': "sortable"}),
																	required = required,
																	)

	def get_choices( self, choices ):
		CHOICES=[]

		choices_delimited = choices.split( ',' )

		for choice in choices_delimited:
			CHOICES.append((choice, choice))

		return CHOICES

