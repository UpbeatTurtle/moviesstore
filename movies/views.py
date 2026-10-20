from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.db.models import Count, Sum



def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.reports = 0
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.reports += 1
    review.save()
    template_data = {}
    return render(request, 'movies/report_review.html',
                {'template_data': template_data})

@staff_member_required
def top_commenter(request):
    #I need the reviews 
    #I need to count user with the most reviews
    #display that user
    reviews = Review.objects.all()
    counts = {}
    for review in reviews:
        if review.user.username in counts:
            counts[review.user.username] += 1
        else:
            counts[review.user.username] = 1
    top_reviewer = ""
    top_count = 0
    for name, count in counts.items():
        if count > top_count:
            top_count = count
            top_reviewer = name
    template_data = {}
    template_data['title'] = "Top Reviewer"
    template_data['top_reviewer'] = top_reviewer
    template_data['top_count'] = top_count
    return render(request, 'movies/top_commenter.html', 
                  {'template_data': template_data})

@user_passes_test(lambda user: user.is_staff)
def admin_stats(request):
    top_selling_movie = (
        Movie.objects
        .annotate(total_sold=Sum('item__quantity'))
        .filter(total_sold__gt=0)
        .order_by('-total_sold', 'name', 'id')
        .first()
    )

    top_reviewed_movie = (
        Movie.objects
        .annotate(review_count=Count('review'))
        .filter(review_count__gt=0)
        .order_by('-review_count', 'name', 'id')
        .first()
    )

    template_data = {
        'title': 'Movie Statistics',
        'top_selling_movie': top_selling_movie,
        'top_reviewed_movie': top_reviewed_movie,
    }

    return render(
        request,
        'movies/admin_stats.html',
        {'template_data': template_data},
    )



