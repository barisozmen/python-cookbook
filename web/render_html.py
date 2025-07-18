
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










"""
html_tree = [
    "html",
    [
        "head",
        ["title", "My Page"],
        ["meta charset='UTF-8'"]
    ],
    [
        "body",
        ["h1", "Hello World"],
        ["p", "This is a paragraph."],
        ["br"],
        ["img src='cat.jpg' alt='A cat'"]
    ]
]

print(render_html(html_tree))

---
<html>
	<head>
		<title>
			My Page
		</title>
		<meta charset='UTF-8'>
	</head>
	<body>
		<h1>
			Hello World
		</h1>
		<p>
			This is a paragraph.
		</p>
		<br>
		<img src='cat.jpg' alt='A cat'>
	</body>
</html>
--

"""
