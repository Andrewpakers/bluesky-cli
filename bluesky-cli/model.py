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
    

def createSkeet(rawSkeet):
    skeet = {}
    skeet['postid'] = rawSkeet['postid']