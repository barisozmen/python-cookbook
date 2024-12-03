
self_closing_tags = ['img', 'br', 'link', 'meta']


def render_html(raw, indent=0):
      # print('raw>',raw)
    if raw is None: return
    splitted = raw[0].split(maxsplit=1)
    tag, attributes = splitted if len(splitted)>1 else (splitted[0], '')
    html = '\t'*indent + (f'<{tag} {attributes}>\n' if len(attributes) else f'<{tag}>\n')
    for c in raw[1:]:
        if isinstance(c, str):
            html += '\t'*(indent+1) + c + '\n'
        else:
            html += render_html(c, indent+1)
    html += '\t'*indent + ('' if tag in self_closing_tags else f'</{tag}>') + '\n'
    return html