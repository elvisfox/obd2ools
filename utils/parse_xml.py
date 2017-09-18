#!/usr/bin/env python3

import io
import save_pids

f_xml = open('00-0.xml', 'r')
pids_list = []
pid = None

def process_dict(pid):
    l = list()
    l.append(0x7E0)
    l.append(pid['cmd'].replace(' ', ''))
    l.append('00')
    if pid['comment'] != b'-':
        l.append(pid['cmd'].replace(' ', ''))
    else:
        l.append(pid['comment'])
    l.append(pid['unit'])
    l.append('0.3f')
    l.append('linear')
    l.append([0.0, 0])

    return l

while 1:
    # read next line
    st = f_xml.readline()
    if not st:
        break
    st = st.strip()
    st = st.replace('/>', ' />')

    fields = st.split(' ')

    while True:
        try:
            f = fields.pop(0)
        except:
            break
        # New block - create empty dictionary
        if f == '<PAR':
            pid = dict()
            #print('New block')
            continue
        elif pid == None:
            continue
        # End of block
        if f == '/>':
            #print('End of block')
            print(str(pid))
            # process fields
            #print(process_dict(pid))
            pids_list.append(process_dict(pid))
            # clear pid object
            pid = None
            continue
        # Fill in fields
        prop = f.split('=')
        try:
            # merge text within ""
            while prop[1][0] == '"' and prop[1][-1] != '"':
                #print(' That is the case: ' + prop[1])
                prop[1] = prop[1] + ' ' + fields.pop(0)
            # remove ""
            prop[1] = prop[1].strip('"')
            # add an item to the dictionary
            pid[prop[0]] = prop[1]
            #print('New field: ' + prop[0] + ' = ' + prop[1])
        except:
            pass

f_xml.close()

save_pids.generate('parsed', pids_list)
