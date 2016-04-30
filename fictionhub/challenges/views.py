import praw    

from django.shortcuts import render

from .models import Prompt


def get_prompts():
    r = praw.Reddit(user_agent='Request new prompts from /r/writingprompts by /u/raymestalez')
    subreddit = r.get_subreddit('writingprompts')
    prompts = subreddit.get_new(limit=128)
    new_prompts = list(prompts)
    prompts = []


    hot_prompts = list(subreddit.get_hot(limit=50))
    
    max_age = 5*60
    # less than 5 replies, more than 1 upvote and less than 60 minutes old
    for prompt in new_prompts:
        # 1 4 5*60
        if (prompt.score > 1) \
        and ((prompt.num_comments-2) < 3) \
        and (age(prompt.created_utc) < max_age):
            if prompt.num_comments > 0:
                prompt.num_comments -= 2 # remove 2 fake replies
            prompt.age = round(age(prompt.created_utc)/60,1)
            # prompt.permalink = prompt.permalink.replace("www", "zn")
            prompt.sort = prompt.score * (1-(prompt.age/5))

            # prompt position
            for index, p in enumerate(hot_prompts):
                if prompt.title == p.title:
                    setattr(prompt, "position", index)
                    # prompt.position == index

            prompt.title = prompt.title.replace("[WP]", "", 1).strip()   
            prompts.append(prompt)
                


    # sort by score
    prompts.sort(key=lambda p: p.score, reverse=True)

    for p in prompts:
        prompt = Prompt.objects.get_or_create(reddit_url = p.permalink)
        prompt.prompt = p.title
        prompt.position = p.position
        prompt.score = p.score
        prompt.num_comments = p.num_comments
        prompt.age = p.age
        prompt.save()
        
        

    return prompts[:16]
