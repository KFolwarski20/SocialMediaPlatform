from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Image
from .forms import ImageCreateForm


@login_required
def image_create(request):
    if request.method == 'POST':
        # Formularz został wysłany
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Dane formularza są prawidłowe.
            new_item = form.save(commit=False)
            # Przypisanie bieżącego użytkownika do elementu
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Obraz został dodany.')
            # Przekierowanie do widoku szczegółowego dla nowo utworzonego elementu.
            return redirect(new_item.get_absolute_url())
    else:
        # Utworzenie formularza na podstawie danych dostarczonych przez bookmarklet w żądaniu GET.
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html',
                  {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Jeżeli zmienna page nie jest liczbą całkowitą, wówczas pobierana jest pierwsza strona wyników
        images = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Jeżeli żądanie jest w technologii AJAX i zmienna page ma wartość spoza zakresu,
            # wówczas zwracana jest pusta strona.
            return HttpResponse('')
        # Jeżeli zmienna page ma wartość większą niż numer ostatniej strony wyników, wtedy pobierana
        # jest ostatnia strona wyników.
        images = paginator.page(paginator.num_pages)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})
