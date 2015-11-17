'''
Created on 20151111

@author: xiaobena
'''
import csv
import re
import urllib.request

from libsaas.services import github

basic = github.Github('username', 'password')

repo = basic.repo('scipy', 'scipy')

headers = ['number', 'id', 'reporter', 'created_at', 'updated_at', 'closed_at', 'state', 
           'locked', 'assignee', 'milestone', 'comments', 'label_name', 'title', 'pull_request',
           'user', 'labels', 'html_url', 'labels_url', 'url', 'events_url', 'diff', 'patch',
           'comments_url', 'body']
patch_headers = ['number', 'ncommit', 'hash', 'author', 'date', 'subject', 'nfiles', 'ninsertions',
                 'ndeletions', 'file','changes', 'insertions', 'deletions', 'locations', 'roots']
             
def parseDiffFile(diff):   
    location = ''
    root = ''
    
    for line in diff:
        if line.startswith('@@'):
            location = location + line.split('@@')[1] + ';'
            root = root + line.split('@@')[2][1:-1] + ';'
       
    return location, root 

def parseCommit(commit):         
    hash = commit[0][5:12]
#    print('hash: ', hash)
    author = commit[1][5:]
#    print('author: ', author)
    date = commit[2][5:]
#    print('date: ', date)
    
    subject = commit[3][5:]
    index = 4
    for i in range(index, len(commit)):
        if commit[i]=='---':
            break
        else:
            subject += commit[i]
#    print('subject: ', subject)
                    
    index = i+1
#   print(i)
    nfiles = 0
    ninsertions = 0
    ndeletions = 0
                    
    files = []
    changes = []
    insertions = []
    deletions = []
    
#    print('get changed files.')                
    for j in range(index, len(commit)):
#        print('j:', j)        
        if '|' not in commit[j]:                            
            temp = commit[j].strip().split(',')
            for str in temp:
                if 'changed' in str:
                    nfiles = re.findall(r"\d+\.?\d*",str)[0]
                if 'insertions' in str:
                    ninsertions = re.findall(r"\d+\.?\d*",str)[0]
                if 'deletions' in str:
                    ndeletions = re.findall(r"\d+\.?\d*",str)[0]    
            break
                        
        else:
            temp = commit[j].split('|')
            files.append(temp[0].strip()) 
            changes.append(re.findall(r"\d+\.?\d*",temp[1]))
#            print(re.findall(r"\d+\.?\d*",temp[1]))
            insertions.append(temp[1].count('+'))
            deletions.append(temp[1].count('-'))
                     
    index = j + 2       
    file_index = []
                    
    for k in range(index,len(commit)):
        if commit[k].startswith('diff --'):
            file_index.append(k)  
    file_index.append(k)
    
#    print ('number of files: ', len(file_index)-1)
            
    locations = [] 
    roots = [] 
            
    for fi in range(0,(len(file_index)-1)):
#        print(commit[file_index[fi]:file_index[fi+1]])
#        print('parse file: ', fi+1)
        location, root = parseDiffFile(commit[file_index[fi]:file_index[fi+1]]) 
        locations.append(location)
        roots.append(root)          
     
    results = {'hash':hash, 'author':author, 'date':date, 'subject':subject, 'nfiles':nfiles,
               'ninsertions':ninsertions, 'ndeletions':ndeletions,
               'files':files, 'changes':changes, 'insertions':insertions,
                'deletions':deletions, 'locations':locations, 'roots':roots}  
    
    return results
             
def getPatch(patch):   
    patch_content = urllib.request.urlopen(patch)
    content = patch_content.read().decode("utf8")
                    
    lines = content.splitlines()
 #   print('patch content length: ', len(lines))
    
    commit_index = []
                    
    for n in range(0,len(lines)):
        if lines[n].startswith('From '):
            commit_index.append(n)
    commit_index.append(n)
    
#    print ('number of commits: ', len(commit_index)-1)
    patch = []
            
    for ci in range(0, (len(commit_index)-1)):
#        print(commit_index[ci+1] - commit_index[ci])
#        print(len(lines[commit_index[ci]:commit_index[ci+1]]))
#        print('parse commit :' , ci+1)
        patch.append(parseCommit(lines[commit_index[ci]:commit_index[ci+1]]))
    
    return patch


#with open('F:/scipy_patch.csv', 'a', newline='') as patch_file:
#    pf_csv = csv.DictWriter(patch_file, patch_headers)
#    pf_csv.writeheader()
    
with open('F:/scipy.csv','a',newline='') as f:
    f_csv = csv.DictWriter(f, headers)
#    f_csv.writeheader()
    
    for page in range(1,100):
        print ("page: ", page)
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
                    diff_url = issue['pull_request']['diff_url']
                    patch_url = issue['pull_request']['patch_url']
                    patch = getPatch(patch_url)
                    
                    
#                    print('writing_number of commits: ', len(patch))
                    for commit in patch:
                        commit_basic = {'hash':commit['hash'], 'author':commit['author'], 'date':commit['date'],
                                        'subject':commit['subject'], 'nfiles':commit['nfiles'], 
                                        'ninsertions':commit['ninsertions'], 'ndeletions':commit['ndeletions']}
                            
#                        print('writing_number of files: ', len(commit['files']))
                        files = commit['files']
                        changes = commit['changes']
                        insertions = commit['insertions']
                        deletions = commit['deletions']
                        locations = commit['locations']
                        roots = commit['roots']
                        for nn in range(0, len(commit['files'])):
#                            print('writing file: ', nn+1, files[nn])                            
                            commit_file = {'file':files[nn], 'changes':changes[nn],'insertions':insertions[nn], 
                                           'deletions':deletions[nn], 'locations':locations[nn], 'roots':roots[nn]}
                            commit = {'number':issue['number'], 'ncommit':len(patch)}
                            commit.update(commit_basic)
                            commit.update(commit_file)
#                            print(commit)
                            with open('F:/scipy_patch.csv', 'a', newline ='') as p:
                                p_csv = csv.DictWriter(p, patch_headers)
                                p_csv.writerow(commit)
                                                                                     
                issue_part = {'reporter':reporter, 'label_name':label_name,
                              'diff':diff_url, 'patch':patch_url}
                
                issue_all = {}
                issue_all.update(issue)
                issue_all.update(issue_part)
                
                f_csv.writerow(issue_all)
                
            except Exception as e:
                print(issue['number'], ': ', e)  
                with open ('F:/exception.txt', 'a') as ef:
                    ef.write(str(issue['number']) + ': ' + str(e) + '\t\n')
                              
               
                
