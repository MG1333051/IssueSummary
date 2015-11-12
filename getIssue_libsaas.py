'''
Created on 20151111

@author: xiaobena
'''
import csv
from libsaas.services import github

basic = github.Github('username', 'passport')

repo = basic.repo('numpy', 'numpy')

headers = ['number', 'id', 'created_at', 'updated_at', 'closed_at', 'state', 
           'locked', 'assignee', 'milestone', 'comments', 'title', 'pull_request',
           'user','closed_by', 'labels', 'html_url', 'labels_url', 'url', 'events_url', 
           'comments_url', 'body']

with open('F:/stocks.csv','w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    
    for i in range(1,2):
        issues = repo.issues().get(state='closed', page = i)
        for issue in issues:
            try:
                print ('issue: ', issue)
                f_csv.writerow(issue)
            except:
                print(issue['number'])


    


