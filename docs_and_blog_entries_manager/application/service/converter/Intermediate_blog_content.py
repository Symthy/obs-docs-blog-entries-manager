from domain.blogs.value.blog_content import BlogContent


class IntermediateBlogContent:
    def __init__(self, blog_content: BlogContent):
        self.__blog_content = blog_content

    @property
    def value(self):
        return self.__blog_content.value
