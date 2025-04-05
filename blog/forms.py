from django import forms
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class CommentForm(forms.ModelForm):
  class Meta:
      model = Comment
      fields = ["content"]

  def __init__(self, *args, **kwargs):
      super(CommentForm, self).__init__(*args, **kwargs)
      self.helper = FormHelper()
      self.helper.add_input(Submit('submit', 'Submit'))
