from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import auth
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime as dt
from .utils import *
from django.http import HttpResponseRedirect
from django.db.models import Q
import re

# Create your views here.
@login_required(login_url='signin')
def index(request):
    posts_v1 = Post.objects.filter(Q(privacy__lt=2) | Q(user=request.user))
    status = ['Public', 'Friends', 'Only me']
    return render(request, 'index.html', {
        'user': request.user,
        'posts': post_show(posts=posts_v1, user=request.user),
        'status': status,
    })

def signup(request):
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if pass1 != pass2:
            messages.info(request, "Passwords don't match")
            return redirect('signup')
        else:
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect('signup')
            else:
                phone = request.POST['phone']
                if User.objects.filter(phone=phone).exists():
                    messages.info(request, "Phone already exists")
                    return redirect('signup')
                else:
                    birth = dt.strptime(request.POST['birth'], '%Y-%m-%d').date()
                    if (dt.now().date()-birth).total_seconds() < 16*365*24*60*60:
                        messages.info(request, "User must be at least 16 years ago")
                        return redirect('signup')
                    else:
                        first = request.POST['first']
                        last = request.POST['last']
                        is_male = request.POST.get('sex') == 'm'
                        
                        code = random_with_N_digits(6)
                        user = User.objects.create(first_name=first, last_name=last, email=email, phone=phone,
                                is_male=is_male, birth=birth, code=code)
                        user.set_password(pass1)
                        # till account activation
                        user.is_active = False
                        user.save()

                        # send activation mail
                        domain = get_current_site(request).domain
                        
                        encoded_uid = urlsafe_base64_encode(force_bytes(user.id))
                        token = token_gen.make_token(user=user)
                        link = reverse('activate', kwargs={
                            'uidb64': encoded_uid,
                            'token': token,
                        })
                        activate_link = f'http://{domain}{link}'

                        email_subject = 'Activate your account'
                        email_body = render_to_string('emails/confirm.html', {
                            'name': first,
                            'code': code,
                            'link': activate_link,
                        })
                        email = EmailMessage(
                            subject=email_subject,
                            body=email_body,
                            from_email=settings.EMAIL_HOST_USER,
                            to=[email],
                        )

                        email.send(fail_silently=False)

                        messages.success(request, 'Email created successfully check your inbox to activate your account')
                        return HttpResponseRedirect(f'../account/confirm/{encoded_uid}/')
    
    return render(request, 'signup.html', {})

def activate(request, uidb64, token):
    try:
        decoded_uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=decoded_uid)
        
        if not token_gen.check_token(user, token):
            return redirect('signin')

        if user.is_active:
            return redirect('signin')
            
        user.is_active = True
        user.code = '0'
        user.save()
        
        return render(request, 'signin.html', {
            'success_message': 'Account activated successfully',
            })
    except Exception as e:
        print(e)
        return redirect('error404')
    return redirect('signin')

def confirm(request, uidb64):
    try:
        decoded_uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=decoded_uid)
        
        if user.is_active:
            return render(request, 'signin.html', {
                'success_message': 'Account is already activated',
                })
        
        if request.method == "POST":
            code2 = request.POST['c0'][0]+request.POST['c1'][0]+request.POST['c2'][0]+request.POST['c3'][0]+request.POST['c4'][0]+request.POST['c5'][0]
            code1 = user.code

            if code1 != code2:
                return render(request, 'confirm.html', {
                    'success_message': '',
                    'fail_message': 'Check the code again from the mail and resubmit'
                    })
            
            user.code = '0'
            user.is_active = True
            user.save()

            return render(request, 'signin.html', {
                'success_message': 'Account activated successfully',
                })
    except Exception as e:
        print(e)
        return redirect('error404')

    return render(request, 'confirm.html', {
        'success_message': '',
        'fail_message': ''
        })

def reset(request):
    pass

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']

        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('signin')

    return render(request, 'signin.html', {
        'success_message': ''
    })

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

def error404(request):
    if request.method == "POST":
        error = request.POST['error']

    return render(request, '404.html', {})

@login_required(login_url='signin')
def settings_page(request, id):
    if str(request.user.id) != str(id):
        return redirect('error404')
    if request.method == 'POST':
        user = request.user
        if request.FILES.get('cover') != None:
            user.cover_img = request.FILES.get('cover')
        if request.FILES.get('profile') != None:
            user.cover_img = request.FILES.get('profile')
        user.location = request.POST['loc']
        user.bio = request.POST['bio']
        user.education = request.POST['edu']
        user.job = request.POST['job']
        user.save()

        return redirect('settings', user.id)

    return render(request, 'settings.html', {
        'user': request.user,
    })

@login_required(login_url='signin')
def profile(request, id):
    # if str(request.user.id) != str(id):
    #     return redirect('error404')
    user = User.objects.get(id=id)
    skills = User_Skill.objects.filter(user=user)
    try: tab = request.GET['tab']
    except: tab = 'timeline'
    status = ['Public', 'Friends', 'Only me']
    posts = []
    if tab == 'timeline':
        posts_v1 = Post.objects.filter(user=user)
        posts = post_show(posts=posts_v1, user=user)

    return render(request, 'profile.html', {
        'tab': tab,
        'user': user,
        'profile': str(user.profile_img.path).split('/')[-1],
        'cover': str(user.cover_img.path).split('/')[-1],
        'skills': skills,
        'rates': range(1, 6),
        'status': status,
        'privacy': status[user.privacy],
        'posts': posts,
        'me': user == request.user,
    })

@login_required(login_url='signin')
def add_skill(request, id):
    if request.method == 'POST':
        user = request.user
        rate = request.POST['rate']
        (skill, flag) = Skill.objects.get_or_create(name=request.POST['skill'].title())
        if not flag: skill.save()

        User_Skill.objects.create(user=user, skill=skill, rate=rate).save()
        return redirect('profile', id)

@login_required(login_url='signin')
def remove_skill(request, id, name):
    user = request.user
    skill = Skill.objects.get(name=name)
    user_skill = User_Skill.objects.filter(user=user, skill=skill).first()
    user_skill.delete()
    return redirect('profile', id)

@login_required(login_url='signin')
def add_post(request):
    if request.method == 'POST':
        content = request.POST['content']
        privacy = request.POST['privacy']
        
        (content, tags) = make_hashtags(content)

        privacy_choices = {
            'Public': 0,
            'Friends': 1,
            'Only me': 2,
        }
        post = Post.objects.create(
            user = request.user,
            content = content,
            privacy = privacy_choices[privacy],
            has_img = request.FILES.get('image') != None,
            has_vid = request.FILES.get('video') != None,
            time = dt.now(),
        )
        post.save()

        user = request.user
        user.privacy = privacy_choices[privacy]
        user.save()

        if request.FILES.get('image') != None:
            images = request.FILES.getlist('image')
            for img in images:
                Post_Img.objects.create(
                    post = post,
                    img = img,
                ).save()
        
        if request.FILES.get('video') != None:
            videos = request.FILES.getlist('video')
            for vid in videos:
                Post_Video.objects.create(
                    post = post,
                    vid = vid,
                ).save()
        
        for hashtag in tags:
            (tag, flag) = Tag.objects.get_or_create(name=hashtag[1:].lower())
            if not flag: tag.save()
            Post_Tag.objects.create(
                post = post,
                tag = tag,
            ).save()

    return redirect('show-post', post.id)

@login_required(login_url='signin')
def like_post(request, id):
    post = Post.objects.get(id=id)
    user = request.user
    (like, flag) = Post_Like.objects.get_or_create(
        post=post,
        user=user,
    )
    if not flag:
        like.delete()
        post.num_of_likes -= 1
    else: 
        like.save()
        post.num_of_likes += 1
    post.save()
    
    return redirect(to=request.META['HTTP_REFERER'])

@login_required(login_url='signin')
def comment_post(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        content = request.POST['content']

        comment = Post_Comment.objects.create(
            user=request.user,
            content=content,
            post=post,
            time=dt.now(),
        )

        if request.FILES.get('image') != None:
            images = request.FILES.getlist('image')
            for img in images:
                Comment_Img.objects.create(
                    comment = comment,
                    img = img,
                ).save()
            comment.has_img = True
        
        if request.FILES.get('video') != None:
            videos = request.FILES.getlist('video')
            for vid in videos:
                Comment_Vid.objects.create(
                    comment = comment,
                    vid = vid,
                ).save()
            comment.has_vid = False
        comment.save()
        post.num_of_comments += 1
        post.save()

    return redirect('show-post', id)

@login_required(login_url='signin')
def share_post(request, id):
    if request.method == 'POST':
        content = request.POST['content']
        privacy = request.POST['privacy']

        tag_pattern = '#[a-zA-Z0-9_]+'
        tags = re.split(tag_pattern, content)

        privacy_choices = {
            'Public': 0,
            'Friends': 1,
            'Only me': 2,
        }
        
        user = request.user
        user.privacy = privacy_choices[privacy]
        user.save()

        shared_post = Post.objects.get(id=id)

        post = Post.objects.create(
            user = request.user,
            content = content,
            privacy = privacy_choices[privacy],
            time = dt.now(),
            is_shared = True,
            shared_post = shared_post,
        )
        post.save()
        shared_post.num_of_shares += 1
        shared_post.save()

        for hashtag in tags:
            (tag, flag) = Tag.objects.get_or_create(name=hashtag[1:].lower())
            if not flag: tag.save()
            Post_Tag.objects.create(
                post = post,
                tag = tag,
            ).save()

        return redirect('show-post', post.id)
    
    post = Post.objects.get(id=id)
    status = ['Public', 'Friends', 'Only me']
    return render(request, 'post-share.html', {
        'post': post_show(posts=[post], user=request.user, num=1),
        'user': request.user,
        'status': status,
    })

@login_required(login_url='signin')
def show_post(request, id):
    post = Post.objects.get(id=id)
    try: section = request.GET.get('section')
    except: section = 'comments'

    likes = []
    if section == 'likes':
        likes = Post_Like.objects.filter(post=post)
    return render(request, 'post.html', {
        'post': post_show(posts=[post], user=request.user, num=1),
        'section': section,
        'likes': likes,
    })

@login_required(login_url='signin')
def edit_post(request, id):
    post = Post.objects.get(id=id)
    user = request.user
    if request.method == 'POST':
        if post.has_img:
            if request.FILES.get('change-img') != None:
                Post_Img.objects.filter(post=post).delete()
                images = request.FILES.getlist('change-img')
                for img in images:
                    Post_Img.objects.create(
                        post = post,
                        img = img,
                    ).save()
        if request.FILES.get('add-img') != None:
            images = request.FILES.getlist('add-img')
            for img in images:
                Post_Img.objects.create(
                    post = post,
                    img = img,
                ).save()
            post.has_img = True
        if post.has_vid:
            if request.FILES.get('change-vid') != None:
                Post_Video.objects.filter(post=post).delete()
                videos = request.FILES.getlist('change-vid')
                for vid in videos:
                    Post_Video.objects.create(
                        post = post,
                        vid = vid,
                    ).save()
        if request.FILES.get('add-vid') != None:
            videos = request.FILES.getlist('add-vid')
            for vid in videos:
                Post_Video.objects.create(
                    post = post,
                    vid = vid,
                ).save()
            post.has_vid = True
        privacy = request.POST['privacy']
        privacy_choices = {
            'Public': 0,
            'Friends': 1,
            'Only me': 2,
        }

        content = html2text(request.POST['content'])
        (content, tags) = make_hashtags(content)
        for hashtag in tags:
            (tag, flag) = Tag.objects.get_or_create(name=hashtag[1:].lower())
            if not flag: tag.save()
            Post_Tag.objects.get_or_create(
                post = post,
                tag = tag,
            )

        post.content = content
        post.privacy = privacy_choices[privacy]
        post.save()

        return redirect('show-post', id)

    status = ['Public', 'Friends', 'Only me']
    return render(request, 'post-edit.html', {
        'post': post_show(posts=[post], user=user, num=1),
        'content': html2text(post.content),
        'status': status,
    })

@login_required(login_url='signin')
def delete_post(request, id):
    post = Post.objects.get(id=id)
    if post.is_shared:
        post1 = post.shared_post
        post1.num_of_shares -= 1
        post1.save()
    post.delete()
    return redirect(to=request.META['HTTP_REFERER'])

@login_required(login_url='signin')
def disable_comments_post(request, id):
    post = Post.objects.get(id=id)
    post.disable_comments = not post.disable_comments
    post.save()
    return redirect(to=request.META['HTTP_REFERER'])

@login_required(login_url='signin')
def edit_comment(request, id):
    pass

@login_required(login_url='signin')
def delete_comment(request, id):
    comment = Post_Comment.objects.get(id=id)
    post = comment.post
    comment.delete()
    post.num_of_comments -= 1
    post.save()
    return redirect('show-post', post.id)

@login_required(login_url='signin')
def reply_comment(request, id):
    if request.method == 'POST':
        content = request.POST['content']
        comment = Post_comment.objects.get(id=id)
        comment.has_reply = True
        comment.save()
        Post_Comment_Reply.objects.create(
            content=content,
            comment=comment,
            time=dt.now(),
        )
        return redirect(to=request.META['HTTP_REFERER'])

def search_tag(request, tag: str):
    tag = Tag.objects.get(name=tag)
    user = request.user
    ids = Post_Tag.objects.values('post').filter(tag=tag)
    ids = [id['post'] for id in ids]
    posts = Post.objects.filter(id__in=ids).filter(Q(privacy__lt=2) | Q(user=request.user))
    return render(request, 'search.html', {
        'tag': f'# {tag.name.title()}',
        'posts': post_show(posts=posts, user=user),
    })




