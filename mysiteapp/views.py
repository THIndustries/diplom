from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView
from .models import Ingredient, Recipe, Image, Category, RecipeIngredient
from .forms import IngredientForm, RecipeForm, RecipeIngredientForm, CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from django.contrib.auth.decorators import login_required


# рецепты
class AddRecipeView(LoginRequiredMixin, CreateView):
    form_class = RecipeForm
    template_name = 'mysiteapp/recipe_add.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()

        # картинки
        images = self.request.FILES.getlist('photo')
        for image_data in images:
            extension = image_data.name.split('.')[-1]
            filename = f'{uuid4()}.{extension}'
            fs = FileSystemStorage()
            fs.save(filename, image_data)
            image = Image.objects.create(url=filename)
            self.object.images.add(image)

        # ингридиенты
        ingredients_data = self.request.POST.getlist('ingredient_name')
        amounts_data = self.request.POST.getlist('amount')


        for i in range(len(ingredients_data)):
            ingredient_name = ingredients_data[i].strip().lower()
            amount = amounts_data[i]
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)

            RecipeIngredient.objects.create(
                recipe=self.object,
                ingredient=ingredient,
                amount=amount,
            )

        # Категории
        categories = self.request.POST.getlist('category_name')
        for category_data in categories:
            category, _ = Category.objects.get_or_create(name=category_data.strip().lower())
            form.instance.categories.add(category)

        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'mysiteapp/recipe_add.html'
    reverse_lazy = 'home'




class RecipeListView(ListView):
    template_name = 'mysiteapp/main_page.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.select_related('author').filter(is_deleted=False)



class RecipeDetailView(DetailView):
    template_name = 'mysiteapp/detail_recipe.html'
    model = Recipe
    context_object_name = 'recipe'

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            recipe = self.get_object()
            recipe.is_deleted = True
            recipe.save()
            return redirect('home')
        return render(request, self.template_name)


# Отобразить рецепты пользователя
class MyRecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'mysiteapp/main_page.html'
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = context['recipes'].filter(author=self.request.user)
        return context


# Ингредиенты
class AddIngredientView(LoginRequiredMixin, CreateView):
    form_class = IngredientForm
    template_name = 'mysiteapp/ingredient_add.html'


class IngredientListView(ListView):
    model = Ingredient
    context_object_name = 'ingredients'
    template_name = 'mysiteapp/list_of_ingredients.html'


class IngredientDetailView(DetailView):
    template_name = 'mysiteapp/detail_of_ingredient.html'
    model = Ingredient
    context_object_name = 'ingredient'


# Категории
class AddCategoryView(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = 'mysiteapp/category_add.html'


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'mysiteapp/list_of_categories.html'


class CategoryDetailView(DetailView):
    template_name = 'mysiteapp/detail_of_category.html'
    model = Category
    context_object_name = 'category'


def show_about(request):
    return render(request, 'mysiteapp/about.html')
