from django import forms
from .models import Question
from captcha.fields import ReCaptchaField


class SurveyForm( forms.Form ):

	def __init__(self, *args, **kwargs):
		questions = kwargs.pop('questions')
		super(SurveyForm, self).__init__(*args, **kwargs)

		for question in questions:
			required = 'required' if question.required else ''

			if question.input_type == 'text':
				self.fields['%s' % question.id] = forms.CharField(max_length=255, label= question.text, required = True, widget = forms.TextInput( attrs = { required: required } ))

			elif question.input_type == 'textarea':
				self.fields['%s' % question.id] = forms.CharField(label= question.text, widget = forms.Textarea( attrs = { required: required } ) )

			elif question.input_type == 'radio':
				CHOICES = self.get_choices( question.choices )

				self.fields['%s' % question.id] = forms.ChoiceField(
													label = question.text, 
													choices = CHOICES, 
													widget = forms.RadioSelect( attrs = { required: required } )												)

			elif question.input_type == 'select':
				CHOICES = self.get_choices( question.choices )

				self.fields['%s' % question.id] = forms.ChoiceField(label= question.text, choices = CHOICES,  widget=forms.Select(attrs={ 'checked': 'checked' }), required = True )

			elif question.input_type == 'checkbox':
				CHOICES = self.get_choices( question.choices )

				self.fields['%s' % question.id] = forms.MultipleChoiceField(
													label= question.text, 
													choices = CHOICES, 
													widget=forms.CheckboxSelectMultiple( 
														attrs = { 'class' : 'multiple-choice' } 
													)
												)

			elif question.input_type == 'order':
				CHOICES = self.get_choices( question.choices )

				self.fields['%s' % question.id] = forms.MultipleChoiceField(label= question.text, 
													choices=CHOICES, 
													widget=forms.CheckboxSelectMultiple(
														attrs={'class': "sortable", 'checked': 'checked' }
													),
												)
		self.fields['captcha'] = ReCaptchaField( attrs={'theme' : 'clean'} )

	def get_choices( self, choices ):
		CHOICES=[]

		choices_delimited = choices.split( ',' )

		for choice in choices_delimited:
			CHOICES.append((choice, choice))

		return CHOICES

