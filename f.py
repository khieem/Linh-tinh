def extent_based(filesize_mb = 15, blocksize_kb = 2, extentsize_block = 200, referece=1):
   if referece >= filesize_mb*1024*1024:
      print('invalid reference')
      return
   filesize = filesize_mb*1024*1024
   blocksize = blocksize_kb*1024
   extentsize = extentsize_block*blocksize
   extent = referece // extentsize
   block_id = (referece // blocksize) % extentsize_block
   offset = referece % blocksize
   print('extend id =', referece, 'div', extentsize,'=',extent)
   print('block id = (', referece, ' div ', blocksize,') mod ', extentsize_block,' = ',block_id, sep='')
   print('block offset = {} % {} = {}'.format(referece, blocksize, offset))

def linked_list(filesize_mb, blocksize_kb = 4, pointersize_b = 4, reference=1):
   if reference >= filesize_mb*1024*1024:
      print('invalid reference')
      return
   datasize = blocksize_kb*1024-pointersize_b
   block_id = reference // datasize
   offset = 4 + reference%datasize
   print('\tblock id = {} div {} = {}'.format(reference, datasize, block_id))
   print('\toffset = {} + ({} mod {}) = {}'.format(pointersize_b, reference, datasize, offset))

def index(reference, blocksize_kb=4, pointersize_b=4, filesize_mb=4):
   if reference >= filesize_mb*1024*1024:
      print('invalid reference')
      return
   block_id = reference//(blocksize_kb*1024)
   offset = reference % (blocksize_kb*1024)
   print('\tblock id = {} div {} = {}'.format(reference, blocksize_kb*1024, block_id))
   print('\toffset = {} mod {} = {}'.format(reference, blocksize_kb*1024, offset))

def two_level_index(reference, blocksize_kb=4, pointersize_b=4):
   ppb = blocksize_kb*1024 // pointersize_b
   block_id = reference // (blocksize_kb*1024)
   block_2_id = block_id // ppb
   level2_offset = block_id % ppb
   offset = reference % (blocksize_kb * 1024)
   print('\tblock_id = {} div {} = {}'.format(reference, blocksize_kb*1024, block_id))
   print('\tlevel 2 index block = {} div {} = {}'.format(block_id, ppb, block_2_id))
   print('\tlevel 2 offset = {} mod {} = {}'.format(block_id, ppb, level2_offset))   
   print('\toffset = {} mod {} = {}'.format(reference, blocksize_kb*1024, offset))

def link_index(reference, blocksize_kb=2, pointersize_b=4):
   ppb = blocksize_kb*1024//pointersize_b - 1
   # print('total pointers per block: {} / {} - 1 = {}'.format(blocksize_kb*1024, pointersize_b, ppb))
   block_id = reference // (blocksize_kb*1024)
   index_block_id = block_id // ppb
   print('\tblock_id = {} div {} = {}'.format(reference, blocksize_kb*1024, block_id))
   print('\tindex_block_id = {} div {} = {}'.format(block_id, ppb, index_block_id))
   data_block_offset = block_id % ppb
   # print('data block offset = {} mod {} = {}'.format(block_id, ppb, data_block_offset))
   offset = reference % (blocksize_kb*1024)
   print('\toffset = {} mod {} = {}'.format(reference, blocksize_kb*1024, offset))

def unix(reference, blocksize_kb=4, pointersize_b=4, direct_pointer=12):
   blocksize_b = blocksize_kb*1024
   ppb = blocksize_b//pointersize_b
   # print('total pointers per block = {} div {} = {}'.format(blocksize_b, pointersize_b, ppb))
   print('\tdirect pointer: {}'.format(direct_pointer))
   indirect_pointer = ppb
   print('\tindirect_pointer:', indirect_pointer)
   double_pointer = ppb**2
   print('\tdouble pointer:', double_pointer)
   triple_pointer = ppb**3
   print('\ttriple_pointer:', triple_pointer)
   print()
   block_id = reference // blocksize_b
   offset = reference % blocksize_b
   print('\tdirect: block_id: {}, offset: {}'.format(block_id, offset))
   if block_id >= direct_pointer:
      print('\tindirect pointer: block_id: {}, datablock in index block: {} - {} = {}, offset: {}'.format(block_id, block_id, direct_pointer, block_id-direct_pointer, offset))
      if block_id >= indirect_pointer:
         blocks_in_2nd_level = block_id-direct_pointer-indirect_pointer
         print(f'\tdouble pointer: {block_id}, blocks in 2nd level: {blocks_in_2nd_level}, 2nd level: {blocks_in_2nd_level//ppb}, data block: {blocks_in_2nd_level%ppb}, offset: {offset}')
         if block_id >= double_pointer:
            blocks_in_3rd_level = block_id-direct_pointer-indirect_pointer-double_pointer
            print(f'\tblock_id: {block_id}, blocks in 3rd level: {blocks_in_3rd_level}, index 2: {blocks_in_3rd_level//ppb**2}, index 3: {blocks_in_3rd_level % (ppb**2 // ppb)}, offset: {offset}')
def unix_max_file_size(pointersize_b=4, blocksize_kb=4, direct=12):
   indirect_pointer = blocksize_kb*1024/pointersize_b
   double = indirect_pointer**2
   triple = indirect_pointer**3
   total_pointer = direct+indirect_pointer+double+triple
   print(f'max file size: {total_pointer*blocksize_kb} KB')
def linux_max_file_size(pointersize_b=4, blocksize_kb=4, direct=10):
   unix_max_file_size(pointersize_b=pointersize_b, blocksize_kb=blocksize_kb, direct=direct)
def linux(reference, blocksize_kb=4, pointersize_b=4):
   unix(reference=reference, direct_pointer=10, blocksize_kb=blocksize_kb, pointersize_b=pointersize_b)

def max(a):
   max = a[0]
   for i in a:
      if max < i:
         max = i
   return max
def min(a):

   min = a[0]
   for i in a:
      if min > i:
         min = i
   return min
def floor(x, a):
   ma = max(a)
   for i in range(0, len(a)):
      if a[i] < ma and a[i] > x:
         ma = a[i]
   return ma

def fifo(queue, current_pos, move_left=True, serve_left=True, cylinders=320):
   rs = abs(current_pos-queue[0])
   for i in range(1, len(queue)):
      rs += abs(queue[i]-queue[i-1])
   print('FIFO:', rs)

def sstf(queue, current_pos, move_left=True, serve_left=True, cylinders=320):
   m = [False] * cylinders
   r = 0
   for i in queue:
      m[i] = True
   # print(m)
   l = len(queue)
   if current_pos in queue:
      l = l-1
   i = j = current_pos
   # print(i, j, current_pos)
   while (l > 0):
      # print(i, j, current_pos, l)
      if i > 0:
         i = i-1
         # print('i=', i)
      if j < cylinders-1:
         j = j+1
         # print('j=', j)
      if m[i] == True:
         r += abs(current_pos-i)
         current_pos = i
         m[current_pos] = False
         l = l-1
      if m[j] == True:
         r += abs(current_pos-j)
         current_pos = j
         m[current_pos] = False
         l = l-1
   print('SSFT:', r)
def scan(queue, current_pos, move_left=True, serve_left=True, cylinders=320):
   print('SCAN:', current_pos + max(queue))
def c_scan(queue, current_pos, move_left=True, serve_left=True, cylinders=320):
   print('C-SCAN:', current_pos+ cylinders + cylinders -floor(current_pos, queue))
def look(queue, current_pos, move_left=True, serve_left=True, cylinders=320):
   print('LOOK:', current_pos-min(queue) + max(queue) -min(queue))
def c_look(queue, current_pos, move_left=True, serve_left=True, cylinders=320):
   print('C-LOOK:', current_pos-min(queue)+max(queue)-min(queue)+max(queue)-floor(current_pos,queue))
# linux(reference = 12*1024**2)
q = [98, 183, 37, 122, 14, 124, 65, 67]
two_level_index(reference=12*1024*1024-1, blocksize_kb=4, pointersize_b=4)