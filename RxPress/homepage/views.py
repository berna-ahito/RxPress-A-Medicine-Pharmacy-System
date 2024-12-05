from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Medicine, Cart

# # from .forms import RegisterForm

# # # Homepage View
# # def homepage(request):
# #     medicines = Medicine.objects.all()
# #     return render(request, 'pharmacy/homepage.html', {'medicines': medicines})

# # def order_view(request):
# #     orders = Order.objects.all()
# #     return render(request, 'order.html', {'orders': orders})


# def homepage(request):
#     return render(request, 'homepage.html')

# def order_view(request):
#     return render(request, 'order.html')

# def cart_view(request):
#     return render(request, 'cart.html')


# # def update_cart(request, item_id):
# #     if request.method == 'POST':
# #         cart_item = get_object_or_404(Cart, id=item_id)
# #         cart_item.quantity = int(request.POST.get('quantity', 1))
# #         cart_item.save()
# #     return redirect('pharmacy:cart_view')

# # def remove_from_cart(request, item_id):
# #     if request.method == 'POST':
# #         cart_item = get_object_or_404(Cart, id=item_id)
# #         cart_item.delete()
# #     return redirect('pharmacy:cart_view')

# # def checkout(request):
# #     # Handle checkout logic here
# #     return redirect('pharmacy:order_view')


# # def add_to_cart(request):
# #     if request.method == 'POST':
# #         selected_items = request.POST.getlist('selected_items')
# #         for item_id in selected_items:
# #             quantity = request.POST.get(f'quantity_{item_id}')
# #             medicine = Medicine.objects.get(id=item_id)
# #             Cart.objects.create(
# #                 medicine=medicine,
# #                 quantity=int(quantity),
# #                 user=request.user  # Assuming the user is logged in
# #             )
# #         return redirect('pharmacy:cart_view')  # Redirect to the cart page
# #     return HttpResponse("Invalid Request", status=400)


