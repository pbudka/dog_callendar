# 0 English 1 Czech 
lang = 1

def message(string, *args):
    global lang
    if string in messages:
        string = messages[string][lang]
    if len(args) > 0:
        string = string.format(*args)
    return string

def switchLang():
    global lang
    if lang == 0: lang = 1
    else: lang = 0

messages = \
{'no_record':       ['No record',               'Zadny zaznam.'],
 'type_password':   ['Type passw & 0\n',     'Zadej heslo a 0\n'],
 'new_password':    ['New passw & 0\n',      'Nove heslo a 0\n'],
 'again_password':  ['Again passw & 0\n',       'Znova heslo a 0\n'],
 'wrong_password':  ['Cannot use.\nAgain passw & 0', 'Nelze pouzit.\nNove heslo a 0'],
 'week_stat':       ['Week stat:',              'Tyden stat:'],
 'month_stat':      ['Month stat:',              'Mesic stat:'],
 'wrong_password':  ['Wrong password',          'Spatne heslo.'],
 'bye':             ['Bye!',                   'Ahoj!'],
 'hi_dog_home':     ['Hello {:s}!!!\nDog is home.', 'Ahoj {:s}!!!\nPes je doma.'],
 'hi_dog_out':      ['Hello {:s}!!!\n{:s} is out.', 'Ahoj {:s}!!!\nVenku je {:s}.'],
 'logged_back':     ['1:BACK 0:logout\n2:new password', '1:DOMA 0:logout\n2:zmena hesla'],
 'logged_go':       ['1:OUT 0:logout\n2:new password', '1:JDU 0:logout\n2:zmena hesla'],
 'logged_blame':    ['1:{:s} NO! 0:logout\n2:new password', '1:{:s} NE! 0:logout\n2:zmena hesla'],
 'recording':       ['{:s} is back\nRecord {:d}:{:02d}.', '{:s} je zpet\nZapisuju {:d}:{:02d}.'],
 'no_record':       ['{:s} don\'t record\nToo short.', '{:s} nezapisuji\nPrilis kratke.'],
 'blame':           ['Isn\'t {:s} out?\n1:isn\'t 2:cancel', 'Neni {:s} venku?\n1:neni 2:zrusit'],
 'log_as':          ['Log as\n1:R 2:B 3:M', 'Login jako\n1:R 2:B 3:M'],
 'blamed':          ['{:s} claims that\n{:s} isn\'t out', '{:s} tvrdi ze\n{:s} neni venku'],
 'canceled':        ['Canceled.',               'Zruseno.'],
 'storing_password':['Storing password\nRemember {:s}','Ukladam heslo.\nZapamatuj si ho {:s}'],
 'wrong_password':  ['Wrong password\nLogout.','Spatne heslo\nOdhlasuji.'],
 'dog_home':        ['Dog home 0:login\n1:week 2:month','Pes doma 0:log\n1:tyden 2:mesic'],
 'dog_out':         ['{:s} out 0:login\n1:week 2:month','{:s} venci 0:log\n1:tyden 2:mesic']}