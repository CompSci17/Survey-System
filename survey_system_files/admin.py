from django.contrib import admin

# Register your models here.

from .models import Survey, Question


class SurveyAdmin( admin.ModelAdmin ):
	date_hierarchy = "created_at"
	fields = ( "published", "title", "slug" )
	list_display = [ "published", "title", "created_at", "updated_at" ]
	list_display_links = [ "title" ]
	list_editable = [ "published" ]
	list_filter = [ "published", "updated_at", "created_at" ]
	prepopulated_fields = { "slug": ( "title", ) }
	search_fields = [ "title", "created_at" ]

admin.site.register( Survey, SurveyAdmin )

class QuestionAdmin( admin.ModelAdmin ):
	fields = ( "survey", "text", "help_text", "input_type", "required", "order", "choices" )

admin.site.register( Question, QuestionAdmin )