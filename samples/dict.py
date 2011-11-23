tel = {'jack': 4098, 'sape': 4139}
tel['guido'] = 4127
tel
{'sape': 4139, 'guido': 4127, 'jack': 4098}
tel['jack']
4098
del tel['sape']
tel['irv'] = 4127
tel
{'guido': 4127, 'irv': 4127, 'jack': 4098}
tel.keys()
['guido', 'irv', 'jack']
'guido' in tel
True