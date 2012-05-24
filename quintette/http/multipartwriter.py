from django.http import HttpResponse

from email.message import Message
from email.mime.multipart import MIMEMultipart

__all__ = ('ResponseToMIME', 'MultiPartWriter')


class ResponseToMIME(Message):

    def __init__(self, response, disposition="inline", **params):
        Message.__init__(self)
        for k,v in response.items():
            self.add_header(k,v)

        content = response.content
        self.set_payload(content)
        self.add_header('Content-Length', "%d"%(len(content)))

        self.add_header('Content-Disposition', disposition, **params)



class MultiPartWriter(MIMEMultipart):

    def _write_headers(self, generator):
        pass


    def __init__(self, *args):
        MIMEMultipart.__init__(self, "mixed", _subparts=args)


    def as_response(self):
        content = self.as_string()
        return HttpResponse(content, content_type=self['Content-Type'])


