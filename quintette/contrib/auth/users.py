class AnonymousUser(object):
    id = None
    
    def __init__(self, request):
        pass

    def __unicode__(self):
        return u'AnonymousUser'

    def __str__(self):
        return unicode(self).encode('utf-8')

    def is_anonymous(self):
        return True

    def is_authenticated(self):
        return False



