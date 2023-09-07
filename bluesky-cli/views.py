import textwrap
import statics
import cli_box

class bcolors:
    GRAY = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN =  '\033[36m'
    WHITE = '\033[37m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class viewsRenderer():
    def __init__(self):
        self.logo = statics.logo_string
        self.help = statics.help_string
        self.max_width = 70
    def color(self, color, text):
        return f'{getattr(bcolors, color)}{text}{bcolors.ENDC}'
    def renderBox(self, text):
        def wrp_message(message):
            lines = message.split('\n')
            section = ''
            for line in lines:
                if len(line) > self.max_width:
                    w = textwrap.TextWrapper(width=self.max_width, break_long_words=False)
                    line = '\n'.join(w.wrap(line))
                section += line + "\n"
            return section
        rendered_message = []
        if 'parent' in text.keys():
            rendered_message.append(wrp_message(text['parent']))
        rendered_message.append(wrp_message(text['author']))
        return cli_box.box(rendered_message, align="left")
    def renderLogo(self):
        print(self.color('BLUE', self.logo))
    def renderSkeet(self, skeet):
        text = {}
        if 'reply' in skeet.keys():
            if skeet['reply']['parent']['$type'] == "app.bsky.feed.defs#postView":
                text['parent'] = self.color('GRAY', 'Replying to ' + skeet['reply']['parent']['author']['displayName'] + ' [' + skeet['reply']['parent']['author']['handle']) + ']\n'
                text['parent'] += skeet['reply']['parent']['record']['text']
        text['author'] = skeet['post']['author']['displayName'] + ' ' + self.color('GRAY', '@' + skeet["post"]['author']['handle']) + '\n'
        text['author'] += skeet['post']['record']['text'] + '\n'
        text['author'] += 'Likes: ' + str(skeet['post']['likeCount']) + ' ' + 'Replies: ' + str(skeet['post']['replyCount']) + ' ' + 'Reposts: ' + str(skeet['post']['repostCount'])
        rendered_box = self.renderBox(text)
        print(rendered_box)