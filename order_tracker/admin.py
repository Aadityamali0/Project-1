from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.http import HttpResponseNotAllowed
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone_number', 'status', 'total_price']
    inlines = [OrderItemInline]

    def get_urls(self):
        custom_urls = [
            path(
                '<int:order_id>/update-status/',
                self.admin_site.admin_view(self.update_status),
                name='order_tracker_order_update_status',
            ),
        ]
        return custom_urls + super().get_urls()

    def changelist_view(self, request, extra_context=None):
        """Orders grouped per user; each user is a dropdown holding their orders."""
        if not self.has_view_permission(request):
            raise PermissionDenied

        orders = (
            Order.objects
            .select_related('user')
            .prefetch_related('items')
            .order_by('user__username', '-created_at')
        )

        groups = []
        by_user = {}
        for order in orders:
            group = by_user.get(order.user_id)
            if group is None:
                group = {'user': order.user, 'orders': [], 'pending': 0}
                by_user[order.user_id] = group
                groups.append(group)
            group['orders'].append(order)
            if order.status == Order.Status.PENDING:
                group['pending'] += 1

        context = {
            **self.admin_site.each_context(request),
            'title': 'Orders',
            'opts': self.model._meta,
            'groups': groups,
            'status_choices': Order.Status.choices,
            'can_change': self.has_change_permission(request),
            'open_user': request.GET.get('open', ''),
            **(extra_context or {}),
        }
        return TemplateResponse(request, 'order/admin_orders.html', context)

    def update_status(self, request, order_id):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])
        order = get_object_or_404(Order, id=order_id)
        if not self.has_change_permission(request, order):
            raise PermissionDenied

        status = request.POST.get('status')
        if status in Order.Status.values:
            order.status = status
            order.save(update_fields=['status'])
            messages.success(request, f"Order #{order.id} marked as {order.get_status_display()}.")
        else:
            messages.error(request, 'Invalid status.')

        url = reverse('admin:order_tracker_order_changelist')
        return redirect(f"{url}?open={order.user_id}")


admin.site.register(Order, AdminOrder)
