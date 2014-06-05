'''test IR Remote
'''

import time
from sensor import IRRemote
from tts import say

ir = IRRemote()

value_description = {#0: 'none',
                     1: 'red up',
                     2: 'red down',
                     3: 'blue up',
                     4: 'blue down',
                     5: 'red up and blue up',
                     6: 'red up and blue down',
                     7: 'red down and blue up',
                     8: 'red down and blue down',
                     9: 'beacon mode on',
                     10: 'red up and red down',
                     11: 'blue up and blue down',
                     }

while True:
    bt = ir.button
    if bt in value_description.keys():
        say(value_description[bt])
        time.sleep(0.5)
