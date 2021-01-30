#!/usr/bin/env python
# coding: utf-8

# # Exploration of Hacker News data
# 
# In this project, we will be loading a data set from Hacker News, where user-submitted stories (known as "posts") are voted and commented upon, similar to reddit. Hacker News is extremely popular in technology and startup circles, and posts that make it to the top of Hacker News' listings can get hundreds of thousands of visitors as a result.
# 
# We're specifically interested in posts whose titles begin with either `Ask HN` or `Show HN`. Users submit `Ask HN` posts to ask the Hacker News community a specific question.
# 
# We'll compare these two types of posts to determine:
# - Do `Ask HN` or `Show HN` receive more comments on average?
# - Do posts created at a certain time receive more comments on average?

# First, let's import necessary librarys and read the data set into a list of lists:

# In[1]:


from csv import reader
opened_file = open('hacker_news.csv')
read_file = reader(opened_file)
hn = list(read_file)
# display first five rows
print(hn[:5])


# The first row is just the headers, so those can be extracted and removed from the data set.

# In[2]:


headers = hn[0]
print(headers)
hn = hn[1:]
print(hn[:5])


# Filter the data to only retain data columns that contain posts.

# In[3]:


ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = str(row[1])
    if title.lower().startswith('ask hn'):
        ask_posts.append(row)
    elif title.lower().startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)
# check number of posts in each list
print(len(ask_posts))
print(len(show_posts))
print(len(other_posts))


# Now, let's find the total number of comments in each type of post.

# In[4]:


total_ask_comments = 0

for row in ask_posts:
    total_ask_comments += int(row[4])
# find average number of comments per ask post
avg_ask_comments = total_ask_comments / len(ask_posts)
print(avg_ask_comments)

total_show_comments = 0

for row in show_posts:
    total_show_comments += int(row[4])
# find average number of comments per show post
avg_show_comments = total_show_comments / len(show_posts)
print(avg_show_comments)


# Based on the average number of comments in ask and show posts, it appears that ask posts get ~4 more comments that show posts on average. Let's focus on these ask posts for the rest of the analysis.

# Now, let's determine if ask posts created at a certain time are more likely to attract comments.

# In[5]:


import datetime as dt

result_list = []

for row in ask_posts:
    created_at = row[6]
    num_posts = int(row[4])
    time_num_list = [created_at, num_posts]
    result_list.append(time_num_list)

# create two empty dictionaries
counts_by_hour = {}
comments_by_hour = {}
# extract time information
for row in result_list:
    time = dt.datetime.strptime(row[0], '%m/%d/%Y %H:%M')
    hour = dt.datetime.strftime(time, '%H')
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = row[1]
    else:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += row[1]

print(counts_by_hour)
print(comments_by_hour)
    


# Now, let's find the average number of posts in each hour using the two dictionaries that I created.

# In[6]:


avg_posts_per_hour = []

for hour in comments_by_hour:
    avg_posts_per_hour.append([hour, (comments_by_hour[hour]/counts_by_hour[hour])])

print(avg_posts_per_hour)


# We have the information we need, but it is hard to make out given the format of the data. I will sort the list of lists and display the five highest values.

# In[7]:


# swap order of elements in avg_posts_per_hour list
swap_avg_by_hour = []

for hour in avg_posts_per_hour:
    swap_avg_by_hour.append([hour[1], hour[0]])

print(swap_avg_by_hour)

# sort the list of lists
sorted_swap = sorted(swap_avg_by_hour, reverse = True)

print(sorted_swap)

for elem in sorted_swap[:5]:
    hour = dt.datetime.strptime(elem[1], "%H")
    hour = hour.strftime('%H:%M')
    average = elem[0]
    print('{0}: {1:.2f} average comments per post'.format(hour, average))


# Timezones are in EST. Which means, in CST, the most common times (in order from most to least) are 2:00 PM, 1:00 PM, 7:00 PM, 3:00 PM, and 10:00 PM.
