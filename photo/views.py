# from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse
from django.utils import timezone
from django.db.models import Q
from .models import Photo, Comment
from .forms import CommentForm
from flask import request
from django.http import HttpResponseRedirect
from django.contrib import messages
# from .forms import CommentForm, PostSearchForm
# Create your views here.

class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'

class PhotoCreate(CreateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_create'
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})
    
class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_update'
    # success_url = '/'
    
    def dispatch(self, request, *args, **kwargs) :
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)

class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'
    
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'

class PhotoUp(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.up.all():
                    photo.up.remove(user)
                else:
                    photo.up.add(user)
                    
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
        
class PhotoDown(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.down.all():
                    photo.down.remove(user)
                else:
                    photo.down.add(user)
                    
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
    
class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
                    
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
        
class PhotoBookmark(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login')
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.bookmark.all():
                    photo.bookmark.remove(user)
                else:
                    photo.bookmark.add(user)
            return HttpResponseRedirect('/')
        
class PhotoLikeList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '로그인을 먼저 하세요')
            return HttpResponseRedirect('/')
        return super(PhotoLikeList, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        queryset = user.like_post.all()
        return queryset
    
class PhotoBookmarkList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '로그인을 먼저 하세요')
            return HttpResponseRedirect('/')
        return super(PhotoBookmarkList, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        queryset = user.bookmark_post.all()
        return queryset
    
class PhotoMyList(ListView):
    model = Photo
    template_name = 'photo/photo_mylist.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '로그인을 먼저 하세요')
            return HttpResponseRedirect('/')
        return super(PhotoMyList, self).dispatch(request, *args, **kwargs)
    
    
@login_required(login_url='accounts:login')
def comment_create_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    if request.method == "POST":
        form = CommentForm(request.POST) #폼 불러오기
        if form.is_valid():
            comment = form.save(commit=False) #폼 객체를 통해 데이터 저장, 추가적인 데이터 저장 위해 DB에 바로 반영 X
            comment.author = request.user #댓글 작성자 <= 현재 유저 대입
            comment.create_date = timezone.now() #댓글 작성 시간 <= 현재 시간 대입
            comment.photo = photo #댓글이 달린 사진 <= 지금 사진
            comment.save() #최종적으로 저장
            return redirect('photo:detail', pk=photo.id)
            # return HttpResponseRedirect('/')
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'photo/comment_form.html', context)

@login_required(login_url='accounts:login')
def comment_modify_photo(request, comment_id):
    """
    photo 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('photo:detail', pk=comment.photo.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('photo:detail', pk=comment.photo.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'photo/comment_form.html', context)

@login_required(login_url='accounts:login')
def comment_delete_photo(request, comment_id):
    """
    photo 질문댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('photo:detail', pk=comment.photo.id)
    else:
        comment.delete()
    return redirect('photo:detail', pk=comment.photo.id)


def SearchFormView(request):
    content_list = Photo.objects.all() #모든 게시글을 가져오기
    search_word = request.GET.get('search_word','') #검색어 값이 있으면 가져오고, 없으면 빈 문자열을 넣음
    
    if(search_word == ''):
        post_list = []
        
    else:
        post_list = content_list.filter(Q(text__icontains=search_word)).distinct()
        #검색어 값과 일치하는 부분이 있는 게시글만 따로 저장, Q객체 사용

    context = {}
    context['search_term'] = search_word
    context['object_list'] = post_list
    #잘 집어넣어서 넘겨주기

    return render(request, 'photo/search.html', context)



