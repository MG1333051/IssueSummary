'''
Created on 20151111

@author: xiaobena
'''
import csv
import re
import urllib.request

from libsaas.services import github

basic = github.Github('username', 'password')

repo = basic.repo('numpy', 'numpy')

headers = ['number', 'id', 'reporter', 'created_at', 'updated_at', 'closed_at', 'state', 
           'locked', 'assignee', 'milestone', 'comments', 'label_name', 'title', 'pull_request',
           'user', 'labels', 'html_url', 'labels_url', 'url', 'events_url', 'diff', 'patch',
           'comments_url', 'body']

with open('F:/numpy.csv','w',newline='') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    
    for page in range(1,2):
        issues = repo.issues().get(state='closed', page = page)
        for issue in issues:
            try:
                print('issue: ', issue['number'])
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
                    
                    patch_content = urllib.request.urlopen(patch)
                    content = patch_content.read().decode("utf8")
                    
                    lines = content.splitlines()
                    print('content length: ', len(lines))
                    
                    hash = lines[0][5:12]
                    print('hash: ', hash)
                    author = lines[1][5:]
                    print('author: ', author)
                    date = lines[2][5:]
                    print('date: ', date)
                    
                    subject = lines[3][5:]
                    
                    index = 4
                    
                    for i in range(index, len(lines)):
                        if lines[i]=='---':
                            break
                        else:
                            subject += lines[i]
                    print('subject: ', subject)
                    
                    index = i+1
#                    print(i)
                    nfiles = 0
                    ninsertions = 0
                    ndeletions = 0
                    
                    files = []
                    changes = []
                    insertions = []
                    deletions = []
                    
                    for j in range(index, len(lines)):
                        print('j:', j)
                        if '|' not in lines[j]:
                            print('get changed files.')
                            temp = lines[j].strip().split(',')
                            for str in temp:
                                if 'changed' in str:
                                    nfiles = re.findall(r"\d+\.?\d*",str)[0]
                                if 'insertions' in str:
                                    ninsertions = re.findall(r"\d+\.?\d*",str)[0]
                                if 'deletions' in str:
                                    ndeletions = re.findall(r"\d+\.?\d*",str)[0]    
                            break
                        
                        else:
                            temp = lines[j].split('|')
                            files.append(temp[0].strip()) 
                            changes.append(re.findall(r"\d+\.?\d*",temp[1]))
                            print(re.findall(r"\d+\.?\d*",temp[1]))
                            insertions.append(temp[1].count('+'))
                            deletions.append(temp[1].count('-'))
                     
                    index = j + 2       
                    locations = []
                    roots = []
                                       
                
                issue_part = {'reporter':reporter, 'label_name':label_name,
                              'diff':diff, 'patch':patch}
                
                issue_all = {}
                issue_all.update(issue)
                issue_all.update(issue_part)
                
                f_csv.writerow(issue_all)
                
            except Exception as e:
                print(issue['number'], ': ', e)                
               
                
                