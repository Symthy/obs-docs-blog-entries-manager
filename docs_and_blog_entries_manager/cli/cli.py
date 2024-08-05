from cli.comand.blog.blog_command import BlogCommand
from cli.comand.blog.options.display_blog_entry_option import DisplayBlogEntryOption
from cli.comand.main_command import MainCommand
from config.blog_config import BlogConfig


def main():
    blog_config = BlogConfig.load()
    MainCommand(BlogCommand(blog_config, DisplayBlogEntryOption(blog_config))).run()


if __name__ == '__main__':
    main()
