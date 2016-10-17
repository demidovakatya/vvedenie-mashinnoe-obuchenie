# process_links.py

# def add_mooc_tag(df):
#     save_updated_links(df) 
#     mooc_sites = ['coursera.org', 'datacamp.com', 
#                   'edx.org', 'ocw.mit.edu', 'stepic.org', 
#                   'udacity.com']               
#     for i in df.index:
#         if df.base[i] in mooc_sites:
#             df.tags[i] += ' mooc'
#     return df
#     # df['mooc'] = [(base in mooc_sites) for base in df['base']]
#     # df['tags'] = [df.loc[i, 'tags'] + df.loc[i, 'mooc'] * ' mooc' for i in df.index]

# def add_social_tag(df):
#     save_updated_links(df) 
#     social_sites = ['reddit.com', 'telegram.me', 'vk.com']               
#     for i in df.index:
#         if df.base[i] in social_sites:
#             df.tags[i] += ' social'
#     return df
#     # df['social'] = [(base in social_sites) for base in df['base']]
