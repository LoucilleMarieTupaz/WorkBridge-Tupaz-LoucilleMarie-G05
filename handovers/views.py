from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden

from accounts.models import User

from .models import HandoverEntry
from .forms import HandoverEntryForm


def can_manage_all(user):
    return user.role in (
        User.Role.ADMIN,
        User.Role.PROJECT_MANAGER
    )


def can_view_entry(user, entry):
    if can_manage_all(user):
        return True

    return (
        entry.created_by_id == user.pk
        or entry.assigned_to_id == user.pk
    )


def can_edit_entry(user, entry):
    if can_manage_all(user):
        return True

    return entry.created_by_id == user.pk


@login_required
def handover_list(request):

    entries = HandoverEntry.objects.select_related(
        'created_by',
        'assigned_to'
    )

    if not can_manage_all(request.user):
        entries = entries.filter(
            Q(created_by=request.user)
            | Q(assigned_to=request.user)
        )

    return render(
        request,
        'handovers/handover_list.html',
        {
            'entries': entries,
            'is_manager_or_admin': can_manage_all(request.user),
        }
    )


@login_required
def handover_create(request):

    if request.user.role not in (
        User.Role.MEMBER,
        User.Role.PROJECT_MANAGER
    ):
        return HttpResponseForbidden(
            'You are not allowed to create handover records.'
        )

    if request.method == 'POST':
        form = HandoverEntryForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():
            entry = form.save(commit=False)
            entry.created_by = request.user
            entry.save()

            messages.success(
                request,
                'Handover record created successfully!'
            )

            return redirect(
                'handovers:detail',
                pk=entry.pk
            )

    else:
        form = HandoverEntryForm(user=request.user)

    return render(
        request,
        'handovers/handover_form.html',
        {
            'form': form,
            'page_title': 'Create Handover Record',
        }
    )


@login_required
def handover_detail(request, pk):

    entry = get_object_or_404(
        HandoverEntry.objects.select_related(
            'created_by',
            'assigned_to'
        ),
        pk=pk
    )

    if not can_view_entry(request.user, entry):
        return HttpResponseForbidden(
            'You are not allowed to view this handover record.'
        )

    return render(
        request,
        'handovers/handover_detail.html',
        {
            'entry': entry,
            'can_edit': can_edit_entry(request.user, entry),
        }
    )


@login_required
def handover_update(request, pk):

    entry = get_object_or_404(HandoverEntry, pk=pk)

    if not can_edit_entry(request.user, entry):
        return HttpResponseForbidden(
            'You are not allowed to update this handover record.'
        )

    if request.method == 'POST':
        form = HandoverEntryForm(
            request.POST,
            instance=entry,
            user=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Handover record updated successfully!'
            )

            return redirect(
                'handovers:detail',
                pk=entry.pk
            )

    else:
        form = HandoverEntryForm(
            instance=entry,
            user=request.user
        )

    return render(
        request,
        'handovers/handover_form.html',
        {
            'form': form,
            'page_title': 'Update Handover Record',
        }
    )


@login_required
def handover_delete(request, pk):

    entry = get_object_or_404(HandoverEntry, pk=pk)

    if not can_edit_entry(request.user, entry):
        return HttpResponseForbidden(
            'You are not allowed to delete this handover record.'
        )

    if request.method == 'POST':
        entry.delete()

        messages.success(
            request,
            'Handover record deleted successfully!'
        )

        return redirect('handovers:list')

    return render(
        request,
        'handovers/handover_confirm_delete.html',
        {'entry': entry}
    )