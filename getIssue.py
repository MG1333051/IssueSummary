'''
@author: Lenovo
'''
import github

gh = github.GitHub()
print(gh.users('michaelliao').get())

L = gh.repos('numpy')('numpy').issues.get(state='closed', sort='created')

for i in L:
    print(i)
