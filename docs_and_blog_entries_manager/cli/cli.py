from cli.comand.main_command import MainCommand
from cli.comand.sub.blog_command import BlogCommand
from cli.comand.sub.options.display_blog_entry_option import DisplayBlogEntryOption
from config.blog_config import BlogConfig


def main():
    blog_config = BlogConfig.load()
    MainCommand(BlogCommand(blog_config, DisplayBlogEntryOption(blog_config))).run()


if __name__ == '__main__':
    main()
