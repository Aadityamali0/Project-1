from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from cart.models import Cart
from customer.models import Customer
from store.models import Product
from .models import Order

class OrderFlowTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            product_name='Jacket', description='warm', price=50, image='x.jpg'
        )
        self.users = []
        for i in range(3):
            u = User.objects.create_user(username=f'user{i}', password='pass12345')
            Customer.objects.create(user=u, name=f'Person {i}', phone_number=f'98000000{i}0')
            self.users.append(u)
        self.admin = User.objects.create_superuser('boss', 'b@x.com', 'pass12345')

    def _place(self, user, qty):
        Cart.objects.create(
            user=user, name='n', phone_number='1', product=self.product,
            quantity=qty, price=self.product.price,
        )
        self.client.force_login(user)
        return self.client.post(reverse('order_tracker:place_order'))

    def test_place_order_creates_order_and_clears_cart(self):
        response = self._place(self.users[0], 3)
        self.assertRedirects(response, reverse('order_tracker:my_orders'))
        order = Order.objects.get()
        self.assertEqual(order.name, 'Person 0')
        self.assertEqual(order.phone_number, '9800000000')
        self.assertEqual(order.status, Order.Status.PENDING)
        self.assertEqual(order.total_quantity, 3)
        self.assertEqual(order.total_price, 150)
        self.assertFalse(Cart.objects.filter(user=self.users[0]).exists())

    def test_admin_groups_orders_per_user_and_updates_status(self):
        for i, user in enumerate(self.users):
            self._place(user, i + 1)
        self.client.logout()
        self.client.force_login(self.admin)

        response = self.client.get(reverse('admin:order_tracker_order_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['groups']), 3)
        self.assertContains(response, '<details', count=3)

        order = Order.objects.first()
        response = self.client.post(
            reverse('admin:order_tracker_order_update_status', args=[order.id]),
            {'status': 'accepted'},
        )
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, 'accepted')

        self.client.post(
            reverse('admin:order_tracker_order_update_status', args=[order.id]),
            {'status': 'bogus'},
        )
        order.refresh_from_db()
        self.assertEqual(order.status, 'accepted')
