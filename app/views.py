from django.shortcuts import render
from django.http import *
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
from .forms import *
import pdb

class IndexView(ListView):
    template_name = 'app/index.html'
    context_object_name = 'problems'

    def get_queryset(self):
        return Problem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = [('array','Array'),('hash_table','Hash Table'),('Linked_list','Linked list'),('math','Math'),('two_pointers','Two Pointers'),('string','String'),('binary_search','Binary Search'), ('divide_and_coquer','Divide and coquer'),('dynamic_programming','Dynamic Programming'),('backtracking','Backtracking'),('Stack','stack'),('heap','Heap'),('greedy','Greedy'),('sort','Sort'),('bit_manipulation','Bit Manipulation'),('tree','Tree'),('depth_first_search','DFS'),('breadth_first_search','BFS'),('union_find','Union Find'),('graph','Graph'),('design','Design'),('tpological_sort','Topological Sort'),('trie','Trie'),('binary_search_tree','Binary search tree'), ('queue','Queue')]
        context['difficulties'] = [('easy','Easy'), ('medium','Medium'),('hard','Hard')]
        context['search_form'] = SearchForm()
        return context

class FindByTagView(IndexView):
    tag_name = ''

    def setup(self, request, *args, **kwargs):
        super(FindByTagView, self).setup(request, *args, **kwargs)
        self.tag_name = kwargs['tag_name']

    def get_queryset(self):
        return Problem.objects.filter(tags__name=self.tag_name)

class FindByDifficultyView(IndexView):
    difficulty_name = ''

    def setup(self, request, *args, **kwargs):
        super(FindByDifficultyView, self).setup(request, *args, **kwargs)
        self.difficulty_name = kwargs['difficulty_name']

    def get_queryset(self):
        return Problem.objects.filter(difficulty=self.difficulty_name)

class SearchByNameView(IndexView):
    pass


class ProblemDetailView(DetailView):
    model = Problem
    # context_object_name = 'problem'
    template_name = 'app/problem_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solutions'] = ProblemResolution.objects.filter(problem=self.object)
        return context


class ProblemCreateView(CreateView):
    model = Problem
    form_class = ProblemForm
    template_name = 'app/problem_form.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        problem_resolution_form = ProblemResolutionFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, problem_resolution_form=problem_resolution_form, ))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        problem_form = self.get_form(form_class)
        problem_resolution_form = ProblemResolutionFormSet(request.POST)
        self.object = None
        if problem_form.is_valid() and problem_resolution_form.is_valid():
            # hago insert en la bd
            # new_problem = Problem(form.cleaned_data())
            self.object = problem_form.save()  # commit=False
            for resolution_form in problem_resolution_form:
                resolution = resolution_form.save(commit=False)
                resolution.problem = self.object
                resolution.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=problem_form, problem_resolution_form=problem_resolution_form, ))


def create(request):
    if request.method == 'POST':
        problem_form, resolution_form = ProblemForm(request.POST), ProblemResolutionForm(request.POST)
        if problem_form.is_valid() and resolution_form.is_valid():
            problem_form.save()
            resolution_form.save()
            return HttpResponseRedirect('index')
    else:
        problem_form = ProblemForm()
        resolution_form = ProblemResolutionForm()

    return render(request, 'app/problem_form.html', {'form': problem_form, 'resolution_form': resolution_form})


class ProblemUpdateView(UpdateView):
    model = Problem
    form_class = ProblemForm
    object = None

    def get_object(self, queryset=None):
        self.object = super(ProblemUpdateView, self).get_object()
        return self.object

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates form with data in db
        and its inline formsets.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.instance = self.get_object()
        form.initial = form.instance.__dict__
        problem_resolution_form = ProblemResolutionFormSet(instance=self.get_object())
        return self.render_to_response(
            self.get_context_data(form=form, problem_resolution_form=problem_resolution_form, ))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        problem_form = self.get_form(form_class)
        problem_form.data = request.POST
        problem_form.instance = self.get_object()
        problem_resolution_form = ProblemResolutionFormSet(request.POST, instance=self.get_object())

        if problem_form.is_valid() and problem_resolution_form.is_valid():
            self.object = problem_form.save()
            problem_resolution_form = problem_resolution_form.save(commit=False)
            for resolution_form in problem_resolution_form:
                resolution = resolution_form.save(commit=False)
                if resolution.problem is None:
                    resolution.problem = self.object
                resolution.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=problem_form, problem_resolution_form=problem_resolution_form, ))


class ProblemDeleteView(DeleteView):
    model = Problem
    success_url = reverse_lazy('index')
    template_name = 'app/index.html'
