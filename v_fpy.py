###coding: utf-8

import ffmpy

inp = {'1.mp4': None}
outp = {'13.mp4': [
        '-ss','00:25:33',
        '-t', '00:03:04'],

        }


if __name__ == '__main__':
    ff = ffmpy.FFmpeg(
            inputs=inp,
            outputs = outp,
            )
    print(ff.cmd)
    ff.run()
