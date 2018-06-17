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


import sys

# Metadata syntax changed between LLVM versions
def processMetadata(l):
    aux=l[l.find("{")+1:l.find("}/n")-1]
    aux=aux.replace("!","metadata !")
    aux=aux.replace("speculatable","")
    aux=aux.replace("distinct","")
    if aux=='':
        aux='metadata !""'
    l=l[0:l.find("{")-1]+"metadata !{"+aux+"}\n"
    l=l.replace("distinct ","")
    f_out.write(l)

# Update synthax of a single operation
def processLine(l):
    #  source_filename is not required in older LLVM versions
    if "source_filename" in l:
        return

    # The getelementptr syntax changed between LLVM versions
    elif "= getelementptr" in l:
        if "inbounds" in l:
            f_out.write(l.replace(l[l.find("getelementptr inbounds")+22:l.find(",")+1],""))
        else:
            f_out.write(l.replace(l[l.find("getelementptr")+13:l.find(",")+1],""))

    # The load syntax changed between LLVM versions    
    elif "= load" in l:
        f_out.write(l[0:l.find(" load")+5]+l[l.find(",")+1:])

    #Dealing with metadata
    elif l[0]=="!" and l[1].isdigit(): 
        processMetadata(l)

    # Only introduced in later LLVM versions
    elif "local_unnamed_addr" in l:
        f_out.write(l[0:l.find("local_unnamed_addr")]+l[l.find("local_unnamed_addr")+18:])  
    
    # This attribute is not supported by old LLVM versions
    elif "norecurse" in l: 
        f_out.write(l.replace("norecurse ",""))

    # This attribute is not supported by old LLVM versions
    elif "speculatable" in l:
        f_out.write(l.replace("speculatable ",""))

    # remove unsupported fast ops
    elif "fcmp fast" in l:
        f_out.write(l.replace("fcmp fast","fcmp"))

    # remove unsupported fast ops
    elif "tail call fast" in l:
        f_out.write(l.replace("tail call fast","tail call"))

    else:
        f_out.write(l)

# Receive input and output files
input_file=sys.argv[1]
output_file=sys.argv[2]

# Open input and output files 
f_in = open(input_file,'r')
f_out = open(output_file,'w')

# Write to output file according to old syntax
while True:
    # Read line by line and exit when done
    line = f_in.readline()
    if not line:
        break

    # Process line
    processLine(line)

# Close both files
f_in.close()
f_out.close()
