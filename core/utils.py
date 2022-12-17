from random import randint
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from .models import *
from datetime import datetime as dt
import re

def num_show(num: int):
    if num == 0: return 'no'
    if num < 1000: return num
    if num >= 1000 and num < 1000000: return f'{num%1000}k'
    if num >= 1000000 and num < 1000000000: return f'{num%1000000}m'
    if num >= 1000000000 and num < 1000000000000: return f'{num%1000000000}p'

def time_show(time: dt):
    now = dt.now()
    time = time.replace(tzinfo=None)
    diff = (now - time).total_seconds()

    if diff < 60: unit = 'second'
    elif diff >= 60 and diff < 60*60: diff //= 60; unit='minute'
    elif diff >= 60*60 and diff < 60*60*24: diff //= (60*60); unit='hour'
    elif diff >= 60*60*24 and diff < 60*60*24*30: diff //= (60*60*24); unit='day'
    elif diff >= 60*60*24*30 and diff < 60*60*24*365: diff //= (60*60*24*30); unit='month'
    elif diff >= 60*60*24*365: diff //= (60*60*24*365); unit='year'
    
    if diff != 1: unit += 's'
    return f'{int(diff)} {unit} ago'

def post_show(posts: Post, user: User, num: int = 0):
    posts_v1 = []
    for post_v1 in posts:
        # collecting post images
        imgs = []
        if post_v1.has_img:
            imgs_v1 = Post_Img.objects.filter(post=post_v1)
            for img_v1 in imgs_v1:
                imgs.append(img_v1.img)
        vids = []
        # collecting post videos
        if post_v1.has_vid:
            vids_v1 = Post_Video.objects.filter(post=post_v1)
            for vid_v1 in vids_v1:
                vids.append(vid_v1.vid)
        # is the user liked the post before?
        is_liked = Post_Like.objects.filter(user=user, post=post_v1).exists()
        post = {
            'id': post_v1.id,
            'content': post_v1.content,
            'user': post_v1.user,
            'imgs': imgs,
            'vids': vids,
            'time': time_show(post_v1.time),
            'privacy': post_v1.privacy,
            'has_img': post_v1.has_img,
            'has_vid': post_v1.has_vid,
            'liked': is_liked,
            'likes_num': num_show(num=post_v1.num_of_likes),
            'comments_num': num_show(num=post_v1.num_of_comments),
            'shares_num': num_show(num=post_v1.num_of_shares),
            'is_shared': post_v1.is_shared,
            'shared_post': post_show(posts=[post_v1.shared_post], user=user, num=1) if post_v1.is_shared else None,
            'disable_comments': post_v1.disable_comments,
            'comments': comment_show(comments=Post_Comment.objects.filter(post=post_v1))
            }
        if num == 1: return post
        posts_v1.append(post)
    return posts_v1

def comment_show(comments: Post_Comment):
    comments_v1 = []
    for comment in comments:
        imgs = []
        if comment.has_img:
            imgs_v1 = Comment_Img.objects.filter(comment=comment)
            for img_v1 in imgs_v1:
                imgs.append(img_v1.img)
        vids = []
        if comment.has_vid:
            vids_v1 = Comment_Vid.objects.filter(comment=comment)
            for vid_v1 in vids_v1:
                vids.append(vid_v1.vid)
        replies = []
        if comment.has_reply:
            replies_v1 = Post_Comment_Reply.objects.filter(comment=comment)
            for reply_v1 in replies_v1:
                imgs = []
                if reply_v1.has_img:
                    imgs_v1 = Reply_Img.objects.filter(reply=reply_v1)
                    for img_v1 in imgs_v1:
                        imgs.append(img_v1.img)
                vids = []
                if comment.has_vid:
                    vids_v1 = Reply_Vid.objects.filter(reply=reply_v1)
                    for vid_v1 in vids_v1:
                        vids.append(vid_v1.vid)
                replies.append({
                    'user': reply_v1.user,
                    'content': reply_v1.content,
                    'has_img': reply_v1.has_img,
                    'has_vid': reply_v1.has_vid,
                    'imgs': imgs,
                    'vids': vids,
                    'time': time_show(reply_v1.time),
                })

        comment_v1 = {
            'id': comment.id,
            'content': comment.content,
            'user':comment.user,
            'imgs': imgs,
            'vids': vids,
            'has_img': comment.has_img,
            'has_vid': comment.has_vid,
            'time': time_show(comment.time),
            'replies': replies,
        }
        comments_v1.append(comment_v1)
    return comments_v1

def make_hashtag(pattern: str, string: str):
	matches = re.finditer(pattern, string)
	output_string = ''
	last = 0
	for match in matches:
		(s, e) = match.span()
		tag = string[s: e]
		output_string += '{0}<a href="/search/tags/{2}/"style="text-decoration:none;">{1}</a>'.format(string[last: s], tag, tag[1:].lower())
		last = e
	output_string += string[last:]
	return output_string

def make_hashtags(content):
    tag_pattern = '#[a-zA-Z0-9_]+'
    tags = re.findall(tag_pattern, content)
    content = make_hashtag(tag_pattern, content)
    return (content, tags)

def html2text(html: str):
    tag_pattern = '<.*?>'
    return re.sub(tag_pattern, '', html)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# this class to generate token which used to makesure that user will use the link for only once
class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))

token_gen = AppTokenGenerator()
