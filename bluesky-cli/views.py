import textwrap
import statics
import cli_box
import re

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
    def wrapText(self, text, max_length=None):
        if not max_length:
            max_length = self.max_width
        def wrp_message(message):
            lines = message.split('\n')
            section = ''
            for line in lines:
                # if '\033]8;' in line or "╭" in line or "│" in line:
                #     section += line + "\n"
                #     continue
                if len(line) > max_length:
                    w = textwrap.TextWrapper(width=max_length, break_long_words=True)
                    line = '\n'.join(w.wrap(line))
                section += line + "\n"
            return section
        rendered_message = []
        for line in text:
            rendered_message.append(wrp_message(line))
        return rendered_message
    def renderLogo(self):
        print(self.color('BLUE', self.logo))
    def link(self, uri, label=None):
        # return uri
        if label is None: 
            label = uri
        parameters = ''
        # label = textwrap.shorten(label, width=50, placeholder="...")

        # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
        # escape_mask = f'\033]8;{parameters};{uri}\033\\{label}\033]8;;\033\\'
        string = f'\033]8;{parameters};{uri}\033\\{label}\033]8;;\033\\'
        return string
        # return escape_mask.format(parameters, uri, label)
    def renderEmbed(self, embed):
        x = re.split("embed.", embed['$type'])[1]
        recordType = re.split('#', x)[0]
        text = ""
        try:
            if recordType == 'record' and '$type' in embed['record'].keys():
                ref = re.split("#", embed['record']['$type'])[1]
                if ref == 'viewRecord':
                    text = "\n" + self.color("UNDERLINE", self.color("RED","Quoted")) + "\n" + self.color('GREEN', embed['record']['author']['displayName']) + ' ' + self.color('GRAY', '@' + embed["record"]['author']['handle']) + '\n'
                    text += embed['record']['value']['text'] + '\n'
                    if 'embed' in embed['record']['value'].keys():
                        text += self.renderEmbed(embed['record']['value']['embed'])
                if ref == "generatorView":
                    pass
            if recordType == 'images':
                images = embed['images']
                for image in images:
                    if 'fullsize' in image.keys():
                        text += "\n" + self.color("UNDERLINE", self.color("BLUE","Image")) + "\n" + self.link(image["fullsize"], "(Link)") + "\nAlt: " + image['alt'] + '\n'
                    else:
                        text += "\n" + self.color("UNDERLINE", self.color("BLUE","Image")) + "\n" + image['alt'] + '\n'
            if recordType == 'external':
                external = embed['external']
                text += "\n" + self.color("UNDERLINE", self.color("BLUE", self.link(external['uri'], "(Link)"))) + "\nTitle: " + external['title'] + '\n'
        except Exception as error:
            print('ERROR', error)
            print('embed', embed)
        if text == "":
            return ""
        # return cli_box.rounded(self.wrapText([text]), align="left")
        return text
        # return cli_box.rounded(text)
    def renderSkeet(self, skeet):
        text = []
        if 'reply' in skeet.keys():
            if skeet['reply']['parent']['$type'] == "app.bsky.feed.defs#postView":
                string = ''
                string = self.color('GRAY', skeet['reply']['parent']['author']['displayName'] + ' [' + skeet['reply']['parent']['author']['handle']) + ']\n'
                string += skeet['reply']['parent']['record']['text']
                if 'embed' in skeet['reply']['parent'].keys():
                    string += '\n' + self.renderEmbed(skeet['reply']['parent']['embed'])
                text.append(string)
        string = ''
        string = self.color('GREEN', skeet['post']['author']['displayName']) + ' ' + self.color('GRAY', '@' + skeet["post"]['author']['handle']) + '\n'
        string += skeet['post']['record']['text'] + '\n'
        string += 'Likes: ' + str(skeet['post']['likeCount']) + ' ' + 'Replies: ' + str(skeet['post']['replyCount']) + ' ' + 'Reposts: ' + str(skeet['post']['repostCount'])
        # Use the renderEmbed function
        if 'embed' in skeet['post'].keys():
            string += '\n' + self.renderEmbed(skeet['post']['embed'])
        text.append(string)
        # print('text', text)
        rendered_box = cli_box.rounded(self.wrapText(text), align="left")
        print(rendered_box)