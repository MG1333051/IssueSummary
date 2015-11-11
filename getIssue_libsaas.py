'''
Created on 20151111

@author: Lenovo
'''

from libsaas.services import github

basic = github.Github('username', 'passport')

repo = basic.repo('numpy', 'numpy')

for i in range(1,101):
    issues = repo.issues().get(state='closed', page = i)
    for issue in issues:
        print ('issue: ', issue)

