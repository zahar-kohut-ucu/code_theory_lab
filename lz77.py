import time
import matplotlib.pyplot as plt



class LZ77:
    """LZ77 algorithm implementation."""

    def __init__(self, buffer_size):
        """Initialize LZ77 algorithm.

        :param window_size: size of window
        :param buffer_size: size of buffer
        """
        self.buffer_size = buffer_size

    def get_data(self, file):

        with open(file, 'r', encoding='utf-8') as f:
            data = f.readlines()
        data = ''.join(data)
        return data


    def lz77_compress(self, file=None, data=None):
        """Compress data using LZ77 algorithm.

        :param data: data to compress
        :return: data data
        >>> lz77 = LZ77(13, 6)
        >>> lz77.lz77_compress('cabracadabrarrarrad')
        [(0, 0, 'c'), (0, 0, 'a'), (0, 0, 'b'), (0, 0, 'r'),\
    (3, 1, 'c'), (2, 1, 'd'), (7, 4, 'r'), (3, 3, 'r'), (3, 1, 'd')]
        """
        data = self.get_data(file) if data is None else data
        compressed_data = []
        search_buffer = ''
        pos = 0
        while pos < len(data):

            if data[pos] not in search_buffer:
                compressed_data.append((0, 0, data[pos]))
                search_buffer += data[pos]
                pos += 1
            else:
                for i in range(self.buffer_size+1):
                    if data[pos:pos+i+1] in search_buffer:
                        element = data[pos:pos+i+1]
                index = search_buffer.rfind(element)
                next_el = data[pos+len(element)] if pos+len(element) < len(data) else ''
                compressed_data.append((len(search_buffer)-index, len(element), next_el))
                search_buffer += element + next_el
                pos += len(element) + 1
        with open('compressed.txt', 'w', encoding='utf-8') as f:
            for tpl in compressed_data:
                for i in tpl:
                    f.write(str(i))
        return compressed_data


    def lz77_decompress(self, data, file=None):
        """Decompress data using LZ77 algorithm.

        :param data: data to decompress
        :return: decompressed data
        >>> lz77 = LZ77(13, 6)
        >>> lz77.lz77_decompress([(0, 0, 'c'), (0, 0, 'a'), (0, 0, 'b'), (0, 0, 'r'),\
(3, 1, 'c'), (2, 1, 'd'), (7, 4, 'r'), (3, 3, 'r'), (3, 1, 'd')])
        'cabracadabrarrarrad'
        """
        decompressed_data = ""
        while len(data):
            if data[0][0] == 0 and data[0][1] == 0:
                decompressed_data += data[0][2]
                data.pop(0)
            else:
                index = len(decompressed_data) - int(data[0][0])
                length = int(data[0][1])
                for i in range(length):
                    decompressed_data += decompressed_data[index+i]
                decompressed_data += data[0][2]
                data.pop(0)
        if file:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(decompressed_data)
        return decompressed_data

def encode_decode_speed(file, lz77_):
    with open(file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    data = ''.join(data)
    result = {}
    for i in range(1, 10):
        new_data = data[:100000*i]
        start = time.time()
        comp = lz77_.lz77_compress(data=new_data)
        lz77_.lz77_decompress(comp)
        result[f'{i}*10^5'] = (time.time() - start)
    plt.plot(result.keys(), result.values(), marker = 'o')
    plt.xlabel('characters')
    plt.ylabel('time')
    plt.show()

def number_symbols_compress(file, lz77_):
    with open(file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    data = ''.join(data)
    result = {}
    for i in range(1, 10):
        new_data = data[:1000*i]
        comp = lz77_.lz77_compress(data=new_data)
        symb = len(comp)*3
        result[f'{i}*10^5'] = (100000*i/symb)
    plt.figure().set_figwidth(10)
    plt.plot(result.keys(), result.values(), marker = 'o')
    plt.title('Degree of compression relative to the size of the input data (in percent)')

    plt.xlabel('characters')
    plt.ylabel('percentages')
    # plt.figure().set_figwidth(15)
    plt.show()

lz77 = LZ77(6)
x = 'abracadabrarrarrad'
comp = lz77.lz77_compress(data=x)
# lz77.lz77_decompress(comp, file='decompressed.txt')
# # print(comp)
# encode_decode_speed('data.txt', lz77)
# number_symbols_compress('data.txt', lz77)