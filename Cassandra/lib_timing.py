# coding=utf-8
from __future__ import print_function, unicode_literals
from collections import OrderedDict


class TMOD(OrderedDict):
    TOTAL = 'TOTAL'

    def human_readable(self):
        '''
        Affichage du dictionnaire des durées
        :param tm: OrderedDict des durées, une entrée peut être elle-même un OrderedDict
               dont une entrée TOTAL doit contenir le sous total de la durée
        '''

        def human_readable_helper(tm, level=0, pfx='', tm_total=None):
            indent = ''.join(['    '] * level)
            filler = ['.'] * 100
            len_max = max([len(tm_name) for tm_name in tm])
            if not tm_total:
                tm_total = sum([tm[tm_name][TMOD.TOTAL]
                                if isinstance(tm[tm_name], OrderedDict)
                                else tm[tm_name] for tm_name in tm])

            for num, tm_name in enumerate(tm):
                if isinstance(tm[tm_name], OrderedDict):
                    print('{0:s}{1:s}{2:2d} {3:s} {4:s} : {5:6.3f}s  {6:3.1f}%'
                          .format(indent, pfx, num + 1, tm_name, ''.join(filler[:len_max + 2 - len(tm_name)]),
                                  tm[tm_name][TMOD.TOTAL],
                                  100. * tm[tm_name][TMOD.TOTAL] / tm_total))
                    sub_tm_total = tm[tm_name].pop(TMOD.TOTAL)
                    human_readable_helper(tm=tm[tm_name], level=level + 1, pfx='{}.'.format(num + 1), tm_total=tm_total)
                    tm[tm_name][TMOD.TOTAL] = sub_tm_total
                else:
                    print('{0:s}{1:s}{2:2d} {3:s} {4:s} : {5:6.3f}s  {6:3.1f}%'
                          .format(indent,
                                  pfx,
                                  num + 1,
                                  tm_name,
                                  ''.join(filler[:len_max + 2 - len(tm_name)]),
                                  tm[tm_name],
                                  100. * tm[tm_name] / tm_total))
            if level == 0:
                print('{0:s} {1:s} : {2:6.3f}s'
                      .format('Total', ''.join(filler[:len_max + 5 - len('Total')]), tm_total))

        human_readable_helper(self, level=0, pfx='', tm_total=None)

