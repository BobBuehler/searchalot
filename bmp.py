import struct

def write(file_path, width, height, bgr_callback):
    d = {
        'mn1':66,
        'mn2':77,
        'filesize':0,
        'undef1':0,
        'undef2':0,
        'offset':54,
        'headerlength':40,
        'width':width,
        'height':height,
        'colorplanes':0,
        'colordepth':24,
        'compression':0,
        'imagesize':0,
        'res_hor':0,
        'res_vert':0,
        'palette':0,
        'importantcolors':0
        }


    #Build the byte array.  This code takes the height
    #and width values from the dictionary above and
    #generates the pixels row by row.  The row_mod and padding
    #stuff is necessary to ensure that the byte count for each
    #row is divisible by 4.  This is part of the specification.
    the_bytes = ''
    for row in range(height-1,-1,-1):# (BMPs are L to R from the bottom L row)
        for column in range(width):
            (b,g,r) = bgr_callback(row, column)
            pixel = struct.pack('<BBB',b,g,r)
            the_bytes = the_bytes + pixel
        row_mod = (d['width']*d['colordepth']/8) % 4
        if row_mod == 0:
            padding = 0
        else:
            padding = (4 - row_mod)
        padbytes = ''
        for i in range(padding):
            x = struct.pack('<B',0)
            padbytes = padbytes + x
        the_bytes = the_bytes + padbytes

    mn1 = struct.pack('<B',d['mn1'])
    mn2 = struct.pack('<B',d['mn2'])
    filesize = struct.pack('<L',d['filesize'])
    undef1 = struct.pack('<H',d['undef1'])
    undef2 = struct.pack('<H',d['undef2'])
    offset = struct.pack('<L',d['offset'])
    headerlength = struct.pack('<L',d['headerlength'])
    width = struct.pack('<L',d['width'])
    height = struct.pack('<L',d['height'])
    colorplanes = struct.pack('<H',d['colorplanes'])
    colordepth = struct.pack('<H',d['colordepth'])
    compression = struct.pack('<L',d['compression'])
    imagesize = struct.pack('<L',d['imagesize'])
    res_hor = struct.pack('<L',d['res_hor'])
    res_vert = struct.pack('<L',d['res_vert'])
    palette = struct.pack('<L',d['palette'])
    importantcolors = struct.pack('<L',d['importantcolors'])
    
    outfile = open(file_path,'wb')
    outfile.write(mn1+mn2+filesize+undef1+undef2+offset+headerlength+width+height+\
                  colorplanes+colordepth+compression+imagesize+res_hor+res_vert+\
                  palette+importantcolors+the_bytes)
    outfile.close()

def write_many(file_path, width, height, bgr_callback_grid):
    cg_width = max([len(c) for c in bgr_callback_grid])
    cg_height = len(bgr_callback_grid)
    total_width = cg_width * (width + 1) + 1
    total_height = cg_height * (height + 1) + 1
    def callback(y, x):
        cg_y = y / (height + 1)
        cg_x = x / (width + 1)
        local_y = y % (height + 1) - 1
        local_x = x % (width + 1) - 1
        if cg_y == cg_height or cg_x == cg_width or local_y < 0 or local_x < 0:
            return (0,0,0)
        else:
            cb_row = bgr_callback_grid[cg_y]
            if cg_x < len(cb_row) and cb_row[cg_x] is not None:
                return cb_row[cg_x](local_y,local_x)
            else:
                return (0,0,0)
    write(file_path, total_width, total_height, callback)
