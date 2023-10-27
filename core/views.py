from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.generic import DetailView, ListView, View


from core.models import Item, ItemOrder, Order, BillingAddress
from core.forms import CheckoutForm

class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = 'home.html'



class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        template_name = 'order_summary.html'
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order,
            }
            return render(self.request, template_name,context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect('/')


     


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_item, created = ItemOrder.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('order-summary')
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('order-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect('order-summary')



@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = ItemOrder.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect('order-summary')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)




@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = ItemOrder.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity >1:

                order_item.quantity -=1
            else:
                order.items.remove(order_item)                
            order_item.save()           
            messages.info(request, "This item quantity was updated .")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)










class CheckoutView(View):
    def get(self, *args, **kwargs):
        template_name = 'checkout.html'

        form = CheckoutForm()
        context = {
            'form':form
        }
        return render(self.request, template_name,context)

    
    
    def post(self, *args, **kwargs):
        template_name = 'checkout.html'
        
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                print(form.cleaned_data)
                print("Form is valid")
                streep_address = form.cleaned_data.get('streep_address')
                appartment_address = form.cleaned_data.get('appartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add the functionality for these field
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    streep_address=streep_address,
                    appartment_address=appartment_address,
                    country=country,
                    zip=zip,
                             
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add the rediect to the selected payment option
                
                return redirect('checkout')
            messages.warning(self.request, 'Failed chechout')                
            context = {
                'form':form,
                'object':order,
            }
            return render(self.request, template_name, context)
          
            
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect('order-summary')

        
       
