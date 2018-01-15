from django import forms
from django.core.exceptions import ValidationError
from polls.models import Poll, Choice

MISSING_TEXT_ERROR = 'Poll needs to have text'
TWO_CHOICES_ERROR = 'Required to have at least two choices'


class NewPollForm(forms.Form):
    text = forms.CharField(
        max_length=100,
        error_messages={'required': MISSING_TEXT_ERROR},
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your question here...',
            'class': 'form-control form-control-lg'
        })
    )

    def __init__(self, *args, **kwargs):
        super(NewPollForm, self).__init__(*args, **kwargs)

        choice_attrs = {
            'placeholder': 'Enter a choice here...',
            'class': 'form-control'
        }

        if self.is_bound:
            choices = {
                k: v for k, v in self.data.items()
                if k.startswith('choice_')
            }
            for k, v in choices.items():
                self.fields[k] = forms.CharField(
                    label=k.split('_')[1],
                    max_length=50,
                    required=False,
                    widget=forms.TextInput(attrs=choice_attrs)
                )
        # we want the page to have at least 5 choices to start
        # even if the user submitted an invalid form
        for i in range(len(self.fields), 6):
            self.fields[f'choice_{i}'] = forms.CharField(
                label=str(i),
                max_length=50,
                required=False,
                widget=forms.TextInput(attrs=choice_attrs)
            )

    def clean(self):
        super().clean()
        new_data = self.cleaned_data.copy()
        choices = []
        for name, value in self.cleaned_data.items():
            if name.startswith('choice_') and value:
                choices.append(value)
        if len(choices) < 2:
            self.add_error(
                field=None,
                error=ValidationError(TWO_CHOICES_ERROR)
            )
        else:
            new_data['choices'] = choices
        return new_data

    def save(self):
        new_text = self.cleaned_data['text']
        self.poll = Poll.objects.create(text=new_text)
        for choice in self.cleaned_data['choices']:
            Choice.objects.create(text=choice, poll=self.poll)
