"dif.py -- Navy DIF file handler"

# Copyright 2001, 2013 Chris Gonnerman
# All Rights Reserved
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions
# are met:
# 
# Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer. 
# 
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution. 
# 
# Neither the name of the author nor the names of any contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Revision History
#
# 05/29/2007 v1.2 Revised by Sebastien Ramage
#                 Changed number handling code to accept floating-point
#                 values.
# 11/12/2013 v1.3 Released via github

__version__ = "1.3"

class DIFError():
    pass

class DIF:

    def __init__(self, file):
        # DIF file lines should never be all blank, so
        # stripping the line shouldn't cause an early
        # exit.
        line = file.readline().rstrip().upper()
        header = 1
        self.data = []
        self.header = {}
        self.vectors = []
        while line:
            if header:
                if line == "DATA":
                    header = 0
                    tup = None
                    file.readline()
                    file.readline()
                else:
                    line = line.lower()
                    n = list(map(int, file.readline().rstrip().split(",")))
                    s = file.readline().strip()[1:-1]
                    n.append(s)
                    if line in self.header:
                        if type(self.header[line]) is type(()):
                            self.header[line] = [ self.header[line], tuple(n) ]
                        else:
                            self.header[line].append(tuple(n))
                    else:
                        self.header[line] = tuple(n)
                    if line == "vectors":
                        self.vectors = map(lambda x: "FIELD%d" % x, range(n[1]))
                    elif line == "label" and n[1] == 0:
                        self.vectors[n[0]-1] = n[2]
            else:
                nums = line.split(",",1)
                nums[0] = int(nums[0])
                if not nums[1].isdigit() and nums[0] == 0:
                    nums[1] = float(nums[1].replace(',','.')) #convert to float
                elif nums[0] == 0:
                    nums[1] = int(nums[1]) #convert to int
                strv = file.readline().rstrip()
                if nums[0] == -1:
                    if strv == "BOT":
                        if tup:
                            self.data.append(tup)
                        tup = []
                    elif strv == "EOD":
                        self.data.append(tup)
                        tup = []
                        return
                    else:
                        raise DIFError("Invalid Special Data Value [%s]" % strv)
                elif nums[0] == 0:
                    if strv == "V" or strv == "TRUE" or strv == "FALSE":
                        tup.append(nums[1])
                    elif strv == "NA" or strv == "ERROR":
                        tup.append(None)
                    else:
                        raise DIFError("Invalid Numeric Data Type [%s]" % strv)
                elif nums[0] == 1:
                    strv = strv.strip()
                    if strv[0:1] == '"':
                        strv = strv[1:-1]
                    tup.append(strv)
                else:
                    raise DIFError("Invalid Type Indicator [%d]" % nums[0])
            line = file.readline().rstrip().upper()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        row = self.data[key]
        rc = {}
        for i in range(len(row)):
            rc[self.vectors[i]] = row[i]
        return rc

if __name__ == "__main__":

    from distutils.core import setup, Extension

    setup(name="DIF",
        version=__version__,
        description="dif.py",
        long_description="Navy DIF file handler",
        author="Chris Gonnerman",
        author_email="chris.gonnerman@newcenturycomputers.net",
        url="http://newcenturycomputers.net/projects/dif.html",
        py_modules=["dif"]
    )

# end of file.
