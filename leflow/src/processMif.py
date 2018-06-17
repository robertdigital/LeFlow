#-----------------------------------------------------------------------------
#Copyright (c) 2018 Daniel Holanda Noronha, Bahar Salehpour, Steve Wilton
#{danielhn,bahars,stevew}@ece.ubc.ca
#Permission to use, copy, and modify this software and its documentation is
#hereby granted only under the following terms and conditions. Both the
#above copyright notice and this permission notice must appear in all copies
#of the software, derivative works or modified versions, and any portions
#thereof, and both notices must appear in supporting documentation.
#This software may be distributed (but not offered for sale or transferred
#for compensation) to third parties, provided such third parties agree to
#abide by the terms and conditions of this notice.
#THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHORS, AS
#WELL AS THE UNIVERSITY OF BRITISH COLUMBIA DISCLAIM ALL
#WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
#AUTHORS OR THE UNIVERSITY OF BRITISH COLUMBIA OR THE
#UNIVERSITY OF SYDNEY BE LIABLE FOR ANY SPECIAL, DIRECT,
#INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
#PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
#OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
#WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#---------------------------------------------------------------------------


#!/usr/bin/env python
import numpy as np
import struct, inspect, os, sys

def toHex(num):
    return ''.join(hex(ord(c)).replace('0x', '').rjust(2, '0').upper() for c in struct.pack('!f', num))

def toFloat(num):
    return struct.unpack('!f', num.decode('hex'))[0]

def createMem(arrays):

    # Gets name of circuit that is being generated
    project_folder = inspect.getmodule(inspect.stack()[1][0]).__file__.replace(".py","")+"_files/"
    if not os.path.exists(project_folder+"tfArgs/"):
        os.makedirs(project_folder+"tfArgs/")

    # Creates one memory for each parameter
    param_counter=0
    for array in arrays:

        # Create file
        f= open(project_folder+"tfArgs/param"+str(param_counter)+".mif","w+")

        # Create header for file
        flat_array = array.flatten()
        f.write("Depth = "+str(len(flat_array))+";\n")
        f.write("Width = 32;\nAddress_radix = dec;\nData_radix = hex;\nContent\nBegin\n")

        # Populate elements
        for idx,element in enumerate(flat_array):
            f.write(str(idx)+": "+toHex(element)+";\n")
        
        # Close file
        f.write("End;\n")
        f.close()

        param_counter=param_counter+1

def dumpMem(mem):
    f= open(mem,"r+")
    for line in f: 
        if ": " in line:
            content=line[line.find(": ")+2:line.find(";")]
            print(toFloat(content))

def printModelsimDump(mem):
    f= open(mem,"r+")
    for line in f: 
        if "/" not in line:
            print(toFloat(line[:-1]))

# Dump modelsim memory if we receive an argument with its path
if len(sys.argv)==2:
    printModelsimDump(sys.argv[1])
