from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import CreateProductForm, UpdateProductForm
from .models import *
from .utils import cartData


class SearchResultsView(ListView):
    queryset = Product.objects.all()
    template_name = 'main/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(name__icontains=q))
        return queryset