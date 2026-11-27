from django import forms
from django.contrib.auth import get_user_model
from .models import HandoverEntry


User = get_user_model()


class HandoverEntryForm(forms.ModelForm):

    class Meta:
        model = HandoverEntry

        fields = [
            'title',
            'task_description',
            'progress',
            'instructions',
            'pending_work',
            'assigned_to',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter handover title'
            }),

            'task_description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe the task'
            }),

            'instructions': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter instructions for the next member'
            }),

            'pending_work': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter remaining work, if any'
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.requesting_user = user

        super().__init__(*args, **kwargs)

        self.fields['assigned_to'].queryset = User.objects.filter(
            role=User.Role.MEMBER,
            is_active=True
        ).order_by('username')

        self.fields['assigned_to'].required = False

        self.fields['assigned_to'].empty_label = 'Select a project member'

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()

        if not title:
            raise forms.ValidationError(
                'The handover title is required.'
            )

        return title

    def clean(self):
        cleaned_data = super().clean()

        assigned_to = cleaned_data.get('assigned_to')

        if (
            assigned_to
            and self.requesting_user
            and assigned_to.pk == self.requesting_user.pk
        ):
            self.add_error(
                'assigned_to',
                'You cannot assign the handover to yourself.'
            )

        return cleaned_data