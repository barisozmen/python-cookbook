
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



# Another example
"""
# Dashboard HTML structure using the render_html function
dashboard_tree = [
    "html lang='en'",
    [
        "head",
        ["meta charset='UTF-8'"],
        ["meta name='viewport' content='width=device-width, initial-scale=1.0'"],
        ["title", "Advanced Analytics Dashboard"],
        ["style", css_styles]
    ],
    [
        "body",
        [
            "nav class='navbar'",
            ["a href='#' class='navbar-brand'", "DataFlow Analytics"],
            [
                "div class='navbar-menu'",
                ["a href='#' class='navbar-item'", "Dashboard"],
                ["a href='#' class='navbar-item'", "Analytics"],
                ["a href='#' class='navbar-item'", "Reports"],
                ["a href='#' class='navbar-item'", "Users"],
                ["a href='#' class='navbar-item'", "Settings"]
            ]
        ],
        [
            "div class='container'",
            [
                "div class='dashboard-header'",
                ["h1 class='dashboard-title'", "Executive Dashboard"],
                ["p class='dashboard-subtitle'", "Real-time business intelligence and performance metrics"]
            ],
            [
                "div class='stats-grid'",
                [
                    "div class='stat-card'",
                    [
                        "div class='stat-header'",
                        ["div class='stat-title'", "Total Users"],
                        ["div class='stat-icon'", "👥"]
                    ],
                    ["div class='stat-value'", "24,587"],
                    ["div class='stat-change positive'", "↗ +12.5% from last month"]
                ],
                [
                    "div class='stat-card'",
                    [
                        "div class='stat-header'",
                        ["div class='stat-title'", "Monthly Revenue"],
                        ["div class='stat-icon'", "💰"]
                    ],
                    ["div class='stat-value'", "$847,293"],
                    ["div class='stat-change positive'", "↗ +8.2% from last month"]
                ],
                [
                    "div class='stat-card'",
                    [
                        "div class='stat-header'",
                        ["div class='stat-title'", "Orders Processed"],
                        ["div class='stat-icon'", "📦"]
                    ],
                    ["div class='stat-value'", "15,429"],
                    ["div class='stat-change negative'", "↘ -3.1% from last month"]
                ],
                [
                    "div class='stat-card'",
                    [
                        "div class='stat-header'",
                        ["div class='stat-title'", "Conversion Rate"],
                        ["div class='stat-icon'", "📊"]
                    ],
                    ["div class='stat-value'", "3.24%"],
                    ["div class='stat-change positive'", "↗ +0.8% from last month"]
                ]
            ],
            [
                "div class='content-grid'",
                [
                    "div class='chart-container'",
                    [
                        "div class='chart-header'",
                        ["h3 class='chart-title'", "Revenue Trends"],
                        [
                            "select style='padding: 0.5rem; border: 1px solid #ddd; border-radius: 5px;'",
                            ["option", "Last 7 days"],
                            ["option", "Last 30 days"],
                            ["option", "Last 90 days"]
                        ]
                    ],
                    ["div class='chart-placeholder'", "📈 Interactive Chart Would Appear Here"]
                ],
                [
                    "div class='activity-feed'",
                    ["h3 class='chart-title' style='margin-bottom: 1.5rem;'", "Recent Activity"],
                    [
                        "div class='activity-item'",
                        ["div class='activity-avatar'", "JD"],
                        [
                            "div class='activity-content'",
                            ["div class='activity-text'", "John Doe completed a purchase of $2,450"],
                            ["div class='activity-time'", "2 minutes ago"]
                        ]
                    ],
                    [
                        "div class='activity-item'",
                        ["div class='activity-avatar'", "SM"],
                        [
                            "div class='activity-content'",
                            ["div class='activity-text'", "Sarah Miller updated her profile information"],
                            ["div class='activity-time'", "15 minutes ago"]
                        ]
                    ],
                    [
                        "div class='activity-item'",
                        ["div class='activity-avatar'", "RT"],
                        [
                            "div class='activity-content'",
                            ["div class='activity-text'", "Robert Taylor submitted a support ticket"],
                            ["div class='activity-time'", "32 minutes ago"]
                        ]
                    ],
                    [
                        "div class='activity-item'",
                        ["div class='activity-avatar'", "AL"],
                        [
                            "div class='activity-content'",
                            ["div class='activity-text'", "Amanda Lee registered as a new user"],
                            ["div class='activity-time'", "1 hour ago"]
                        ]
                    ],
                    [
                        "div class='activity-item'",
                        ["div class='activity-avatar'", "MJ"],
                        [
                            "div class='activity-content'",
                            ["div class='activity-text'", "Michael Johnson cancelled his subscription"],
                            ["div class='activity-time'", "2 hours ago"]
                        ]
                    ]
                ]
            ],
            [
                "div class='data-table'",
                [
                    "div class='chart-header'",
                    ["h3 class='chart-title'", "Top Performing Products"],
                    ["input type='search' placeholder='Search products...' style='padding: 0.5rem; border: 1px solid #ddd; border-radius: 5px;'"]
                ],
                [
                    "table",
                    [
                        "thead",
                        [
                            "tr",
                            ["th", "Product Name"],
                            ["th", "Category"],
                            ["th", "Sales"],
                            ["th", "Revenue"],
                            ["th", "Status"],
                            ["th", "Description"]
                        ]
                    ],
                    [
                        "tbody",
                        [
                            "tr",
                            ["td", "Premium Dashboard Pro"],
                            ["td", "Software"],
                            ["td", "2,847"],
                            ["td", "$284,700"],
                            ["td", ["span class='status-badge status-active'", "Active"]],
                            ["td", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore."]
                        ],
                        [
                            "tr",
                            ["td", "Analytics Suite Enterprise"],
                            ["td", "Software"],
                            ["td", "1,923"],
                            ["td", "$192,300"],
                            ["td", ["span class='status-badge status-active'", "Active"]],
                            ["td", "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo."]
                        ],
                        [
                            "tr",
                            ["td", "Mobile App Bundle"],
                            ["td", "Mobile"],
                            ["td", "1,456"],
                            ["td", "$145,600"],
                            ["td", ["span class='status-badge status-pending'", "Pending"]],
                            ["td", "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."]
                        ],
                        [
                            "tr",
                            ["td", "Cloud Storage Pro"],
                            ["td", "Cloud"],
                            ["td", "1,234"],
                            ["td", "$123,400"],
                            ["td", ["span class='status-badge status-active'", "Active"]],
                            ["td", "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim."]
                        ],
                        [
                            "tr",
                            ["td", "Legacy System Support"],
                            ["td", "Support"],
                            ["td", "892"],
                            ["td", "$89,200"],
                            ["td", ["span class='status-badge status-inactive'", "Inactive"]],
                            ["td", "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium."]
                        ]
                    ]
                ]
            ]
        ],
        [
            "footer class='footer'",
            [
                "div class='footer-content'",
                [
                    "div class='footer-links'",
                    ["a href='#'", "Privacy Policy"],
                    ["a href='#'", "Terms of Service"],
                    ["a href='#'", "Support"],
                    ["a href='#'", "Documentation"],
                    ["a href='#'", "API"]
                ],
                ["p", "© 2025 DataFlow Analytics. All rights reserved. | Built with modern web technologies for optimal performance and user experience."]
            ]
        ]
    ]
]
"""
