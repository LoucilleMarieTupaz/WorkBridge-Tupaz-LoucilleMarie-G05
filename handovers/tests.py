from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import HandoverEntry


User = get_user_model()


class HandoverManagementTests(TestCase):

    def setUp(self):

        self.member1 = User.objects.create_user(
            username='member1',
            email='member1@example.com',
            password='TestPassword123!',
            role=User.Role.MEMBER
        )

        self.member2 = User.objects.create_user(
            username='member2',
            email='member2@example.com',
            password='TestPassword123!',
            role=User.Role.MEMBER
        )

        self.manager = User.objects.create_user(
            username='manager1',
            email='manager1@example.com',
            password='TestPassword123!',
            role=User.Role.PROJECT_MANAGER
        )

    def create_entry(self, creator, assignee=None):

        return HandoverEntry.objects.create(
            title='Website Development',
            task_description='Continue website development.',
            progress=HandoverEntry.Progress.IN_PROGRESS,
            instructions='Follow the project documentation.',
            pending_work='Complete the remaining pages.',
            created_by=creator,
            assigned_to=assignee
        )

    def test_login_required_for_handover_list(self):

        response = self.client.get(
            reverse('handovers:list')
        )

        self.assertEqual(response.status_code, 302)

    def test_member_can_create_handover(self):

        self.client.login(
            username='member1',
            password='TestPassword123!'
        )

        response = self.client.post(
            reverse('handovers:create'),
            {
                'title': 'Website Development',
                'task_description': 'Continue website development.',
                'progress': 'IN_PROGRESS',
                'instructions': 'Follow the project documentation.',
                'pending_work': 'Complete remaining pages.',
                'assigned_to': self.member2.pk,
            }
        )

        self.assertEqual(response.status_code, 302)

        entry = HandoverEntry.objects.get(
            title='Website Development'
        )

        self.assertEqual(
            entry.created_by,
            self.member1
        )

        self.assertEqual(
            entry.assigned_to,
            self.member2
        )

    def test_member_only_sees_relevant_records(self):

        self.create_entry(self.member1, self.member2)
        self.create_entry(self.manager, self.member2)
        self.create_entry(self.manager, None)

        self.client.login(
            username='member2',
            password='TestPassword123!'
        )

        response = self.client.get(
            reverse('handovers:list')
        )

        self.assertEqual(
            len(response.context['entries']),
            2
        )

    def test_manager_can_view_all_records(self):

        self.create_entry(self.member1)
        self.create_entry(self.member2)

        self.client.login(
            username='manager1',
            password='TestPassword123!'
        )

        response = self.client.get(
            reverse('handovers:list')
        )

        self.assertEqual(
            len(response.context['entries']),
            2
        )

    def test_assigned_member_cannot_edit_another_members_record(self):

        entry = self.create_entry(
            self.member1,
            self.member2
        )

        self.client.login(
            username='member2',
            password='TestPassword123!'
        )

        response = self.client.get(
            reverse(
                'handovers:update',
                kwargs={'pk': entry.pk}
            )
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_manager_can_edit_any_record(self):

        entry = self.create_entry(self.member1)

        self.client.login(
            username='manager1',
            password='TestPassword123!'
        )

        response = self.client.get(
            reverse(
                'handovers:update',
                kwargs={'pk': entry.pk}
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )