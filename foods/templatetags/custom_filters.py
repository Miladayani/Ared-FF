from django import template

register = template.Library()


@register.filter
def count_replies(comment):
    """ شمارش تمام ریپلای‌های تو در تو """
    def recursive_count(comment):
        count = comment.replies.count()
        for reply in comment.replies.all():
            count += recursive_count(reply)
        return count

    return recursive_count(comment)
