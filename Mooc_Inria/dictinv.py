import os
os.chdir(r'D:\Emmanuel\2015-10_MOOC_Python')

def dictinv(d):
    invd = {d[i] : i for i in d}
    return invd

print dictinv(
    { 8  : 'huit',
      10 : 'dixA',
      24 : 'douze',
      12 : 'douze'
      })

print dictinv(
    { 5  : 'cinq',
      10 : 'dixB',
      15 : 'quinze'})

print dictinv(
    { 1 : 'unA',
      2 : 'deux',
      3 : 'troisA'})

print dictinv(
    { 1 : 'unB',
      2 : 'deux',
      4 : 'quatreB'})

