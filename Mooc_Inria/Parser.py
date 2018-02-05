class Parser:
    def __init__(self, sep=' '):
        self.sep = sep
        self.parsed_line = ''
        
    def parse(self, line):
        self.parsed_line = [i.strip() for i in line.split(self.sep)
                            if i.strip().isdigit()]

    def __repr__(self):
        if self.parsed_line:
            return ' '.join(self.parsed_line)
        else:
            return ''

test = '123  : fj356:34:fjjd:    707'

p = Parser(':')
p.parse(test)
print p
