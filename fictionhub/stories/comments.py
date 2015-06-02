import stories.views
import stories.models
comments = stories.models.Comment.objects.all()
nested_comments = list(stories.views.get_comment_list(comments))
print("nested comments" + str(nested_comments))
