from cli.comand.main_command import MainCommand
from cli.comand.sub.blog_command import BlogCommand


def main():
    MainCommand(BlogCommand()).run()


if __name__ == '__main__':
    main()
