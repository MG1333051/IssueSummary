'''
@author: Lenovo
'''
import github
import csv

gh = github.GitHub()
print(gh.users('michaelliao').get())

headers = ['number', 'id', 'reporter', 'created_at', 'updated_at', 'closed_at', 'state', 
           'locked', 'assignee', 'milestone', 'comments', 'label_name', 'title', 'pull_request',
           'user', 'labels', 'html_url', 'labels_url', 'url', 'events_url', 'diff', 'patch',
           'comments_url', 'body']

with open('F:/numpy.csv','w', newline='') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    
    for i in range(1,124):
        issues = gh.repos('numpy')('numpy').issues.get(state='closed', page=i)
        for issue in issues:
            try:
#                print('issue: ', issue)
                reporter = issue['user']['login']
                
                label_names = []
                for label in issue['labels']:
                    label_names.append(label['name'])
                sep =';'
                label_name =  sep.join(label_names)
                
                diff = ''
                patch = ''                
                if 'pull_request' in issue.keys():
                    diff = issue['pull_request']['diff_url']
                    patch = issue['pull_request']['patch_url']
                
                issue_part = {'reporter':reporter, 'label_name':label_name,
                              'diff':diff, 'patch':patch}
                
                issue_all = {}
                issue_all.update(issue)
                issue_all.update(issue_part)
                
                f_csv.writerow(issue_all)
                
            except Exception as e:
                print (issue['number'], ': ', e)                
               
                
                