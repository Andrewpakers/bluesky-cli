# skeet = {
#     "postid": "string",
#     'link': 'string',
#     "author": {
#         "did": "string",
#         "handle": "string",
#         "displayName": "string",
#     },
#     "text": "string",
#     "type": "string",
#     'likeCount': 0,
#     'replyCount': 0,
#     'repostCount': 0,
#     'createdAt': 'string',
#     'embed': {
#         'images': [
#             {
#                 "alt": "string",
#                 "link": "string",
#             },
#         ],
#         'external': {
#             "title": "string",
#             "link": "string",
#         },
#         'record': {
#             "same as post record": "string",
#         },
#         'generatorFeed': {
#             'title': 'string',
#             'link': 'string',
#             'description': 'string',
#         },
#     },
#     "reply": {
#         "parent": {
#             skeet
#         },
#         "root": {
#             skeet
#         },
#     },
# }

def processURI(uri):
    try:
        parsedURI = uri.split('/')
        data = {
            'author': {
                'did': parsedURI[2].split(':')[2],
            },
            'postid': parsedURI[4],
        }
        return data
    except Exception as error:
        print('ERROR', error)
        print('uri', uri)
        return {
            'did': '',
            'postid': '',
        }
def createEmbed(rawEmbed, did):
    try:
        embed = {}
        if 'images' in rawEmbed.keys():
            embed['images'] = []
            for image in rawEmbed['images']:
                if 'fullsize' in image.keys():
                    embed['images'].append({
                        'alt': image['alt'],
                        'link': image['fullsize'],
                    })
                else:
                    link = "https://av-cdn.bsky.app/img/feed_fullsize/plain/did:plc:" + did + '/' + image['image']['ref']['$link']
                    if image['image']['mimeType'] == 'image/jpeg':
                        link += '@jpeg'
                    else:
                        print('image type not detected', image['mimeType'])
                    embed['images'].append({
                        'alt': image['alt'],
                        'link': link,
                    })
        if 'external' in rawEmbed.keys():
            embed['external'] = {
                'title': rawEmbed['external']['title'],
                'link': rawEmbed['external']['uri'],
            }
        if 'record' in rawEmbed.keys():
            if '$type' in rawEmbed['record'] and 'recordWithMedia' in rawEmbed['record']['$type']:
                if "media" in rawEmbed.keys():
                    if "images" in rawEmbed['media'].keys():
                        embed['images'] = []
                        for image in rawEmbed['media']['images']:
                            if 'fullsize' in image.keys():
                                embed['images'].append({
                                    'alt': image['alt'],
                                    'link': image['fullsize'],
                                })
                            else:
                                link = "https://av-cdn.bsky.app/img/feed_fullsize/plain/did:plc:" + did + '/' + image['image']['ref']['$link']
                                if image['image']['mimeType'] == 'image/jpeg':
                                    link += '@jpeg'
                                else:
                                    print('image type not detected', image['mimeType'])
                                embed['images'].append({
                                    'alt': image['alt'],
                                    'link': link,
                                })
            elif '$type' in rawEmbed['record'] and 'record' in rawEmbed['record']['$type']:
                record = {}
                record.update(processURI(rawEmbed['record']['uri']))
                record['author']['handle'] = rawEmbed['record']['author']['handle']
                record['author']['displayName'] = rawEmbed['record']['author']['displayName']
                record['text'] = rawEmbed['record']['value']['text']
                record['link'] = "https://bsky.app/profile/" + record['author']['handle'] + "/post/" + record['postid']
                record['type'] = rawEmbed['record']['value']['$type'].split('.')[3]
                if 'embed' in rawEmbed['record']['value'].keys() and not 'record' in rawEmbed['record']['value']['embed']:
                    record['embed'] = createEmbed(rawEmbed['record']['value']['embed'], record['author']['did'])
                record['createdAt'] = rawEmbed['record']['value']['createdAt']
                embed['record'] = record
            elif '$type' in rawEmbed['record'] and "generator" in rawEmbed['record']['$type']:
                linkData = processURI(rawEmbed['record']['uri'])
                link = "https://bsky.app/profile/did:plc:" + linkData['author']['did'] + "/feed/" + linkData['postid']
                embed['generatorFeed'] = {
                    'title': rawEmbed['record']['displayName'],
                    'link': link,
                    'description': rawEmbed['record']['description'],
                    'author': {
                        'handle': rawEmbed['record']['creator']['handle'],
                        'displayName': rawEmbed['record']['creator']['displayName'],
                        'did': linkData['author']['did'],
                        'link': "https://bsky.app/profile/" + rawEmbed['record']['creator']['handle'],
                    },
                }
        return embed
    except Exception as error:
        print('ERROR', error, error.__cause__, error.__context__)
        print('rawEmbed', rawEmbed)
        return
def processReply(rawReply):
    try:
        reply = {}
        parent = {}
        parent.update(processURI(rawReply['parent']['uri']));
        parent['author']['handle'] = rawReply['parent']['author']['handle']
        parent['author']['displayName'] = rawReply['parent']['author']['displayName']
        parent['author']['link'] = "https://bsky.app/profile/" + rawReply['parent']['author']['handle'],
        parent['text'] = rawReply['parent']['record']['text']
        parent['link'] = "https://bsky.app/profile/" + parent['author']['handle'] + "/post/" + parent['postid']
        parent['type'] = rawReply['parent']['record']['$type'].split('.')[3]
        parent['likeCount'] = rawReply['parent']['likeCount']
        parent['replyCount'] = rawReply['parent']['replyCount']
        parent['repostCount'] = rawReply['parent']['repostCount']
        parent['createdAt'] = rawReply['parent']['record']['createdAt']
        if 'embed' in rawReply['parent'].keys():
            parent['embed'] = createEmbed(rawReply['parent']['embed'], parent['author']['did'])

        root = {}
        root.update(processURI(rawReply['root']['uri']));
        root['author']['handle'] = rawReply['root']['author']['handle']
        root['author']['displayName'] = rawReply['root']['author']['displayName']
        root['author']['link'] = "https://bsky.app/profile/" + rawReply['root']['author']['handle'],
        root['text'] = rawReply['root']['record']['text']
        root['link'] = "https://bsky.app/profile/" + root['author']['handle'] + "/post/" + root['postid']
        root['type'] = rawReply['root']['record']['$type'].split('.')[3]
        root['likeCount'] = rawReply['root']['likeCount']
        root['replyCount'] = rawReply['root']['replyCount']
        root['repostCount'] = rawReply['root']['repostCount']
        root['createdAt'] = rawReply['root']['record']['createdAt']
        if 'embed' in rawReply['root'].keys():
            root['embed'] = createEmbed(rawReply['root']['embed'], root['author']['did'])

        reply['parent'] = parent
        reply['root'] = root
        return reply
    except Exception as error:
        print('ERROR', error)
        print('rawReply', rawReply)
        return
def createSkeet(rawSkeet):
    try:
        skeet = {}
        skeet.update(processURI(rawSkeet['post']['uri']));
        skeet['author']['handle'] = rawSkeet['post']['author']['handle']
        skeet['author']['displayName'] = rawSkeet['post']['author']['displayName']
        skeet['author']['link'] = "https://bsky.app/profile/" + rawSkeet['post']['author']['handle'],
        skeet['text'] = rawSkeet['post']['record']['text']
        skeet['link'] = "https://bsky.app/profile/" + skeet['author']['handle'] + "/post/" + skeet['postid']
        skeet['type'] = rawSkeet['post']['record']['$type'].split('.')[3]
        skeet['likeCount'] = rawSkeet['post']['likeCount']
        skeet['replyCount'] = rawSkeet['post']['replyCount']
        skeet['repostCount'] = rawSkeet['post']['repostCount']
        skeet['createdAt'] = rawSkeet['post']['record']['createdAt']
        if 'embed' in rawSkeet['post'].keys():
            skeet['embed'] = createEmbed(rawSkeet['post']['embed'], skeet['author']['did'])
        if 'reply' in rawSkeet.keys():
            skeet['reply'] = processReply(rawSkeet['reply'])
        return skeet
    except Exception as error:
        print('ERROR', error)
        print('rawSkeet', rawSkeet)
        return