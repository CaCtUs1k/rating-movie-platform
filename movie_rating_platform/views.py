from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic

from movie_rating_platform.forms import MovieSearchForm, VisitorCreationForm, VisitorSearchForm, VisitorUpdateForm, \
    CreateOrUpdateRatingForm
from movie_rating_platform.models import Movie, Rating, Genre, Visitor


@login_required
def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_movies": Movie.objects.count(),
        "num_ratings": Rating.objects.count(),
        "num_genres": Genre.objects.count(),
        "num_users": get_user_model().objects.count()
    }
    return render(
        request,
        template_name="movie_rating_platform/index.html",
        context=context
    )


class MovieListView(LoginRequiredMixin, generic.ListView):
    model = Movie
    paginate_by = 5
    queryset = Movie.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = MovieSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        form = MovieSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )
        return self.queryset


class MovieCreateView(LoginRequiredMixin, generic.CreateView):
    model = Movie
    fields = "__all__"
    success_url = reverse_lazy("movie_rating:movie-list")


class MovieUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Movie
    fields = "__all__"
    success_url = reverse_lazy("movie_rating:movie-list")


class MovieDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Movie
    success_url = reverse_lazy("movie_rating:movie-list")


class VisitorListView(LoginRequiredMixin, generic.ListView):
    model = Visitor
    paginate_by = 5
    queryset = Visitor.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VisitorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = VisitorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = VisitorSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class VisitorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Visitor
    queryset = Visitor.objects.all().prefetch_related("wishlist")


class VisitorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Visitor
    success_url = reverse_lazy("movie_rating:visitor-list")
    form_class = VisitorCreationForm


class VisitorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Visitor
    form_class = VisitorUpdateForm
    success_url = reverse_lazy("movie_rating:visitor-list")


class VisitorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Visitor
    success_url = reverse_lazy("movie_rating:visitor-list")


@login_required
def movie_detail_view(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    max_value = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    movie.ratings.select_related("sender")
    context = {
        "movie": movie,
        "max_value": max_value
    }
    return render(
        request,
        "movie_rating_platform/movie_detail.html",
        context=context)


@login_required
def create_rating_view(request, pk):
    if request.method == 'POST':
        form = CreateOrUpdateRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.sender = request.user
            rating.create_time = timezone.now()
            rating.movie = Movie.objects.get(pk=pk)
            rating.save()
            return redirect('movie_rating:movie-detail', pk=pk)
    else:
        form = CreateOrUpdateRatingForm
    return render(request, "movie_rating_platform/rating_form.html", context={'form': form, "pk": pk})


class RatingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Rating
    form_class = CreateOrUpdateRatingForm
    success_url = reverse_lazy("movie_rating:movie-list")


class RatingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Rating
    success_url = reverse_lazy("movie_rating:movie-list")


@login_required
def toggle_assign_to_movie(request, pk):
    visitor = Visitor.objects.get(id=request.user.id)
    if (
        Movie.objects.get(id=pk) in visitor.wishlist.all()
    ):
        visitor.wishlist.remove(pk)
    else:
        visitor.wishlist.add(pk)
    return HttpResponseRedirect(reverse("movie_rating:movie-detail", args=[pk]))



