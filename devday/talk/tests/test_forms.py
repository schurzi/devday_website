import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import SimpleTestCase
from django.test import TestCase
from django.utils.timezone import now
from django_file_form.uploader import FileFormUploadBackend

from attendee.models import Attendee
from devday.utils.forms import DevDayFormHelper
from event.models import Event
from talk.forms import TalkForm, SpeakerForm, ExistingFileForm, DevDayRegistrationForm, CreateTalkForm, \
    TalkAuthenticationForm, BecomeSpeakerForm, CreateSpeakerForm, EditTalkForm, TalkCommentForm, TalkVoteForm, \
    TalkSpeakerCommentForm
from talk.models import Talk, TalkFormat, Speaker

try:
    from unittest import mock
except ImportError:  # Python 2.7 has no mock in unittest
    import mock

User = get_user_model()


class TalkFormTest(TestCase):
    def test_fields(self):
        form = TalkForm()
        self.assertListEqual(
            list(form.fields.keys()), ['title', 'abstract', 'remarks',
                                       'talkformat'])

    def test_model(self):
        form = TalkForm()
        talk = form.save(commit=False)
        self.assertIsInstance(talk, Talk)

    def test_widgets(self):
        form = TalkForm()
        self.assertIsInstance(form.fields['abstract'].widget, forms.Textarea)
        self.assertIsInstance(form.fields['remarks'].widget, forms.Textarea)


class SpeakerFormTest(TestCase):
    def test_fields(self):
        form = SpeakerForm()
        self.assertListEqual(
            list(form.fields.keys()),
            ['shortbio', 'videopermission', 'shirt_size', 'uploaded_image', 'form_id', 'upload_url', 'delete_url']
        )

    def test_save_uncommitted(self):
        request = HttpRequest()
        request.POST['qqfilename'] = 'mu_at_mil_house.jpg'
        request.POST['form_id'] = 'a_test_speaker_form'
        request.POST['field_name'] = 'uploaded_image'
        backend = FileFormUploadBackend()
        backend.setup(filename='testfile.jpg')
        backend.upload_chunk(open(os.path.join(os.path.dirname(__file__), 'mu_at_mil_house.jpg'), 'rb').read())
        uploaded_file = backend.upload_complete(request=request, filename='testfile.jpg', file_id='0815')
        data = {
            'shortbio': 'A short epic praising the glorious achievements of Example Tester.',
            'shirt_size': '3', 'form_id': 'a_test_speaker_form'
        }
        form = SpeakerForm(data=data)
        form.full_clean()
        speaker = form.save(commit=False)
        self.assertIsInstance(speaker, Speaker)
        self.assertIsNotNone(speaker.portrait.name)
        self.assertIsNone(speaker.id)

    def test_save_committed(self):
        request = HttpRequest()
        request.POST['qqfilename'] = 'mu_at_mil_house.jpg'
        request.POST['form_id'] = 'a_test_speaker_form'
        request.POST['field_name'] = 'uploaded_image'
        backend = FileFormUploadBackend()
        backend.setup(filename='testfile.jpg')
        backend.upload_chunk(open(os.path.join(os.path.dirname(__file__), 'mu_at_mil_house.jpg'), 'rb').read())
        uploaded_file = backend.upload_complete(request=request, filename='testfile.jpg', file_id='0815')
        user = User.objects.create_user(email='test@example.org')
        event = Event.objects.create(title="Test event", slug="test_event", start_time=now(), end_time=now())
        attendee = Attendee.objects.create(user=user, event=event)
        data = {
            'shortbio': 'A short epic praising the glorious achievements of Example Tester.',
            'shirt_size': '3', 'form_id': 'a_test_speaker_form',
        }
        form = SpeakerForm(data=data)
        form.full_clean()
        form.instance.user_id = attendee.id
        speaker = form.save(commit=True)
        self.assertIsInstance(speaker, Speaker)
        self.assertIsNotNone(speaker.portrait.name)
        self.assertIsNotNone(speaker.id)


class ExistingFileFormTest(SimpleTestCase):
    def test_get_upload_url(self):
        form = ExistingFileForm()
        self.assertEqual(
            form.get_upload_url(),
            reverse('talk_handle_upload')
        )


class DevDayRegistrationFormTest(TestCase):
    def test_fields(self):
        form = DevDayRegistrationForm()
        self.assertListEqual(
            list(form.fields.keys()),
            ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'twitter_handle', 'organization',
             'position']
        )

    def test_clean_no_email(self):
        form = DevDayRegistrationForm(data={
            'password1': 's3cr3t',
            'password2': 's3cr3t',
            'phone': '+49-815-1234567'
        })
        form.full_clean()
        self.assertIn('email', form.errors)

    def test_clean_email_becomes_username(self):
        form = DevDayRegistrationForm(data={
            'email': 'test@example.org',
            'password1': 's3cr3t',
            'password2': 's3cr3t',
            'phone': '+49-815-1234567'
        })
        form.full_clean()
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(form.cleaned_data.get(User.USERNAME_FIELD), 'test@example.org')


class CreateTalkFormTest(TestCase):
    def test_init_creates_form_helper(self):
        speaker = mock.Mock()
        form = CreateTalkForm(speaker=speaker)
        self.assertEqual(form.speaker, speaker)
        self.assertIsInstance(form.helper, FormHelper)
        self.assertEqual(form.helper.form_action, reverse('create_session'))
        self.assertEqual(form.helper.form_id, 'create-talk-form')
        self.assertEqual(form.helper.field_template, 'devday/form/field.html')
        self.assertTrue(form.helper.html5_required)

    def test_init_creates_layout(self):
        speaker = mock.Mock()
        form = CreateTalkForm(speaker=speaker)
        self.assertIsInstance(form.helper.layout, Layout)
        layout_fields = [name for [_, name] in
                         form.helper.layout.get_field_names()]
        self.assertEqual(len(layout_fields), 4)
        self.assertIn('title', layout_fields)
        self.assertIn('abstract', layout_fields)
        self.assertIn('remarks', layout_fields)
        self.assertIn('talkformat', layout_fields)

    def test_save(self):
        user = User.objects.create_user(email='test@example.org')
        tf = TalkFormat.objects.create(name='A Talk', duration=60)
        event = Event.objects.create(title="Test event", slug="test_event",
                                     start_time=now(), end_time=now())
        event.talkform = tf
        attendee = Attendee.objects.create(user=user, event=event)
        speaker = Speaker.objects.create(
            videopermission=True, user=attendee, shirt_size=1)
        form = CreateTalkForm(speaker=speaker, data={
            'title': 'Test',
            'abstract': 'Test abstract',
            'remarks': 'Test remarks',
            'talkformat': [tf.id],
        })
        talk = form.save(commit=False)
        self.assertIsInstance(talk, Talk)
        self.assertEqual(talk.speaker, speaker)


class EditTalkFormTest(TestCase):
    def test_init_creates_form_helper(self):
        form = EditTalkForm()
        self.assertIsInstance(form.helper, FormHelper)
        self.assertEqual(form.helper.field_template, 'devday/form/field.html')
        self.assertTrue(form.helper.html5_required)

    def test_init_creates_layout(self):
        form = EditTalkForm()
        self.assertIsInstance(form.helper.layout, Layout)
        layout_fields = [name for [_, name]
                         in form.helper.layout.get_field_names()]
        self.assertEqual(len(layout_fields), 4)
        self.assertIn('title', layout_fields)
        self.assertIn('abstract', layout_fields)
        self.assertIn('remarks', layout_fields)
        self.assertIn('talkformat', layout_fields)


class TalkAuthenticationFormTest(SimpleTestCase):
    def test_init_creates_form_helper(self):
        form = TalkAuthenticationForm()
        self.assertIsInstance(form.helper, FormHelper)
        self.assertEqual(form.helper.form_action, reverse('submit_session'))
        self.assertEqual(form.helper.form_method, 'post')
        self.assertEqual(form.helper.field_template, 'devday/form/field.html')
        self.assertTrue(form.helper.html5_required)

    def test_init_creates_layout(self):
        form = TalkAuthenticationForm()
        self.assertIsInstance(form.helper.layout, Layout)
        layout_fields = [name for [_, name] in form.helper.layout.get_field_names()]
        self.assertEqual(len(layout_fields), 2)
        self.assertIn('username', layout_fields)
        self.assertIn('password', layout_fields)


class BecomeSpeakerFormTest(SimpleTestCase):
    def test_init_creates_form_helper(self):
        form = BecomeSpeakerForm(devdayuserform_model=[])
        self.assertIsInstance(form.helper, FormHelper)
        self.assertEqual(form.helper.form_action, reverse('create_speaker'))
        self.assertEqual(form.helper.form_method, 'post')
        self.assertEqual(form.helper.form_id, 'create-speaker-form')
        self.assertEqual(form.helper.field_template, 'devday/form/field.html')
        self.assertTrue(form.helper.html5_required)

    def test_init_creates_layout(self):
        form = BecomeSpeakerForm(devdayuserform_model=[])
        self.assertIsInstance(form.helper.layout, Layout)
        layout_fields = [name for [_, name] in form.helper.layout.get_field_names()]
        expected_fields = [
            'upload_url', 'delete_url', 'form_id', 'first_name', 'last_name',
            'phone', 'twitter_handle', 'shirt_size', 'uploaded_image', 'shortbio', 'videopermission',
            'organization', 'position',
        ]
        self.assertEqual(len(layout_fields), len(expected_fields))
        for field in expected_fields:
            self.assertIn(field, layout_fields)


class CreateSpeakerFormTest(SimpleTestCase):
    def test_init_creates_form_helper(self):
        form = CreateSpeakerForm(devdayuserform_model=[])
        self.assertIsInstance(form.helper, FormHelper)
        self.assertEqual(form.helper.form_action, reverse('create_speaker'))
        self.assertEqual(form.helper.form_method, 'post')
        self.assertEqual(form.helper.form_id, 'create-speaker-form')
        self.assertEqual(form.helper.field_template, 'devday/form/field.html')
        self.assertTrue(form.helper.html5_required)

    def test_init_creates_layout(self):
        form = CreateSpeakerForm(devdayuserform_model=[])
        self.assertIsInstance(form.helper.layout, Layout)
        layout_fields = [name for [_, name] in form.helper.layout.get_field_names()]
        expected_fields = [
            'upload_url', 'delete_url', 'form_id', 'email', 'first_name', 'last_name', 'password1', 'password2',
            'phone', 'twitter_handle', 'organization', 'position', 'uploaded_image', 'shirt_size', 'shortbio',
            'videopermission']
        self.assertEqual(len(layout_fields), len(expected_fields))
        for field in expected_fields:
            self.assertIn(field, expected_fields)


class TalkCommentFormTest(TestCase):
    def test_fields(self):
        form = TalkCommentForm(instance=mock.MagicMock(pk=1))
        self.assertListEqual(['comment', 'is_visible'], list(form.fields))

    def test_init_creates_form_helper(self):
        form = TalkCommentForm(instance=mock.MagicMock(pk=1))
        self.assertIsInstance(form.helper, DevDayFormHelper)
        self.assertEqual(form.fields['comment'].widget.attrs['rows'], 2)
        self.assertEqual(form.helper.form_action, '/committee/talks/1/comment/')

    def test_init_creates_layout(self):
        form = TalkCommentForm(instance=mock.MagicMock(pk=1))
        self.assertIsInstance(form.helper.layout, Layout)
        layout_fields = [name for [_, name] in form.helper.layout.get_field_names()]
        self.assertListEqual(['comment', 'is_visible'], layout_fields)
        self.assertEqual(len(form.helper.layout.get_layout_objects(Submit)), 1)


class TalkSpeakerCommentFormTest(TestCase):
    def test_fields(self):
        form = TalkSpeakerCommentForm(instance=mock.MagicMock(pk=1))
        self.assertListEqual(['comment'], list(form.fields))

    def test_init_creates_form_helper(self):
        form = TalkSpeakerCommentForm(instance=mock.MagicMock(pk=1))
        self.assertIsInstance(form.helper, DevDayFormHelper)
        self.assertEqual(form.fields['comment'].widget.attrs['rows'], 2)
        self.assertEqual(form.helper.form_action, '/session/speaker/talks/1/comment/')

    def test_init_creates_layout(self):
        form = TalkSpeakerCommentForm(instance=mock.MagicMock(pk=1))
        self.assertIsInstance(form.helper.layout, Layout)
        layout_fields = [name for [_, name] in form.helper.layout.get_field_names()]
        self.assertListEqual(['comment'], layout_fields)
        self.assertEqual(len(form.helper.layout.get_layout_objects(Submit)), 1)


class TalkVoteFormTest(TestCase):
    def test_fields(self):
        form = TalkVoteForm()
        self.assertListEqual(['score'], list(form.fields))
