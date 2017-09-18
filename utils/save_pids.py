#!/usr/bin/env python3

import io

def generate(name, pids_list):

    f_out = open('pids/'+name+'.py', 'w')

    f_out.write('\n')
    f_out.write('def linear(data, gain, offset):\n')
    f_out.write('\treturn data * gain + offset\n')
    f_out.write('\n')
    f_out.write('#\t0\t1\t2\t3\t4\t5\t6\t7\n')
    f_out.write('#\t[header,\tpid,\texample,\tshort name,\tunits,\tformat,\tfunc,\t[params]],\n')
    f_out.write(name + '_pids = [\n')

    for pid in pids_list:

        head = pid[0]

        pid[0] = 'HEADER'
        pid[6] = 'linear'

        ls = '\t' + str(pid)
        ls = ls.replace('\'HEADER\'', hex(head))
        ls = ls.replace('\'linear\'', 'linear')
        ls = ls.replace(', ', ',\t')

        f_out.write(ls + ',\n')

    f_out.write(']\n')
    f_out.close()
