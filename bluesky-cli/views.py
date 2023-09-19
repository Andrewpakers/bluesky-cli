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
        self.max_width = statics.max_width
    def color(self, color, text):
        return f'{getattr(bcolors, color)}{text}{bcolors.ENDC}'
    def wrapText(self, text, max_length=None):
        if not max_length:
            max_length = self.max_width
        def wrp_message(message):
            lines = message.split('\n')
            section = ''
            for o in lines:
                str1 = '\x1b]8;;'
                str2 = '\x1b]8;;\x1b\\'
                idx1 = []
                index = 0
                while index < len(o):
                    index = o.find(str1, index)
                    if index == -1:
                        break
                    idx1.append(index)
                    index += len(str1)
                w = textwrap.TextWrapper(width=max_length, break_long_words=True)
                for splitIndexes in range(len(idx1)):
                    if splitIndexes % 2 != 0:
                        idx1[splitIndexes] = idx1[splitIndexes] + len(str2)
                idx1.insert(0,0)
                parts = [o[i:j] for i,j in zip(idx1, idx1[1:]+[None])]
                for part in parts:
                    if not part.startswith(str1) and len(part) > max_length:
                        section += ('\n'.join(w.wrap(part))) + '\n'
                    else:
                        section += part + '\n'
            return section
        return wrp_message(text)
    def renderLogo(self):
        print(self.color('BLUE', self.logo))
    def link(self, uri, label=None):
        # return uri
        if label is None: 
            label = uri
        parameters = ''
        string = f'\033]8;{parameters};{uri}\033\\{label}\033]8;;\033\\'
        return string
    def renderEmbed(self, embed):
        string = ''
        if 'external' in embed.keys():
            string += "\n" + cli_box.rounded(self.link(embed['external']['link'], self.color("UNDERLINE", self.color("BLUE", "Link:"))) + "\n" + self.wrapText(embed['external']['title']), align="left") + '\n'
            # string += "\n" + self.link(embed['external']['link'], self.color("UNDERLINE", self.color("BLUE", "Link: \n"))) + self.wrapText(embed['external']['title']) + '\n'
        if 'images' in embed.keys():
            for image in embed['images']:
                string += "\n" + cli_box.rounded(self.wrapText(self.link(image["link"], self.color("UNDERLINE", self.color("BLUE", "Image: "))) + image['alt']), align="left") + '\n'
            # print('images', repr(string))
        if 'record' in embed.keys():
            record = ''
            record += "\n" + self.color("UNDERLINE", self.color("RED","Quoted")) + "\n" + self.color('GREEN', embed['record']['author']['displayName']) + ' [' + self.color('GRAY', '@' + embed["record"]['author']['handle']) + ']\n'
            record += self.wrapText(embed['record']['text'])
            if 'embed' in embed['record'].keys():
                record += '\n' + self.renderEmbed(embed['record']['embed'])
            string += "\n" + cli_box.rounded(record, align="left") + '\n'
        if 'generatorFeed' in embed.keys():
            generatorFeed = ''
            generatorFeed += "\n" + self.color("UNDERLINE", self.color("RED","Feed")) + "\n" + self.color('GREEN', embed['generatorFeed']['author']['displayName']) + ' [' + self.color('GRAY', '@' + embed["generatorFeed"]['author']['handle']) + ']\n'
            generatorFeed += self.wrapText(embed['generatorFeed']['description'])
            generatorFeed += '\n' + self.link(embed['generatorFeed']['link'], "(Link)")
            string += "\n" + cli_box.rounded(generatorFeed, align="left") + '\n'
        return string
    def renderSkeet(self, skeet):
        text = []
        if 'reply' in skeet.keys():
            string = ''
            string = self.color('GRAY', skeet['reply']['parent']['author']['displayName'] + ' [' + skeet['reply']['parent']['author']['handle']) + ']\n'
            string += self.wrapText(skeet['reply']['parent']['text'])
            if 'embed' in skeet['reply']['parent'].keys():
                string += '\n' + self.renderEmbed(skeet['reply']['parent']['embed'])
            text.append(string)
        string = ''
        string = self.color('GREEN', skeet['author']['displayName']) + ' ' + self.color('GRAY', '@' + skeet['author']['handle']) + '\n'
        string += self.wrapText(skeet['text'])
        if 'embed' in skeet.keys():
            string += '\n' + self.renderEmbed(skeet['embed'])
        string += '\n' + 'Likes: ' + str(skeet['likeCount']) + ' ' + 'Replies: ' + str(skeet['replyCount']) + ' ' + 'Reposts: ' + str(skeet['repostCount'])
        text.append(string)
        rendered_box = cli_box.rounded(text, align="left")
        print(rendered_box)