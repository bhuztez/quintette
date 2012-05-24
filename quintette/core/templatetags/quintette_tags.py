from django import template
from quintette.conf import settings


register = template.Library()


class PreprocessNode(template.Node):
    def render(self, context):
        return ''


class Parser(template.Parser):

    def __init__(self, tokens, tags, filters):
        self.tokens = tokens
        self.tags = tags
        self.filters = filters


    def parse(self, parse_until=[]):
        tokens = []

        while self.tokens:
            token = self.next_token()
            if token.token_type != template.TOKEN_BLOCK:
                tokens.append(token)
                continue

            if token.contents in parse_until:
               # put token back on token list so calling code knows why it terminated
               self.prepend_token(token)
               return tokens

            try:
                command = token.contents.split()[0]
            except IndexError:
                self.empty_block_tag(token)

            if not command.isupper():
                tokens.append(token)
                continue

            try:
                compile_func = self.tags[command]
            except KeyError:
                self.invalid_block_tag(token, command, parse_until)
            try:
                compiled_result = compile_func(self, token)
            except template.TemplateSyntaxError, e:
                if not self.compile_function_error(token, e):
                    raise

            tokens.extend(compiled_result)


        if parse_until:
            self.unclosed_block_tag(parse_until)

        return tokens



@register.tag
def preprocess(parser, node):
    parser.tokens = Parser(parser.tokens, parser.tags, parser.filters).parse()
    return PreprocessNode()



@register.tag
def IF(parser, node):
    try:
        tag_name, app, arg = node.contents.split(None, 2)
    except ValueError:
        raise template.TemplateSyntaxError("'IF' tag requires exactly two argument.")

    if arg != 'INSTALLED':
        raise template.TemplateSyntaxError("The second argument of 'IF' tag must be 'INSTALLED'")

    tokens_true = parser.parse(('ELSE', 'ENDIF'))

    token = parser.next_token()
    if token.contents == 'ELSE':
        tokens_false = parser.parse(('ENDIF',))
        parser.delete_first_token()
    else:
        tokens_false = []


    if app in settings.INSTALLED_APPS:
        return tokens_true

    return tokens_false







