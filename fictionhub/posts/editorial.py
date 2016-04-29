import praw, os, dropbox

from django.http import HttpResponse
# slugify dropbox title
from django.template.defaultfilters import slugify



from .utils import get_prompts, age


# Editorial
def prompt(request):
    prompts = get_prompts()

    promptslist = ["\n\n" + p.title for p in prompts]
    return HttpResponse(promptslist) #prompt.title
    

    
def prompts_repost(request):
    print ("\n\n################ Log ################") 
    print (time.strftime("%d/%m/%Y"))
    print(time.strftime("%H:%M:%S"))
    print ("################")
    
    # Dropbox
    access_token = os.environ["ACCESS_TOKEN"]
    client = dropbox.client.DropboxClient(access_token)
    folder_metadata = client.metadata('/prompts/')
    
    teststring = "\n\n"
    imported = ""
    updated = ""
    
    for file in folder_metadata["contents"]:
        if not file["is_dir"]:
            path = file["path"]
            f, metadata = client.get_file_and_metadata(path)
            text = f.read()
            text = text.decode("utf-8")
    
            md = Markdown(extensions = ['meta', 'codehilite'])
            content = md.convert(text)
            metadata = {}
            for name, value in md.Meta.items():
                metadata[name] = value[0]
                # teststring += name + ": " + value[0] + "<br/>"
    
            # teststring += "Title: " + metadata['title'] + "\n" + \
            #               "Date: " + metadata['date'] + \
            #               "Content: " + content
    
            publish = False
            try:
                if metadata['publish'].strip() == "True":
                    publish = True
            except:
                pass
                    
    
            if publish:
                # Reddit
                r = praw.Reddit(user_agent='Auto submit prompt replies from dropbox by /u/raymestalez')
                r.login(os.environ["REDDITUNAME"],os.environ["REDDITUPASS"])
                subreddit = r.get_subreddit('WritingPrompts')
                
                title = metadata["prompt"].strip()
                # print("Title: " + title)
                
                # remove meta from text
                text = "".join(text.split("\n\n", 1)[1:]).strip()
                body = text
    
                # Get or create prompt            
                thread = list(r.search(title, subreddit=subreddit, sort="new")) #, syntax='cloudsearch'
                if thread:
                    thread = thread[0]
                    teststring += "Thread selected " + title + "\n"
                # else:
                #     thread = r.submit('/r/WritingPrompts', title, text=' ')
                #     print("Thread created " + title)
    

                edited = False
                comments = praw.helpers.flatten_tree(thread.comments)
                for comment in comments:
                    try:
                        if comment.author.name == "raymestalez":
                            comment.edit(body)
                            print ("################")
                            edited = True
                            teststring += "Prompt Edited " + body[:10] + "\n"
                    except:
                        pass
                        
                if not edited:
                    thread.add_comment(body)
                    print ("################")
                    teststring += "Prompt Submitted  " + body[:10]

    return render(request, 'posts/test.html', {
        'teststring': teststring,
    })


