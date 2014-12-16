from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Survey(models.Model):
	created_at = models.DateTimeField( auto_now_add = True, editable = False )
	updated_at = models.DateTimeField( auto_now = True, editable = False )
	title = models.CharField( max_length = 255 )
	slug = models.SlugField( max_length = 255, blank = True, default = '' )
	published = models.BooleanField( default = True )
	author = models.ForeignKey( User, related_name = "surveys" )

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super(Survey, self).save(*args, **kwargs)

class Question( models.Model ):
	survey = models.ForeignKey( 'Survey' )
	text = models.CharField( max_length = 255 )
	help_text = models.TextField( null=True, blank=True )


	types_of_input = (
		("select", "select"),			# For "order of importance" questions
		("radio", "radio"),				# Single choice, multiple answer questions
		("checkbox", "checkbox"),		# Multiple choice questions
		("text", "text"),				# Short open questions
		("textarea", "textarea")		# Long open questions
	)

	input_type = models.CharField( max_length = 50, default = "text", choices = types_of_input )
	required = models.BooleanField( default = True )
	order = models.IntegerField( default = 1 )
	created_at = models.DateTimeField( auto_now_add = True, editable = False )
	choices = models.TextField( default = '', null = True, blank = True )

	def __unicode__(self):
		return self.text

class Answers( models.Model ):
	survey = models.ForeignKey( 'Survey' )
	question = models.ForeignKey( 'Question' )
	text = models.TextField( default = ' ', null=True )
	ip_address = models.GenericIPAddressField( default = "127.0.0.1")
	session_id = models.CharField( max_length = 255 )	# use uuid.uuid1() to generate a session ID

	def __unicode__(self):
		return unicode(self.text) or u''

	def save(self, *args, **kwargs):
		super(Answers, self).save(*args, **kwargs)