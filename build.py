import os
import frontmatter
from markdown import markdown


def eval_template(template, metadata):
	return eval('f"""'+template+'"""', metadata)


def build_post(post_path):
	post = frontmatter.load(post_path)
	post.metadata['html'] = markdown(post.content, extensions=['extra'])
	post.metadata['link'] = '/'+post_path[:-3]+'.html'
	with open('templates/post.mustache', 'r') as f:
		html = eval_template(f.read(), post.metadata)
		with open(post_path[:-3]+'.html', 'w') as f:
			f.write(html)
	return post.metadata


def build_landing_page(posts):
	with open('templates/post_card.mustache', 'r')as f:
		post_card_template = f.read()
	html = ''
	for post in posts:
		html += eval_template(post_card_template, post)
	with open('templates/index.mustache', 'r') as f:
		html = eval_template(f.read(), locals())
		with open('index.html', 'w') as f:
			f.write(html)


# {'title': 'Markdown Test Page', 'date': 'Today', 'summary': 'Testing Markdown', 'link': '/post/testing_post.html'}


def build_folder_recursively(folder):
	posts = [os.path.join(folder, i) for i in os.listdir(folder)]
	posts_built = []
	for post in posts:
		if os.path.isdir(post):
			posts_built.extend(build_folder_recursively(post))
		elif post.endswith('.md'):
			posts_built.append(build_post(post))
	return posts_built


built = build_folder_recursively('post')
build_landing_page(built)
